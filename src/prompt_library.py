from enum import Enum
from langchain.prompts import PromptTemplate

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