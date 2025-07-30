# 🎓 ScolarForge

**The Ultimate Academic Research & Paper Generation Suite**

A comprehensive desktop application that revolutionizes academic writing by combining intelligent AI assistance with powerful research automation. ScolarForge integrates multiple AI services to help students and researchers create high-quality university papers with proper citations, formatting, and evidence-based content.

## ✨ Core Features

### 🤖 **Dual AI Integration**
- **Claude API**: Advanced paper generation with sophisticated academic writing capabilities
- **Perplexity API**: Real-time internet research and source verification
- **Intelligent Prompting**: Customizable system prompts optimized for academic writing
- **Multi-Model Support**: Flexible API configuration for different AI providers

### 📚 **Advanced Research Automation**
- **Automatic Search Term Generation**: AI analyzes your instructions to create targeted research queries
- **Internet Source Management**: Organize and manage research sources with full text extraction
- **Smart Content Synthesis**: Automatically integrates research findings into coherent academic arguments
- **Citation Management**: Harvard-style citations generated automatically from sources

### 📝 **Professional Academic Formatting**
- **University-Standard Templates**: Pre-configured formats for academic papers
- **Multi-Level Headings**: Proper heading hierarchy with automatic numbering
- **Bibliography Generation**: Automatic creation of properly formatted reference lists
- **Document Export**: Export to Word documents with professional formatting
- **Title Page Integration**: Automated title page generation with student details

### 🗂️ **Comprehensive Content Management**
- **Script Management**: Upload and organize lecture notes, study materials, and reference documents
- **Instruction Processing**: Define paper requirements and academic guidelines
- **Multi-Format Support**: Handle PDFs, text files, and various document formats
- **Content Extraction**: Intelligent text extraction from uploaded documents

### ⚙️ **Advanced Configuration**
- **Custom Prompt System**: Create and manage specialized prompts for different paper types
- **Formatting Controls**: Fine-tune margins, fonts, spacing, and document layout
- **API Management**: Secure storage and management of API credentials
- **Settings Persistence**: All configurations saved automatically across sessions

