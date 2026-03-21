import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Max file size to read in one go (e.g., 10MB)
MAX_FILE_SIZE_MB = 10
MAX_BUFFER_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

# Extractor settings
MAX_ERROR_LINES = 50  # Max lines to send to AI per error
