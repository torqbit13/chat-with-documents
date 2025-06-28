import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
EMBEDDING_MODEL_NAME = "models/text-embedding-004"
LLM_MODEL_NAME = "gemini-1.5-flash-8b"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Vector Store Configuration
VECTOR_STORE_SEARCH_TYPE = "similarity"
VECTOR_STORE_SEARCH_K = 2

