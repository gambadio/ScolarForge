# app.py

import tkinter as tk
from tkinter import ttk, messagebox
from windows import SettingsWindow, FormattingWindow, ScriptsWindow, InstructionsWindow, InternetSourcesWindow, CustomPromptsWindow, AutomaticInternetSearchWindow
from utils import FileHandler, APIHandler, DocumentHandler
from config import load_default_prompts

class ClaudeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Paper Generator")
        self.geometry("900x600")

        self.file_handler = FileHandler()
        self.api_handler = APIHandler()
        self.doc_handler = DocumentHandler()

        # Initialize variables
        self.api_key = ""
        self.perplexity_api_key = ""
        self.first_name = ""
        self.last_name = ""
        self.date = ""
        self.font_name = "Times New Roman"
        self.font_size_normal = 12
        self.font_size_heading1 = 16
        self.font_size_heading2 = 14
        self.font_size_heading3 = 12
        self.line_spacing = "1.5 lines"
        self.margin_top = 2.0
        self.margin_bottom = 2.0
        self.margin_left = 2.0
        self.margin_right = 2.0
        self.scripts = []
        self.instructions = []
        self.internet_sources = []
        self.custom_prompts = load_default_prompts()
        self.system_prompt = self.custom_prompts["default_system_prompt"]

        self.load_settings()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Green.TButton", foreground="black", background="lightgreen")
        style.map("Green.TButton", background=[('active', 'green')])
        style.configure("Blue.TButton", foreground="black", background="lightblue")
        style.map("Blue.TButton", background=[('active', 'blue')])

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_top_buttons(main_frame)
        self.create_switchable_frame(main_frame)
        self.create_middle_buttons(main_frame)
        self.create_output_text(main_frame)
        self.create_action_buttons(main_frame)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def create_top_buttons(self, parent):
        top_buttons_frame = ttk.Frame(parent)
        top_buttons_frame.grid(row=0, column=0, sticky=tk.W+tk.E, pady=5)

        ttk.Button(top_buttons_frame, text="⚙ Settings", command=self.open_settings_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons_frame, text="Save All Settings", command=self.save_all_settings).pack(side=tk.LEFT, padx=5)
        self.advanced_button = ttk.Button(top_buttons_frame, text="Advanced", command=self.toggle_advanced)
        self.advanced_button.pack(side=tk.RIGHT, padx=5)

    def create_switchable_frame(self, parent):
        self.switchable_frame = ttk.Frame(parent)
        self.switchable_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.basic_frame = ttk.Frame(self.switchable_frame)
        self.advanced_frame = ttk.Frame(self.switchable_frame)

        self.create_basic_frame()
        self.create_advanced_frame()

        self.basic_frame.pack(fill=tk.BOTH, expand=True)

    def create_basic_frame(self):
        self.create_prompt_frame(self.basic_frame)

    def create_advanced_frame(self):
        ttk.Label(self.advanced_frame, text="Advanced options will be added here.").pack(pady=20)

    def create_prompt_frame(self, parent):
        prompt_frame = ttk.Frame(parent)
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Label(prompt_frame, text="System Prompt:").pack(side=tk.LEFT, padx=5)
        self.system_prompt_text = tk.Text(prompt_frame, wrap=tk.WORD, height=10)
        self.system_prompt_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.system_prompt_text.insert(tk.END, self.system_prompt)

        prompt_buttons_frame = ttk.Frame(prompt_frame)
        prompt_buttons_frame.pack(side=tk.RIGHT, padx=5)

        button_width = 15
        ttk.Button(prompt_buttons_frame, text="Save Prompt", command=self.save_custom_prompt, width=button_width).pack(pady=2)
        ttk.Button(prompt_buttons_frame, text="Manage Prompts", command=self.open_custom_prompts_window, width=button_width).pack(pady=2)
        ttk.Button(prompt_buttons_frame, text="Reset Prompt", command=self.reset_system_prompt, width=button_width).pack(pady=2)

    def create_middle_buttons(self, parent):
        self.middle_buttons_frame = ttk.Frame(parent)
        self.middle_buttons_frame.grid(row=2, column=0, sticky=tk.W, pady=5)

        ttk.Button(self.middle_buttons_frame, text="Manage Scripts", command=self.open_scripts_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.middle_buttons_frame, text="Manage Instructions", command=self.open_instructions_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.middle_buttons_frame, text="Manage Internet Sources", command=self.open_internet_sources_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.middle_buttons_frame, text="Automatic Internet Search", command=self.open_automatic_internet_search_window).pack(side=tk.LEFT, padx=5)

    def create_output_text(self, parent):
        output_frame = ttk.Frame(parent)
        output_frame.grid(row=3, column=0, sticky=tk.NSEW, pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=12)
        self.output_text.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.output_text.config(yscrollcommand=scrollbar.set)

    def create_action_buttons(self, parent):
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=4, column=0, pady=10)

        ttk.Button(buttons_frame, text="Generate Paper", command=self.generate_paper, style="Green.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Output", command=self.save_output, style="Blue.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Formatting Options", command=self.open_formatting_window).pack(side=tk.LEFT, padx=5)

    def toggle_advanced(self):
        if self.basic_frame.winfo_viewable():
            self.basic_frame.pack_forget()
            self.advanced_frame.pack(fill=tk.BOTH, expand=True)
            self.advanced_button.config(text="Basic")
        else:
            self.advanced_frame.pack_forget()
            self.basic_frame.pack(fill=tk.BOTH, expand=True)
            self.advanced_button.config(text="Advanced")

    def open_settings_window(self):
        SettingsWindow(self)

    def open_formatting_window(self):
        FormattingWindow(self)

    def open_scripts_window(self):
        ScriptsWindow(self)

    def open_instructions_window(self):
        InstructionsWindow(self)

    def open_internet_sources_window(self):
        InternetSourcesWindow(self)

    def open_custom_prompts_window(self):
        CustomPromptsWindow(self)

    def open_automatic_internet_search_window(self):
        if not self.perplexity_api_key:
            messagebox.showerror("Error", "Please enter your Perplexity API key in the settings.")
            return
        AutomaticInternetSearchWindow(self)

    def save_custom_prompt(self):
        self.file_handler.save_custom_prompt(self)

    def generate_paper(self):
        self.api_handler.send_request(self)

    def save_output(self):
        self.doc_handler.save_output(self)

    def reset_system_prompt(self):
        self.system_prompt_text.delete(1.0, tk.END)
        self.system_prompt_text.insert(tk.END, self.custom_prompts["default_system_prompt"])

    def load_settings(self):
        settings = self.file_handler.load_all_settings()
        for key, value in settings.items():
            if key == 'internet_sources':
                self.internet_sources = value
            elif key == 'perplexity_api_key':
                self.perplexity_api_key = value
            else:
                setattr(self, key, value)

    def save_all_settings(self):
        self.file_handler.save_all_settings(self)

    def update_system_prompt(self):
        self.system_prompt = self.system_prompt_text.get(1.0, tk.END).strip().format(
            scripts=self.file_handler.format_scripts(self.scripts),
            instructions=self.file_handler.format_instructions(self.instructions),
            internet=self.file_handler.format_internet_sources(self.internet_sources),
            first_name=self.first_name,
            last_name=self.last_name,
            date=self.date
        )
