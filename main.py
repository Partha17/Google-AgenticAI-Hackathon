#!/usr/bin/env python3
"""
Agentic AI Financial Insights System
Main entry point for the application
"""

import logging
import signal
import sys
import time
from datetime import datetime
import argparse
from services.data_collector import data_collector
from services.insight_generator import insight_generator
from models.database import create_tables
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agentic_ai.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AgenticAISystem:
    """Main system orchestrator"""
    
    def __init__(self):
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Initialize database
        create_tables()
        logger.info("Database initialized")
    
    def start(self, start_collector=True, start_generator=True):
        """Start all services"""
        logger.info("Starting Agentic AI System...")
        self.running = True
        
        try:
            if start_collector:
                data_collector.start_collection()
                logger.info("Data collector started")
            
            if start_generator:
                insight_generator.start_generation()
                logger.info("Insight generator started")
            
            logger.info("System started successfully")
            logger.info(f"Data collection interval: {settings.collection_interval_minutes} minutes")
            logger.info(f"Insight generation interval: {settings.insights_generation_interval_minutes} minutes")
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error starting system: {e}")
            self.stop()
    
    def stop(self):
        """Stop all services"""
        logger.info("Stopping Agentic AI System...")
        self.running = False
        
        try:
            data_collector.stop_collection()
            insight_generator.stop_generation()
            logger.info("System stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping system: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def status(self):
        """Show system status"""
        from models.database import SessionLocal, MCPData, AIInsight
        
        logger.info("=== Agentic AI System Status ===")
        
        db = SessionLocal()
        try:
            # Data statistics
            total_data = db.query(MCPData).count()
            unprocessed_data = db.query(MCPData).filter(MCPData.processed == False).count()
            total_insights = db.query(AIInsight).count()
            
            logger.info(f"MCP Data Records: {total_data}")
            logger.info(f"Unprocessed Records: {unprocessed_data}")
            logger.info(f"Generated Insights: {total_insights}")
            
            # Recent activity
            recent_data = db.query(MCPData).order_by(MCPData.timestamp.desc()).first()
            recent_insight = db.query(AIInsight).order_by(AIInsight.created_at.desc()).first()
            
            if recent_data:
                logger.info(f"Last Data Collection: {recent_data.timestamp}")
            else:
                logger.info("Last Data Collection: Never")
                
            if recent_insight:
                logger.info(f"Last Insight Generated: {recent_insight.created_at}")
            else:
                logger.info("Last Insight Generated: Never")
                
        except Exception as e:
            logger.error(f"Error checking status: {e}")
        finally:
            db.close()
    
    def collect_now(self):
        """Trigger immediate data collection"""
        logger.info("Triggering immediate data collection...")
        data_collector.collect_data()
        logger.info("Data collection completed")
    
    def generate_now(self):
        """Trigger immediate insight generation"""
        logger.info("Triggering immediate insight generation...")
        insight_generator.generate_insights()
        logger.info("Insight generation completed")

def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(description="Agentic AI Financial Insights System")
    parser.add_argument('command', nargs='?', default='start',
                       choices=['start', 'stop', 'status', 'collect', 'generate', 'dashboard'],
                       help='Command to execute')
    parser.add_argument('--no-collector', action='store_true',
                       help='Start without data collector')
    parser.add_argument('--no-generator', action='store_true',
                       help='Start without insight generator')
    
    args = parser.parse_args()
    
    system = AgenticAISystem()
    
    if args.command == 'start':
        try:
            system.start(
                start_collector=not args.no_collector,
                start_generator=not args.no_generator
            )
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            system.stop()
    
    elif args.command == 'status':
        system.status()
    
    elif args.command == 'collect':
        system.collect_now()
    
    elif args.command == 'generate':
        system.generate_now()
    
    elif args.command == 'dashboard':
        logger.info("Starting dashboard...")
        logger.info("Run: streamlit run dashboard/app.py")
        import subprocess
        subprocess.run(["streamlit", "run", "dashboard/app.py"])
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 