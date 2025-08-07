# utils/agents.py
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from utils.config import OPENAI_API_KEY

# Initialize the LLM for agents
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.2)

# Tool for bug detection and fixing
@tool
def detect_and_fix_bugs(code: str, language: str) -> str:
    """
    Detect bugs in the code and provide fixes.
    
    Args:
        code: The source code to analyze
        language: The programming language of the code
    
    Returns:
        A string with bug analysis and fixed code
    """
    prompt = f"""
    Analyze the following {language} code for bugs:
    - Identify syntax errors
    - Identify logical errors
    - Identify potential runtime errors
    - Provide fixed code
    
    Code:
    {code}
    
    Analysis and fixed code:
    """
    
    response = llm.invoke(prompt)
    return response.content

# Tool for code optimization
@tool
def optimize_code(code: str, language: str) -> str:
    """
    Optimize the code for performance, security, and readability.
    
    Args:
        code: The source code to optimize
        language: The programming language of the code
    
    Returns:
        A string with optimization suggestions and optimized code
    """
    prompt = f"""
    Optimize the following {language} code for:
    - Performance (time and space complexity)
    - Security (vulnerabilities, best practices)
    - Readability (naming, structure, comments)
    
    Provide:
    1. Optimization suggestions
    2. Optimized code
    
    Code:
    {code}
    
    Optimization analysis and optimized code:
    """
    
    response = llm.invoke(prompt)
    return response.content

# Tool for auto-documentation
@tool
def generate_documentation(code: str, language: str) -> str:
    """
    Generate documentation for the code including docstrings, comments, and markdown.
    
    Args:
        code: The source code to document
        language: The programming language of the code
    
    Returns:
        A string with documented code and markdown documentation
    """
    prompt = f"""
    Generate comprehensive documentation for the following {language} code:
    1. Add detailed docstrings to functions/classes
    2. Add inline comments where needed
    3. Create markdown documentation explaining:
       - Purpose of the code
       - How to use it
       - Parameters and return values
       - Examples
    
    Code:
    {code}
    
    Documented code and markdown documentation:
    """
    
    response = llm.invoke(prompt)
    return response.content

# List of tools
tools = [
    detect_and_fix_bugs,
    optimize_code,
    generate_documentation
]

# Create the prompt template for the agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert software engineer assistant. Your task is to help with code analysis, optimization, and documentation."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent(input_text, code, language):
    """
    Run the agent with the given input, code, and language.
    
    Args:
        input_text: The user's request
        code: The code to analyze
        language: The programming language
    
    Returns:
        The agent's response
    """
    formatted_input = f"{input_text}\n\nCode:\n{code}\n\nLanguage: {language}"
    response = agent_executor.invoke({"input": formatted_input})
    return response["output"]