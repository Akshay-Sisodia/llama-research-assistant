import unittest
from unittest.mock import patch, MagicMock
from src.research_assistant import ResearchAssistant, GraphState

class TestResearchAssistant(unittest.TestCase):
    @patch('streamlit.sidebar')
    @patch('langchain_community.chat_models.ChatOllama')
    @patch('langchain_community.utilities.GoogleSerperAPIWrapper')
    def setUp(self, mock_serper, mock_ollama, mock_sidebar):
        self.assistant = ResearchAssistant()
        self.mock_serper = mock_serper
        self.mock_ollama = mock_ollama

    def test_workflow_initialization(self):
        self.assertIsNotNone(self.assistant.workflow)
        
    @patch('streamlit.markdown')
    def test_process_query(self, mock_markdown):
        test_query = "What is artificial intelligence?"
        mock_result = {"generation": "Test response about AI"}
        self.assistant.workflow.invoke = MagicMock(return_value=mock_result)
        
        response = self.assistant.process_query(test_query)
        self.assertEqual(response, "")
        mock_markdown.assert_called_once_with("Test response about AI", unsafe_allow_html=True)