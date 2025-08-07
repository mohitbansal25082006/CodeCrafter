# utils/config.py
import os
import streamlit as st

# Get OpenAI API key from environment or secrets
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

# Get GitHub token from environment or secrets
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or st.secrets.get("GITHUB_TOKEN", "")

# Check if OpenAI API key is set
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in your Streamlit Cloud secrets or environment variables.")
    st.stop()

# Simple vector store settings - use /tmp for Streamlit Cloud
VECTOR_STORE_PATH = os.environ.get("VECTOR_STORE_PATH", "/tmp/codecrafter_snippets.json")

# App settings
APP_TITLE = "CodeCrafter"
APP_ICON = "🛠️"