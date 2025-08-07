# app.py
import streamlit as st
import uuid
import time
import base64
import threading
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv

# Import our utility modules
from utils.code_generator import generate_code
from utils.explainer import explain_code
from utils.test_generator import generate_tests
from utils.agents import run_agent
from utils.github_api import GitHubAPI
from utils.pr_reviewer import generate_pr_review, extract_line_comments
from utils.vector_store import vector_store
from utils.config import APP_TITLE, APP_ICON
from utils.logger import logger

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Create FastAPI app for VS Code extension
api = FastAPI()

# Define request models for API endpoints
class GenerateCodeRequest(BaseModel):
    prompt: str
    language: str

class ExplainCodeRequest(BaseModel):
    code: str
    language: str

# API endpoints for VS Code extension
@api.post("/generate-code")
async def generate_code_api(request: GenerateCodeRequest):
    try:
        logger.info(f"API request to generate code: {request.prompt}")
        generated_code = generate_code(request.language, request.prompt)
        return {"code": generated_code}
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        return {"error": str(e)}

@api.post("/explain-code")
async def explain_code_api(request: ExplainCodeRequest):
    try:
        logger.info(f"API request to explain code")
        explanation = explain_code(request.code)
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"Error explaining code: {str(e)}")
        return {"error": str(e)}

# Function to get logo as base64
def get_img_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Initialize session state variables
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'tests' not in st.session_state:
    st.session_state.tests = ""
if 'snippet_id' not in st.session_state:
    st.session_state.snippet_id = None
if 'bug_analysis' not in st.session_state:
    st.session_state.bug_analysis = ""
if 'optimized_code' not in st.session_state:
    st.session_state.optimized_code = ""
if 'documentation' not in st.session_state:
    st.session_state.documentation = ""
if 'pr_review' not in st.session_state:
    st.session_state.pr_review = ""
