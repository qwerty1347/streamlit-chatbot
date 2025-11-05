from decouple import config
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
STORAGE_PATH = PROJECT_ROOT / "storage"