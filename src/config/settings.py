from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "sqlite:///src/database/questionnaire.db"


settings = Settings()
