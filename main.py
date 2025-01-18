import streamlit as st
from src.research_assistant import ResearchAssistant

def main():
    """Main application entry point."""
    st.title("Research Assistant powered by LLMs")
    
    assistant = ResearchAssistant()
    
    user_query = st.text_input("Enter your research question:", "")
    if st.button("Run Query") and user_query:
        with st.spinner("Processing your query..."):
            assistant.process_query(user_query)  # Response is now handled within process_query

if __name__ == "__main__":
    main()