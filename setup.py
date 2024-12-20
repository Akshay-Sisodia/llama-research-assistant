from setuptools import setup, find_packages

setup(
    name="llama-research-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.24.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.1",
        "langgraph>=0.0.1",
        "typing-extensions>=4.7.1",
        "python-dotenv>=0.19.0",
        "google-serper>=0.1.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A research assistant powered by Llama 3.2, LangChain, and LangGraph",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llama-research-assistant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)