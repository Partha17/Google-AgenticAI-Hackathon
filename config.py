import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Existing settings
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./agentic_ai.db")
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    collection_interval_minutes: int = int(os.getenv("COLLECTION_INTERVAL_MINUTES", "5"))
    insights_generation_interval_minutes: int = int(os.getenv("INSIGHTS_GENERATION_INTERVAL_MINUTES", "15"))
    
    # AI quota management
    max_daily_ai_requests: int = int(os.getenv("MAX_DAILY_AI_REQUESTS", "30"))
    max_hourly_ai_requests: int = int(os.getenv("MAX_HOURLY_AI_REQUESTS", "5"))
    ai_insights_on_demand_only: bool = os.getenv("AI_INSIGHTS_ON_DEMAND_ONLY", "true").lower() == "true"
    
    # Google Cloud ADK Configuration
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    google_genai_use_vertexai: bool = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "1") == "1"
    
    # Multi-Agent System Configuration
    adk_port: int = int(os.getenv("ADK_PORT", "8000"))
    adk_host: str = os.getenv("ADK_HOST", "localhost")
    agent_communication_timeout: int = int(os.getenv("AGENT_COMMUNICATION_TIMEOUT", "30"))
    max_concurrent_agents: int = int(os.getenv("MAX_CONCURRENT_AGENTS", "5"))
    
    class Config:
        env_file = ".env"

settings = Settings() 