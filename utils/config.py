# utils/config.py
import os
import streamlit as st

# Try to get API keys from Streamlit secrets first, then environment variables
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", os.environ.get("GITHUB_TOKEN"))

# ChromaDB settings
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "data/chroma_db")

# App settings
APP_TITLE = "CodeCrafter"
APP_ICON = "🛠️"