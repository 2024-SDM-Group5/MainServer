from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    @staticmethod
    def init_app(app):
        pass

config = {
    'default': Config,
}
