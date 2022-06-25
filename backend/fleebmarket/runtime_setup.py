import os
from pathlib import Path  # Python 3.6+ only

from dotenv import load_dotenv

root_path = Path(__file__).absolute().parent.parent.parent
env_paths = root_path / ".env"
print("Loading .env from", env_paths)
load_dotenv(dotenv_path=env_paths)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fleebmarket.settings")