## 🚀 Quick Start Guide

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Claude API Key** from Anthropic
3. **Perplexity API Key** for research capabilities

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gambadio/ScolarForge.git
   cd ScolarForge
   ```

2. **Install required dependencies**:
   ```bash
   pip install requests python-docx PyPDF2 beautifulsoup4
   ```

3. **Launch ScolarForge**:
   ```bash
   python main.py
   ```

4. **Configure API Keys**:
   - Click "⚙ Settings" in the main interface
   - Enter your Claude API key
   - Enter your Perplexity API key
   - Configure your personal details (name, date, etc.)

## 📖 Comprehensive Usage Guide

### Creating Your First Academic Paper

1. **Set Up Your Project**:
   - Launch ScolarForge and configure your settings
   - Upload relevant scripts and study materials via "Manage Scripts"
   - Define paper instructions and requirements via "Manage Instructions"

2. **Research Phase**:
   - Use "Automatic Internet Search" to generate research queries
   - The system will automatically search for relevant academic sources
   - Review and organize found sources via "Manage Internet Sources"

3. **Paper Generation**:
   - Customize the system prompt for your specific paper type
   - Click "Generate Paper" to create your academic work
   - The AI will integrate your materials, research, and instructions

4. **Formatting & Export**:
   - Use "Formatting Options" to adjust document appearance
   - Click "Save Output" to export your paper to Word format
   - Final document includes proper citations and bibliography

### Advanced Features

**Custom Prompt Management**:
- Create specialized prompts for different assignment types
- Save and reuse successful prompt configurations
- Template system for common academic formats

**Research Workflow**:
- Automated generation of search terms based on your paper requirements
- Intelligent filtering and ranking of research results
- Integration of findings with proper academic citations

**Document Processing**:
- Extract text from PDFs and various document formats
- Organize materials by relevance and topic
- Automatic integration of quotes and references

## 🏗️ Technical Architecture

### Core Components

**Main Application (`app.py`)**
- Tkinter-based GUI with professional styling
- Modular window system for different functions
- Integrated settings and configuration management
- Real-time API communication and response handling

**Research Engine (`internet_search.py`)**
- Automated search term generation using Claude
- Perplexity API integration for web research
- Result processing and relevance scoring
- Citation-ready source formatting

**Document Processing (`utils.py`)**
- Multi-format file reading (PDF, TXT, DOCX)
- Intelligent text extraction and cleanup
- Academic formatting and styling
- Export functionality with proper document structure

**Configuration System (`config.py`)**
- Default academic prompts and templates
- Customizable system behaviors
- Template management for different paper types
- Settings persistence and validation

**GUI Components (`windows.py`)**
- Settings management interface
- Script and instruction organization
- Research source management
- Formatting and export controls

### Dependencies

- **requests**: API communication and web requests
- **python-docx**: Word document generation and formatting
- **PyPDF2**: PDF text extraction and processing
- **beautifulsoup4**: Web content parsing and cleanup

## 🎯 Paper Types & Templates

### Supported Academic Formats

- **Research Papers**: Full academic research with literature review
- **Essay Assignments**: Structured argumentative essays
- **Literature Reviews**: Comprehensive source analysis
- **Case Studies**: Detailed analytical papers
- **Lab Reports**: Scientific report formatting
- **Thesis Chapters**: Extended academic writing

### Built-in Features

- **Harvard Citation Style**: Automatic in-text citations and bibliography
- **Academic Tone**: B2/C1 level English with appropriate academic vocabulary
- **Proper Structure**: Introduction, body, conclusion, and references
- **Professional Formatting**: University-standard layout and typography

## ⚙️ Configuration Options

### API Settings
- **Claude API Configuration**: Model selection and parameters
- **Perplexity Integration**: Search parameters and result limits
- **Rate Limiting**: Automatic handling of API rate limits
- **Error Recovery**: Fallback strategies for API failures

### Document Formatting
- **Font Settings**: Family, size, and styling options
- **Layout Controls**: Margins, spacing, and alignment
- **Heading Styles**: Multi-level heading formatting
- **Citation Format**: Harvard, APA, or custom citation styles

### Content Management
- **Script Organization**: Categorization and tagging of source materials
- **Instruction Templates**: Reusable assignment guidelines
- **Source Management**: Automatic citation generation and reference tracking
- **Version Control**: Multiple drafts and revision tracking

## 🔧 Advanced Customization

### Custom Prompt Engineering
ScolarForge uses sophisticated prompt templates that can be customized for specific needs:

```
System Prompt Structure:
- Paper type and requirements
- Citation style preferences
- Content integration instructions
- Formatting specifications
- Quality control parameters
```

### Research Automation
The automated research system can be configured for different academic fields:
- **Search Strategy**: Keywords and phrase generation
- **Source Filtering**: Academic vs. general sources
- **Relevance Scoring**: Automatic content ranking
- **Citation Extraction**: Proper academic reference formatting

## 🛠️ Troubleshooting

### Common Issues

**API Connection Problems**:
- Verify API keys are correctly entered in settings
- Check internet connection and API service status
- Ensure sufficient API credits are available

**Document Processing Errors**:
- Verify uploaded files are not corrupted
- Check file permissions and accessibility
- Ensure supported file formats (PDF, TXT, DOCX)

**Formatting Issues**:
- Review formatting settings in the configuration panel
- Check Word document compatibility
- Verify citation style requirements

**Research Quality**:
- Refine instruction clarity and specificity
- Adjust search parameters for better results
- Review and curate internet sources manually

### Performance Optimization

- **Batch Processing**: Handle multiple documents efficiently
- **Caching**: Store frequently used prompts and settings
- **Memory Management**: Optimize for large document processing
- **API Efficiency**: Minimize unnecessary API calls

## 🤝 Contributing

ScolarForge welcomes contributions to enhance academic writing capabilities:

- **Template Expansion**: Additional paper formats and citation styles
- **AI Integration**: Support for new AI providers and models
- **Research Tools**: Enhanced source verification and fact-checking
- **Export Options**: Additional output formats and styling options
- **Collaboration Features**: Multi-user editing and sharing capabilities

## 📄 License

This project is open source. Please check the repository for specific license terms.

## 🌟 Acknowledgments

- **Anthropic**: For providing the Claude API that powers intelligent paper generation
- **Perplexity AI**: For enabling comprehensive internet research capabilities
- **Academic Community**: For inspiration and requirements that shaped this tool
- **Open Source Libraries**: For the foundation that makes this project possible

---

*Empowering academic excellence through intelligent automation - where research meets artificial intelligence.*