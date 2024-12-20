# Llama Research Assistant 🦙📚

A powerful research assistant powered by Llama 3.2 (via Ollama), LangChain, and LangGraph. This application helps users conduct research by automatically routing queries, performing web searches, and generating comprehensive research reports.

## 🌟 Features

- **Llama 3.2 Integration**: Uses Ollama to run Llama 3.2 locally
- **Intelligent Query Routing**: Automatically determines whether to use direct generation or web search
- **Advanced Web Search**: Integrates with Google Serper API for up-to-date information
- **Research Report Generation**: Creates well-structured reports with proper citations
- **Graph-based Workflow**: Uses LangGraph for sophisticated query processing
- **User-friendly Interface**: Built with Streamlit for easy interaction

## 🚀 Quick Start

### Prerequisites

1. Install Ollama:

   **For macOS:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   **For Linux:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   **For Windows:**
   - Download and install from [Ollama's website](https://ollama.com/download)

2. Pull the Llama 3.2 model:
   ```bash
   ollama pull llama3.2:3b
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llama-research-assistant.git
   cd llama-research-assistant
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

6. Run the application:
   ```bash
   streamlit run src/main.py
   ```

## 🔧 Configuration

Required configurations:
- **Ollama**: Must be running locally.
- `SERPER_API_KEY`: Your Google Serper API key

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.