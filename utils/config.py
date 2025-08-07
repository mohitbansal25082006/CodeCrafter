# utils/config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ChromaDB settings
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "E:/CodeCrafter/data/chroma_db")

# App settings
APP_TITLE = os.getenv("APP_TITLE", "CodeCrafter")
APP_ICON = os.getenv("APP_ICON", "🛠️")