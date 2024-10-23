import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024 * 1024))  # Default to 1 MB if not set
