import os
from dotenv import load_dotenv
import streamlit as st
from research_assistant import ResearchAssistant

# Load environment variables
load_dotenv()

def main():
    """Main application entry point."""
    st.title("Research Assistant powered by Llama 3.2")
    
    assistant = ResearchAssistant()
    
    user_query = st.text_input("Enter your research question:", "")
    if st.button("Run Query") and user_query:
        with st.spinner("Processing your query..."):
            assistant.process_query(user_query)

if __name__ == "__main__":
    main()