if 'github_token' not in st.session_state:
    st.session_state.github_token = ""

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5E35B1;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .code-container {
        background-color: #262730;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 0.9rem;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stDownloadButton button {
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .stDownloadButton button:hover {
        background-color: #0b7dda;
    }
</style>
""", unsafe_allow_html=True)

# Add logo if available
try:
    img_base64 = get_img_as_base64("logo.png")
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{img_base64}");
                background-repeat: no-repeat;
                padding-top: 80px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
except:
    pass

# Main app title
st.markdown(f'<h1 class="main-header">{APP_ICON} {APP_TITLE}</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color: #757575; font-size: 1.2rem;">AI-Powered Code Generation Assistant</p>', unsafe_allow_html=True)

# Sidebar for GitHub settings
st.sidebar.header("GitHub Settings")
st.session_state.github_token = st.sidebar.text_input("GitHub Token", type="password", value=st.session_state.github_token)

# Main tabs
tab1, tab2 = st.tabs(["Code Generation", "GitHub PR Review"])

with tab1:
    # Input fields
    col1, col2 = st.columns([1, 2])
    with col1:
        language = st.selectbox("Select Language", ["Python", "JavaScript", "Java", "C++"])
        testing_framework = st.selectbox("Testing Framework", ["pytest", "unittest", "Jest", "JUnit"])
    with col2:
        task = st.text_area("Describe the task:", height=150)

    # Search for similar snippets
    st.markdown('<h3 class="sub-header">Search for Similar Code Snippets</h3>', unsafe_allow_html=True)
    search_query = st.text_input("Enter a query to search for similar snippets:")
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                logger.info(f"Searching for snippets: {search_query}")
                results = vector_store.search_snippets(search_query)
                if results['documents']:
                    st.write("Found similar snippets:")
                    for i, doc in enumerate(results['documents'][0]):
                        with st.expander(f"Snippet {i+1}"):
                            st.code(doc, language=results['metadatas'][0][i]['language'].lower())
                            st.write(f"Task: {results['metadatas'][0][i]['task']}")
                else:
                    st.write("No similar snippets found.")
        else:
            st.error("Please enter a search query.")

    # Generate code button
    if st.button("Generate Code", type="primary"):
        if task:
            with st.spinner("Generating code..."):
                logger.info(f"Generating code for task: {task}")
                # Generate code
                generated_code = generate_code(language, task)
                st.session_state.generated_code = generated_code
                
                # Store in vector store
                snippet_id = str(uuid.uuid4())
                st.session_state.snippet_id = snippet_id
                vector_store.add_snippet(
                    snippet_id=snippet_id,
                    code=generated_code,
                    metadata={
                        "language": language,
                        "task": task,
                        "timestamp": time.time()
                    }
                )
                logger.info("Code generated and stored successfully")
                st.success("Code generated and stored successfully!")
        else:
            logger.warning("Empty task submitted")
            st.error("Please enter a task description.")

    # Display results in tabs
    if st.session_state.generated_code:
        subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
            "Generated Code", 
            "Explanation", 
            "Test Cases",
            "Bug Detection",
            "Code Optimization",
            "Documentation"
        ])
        
        with subtab1:
            st.markdown('<h3 class="sub-header">Generated Code</h3>', unsafe_allow_html=True)
            st.code(st.session_state.generated_code, language=language.lower())
            
            # Download button for code
            st.download_button(
                label="Download Code",
                data=st.session_state.generated_code,
                file_name=f"generated_code.{language.lower()}",
                mime="text/plain"
            )
        
        with subtab2:
            st.markdown('<h3 class="sub-header">Code Explanation</h3>', unsafe_allow_html=True)
            if not st.session_state.explanation:
                with st.spinner("Generating explanation..."):
                    logger.info("Generating code explanation")
                    st.session_state.explanation = explain_code(st.session_state.generated_code)
            st.markdown(st.session_state.explanation)
            
            # Download button for explanation
            st.download_button(
                label="Download Explanation",
                data=st.session_state.explanation,
                file_name="explanation.md",
                mime="text/markdown"
            )
        
        with subtab3:
            st.markdown('<h3 class="sub-header">Test Cases</h3>', unsafe_allow_html=True)
            if not st.session_state.tests:
                with st.spinner("Generating tests..."):
                    logger.info("Generating test cases")
                    st.session_state.tests = generate_tests(st.session_state.generated_code, testing_framework)
            st.code(st.session_state.tests, language=language.lower())
            
            # Download button for tests
            st.download_button(
                label="Download Tests",
                data=st.session_state.tests,
                file_name=f"test_{language.lower()}.{language.lower()}",
                mime="text/plain"
            )
        
        with subtab4:
            st.markdown('<h3 class="sub-header">Bug Detection</h3>', unsafe_allow_html=True)
            bug_request = st.text_area("Describe what you want to check for bugs:", 
                                       value="Check for any bugs in this code", height=100)
            
            if st.button("Detect Bugs", key="bug_button"):
                with st.spinner("Analyzing for bugs..."):
                    logger.info("Running bug detection")
                    st.session_state.bug_analysis = run_agent(
                        bug_request, 
                        st.session_state.generated_code, 
                        language
                    )
            
            if st.session_state.bug_analysis:
                st.markdown(st.session_state.bug_analysis)
                
                # Download button for bug analysis
                st.download_button(
                    label="Download Bug Analysis",
                    data=st.session_state.bug_analysis,
                    file_name="bug_analysis.md",
                    mime="text/markdown"
                )
        
        with subtab5:
            st.markdown('<h3 class="sub-header">Code Optimization</h3>', unsafe_allow_html=True)
            opt_request = st.text_area("Describe optimization goals:", 
                                       value="Optimize this code for performance and readability", height=100)
            
            if st.button("Optimize Code", key="opt_button"):
                with st.spinner("Optimizing code..."):
                    logger.info("Running code optimization")
                    st.session_state.optimized_code = run_agent(
                        opt_request, 
                        st.session_state.generated_code, 
                        language
                    )
            
            if st.session_state.optimized_code:
                st.markdown(st.session_state.optimized_code)
                
                # Download button for optimized code
                st.download_button(
                    label="Download Optimized Code",
                    data=st.session_state.optimized_code,
                    file_name=f"optimized_code.{language.lower()}",
                    mime="text/plain"
                )
        
        with subtab6:
            st.markdown('<h3 class="sub-header">Documentation</h3>', unsafe_allow_html=True)
            doc_request = st.text_area("Describe documentation needs:", 
                                       value="Generate comprehensive documentation for this code", height=100)
            
            if st.button("Generate Documentation", key="doc_button"):
                with st.spinner("Generating documentation..."):
                    logger.info("Generating documentation")
                    st.session_state.documentation = run_agent(
                        doc_request, 
                        st.session_state.generated_code, 
                        language
                    )
            
            if st.session_state.documentation:
                st.markdown(st.session_state.documentation)
                
                # Download button for documentation
                st.download_button(
                    label="Download Documentation",
                    data=st.session_state.documentation,
                    file_name="documentation.md",
                    mime="text/markdown"
                )

with tab2:
    st.markdown('<h2 class="sub-header">GitHub Pull Request Review</h2>', unsafe_allow_html=True)
    
    # Input fields for PR review
    col1, col2 = st.columns(2)
    with col1:
        repo_owner = st.text_input("Repository Owner", placeholder="e.g., facebook")
        repo_name = st.text_input("Repository Name", placeholder="e.g., react")
    with col2:
        pr_number = st.number_input("Pull Request Number", min_value=1, step=1)
    
    # Review PR button
    if st.button("Review Pull Request", type="primary"):
        if not st.session_state.github_token:
            st.error("Please enter your GitHub token in the sidebar.")
        elif not all([repo_owner, repo_name, pr_number]):
            st.error("Please fill in all repository and PR details.")
        else:
            with st.spinner("Analyzing pull request..."):
                try:
                    logger.info(f"Reviewing PR {pr_number} in {repo_owner}/{repo_name}")
                    # Initialize GitHub API
                    github_api = GitHubAPI(token=st.session_state.github_token)
                    
                    # Get PR details
                    pr_details = github_api.get_pull_request(repo_owner, repo_name, pr_number)
                    pr_title = pr_details.get("title", "")
                    pr_description = pr_details.get("body", "")
                    
                    # Get PR files
                    pr_files = github_api.get_pull_request_files(repo_owner, repo_name, pr_number)
                    
                    # Generate review
                    review = generate_pr_review(
                        f"{repo_owner}/{repo_name}",
                        pr_number,
                        pr_title,
                        pr_description,
                        pr_files
                    )
                    
                    st.session_state.pr_review = review
                    
                    # Extract line comments
                    line_comments = extract_line_comments(review)
                    
                    # Post line comments to GitHub (optional)
                    if line_comments and st.checkbox("Post comments to GitHub"):
                        for comment in line_comments:
                            try:
                                # Find the file in PR files
                                file_info = next((f for f in pr_files if f['filename'] == comment['file']), None)
                                if file_info:
                                    # Get the commit ID
                                    commit_id = file_info.get('sha', '')
                                    
                                    # Post the comment
                                    github_api.create_pull_request_review_comment(
                                        repo_owner,
                                        repo_name,
                                        pr_number,
                                        commit_id,
                                        comment['file'],
                                        comment['line'],
                                        comment['comment']
                                    )
                            except Exception as e:
                                st.warning(f"Failed to post comment: {str(e)}")
                    
                    logger.info("Pull request review completed successfully")
                    st.success("Pull request review completed successfully!")
                    
                except Exception as e:
                    logger.error(f"Error reviewing pull request: {str(e)}")
                    st.error(f"Error reviewing pull request: {str(e)}")
    
    # Display PR review
    if st.session_state.pr_review:
        st.markdown('<h3 class="sub-header">Pull Request Review</h3>', unsafe_allow_html=True)
        st.markdown(st.session_state.pr_review)
        
        # Download button for PR review
        st.download_button(
            label="Download Review",
            data=st.session_state.pr_review,
            file_name=f"pr_{pr_number}_review.md",
            mime="text/markdown"
        )

# Footer
st.markdown(
    """
    <div class="footer">
        <p>CodeCrafter © 2023 | AI-Powered Coding Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Run FastAPI in a separate thread for VS Code extension
def run_fastapi():
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="error")

if __name__ == "__main__":
    # Start FastAPI in a daemon thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Run Streamlit
    import streamlit.web.cli as stcli
    import sys
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())