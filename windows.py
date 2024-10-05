# windows.py

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import date, datetime
from internet_search import InternetSearch

class BaseWindow(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.geometry("600x400")
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError
    
# windows.py (update only the AutomaticInternetSearchWindow class)

class AutomaticInternetSearchWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Automatic Internet Search")
        self.internet_search = InternetSearch(self.parent.api_key, self.parent.perplexity_api_key)

    def create_widgets(self):
        self.search_listbox = tk.Listbox(self, width=80, height=15)
        self.search_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(self, textvariable=self.progress_var)
        self.progress_label.pack(pady=5)

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10, fill=tk.X)

        self.run_button = ttk.Button(buttons_frame, text="Run Search", command=self.run_search)
        self.run_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="View Selected", command=self.view_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Close", command=self.on_close).pack(side=tk.LEFT, padx=5)

    def run_search(self):
        if not self.parent.perplexity_api_key:
            messagebox.showerror("Error", "Please enter your Perplexity API key in the settings.")
            return

        self.run_button.config(state=tk.DISABLED)
        self.progress_var.set("Generating search terms...")
        self.update_idletasks()

        search_terms = self.internet_search.generate_search_terms(
            [instr[1] for instr in self.parent.instructions],
            [script[1] for script in self.parent.scripts]
        )

        if not search_terms:
            messagebox.showinfo("Info", "Failed to generate valid search terms. Please check searchterms.json for the raw API response.")
            self.run_button.config(state=tk.NORMAL)
            return

        self.progress_var.set("Performing internet search...")
        self.update_idletasks()

        results = self.internet_search.perform_internet_search(search_terms)

        self.parent.internet_sources = results
        self.progress_var.set("Search completed.")
        self.run_button.config(state=tk.NORMAL)
        self.update_listbox()
        self.parent.update_system_prompt()
        self.parent.file_handler.save_internet_sources(self.parent)

    def view_selected(self):
        selection = self.search_listbox.curselection()
        if selection:
            source = self.parent.internet_sources[selection[0]]
            ViewSourceWindow(self, source)

    def delete_selected(self):
        selection = self.search_listbox.curselection()
        if selection:
            del self.parent.internet_sources[selection[0]]
            self.update_listbox()
            self.parent.file_handler.save_internet_sources(self.parent)

    def update_listbox(self):
        self.search_listbox.delete(0, tk.END)
        for source in self.parent.internet_sources:
            search_term = source.get('search_term', 'N/A')
            date_retrieved = source.get('date_retrieved', 'N/A')
            title = source.get('title', 'N/A')
            url = source.get('url', 'unknown')
            self.search_listbox.insert(tk.END, f"{search_term} - {date_retrieved} - {title} - {url}")

    def on_close(self):
        self.parent.update_system_prompt()
        self.parent.save_all_settings()
        self.destroy()


