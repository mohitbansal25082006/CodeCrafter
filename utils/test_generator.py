# utils/test_generator.py
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from utils.config import OPENAI_API_KEY

# Initialize the LLM
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.3)

# Create a prompt template for test generation
test_template = """
You are an expert in software testing. Generate unit tests for the following code.
Use the {testing_framework} framework.
Include:
- Basic test cases
- Boundary cases
- Edge cases

Code:
{code}

Tests:
"""

test_prompt = PromptTemplate(
    input_variables=["code", "testing_framework"],
    template=test_template
)

# Create the chain using the pipe operator
test_chain = test_prompt | llm

def generate_tests(code, testing_framework="pytest"):
    """Generate unit tests for the given code."""
    result = test_chain.invoke({"code": code, "testing_framework": testing_framework})
    return result