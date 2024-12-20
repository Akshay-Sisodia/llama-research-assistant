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