class ViewSourceWindow(BaseWindow):
    def __init__(self, parent, source):
        self.source = source  # Set the source attribute before calling super().__init__
        super().__init__(parent, f"Source: {source.get('title', 'Unknown')}")
        self.geometry("800x600")

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas with scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add source information
        for key, value in self.source.items():
            if key != "content":
                ttk.Label(scrollable_frame, text=f"{key.capitalize()}:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10, 0))
                ttk.Label(scrollable_frame, text=str(value), wraplength=750).pack(anchor="w", pady=(0, 5))

        # Add content
        ttk.Label(scrollable_frame, text="Content:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10, 0))
        content_text = tk.Text(scrollable_frame, wrap=tk.WORD, width=90, height=20)
        content_text.pack(pady=(0, 10))
        content_text.insert(tk.END, self.source.get('content', 'No content available'))
        content_text.config(state=tk.DISABLED)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10)

class SettingsWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Settings")

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        fields = [
            ("API Key:", "api_key", "*"),
            ("Perplexity API Key:", "perplexity_api_key", "*"),
            ("First Name:", "first_name", None),
            ("Last Name:", "last_name", None),
            ("Date (YYYY-MM-DD):", "date", None)
        ]

        for i, (label_text, attr_name, show) in enumerate(fields):
            ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(main_frame, width=40, show=show)
            entry.grid(row=i, column=1, pady=5)
            
            if attr_name == "date":
                # Set today's date as default
                today = date.today().strftime("%Y-%m-%d")
                entry.insert(0, today if not getattr(self.parent, attr_name) else getattr(self.parent, attr_name))
            else:
                entry.insert(0, getattr(self.parent, attr_name))
            
            setattr(self, f"{attr_name}_entry", entry)

        ttk.Button(main_frame, text="Save", command=self.save_settings).grid(row=len(fields), column=0, pady=20)
        ttk.Button(main_frame, text="Close", command=self.destroy).grid(row=len(fields), column=1, pady=20)

    def save_settings(self):
        for attr in ['api_key', 'perplexity_api_key', 'first_name', 'last_name', 'date']:
            setattr(self.parent, attr, getattr(self, f"{attr}_entry").get().strip())
        self.parent.save_all_settings()
        self.destroy()

class FormattingWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Formatting Options")

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True)

        self.create_font_options(main_frame)
        self.create_size_options(main_frame)
        self.create_margin_options(main_frame)

        ttk.Button(main_frame, text="Save", command=self.save_formatting).grid(row=4, column=0, pady=10)
        ttk.Button(main_frame, text="Back to Default", command=self.set_default_formatting).grid(row=4, column=1, pady=10)

    def create_font_options(self, parent):
        ttk.Label(parent, text="Font Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.font_name_var = tk.StringVar(value=self.parent.font_name)
        font_options = ["Times New Roman", "Arial", "Calibri", "Cambria", "Verdana"]
        self.font_name_combobox = ttk.Combobox(parent, textvariable=self.font_name_var, values=font_options, state="readonly", width=30)
        self.font_name_combobox.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=5)

        ttk.Label(parent, text="Line Spacing:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.line_spacing_var = tk.StringVar(value=self.parent.line_spacing)
        line_spacing_options = ["Single", "1.5 lines", "Double"]
        self.line_spacing_combobox = ttk.Combobox(parent, textvariable=self.line_spacing_var, values=line_spacing_options, state="readonly", width=30)
        self.line_spacing_combobox.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5, padx=5)

    def create_size_options(self, parent):
        ttk.Label(parent, text="Font Sizes (pt):").grid(row=2, column=0, sticky=tk.W, pady=5)
        sizes_frame = ttk.Frame(parent)
        sizes_frame.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5, padx=5)

        size_fields = [
            ("Normal Text:", "font_size_normal"),
            ("Heading 1:", "font_size_heading1"),
            ("Heading 2:", "font_size_heading2"),
            ("Heading 3:", "font_size_heading3")
        ]

        for i, (label_text, attr_name) in enumerate(size_fields):
            ttk.Label(sizes_frame, text=label_text).grid(row=i, column=0, sticky=tk.W)
            var = tk.IntVar(value=getattr(self.parent, attr_name))
            spinbox = ttk.Spinbox(sizes_frame, from_=8, to=72, textvariable=var, width=5)
            spinbox.grid(row=i, column=1, sticky=tk.W+tk.E)
            setattr(self, f"{attr_name}_var", var)

    def create_margin_options(self, parent):
        ttk.Label(parent, text="Margins (cm):").grid(row=3, column=0, sticky=tk.W, pady=5)
        margins_frame = ttk.Frame(parent)
        margins_frame.grid(row=3, column=1, sticky=tk.W+tk.E, pady=5, padx=5)

        margin_fields = [
            ("Top:", "margin_top"),
            ("Bottom:", "margin_bottom"),
            ("Left:", "margin_left"),
            ("Right:", "margin_right")
        ]

        for i, (label_text, attr_name) in enumerate(margin_fields):
            ttk.Label(margins_frame, text=label_text).grid(row=i, column=0, sticky=tk.W)
            var = tk.DoubleVar(value=getattr(self.parent, attr_name))
            spinbox = ttk.Spinbox(margins_frame, from_=0, to=10, increment=0.1, textvariable=var, width=5)
            spinbox.grid(row=i, column=1, sticky=tk.W+tk.E)
            setattr(self, f"{attr_name}_var", var)

    def save_formatting(self):
        for attr in ['font_name', 'line_spacing']:
            setattr(self.parent, attr, getattr(self, f"{attr}_var").get())
        for attr in ['font_size_normal', 'font_size_heading1', 'font_size_heading2', 'font_size_heading3',
                     'margin_top', 'margin_bottom', 'margin_left', 'margin_right']:
            setattr(self.parent, attr, getattr(self, f"{attr}_var").get())
        self.parent.save_all_settings()
        self.destroy()

    def set_default_formatting(self):
        defaults = {
            'font_name': "Times New Roman",
            'line_spacing': "1.5 lines",
            'font_size_normal': 12,
            'font_size_heading1': 16,
            'font_size_heading2': 14,
            'font_size_heading3': 12,
            'margin_top': 2.0,
            'margin_bottom': 2.0,
            'margin_left': 2.0,
            'margin_right': 2.0
        }
        for attr, value in defaults.items():
            getattr(self, f"{attr}_var").set(value)

class ScriptsWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Manage Scripts")

    def create_widgets(self):
        self.scripts_listbox = tk.Listbox(self, width=80, height=15)
        self.scripts_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10, fill=tk.X)

        buttons = [
            ("Upload Script", self.upload_script),
            ("Add Text", self.add_text),
            ("Move Up", self.move_up),
            ("Move Down", self.move_down),
            ("Delete Selected", self.delete_selected),
            ("Close", self.on_close)
        ]

        for text, command in buttons:
            ttk.Button(buttons_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        self.update_listbox()

    def upload_script(self):
        file_paths = self.parent.file_handler.get_file_paths("Select Script(s) or Paper(s)")
        for file_path in file_paths:
            self.parent.file_handler.upload_script(self.parent, file_path)
        self.update_listbox()

    def add_text(self):
        AddTextWindow(self, "script")

    def move_up(self):
        self.move_item(-1)

    def move_down(self):
        self.move_item(1)

    def move_item(self, direction):
        selection = self.scripts_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index + direction < len(self.parent.scripts):
                self.parent.scripts[index], self.parent.scripts[index + direction] = \
                    self.parent.scripts[index + direction], self.parent.scripts[index]
                self.update_listbox()
                self.scripts_listbox.select_set(index + direction)
                self.parent.file_handler.save_script_texts(self.parent)

    def delete_selected(self):
        selection = self.scripts_listbox.curselection()
        if selection:
            del self.parent.scripts[selection[0]]
            self.update_listbox()
            self.parent.file_handler.save_script_texts(self.parent)

    def update_listbox(self):
        self.scripts_listbox.delete(0, tk.END)
        for script in self.parent.scripts:
            self.scripts_listbox.insert(tk.END, script[0])

    def on_close(self):
        self.parent.update_system_prompt()
        self.parent.save_all_settings()
        self.destroy()

class InstructionsWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Manage Instructions")

    def create_widgets(self):
        self.instructions_listbox = tk.Listbox(self, width=80, height=15)
        self.instructions_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10, fill=tk.X)

        buttons = [
            ("Upload Instruction", self.upload_instruction),
            ("Add Text", self.add_text),
            ("Move Up", self.move_up),
            ("Move Down", self.move_down),
            ("Delete Selected", self.delete_selected),
            ("Close", self.on_close)
        ]

        for text, command in buttons:
            ttk.Button(buttons_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        self.update_listbox()

    def upload_instruction(self):
        file_paths = self.parent.file_handler.get_file_paths("Select Instruction File(s)")
        for file_path in file_paths:
            self.parent.file_handler.upload_instruction(self.parent, file_path)
        self.update_listbox()

    def add_text(self):
        AddTextWindow(self, "instruction")

    def move_up(self):
        self.move_item(-1)

    def move_down(self):
        self.move_item(1)

    def move_item(self, direction):
        selection = self.instructions_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index + direction < len(self.parent.instructions):
                self.parent.instructions[index], self.parent.instructions[index + direction] = \
                    self.parent.instructions[index + direction], self.parent.instructions[index]
                self.update_listbox()
                self.instructions_listbox.select_set(index + direction)
                self.parent.file_handler.save_instruction_texts(self.parent)  # Add this line

    def delete_selected(self):
        selection = self.instructions_listbox.curselection()
        if selection:
            del self.parent.instructions[selection[0]]
            self.update_listbox()
            self.parent.file_handler.save_instruction_texts(self.parent)

    def update_listbox(self):
        self.instructions_listbox.delete(0, tk.END)
        for instruction in self.parent.instructions:
            self.instructions_listbox.insert(tk.END, instruction[0])

    def on_close(self):
        self.parent.update_system_prompt()
        self.parent.save_all_settings()
        self.destroy()

class InternetSourcesWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Manage Internet Sources")

    def create_widgets(self):
        self.internet_listbox = tk.Listbox(self, width=80, height=15)
        self.internet_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10, fill=tk.X)

        buttons = [
            ("Add Link", self.add_link),
            ("Move Up", self.move_up),
            ("Move Down", self.move_down),
            ("Delete Selected", self.delete_selected),
            ("Close", self.on_close)
        ]

        for text, command in buttons:
            ttk.Button(buttons_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        self.update_listbox()

    def add_link(self):
        AddLinkWindow(self)

    def move_up(self):
        self.move_item(-1)

    def move_down(self):
        self.move_item(1)

    def move_item(self, direction):
        selection = self.internet_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index + direction < len(self.parent.internet_sources):
                self.parent.internet_sources[index], self.parent.internet_sources[index + direction] = \
                    self.parent.internet_sources[index + direction], self.parent.internet_sources[index]
                self.update_listbox()
                self.internet_listbox.select_set(index + direction)
                self.parent.file_handler.save_internet_sources(self.parent)  # Add this line

    def delete_selected(self):
        selection = self.internet_listbox.curselection()
        if selection:
            del self.parent.internet_sources[selection[0]]
            self.update_listbox()
            self.parent.file_handler.save_internet_sources(self.parent)

    def update_listbox(self):
        self.internet_listbox.delete(0, tk.END)
        for source in self.parent.internet_sources:
            self.internet_listbox.insert(tk.END, f"{source['url']} (Author: {source['author']}, Date: {source['date']})")

    def on_close(self):
        self.parent.update_system_prompt()
        self.parent.save_all_settings()
        self.destroy()

class AddLinkWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Add Internet Source")
        self.geometry("500x250")

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, pady=5)

        ttk.Label(main_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.author_entry = ttk.Entry(main_frame, width=50)
        self.author_entry.grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=20)
        self.date_entry.grid(row=2, column=1, pady=5)
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_entry.insert(0, current_date)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(buttons_frame, text="OK", command=self.save_link).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def save_link(self):
        url = self.url_entry.get().strip()
        author = self.author_entry.get().strip()
        date = self.date_entry.get().strip()

        if not url or not author or not date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        content = self.parent.parent.file_handler.scrape_webpage(url)
        if content is None:
            return

        source = {
            'url': url,
            'author': author,
            'date': date,
            'content': content
        }

        self.parent.parent.internet_sources.append(source)
        self.parent.parent.file_handler.save_internet_sources(self.parent.parent)
        self.parent.update_listbox()
        self.destroy()

