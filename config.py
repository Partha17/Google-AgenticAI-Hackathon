import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Existing settings
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./agentic_ai.db")
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app")
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
    
    # Google Cloud Storage Configuration
    google_cloud_storage_bucket: str = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "")
    google_cloud_storage_prefix: str = os.getenv("GOOGLE_CLOUD_STORAGE_PREFIX", "financial-data/")
    
    # Google Cloud Firestore Configuration
    google_firestore_database: str = os.getenv("GOOGLE_FIRESTORE_DATABASE", "(default)")
    google_firestore_collection: str = os.getenv("GOOGLE_FIRESTORE_COLLECTION", "financial_data")
    google_firestore_real_time_sync: bool = os.getenv("GOOGLE_FIRESTORE_REAL_TIME_SYNC", "true").lower() == "true"
    
    # Google Cloud Functions Configuration
    google_cloud_functions_region: str = os.getenv("GOOGLE_CLOUD_FUNCTIONS_REGION", "us-central1")
    google_cloud_functions_memory: str = os.getenv("GOOGLE_CLOUD_FUNCTIONS_MEMORY", "512Mi")
    google_cloud_functions_timeout: int = int(os.getenv("GOOGLE_CLOUD_FUNCTIONS_TIMEOUT", "540"))
    
    # Google Cloud Monitoring & Logging Configuration
    google_cloud_monitoring_enabled: bool = os.getenv("GOOGLE_CLOUD_MONITORING_ENABLED", "true").lower() == "true"
    google_cloud_logging_enabled: bool = os.getenv("GOOGLE_CLOUD_LOGGING_ENABLED", "true").lower() == "true"
    google_cloud_metrics_prefix: str = os.getenv("GOOGLE_CLOUD_METRICS_PREFIX", "financial_agent")
    
    # Google Cloud Scheduler Configuration
    google_cloud_scheduler_timezone: str = os.getenv("GOOGLE_CLOUD_SCHEDULER_TIMEZONE", "UTC")
    google_cloud_scheduler_location: str = os.getenv("GOOGLE_CLOUD_SCHEDULER_LOCATION", "us-central1")
    
    # Google Authentication Configuration
    google_oauth_client_id: str = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
    google_oauth_client_secret: str = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")
    google_oauth_redirect_uri: str = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "")
    
    # Google Charts & Visualization Configuration
    google_charts_api_key: str = os.getenv("GOOGLE_CHARTS_API_KEY", "")
    google_charts_enable_real_time: bool = os.getenv("GOOGLE_CHARTS_ENABLE_REAL_TIME", "true").lower() == "true"
    
    # Vertex AI Enhanced Configuration
    vertex_ai_model_endpoint: str = os.getenv("VERTEX_AI_MODEL_ENDPOINT", "")
    vertex_ai_prediction_quota: int = int(os.getenv("VERTEX_AI_PREDICTION_QUOTA", "1000"))
    vertex_ai_batch_prediction_enabled: bool = os.getenv("VERTEX_AI_BATCH_PREDICTION_ENABLED", "false").lower() == "true"
    
    # Google Cloud AI Platform Configuration
    google_ai_platform_enable_automl: bool = os.getenv("GOOGLE_AI_PLATFORM_ENABLE_AUTOML", "false").lower() == "true"
    google_ai_platform_model_name: str = os.getenv("GOOGLE_AI_PLATFORM_MODEL_NAME", "")
    
    # Google Cloud Pub/Sub Configuration for Real-time Events
    google_pubsub_project: str = os.getenv("GOOGLE_PUBSUB_PROJECT", "")
    google_pubsub_topic_financial_data: str = os.getenv("GOOGLE_PUBSUB_TOPIC_FINANCIAL_DATA", "financial-data-updates")
    google_pubsub_topic_agent_events: str = os.getenv("GOOGLE_PUBSUB_TOPIC_AGENT_EVENTS", "agent-events")
    google_pubsub_subscription_timeout: int = int(os.getenv("GOOGLE_PUBSUB_SUBSCRIPTION_TIMEOUT", "60"))
    
    # Google Cloud Secret Manager Configuration
    google_secret_manager_enabled: bool = os.getenv("GOOGLE_SECRET_MANAGER_ENABLED", "false").lower() == "true"
    google_secret_manager_project: str = os.getenv("GOOGLE_SECRET_MANAGER_PROJECT", "")
    
    # Google Cloud BigQuery Configuration for Analytics
    google_bigquery_dataset: str = os.getenv("GOOGLE_BIGQUERY_DATASET", "financial_analytics")
    google_bigquery_table_transactions: str = os.getenv("GOOGLE_BIGQUERY_TABLE_TRANSACTIONS", "transactions")
    google_bigquery_table_agent_metrics: str = os.getenv("GOOGLE_BIGQUERY_TABLE_AGENT_METRICS", "agent_metrics")
    google_bigquery_streaming_enabled: bool = os.getenv("GOOGLE_BIGQUERY_STREAMING_ENABLED", "false").lower() == "true"
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings() 