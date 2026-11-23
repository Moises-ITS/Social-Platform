from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str | None = os.getenv("DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
settings = Settings()