class AddTextWindow(BaseWindow):
    def __init__(self, parent, text_type):
        self.text_type = text_type
        super().__init__(parent, f"Add {text_type.capitalize()} Text")
        self.geometry("500x400")

    def create_widgets(self):
        ttk.Label(self, text="Title:").pack(pady=(10, 0))
        self.title_entry = ttk.Entry(self, width=50)
        self.title_entry.pack(pady=(0, 10))

        ttk.Label(self, text="Text:").pack()
        self.text_area = tk.Text(self, wrap=tk.WORD, width=60, height=15)
        self.text_area.pack(pady=10, padx=10)

        ttk.Button(self, text="Save", command=self.save_text).pack(pady=10)

    def save_text(self):
        title = self.title_entry.get().strip()
        text = self.text_area.get(1.0, tk.END).strip()

        if not title or not text:
            tk.messagebox.showerror("Error", "Both title and text must be provided.")
            return

        if self.text_type == "script":
            self.parent.parent.scripts.append((title, text))
            self.parent.parent.file_handler.save_script_texts(self.parent.parent)
        elif self.text_type == "instruction":
            self.parent.parent.instructions.append((title, text))
            self.parent.parent.file_handler.save_instruction_texts(self.parent.parent)

        self.parent.update_listbox()
        self.destroy()

class CustomPromptsWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Manage Custom Prompts")

    def create_widgets(self):
        self.prompts_listbox = tk.Listbox(self, width=80, height=15)
        self.prompts_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10, fill=tk.X)

        buttons = [
            ("Load Selected", self.load_prompt),
            ("Delete Selected", self.delete_prompt),
            ("Close", self.destroy)
        ]

        for text, command in buttons:
            ttk.Button(buttons_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        self.update_listbox()

    def load_prompt(self):
        selection = self.prompts_listbox.curselection()
        if selection:
            prompt_name = self.prompts_listbox.get(selection[0])
            prompt = self.parent.custom_prompts.get(prompt_name)
            if prompt:
                self.parent.system_prompt_text.delete(1.0, tk.END)
                self.parent.system_prompt_text.insert(tk.END, prompt)
                self.destroy()

    def delete_prompt(self):
        selection = self.prompts_listbox.curselection()
        if selection:
            prompt_name = self.prompts_listbox.get(selection[0])
            if tk.messagebox.askyesno("Delete Prompt", f"Are you sure you want to delete the prompt '{prompt_name}'?"):
                del self.parent.custom_prompts[prompt_name]
                self.parent.save_all_settings()
                self.update_listbox()

    def update_listbox(self):
        self.prompts_listbox.delete(0, tk.END)
        for prompt_name in self.parent.custom_prompts.keys():
            self.prompts_listbox.insert(tk.END, prompt_name)
        self.parent
