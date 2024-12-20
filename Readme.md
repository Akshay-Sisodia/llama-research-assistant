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