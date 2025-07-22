from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from config import settings

Base = declarative_base()

class MCPData(Base):
    __tablename__ = "mcp_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data_type = Column(String(100), nullable=False)
    raw_data = Column(Text, nullable=False)  # JSON string
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def get_data(self):
        """Parse the raw JSON data"""
        try:
            return json.loads(self.raw_data)
        except json.JSONDecodeError:
            return {}
    
    def set_data(self, data):
        """Set data as JSON string"""
        self.raw_data = json.dumps(data)

class AIInsight(Base):
    __tablename__ = "ai_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    insight_type = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.0)
    data_source_ids = Column(Text)  # JSON array of MCP data IDs used
    insight_metadata = Column(Text)  # Additional JSON metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def get_metadata(self):
        """Parse the metadata JSON"""
        try:
            return json.loads(self.insight_metadata) if self.insight_metadata else {}
        except json.JSONDecodeError:
            return {}
    
    def set_metadata(self, metadata):
        """Set metadata as JSON string"""
        self.insight_metadata = json.dumps(metadata)
    
    def get_source_ids(self):
        """Parse the data source IDs"""
        try:
            return json.loads(self.data_source_ids) if self.data_source_ids else []
        except json.JSONDecodeError:
            return []
    
    def set_source_ids(self, ids):
        """Set source IDs as JSON string"""
        self.data_source_ids = json.dumps(ids)

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 