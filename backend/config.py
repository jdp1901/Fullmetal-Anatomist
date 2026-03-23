"""Application configuration."""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "fullmetal.db"
TEMPLATES_DIR = BASE_DIR / "templates"
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

# Server
HOST = os.getenv("FMA_HOST", "127.0.0.1")
PORT = int(os.getenv("FMA_PORT", "8765"))

# Encryption key derivation salt (for API key encryption)
ENCRYPTION_SALT = b"fullmetal-anatomist-2026"
