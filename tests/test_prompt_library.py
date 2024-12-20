import unittest
from src.prompt_library import PromptLibrary, PromptType
from langchain.prompts import PromptTemplate

class TestPromptLibrary(unittest.TestCase):
    def setUp(self):
        self.library = PromptLibrary()

    def test_get_prompt(self):
        for prompt_type in PromptType:
            prompt = self.library.get_prompt(prompt_type)
            self.assertIsInstance(prompt, PromptTemplate)
            self.assertTrue(prompt.template)

    def test_generate_prompt_content(self):
        generate_prompt = self.library.get_prompt(PromptType.GENERATE)
        self.assertIn("research assistant", generate_prompt.template.lower())
        self.assertIn("question", generate_prompt.input_variables)
        self.assertIn("context", generate_prompt.input_variables)