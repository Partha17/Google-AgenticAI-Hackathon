import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./agentic_ai.db")
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    collection_interval_minutes: int = int(os.getenv("COLLECTION_INTERVAL_MINUTES", "5"))
    insights_generation_interval_minutes: int = int(os.getenv("INSIGHTS_GENERATION_INTERVAL_MINUTES", "15"))
    
    class Config:
        env_file = ".env"

settings = Settings() 