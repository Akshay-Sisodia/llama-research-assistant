# Llama Research Assistant 🦙📚

A powerful research assistant powered by Llama 3.2, LangChain, and LangGraph. This application helps users conduct research by automatically routing queries, performing web searches, and generating comprehensive research reports.

## 🌟 Features

- **Intelligent Query Routing**: Automatically determines whether to use direct generation or web search
- **Advanced Web Search**: Integrates with Google Serper API for up-to-date information
- **Research Report Generation**: Creates well-structured reports with proper citations
- **Graph-based Workflow**: Uses LangGraph for sophisticated query processing
- **User-friendly Interface**: Built with Streamlit for easy interaction

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llama-research-assistant.git
cd llama-research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application:
```bash
streamlit run src/main.py
```

## 🔧 Configuration

Required environment variables:
- `SERPER_API_KEY`: Your Google Serper API key

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# docs/setup_guide.md
# Detailed Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Serper API key
- Git

## Installation Steps

### 1. Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. API Configuration

1. Get a Google Serper API key from [serper.dev](https://serper.dev)
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Add your API key to `.env`:
```
SERPER_API_KEY=your_key_here
```

### 3. Running the Application

1. Start the Streamlit server:
```bash
streamlit run src/main.py
```
2. Open your browser to `http://localhost:8501`

## Troubleshooting

Common issues and solutions:

1. **ImportError**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. **API Key Error**: Verify your `.env` file contains the correct API key

3. **Model Loading Error**: Ensure you have enough RAM (minimum 8GB recommended)