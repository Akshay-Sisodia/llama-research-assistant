
# Detailed Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Ollama installed
- Google Serper API key
- Git

## Installation Steps

### 1. Ollama Setup

1. Install Ollama based on your operating system:

   **macOS/Linux:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   **Windows:**
   - Download and install from [Ollama's website](https://ollama.com/download)

2. Pull the Llama 3.2 model:
   ```bash
   ollama pull llama3.2:3b
   ```

3. Verify Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

### 2. Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. API Configuration

1. Get a Google Serper API key from [serper.dev](https://serper.dev)
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Add your configurations to `.env`:
```
SERPER_API_KEY=your_key_here
DEFAULT_MODEL=llama3.2:3b
DEFAULT_TEMPERATURE=0.5
```

### 4. Running the Application

1. Ensure Ollama is running:
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   ```

2. Start the Streamlit server:
   ```bash
   streamlit run src/main.py
   ```

3. Open your browser to `http://localhost:8501`

## Troubleshooting

Common issues and solutions:

1. **Ollama Connection Error**:
   - Verify Ollama is running: `curl http://localhost:11434/api/tags`
   - Check if the model is downloaded: `ollama list`
   - Try restarting Ollama service

2. **Model Loading Error**: 
   - Ensure you have enough RAM (minimum 8GB recommended)
   - Try pulling the model again: `ollama pull llama3.2:3b`

3. **API Key Error**: 
   - Verify your `.env` file contains the correct API key