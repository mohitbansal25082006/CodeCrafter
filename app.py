# app.py
import streamlit as st
from utils.code_generator import generate_code
from utils.explainer import explain_code
from utils.test_generator import generate_tests
from utils.vector_store import vector_store
from utils.config import APP_TITLE, APP_ICON
import uuid
import time

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("### AI-Powered Code Generation Assistant")

# Initialize session state variables
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'tests' not in st.session_state:
    st.session_state.tests = ""
if 'snippet_id' not in st.session_state:
    st.session_state.snippet_id = None

# Input fields
col1, col2 = st.columns([1, 2])
with col1:
    language = st.selectbox("Select Language", ["Python", "JavaScript", "Java", "C++"])
    testing_framework = st.selectbox("Testing Framework", ["pytest", "unittest", "Jest", "JUnit"])
with col2:
    task = st.text_area("Describe the task:", height=150)

# Search for similar snippets
st.subheader("Search for Similar Code Snippets")
search_query = st.text_input("Enter a query to search for similar snippets:")
if st.button("Search"):
    if search_query:
        with st.spinner("Searching..."):
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
            st.success("Code generated and stored successfully!")
    else:
        st.error("Please enter a task description.")

# Display results in tabs
if st.session_state.generated_code:
    tab1, tab2, tab3 = st.tabs(["Generated Code", "Explanation", "Test Cases"])
    
    with tab1:
        st.subheader("Generated Code")
        st.code(st.session_state.generated_code, language=language.lower())
        
        # Download button for code
        st.download_button(
            label="Download Code",
            data=st.session_state.generated_code,
            file_name=f"generated_code.{language.lower()}",
            mime="text/plain"
        )
    
    with tab2:
        st.subheader("Code Explanation")
        if not st.session_state.explanation:
            with st.spinner("Generating explanation..."):
                st.session_state.explanation = explain_code(st.session_state.generated_code)
        st.markdown(st.session_state.explanation)
        
        # Download button for explanation
        st.download_button(
            label="Download Explanation",
            data=st.session_state.explanation,
            file_name="explanation.md",
            mime="text/markdown"
        )
    
    with tab3:
        st.subheader("Test Cases")
        if not st.session_state.tests:
            with st.spinner("Generating tests..."):
                st.session_state.tests = generate_tests(st.session_state.generated_code, testing_framework)
        st.code(st.session_state.tests, language=language.lower())
        
        # Download button for tests
        st.download_button(
            label="Download Tests",
            data=st.session_state.tests,
            file_name=f"test_{language.lower()}.{language.lower()}",
            mime="text/plain"
        )