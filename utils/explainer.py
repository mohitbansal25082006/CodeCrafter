# utils/explainer.py
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from utils.config import OPENAI_API_KEY

# Initialize the LLM
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.3)

# Create a prompt template for code explanation
explanation_template = """
You are an expert programming instructor. Explain the following code in detail:
- Line-by-line logic
- Time and space complexity
- Use cases and edge cases

Code:
{code}

Explanation:
"""

explanation_prompt = PromptTemplate(
    input_variables=["code"],
    template=explanation_template
)

# Create the chain using the pipe operator
explanation_chain = explanation_prompt | llm

def explain_code(code):
    """Generate an explanation for the given code."""
    result = explanation_chain.invoke({"code": code})
    return result