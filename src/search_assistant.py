import os
from typing import Tuple, Dict, Any
import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from .prompt_library import PromptLibrary, PromptType

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
        self.serper = GoogleSerperAPIWrapper(api_key=os.getenv("SERPER_API_KEY"), type="news")
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
        
        # Define node functions
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
            """Route question to appropriate processing path."""
            try:
                output = question_router.invoke({"question": state["question"]})
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
                return "websearch"
        
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
            st.markdown(generation, unsafe_allow_html=True)
            return ""
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            return "An error occurred while processing your query."