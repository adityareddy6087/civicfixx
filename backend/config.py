import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment settings
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "civicfix.db"))
