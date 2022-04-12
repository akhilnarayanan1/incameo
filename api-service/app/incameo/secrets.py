from pathlib import Path
import dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, "..", "..", ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)