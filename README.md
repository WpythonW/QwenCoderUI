# AI Code Generation & Completion Tool

The project provides two interfaces for AI-powered code generation and completion:
1. Multi-Language Code Generation Interface - Generates code in multiple programming languages using different AI models
2. Code Completion Interface - Helps complete partial code snippets

## Features

### Code Completion Interface
- Complete partial code with placeholders ([...] or <...>)
- Syntax validation
- Adjustable generation parameters
- Pre-built code templates
- Real-time syntax checking of generated code

### Code Generation Interface
- Support for multiple programming languages:
  - Python
  - JavaScript
  - C++
- Multiple AI models:
  - Qwen 2.5 Coder (32B)
  - StarCoder 2 (15B)
- Customizable generation parameters:
  - Max tokens
  - Temperature
  - Top P
- Language-specific prompt formatting
- Side-by-side comparison of different models' outputs

## Installation

1. Clone the repository:
```bash
git clone https://github.com/WpythonW/QwenCoderUI.git
cd QwenCoderUI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your HuggingFace API key:
```
API_KEY_HUGGINGFACE=your_api_key_here
```

## Usage

### Running the Code Completion Interface
```bash
streamlit run ast_interface.py
```

### Running the Code Generation Interface
```bash
streamlit run app.py
```

## Interface Descriptions

### Code Completion Interface (ast_interface.py)
- Input your code with placeholders ([...] or <...>)
- Adjust generation parameters (max tokens, temperature)
- Use pre-built templates for common code patterns
- View syntax-highlighted completed code
- Get instant feedback on code validity

### Code Generation Interface (app.py)
- Enter your code generation request in natural language
- Choose between different programming languages
- Compare outputs from different AI models
- Fine-tune generation parameters
- View generated code with proper formatting

## Project Structure

```
├── app.py                 # Multi-language code generation interface
├── ast_interface.py       # Code completion interface
├── llms_api_client.py     # Unified API client for AI models
├── requirements.txt       # Project dependencies
└── .env                   # Environment variables (API keys)
```

## Technical Details

- Uses Streamlit for web interface
- Supports asynchronous API calls for better performance
- Implements unified API client for different AI models
- Uses type hints for better code maintainability
- Includes comprehensive error handling and logging
- Supports customizable prompt templates for different languages

## Requirements

- Python 3.8+
- HuggingFace API key
- Internet connection for API access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]