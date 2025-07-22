import logging
import schedule
import threading
import time
from datetime import datetime
from services.data_collector import data_collector
from services.ai_agent import ai_agent
from services.enhanced_ai_agent import enhanced_ai_agent
from config import settings

logger = logging.getLogger(__name__)

class InsightGenerator:
    """Service to generate AI insights from collected MCP data"""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def generate_insights(self):
        """Generate insights from unprocessed MCP data"""
        try:
            logger.info("Starting insight generation...")
            
            # Get unprocessed data
            unprocessed_data = data_collector.get_unprocessed_data()
            
            if not unprocessed_data:
                logger.info("No unprocessed data found")
                return
            
            logger.info(f"Found {len(unprocessed_data)} unprocessed records")
            
            # Process data in batches
            batch_size = 20  # Process 20 records at a time
            processed_ids = []
            
            for i in range(0, len(unprocessed_data), batch_size):
                batch = unprocessed_data[i:i+batch_size]
                
                try:
                    # Generate insights for this batch using enhanced agent
                    insights = enhanced_ai_agent.analyze_data_batch(batch)
                    
                    if insights:
                        # Store insights using enhanced storage
                        stored_ids = enhanced_ai_agent.store_enhanced_insights(insights)
                        logger.info(f"Generated and stored {len(insights)} insights")
                        
                        # Mark records as processed
                        batch_ids = [record.id for record in batch]
                        data_collector.mark_as_processed(batch_ids)
                        processed_ids.extend(batch_ids)
                    
                except Exception as e:
                    logger.error(f"Error processing batch: {e}")
                    continue
            
            logger.info(f"Insight generation completed. Processed {len(processed_ids)} records")
            
        except Exception as e:
            logger.error(f"Error during insight generation: {e}")
    
    def start_generation(self):
        """Start periodic insight generation"""
        if self.running:
            logger.warning("Insight generation is already running")
            return
        
        self.running = True
        
        # Schedule periodic generation
        schedule.every(settings.insights_generation_interval_minutes).minutes.do(self.generate_insights)
        
        # Run initial generation
        self.generate_insights()
        
        # Start scheduler in separate thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info(f"Insight generation started with {settings.insights_generation_interval_minutes} minute intervals")
    
    def stop_generation(self):
        """Stop insight generation"""
        self.running = False
        schedule.clear()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info("Insight generation stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def get_recent_insights(self, limit: int = 50):
        """Get recent insights for dashboard"""
        from models.database import SessionLocal, AIInsight
        
        db = SessionLocal()
        try:
            insights = db.query(AIInsight).order_by(
                AIInsight.created_at.desc()
            ).limit(limit).all()
            return insights
        finally:
            db.close()
    
    def get_insights_by_type(self, insight_type: str, limit: int = 20):
        """Get insights filtered by type"""
        from models.database import SessionLocal, AIInsight
        
        db = SessionLocal()
        try:
            insights = db.query(AIInsight).filter(
                AIInsight.insight_type == insight_type
            ).order_by(
                AIInsight.created_at.desc()
            ).limit(limit).all()
            return insights
        finally:
            db.close()
    
    def get_insights_stats(self):
        """Get statistics about generated insights"""
        from models.database import SessionLocal, AIInsight
        from sqlalchemy import func
        
        db = SessionLocal()
        try:
            stats = db.query(
                AIInsight.insight_type,
                func.count(AIInsight.id).label('count'),
                func.avg(AIInsight.confidence_score).label('avg_confidence')
            ).group_by(AIInsight.insight_type).all()
            
            total_insights = db.query(func.count(AIInsight.id)).scalar()
            
            return {
                'total_insights': total_insights,
                'by_type': [
                    {
                        'type': stat.insight_type,
                        'count': stat.count,
                        'avg_confidence': round(float(stat.avg_confidence), 2)
                    }
                    for stat in stats
                ]
            }
        finally:
            db.close()

# Singleton instance
insight_generator = InsightGenerator() 