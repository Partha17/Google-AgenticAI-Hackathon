import logging
import schedule
import time
import threading
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import MCPData, SessionLocal, create_tables
from services.mcp_mock import mock_mcp
from config import settings

logger = logging.getLogger(__name__)

class DataCollector:
    """Service to collect data from MCP server and store in database"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        create_tables()  # Ensure tables exist
    
    def collect_data(self):
        """Collect data from MCP and store in database"""
        try:
            logger.info("Starting data collection...")
            
            # Get batch data from mock MCP
            batch_data = mock_mcp.get_batch_data(count=5)
            
            db = SessionLocal()
            try:
                for data_item in batch_data:
                    mcp_record = MCPData(
                        data_type=data_item.get("type", "unknown"),
                        raw_data=str(data_item),
                        timestamp=datetime.utcnow()
                    )
                    mcp_record.set_data(data_item)
                    
                    db.add(mcp_record)
                
                db.commit()
                logger.info(f"Successfully stored {len(batch_data)} records")
                
            except Exception as e:
                logger.error(f"Database error during collection: {e}")
                db.rollback()
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error during data collection: {e}")
    
    def start_collection(self):
        """Start periodic data collection"""
        if self.running:
            logger.warning("Data collection is already running")
            return
        
        self.running = True
        
        # Schedule periodic collection
        schedule.every(settings.collection_interval_minutes).minutes.do(self.collect_data)
        
        # Run initial collection
        self.collect_data()
        
        # Start scheduler in separate thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info(f"Data collection started with {settings.collection_interval_minutes} minute intervals")
    
    def stop_collection(self):
        """Stop data collection"""
        self.running = False
        schedule.clear()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info("Data collection stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def get_unprocessed_data(self) -> list:
        """Get unprocessed MCP data for AI analysis"""
        db = SessionLocal()
        try:
            records = db.query(MCPData).filter(MCPData.processed == False).all()
            return records
        finally:
            db.close()
    
    def mark_as_processed(self, record_ids: list):
        """Mark records as processed"""
        db = SessionLocal()
        try:
            db.query(MCPData).filter(MCPData.id.in_(record_ids)).update(
                {MCPData.processed: True}, synchronize_session=False
            )
            db.commit()
        except Exception as e:
            logger.error(f"Error marking records as processed: {e}")
            db.rollback()
        finally:
            db.close()

# Singleton instance
data_collector = DataCollector() 