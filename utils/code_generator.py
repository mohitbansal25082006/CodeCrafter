# utils/code_generator.py
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from utils.config import OPENAI_API_KEY

# Initialize the LLM
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.5)

# Create a prompt template for code generation
code_template = """
You are an expert programmer. Write a {language} function that {task}.
Include comments and a docstring.
Also, analyze the time and space complexity and add it as a comment at the end.

Task: {task}
Language: {language}
"""

code_prompt = PromptTemplate(
    input_variables=["language", "task"],
    template=code_template
)

# Create the chain using the new pipe operator syntax
code_chain = code_prompt | llm

def generate_code(language, task):
    """Generate code based on the task and language."""
    # Format the prompt and invoke the chain
    result = code_chain.invoke({"language": language, "task": task})
    return result