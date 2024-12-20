import os
from enum import Enum
from typing import Tuple, Dict, Any

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from dotenv import load_dotenv

# Constants
load_dotenv()
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MODEL = "llama3.2:3b"
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

class PromptType(Enum):
    """Enumeration of available prompt types."""
    GENERATE = "generate"
    ROUTER = "router"
    QUERY = "query"

class PromptLibrary:
    """Advanced prompt template library with improved prompts."""
    
    @staticmethod
    def get_prompt(prompt_type: PromptType) -> PromptTemplate:
        """Get a specific prompt template by type."""
        
        prompts = {
            PromptType.GENERATE: PromptTemplate.from_template(
                """
                <|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            You are a research assistant skilled at creating comprehensive research reports. Your tasks are to:

            1. Analyze the provided web search context.
            2. Extract key findings.
            3. Synthesize a clear, structured, and concise response.
            4. Cite sources accurately in academic style:
            - "References:
                Author/Org. Name (Year). Title. Publisher. <a href='URL'>Link</a>"
            - Use in-text citations (Author, Year).
            5. Maintain objectivity and note limitations.

            Guidelines:
            - Ensure relevance and accuracy.
            - Use professional, straightforward language.
            - Divide the response into clear sections.
            <|eot_id|>

            <|start_header_id|>user<|end_header_id|>
            Research Question: {question}

            Search Context:
            {context}

            Provide a detailed, well-cited analysis addressing the research question.
            <|eot_id|>

            <|start_header_id|>assistant<|end_header_id|>
            """
            ),
            
            PromptType.ROUTER: PromptTemplate.from_template(
               """
            <|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            You are an expert at determining whether a question requires a web search or direct response generation.

            Use web search for:
            - Recent events or time-sensitive info.
            - Detailed statistics or complex topics.
            - Specific facts requiring reliable sources.

            Use direct generation for:
            - Basic concepts, general knowledge.
            - Logical reasoning or theoretical explanations.

            Output EXACTLY this JSON:
            {{
                "choice": "web_search" or "generate"
            }}
            <|eot_id|>

            <|start_header_id|>user<|end_header_id|>
            Analyze this question: {question}

            Respond ONLY with the JSON format.
            <|eot_id|>

            <|start_header_id|>assistant<|end_header_id|>

               """
            ),
            
            PromptType.QUERY: PromptTemplate.from_template(
            """
          <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        You are a search query optimizer. Transform user questions into precise, effective search queries. 

        Optimization Rules:
        1. Focus on key terms and essential context.
        2. Remove unnecessary words.
        3. Use search operators when useful.
        4. Retain technical and specific terms.

        Output JSON format:
        {{
            "query": "optimized search string"
        }}
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Transform this question into an optimized search query: {question}
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
            """
            )
        }
        return prompts[prompt_type]

class GraphState(TypedDict):
    """Represents the state of our workflow graph."""
    question: str
    generation: str
    search_query: str
    context: str

class ResearchAssistant:
    """Main class implementing the research assistant functionality."""
    
    def __init__(self):
        """Initialize the research assistant with necessary components."""
        self.prompt_library = PromptLibrary()
        self.llm, self.llm_json = self._configure_llm()
        self.serper = GoogleSerperAPIWrapper(api_key=SERPER_API_KEY,type="news")
        self.workflow = self._build_workflow()
    
    def _configure_llm(self) -> Tuple[ChatOllama, ChatOllama]:  
        """Configure LLM models based on user settings."""
        st.sidebar.header("Configure LLM")
        
        model = st.sidebar.selectbox(
            "Choose the LLM Model",
            options=["llama3.2:3b"],
            index=0
        )
        
        temperature = 0.5
        
        return (
            ChatOllama(model=model, temperature=temperature),
            ChatOllama(model=model, format='json', temperature=temperature)
        )
    
    def _build_workflow(self) -> StateGraph:
        """Build the workflow graph for processing queries."""
        # Initialize chains
        generate_chain = (
            self.prompt_library.get_prompt(PromptType.GENERATE) | 
            self.llm | 
            StrOutputParser()
        )
        query_chain = (
            self.prompt_library.get_prompt(PromptType.QUERY) | 
            self.llm_json | 
            JsonOutputParser()
        )
        question_router = (
            self.prompt_library.get_prompt(PromptType.ROUTER) | 
            self.llm_json | 
            JsonOutputParser()
        )
        
        # Define node functions with error handling
        def generate(state: Dict[str, Any]) -> Dict[str, str]:
            """Generate final response."""
            try:
                generation = generate_chain.invoke({
                    "context": state.get("context", ""),
                    "question": state["question"]
                })
                return {"generation": generation}
            except Exception as e:
                st.error(f"Error in generate: {str(e)}")
                return {"generation": "An error occurred while generating the response."}
        
        def transform_query(state: Dict[str, Any]) -> Dict[str, str]:
            """Transform user question for web search."""
            try:
                gen_query = query_chain.invoke({"question": state["question"]})
                return {"search_query": gen_query.get("query", state["question"])}
            except Exception as e:
                st.error(f"Error in transform_query: {str(e)}")
                return {"search_query": state["question"]}
        
        def web_search(state: Dict[str, Any]) -> Dict[str, str]:
            """Perform web search."""
            try:
                result = self.serper.run(state["search_query"])
                return {"context": result}
            except Exception as e:
                st.error(f"Error in web_search: {str(e)}")
                return {"context": "Error performing web search."}
        
        def route_question(state: Dict[str, Any]) -> str:
            """Route question to appropriate processing path with error handling."""
            try:
                output = question_router.invoke({"question": state["question"]})
                # Ensure the output has the expected structure
                if not isinstance(output, dict) or "choice" not in output:
                    st.warning("Invalid router response format. Defaulting to web search.")
                    return "websearch"
                
                choice = output["choice"].lower()
                if choice not in ["web_search", "generate"]:
                    st.warning(f"Unexpected routing choice: {choice}. Defaulting to web search.")
                    return "websearch"
                
                return "websearch" if choice == "web_search" else "generate"
            except Exception as e:
                st.error(f"Error in route_question: {str(e)}")
                return "websearch"  # Default to web search on error
        
        # Build workflow graph
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("websearch", web_search)
        workflow.add_node("transform_query", transform_query)
        workflow.add_node("generate", generate)
        
        # Add edges
        workflow.set_conditional_entry_point(
            route_question,
            {
                "websearch": "transform_query",
                "generate": "generate"
            }
        )
        workflow.add_edge("transform_query", "websearch")
        workflow.add_edge("websearch", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    def process_query(self, query: str) -> str:
        """Process a user query and return the response."""
        try:
            result = self.workflow.invoke({"question": query})
            generation = result.get("generation", "An error occurred while processing your query.")
            # Use st.markdown to render HTML links
            st.markdown(generation, unsafe_allow_html=True)
            return ""  # Return empty string since we're using st.markdown directly
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            return "An error occurred while processing your query."

def main():
    """Main application entry point."""
    st.title("Research Assistant powered by Llama 3.2")
    
    assistant = ResearchAssistant()
    
    user_query = st.text_input("Enter your research question:", "")
    if st.button("Run Query") and user_query:
        with st.spinner("Processing your query..."):
            assistant.process_query(user_query)  # Response is now handled within process_query

if __name__ == "__main__":
    main()