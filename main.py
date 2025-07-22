#!/usr/bin/env python3
"""
Agentic AI Financial Insights System with Real Fi MCP Integration
Clean, production-ready system for financial data analysis
"""

import logging
import signal
import sys
import time
from datetime import datetime
import argparse
from services.real_data_collector import real_data_collector
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
    """Main system orchestrator with real Fi MCP data"""
    
    def __init__(self):
        self.running = False
        self.data_collector = real_data_collector
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Initialize database
        create_tables()
        logger.info("Database initialized")
    
    def start(self, start_collector=True, start_generator=True):
        """Start all services with real Fi MCP data"""
        logger.info("Starting Agentic AI System with Real Fi MCP Data...")
        self.running = True
        
        try:
            if start_collector:
                # Test Fi MCP connection first
                if not real_data_collector.test_mcp_connection():
                    logger.error("Failed to connect to Fi MCP server. Please ensure it's running on port 8080")
                    logger.info("To start Fi MCP server: cd fi-mcp-server && FI_MCP_PORT=8080 go run . &")
                    return False
                
                self.data_collector.start_collection()
                logger.info("Real data collector started")
            
            if start_generator:
                insight_generator.start_generation()
                logger.info("AI insight generator started")
            
            logger.info("System started successfully")
            logger.info("🎉 Analyzing REAL FINANCIAL DATA from Fi MCP server!")
            logger.info("📊 Data types: Net Worth, Bank Transactions, EPF Details, Credit Reports")
            logger.info(f"Data collection interval: {settings.collection_interval_minutes} minutes")
            logger.info(f"Insight generation interval: {settings.insights_generation_interval_minutes} minutes")
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error starting system: {e}")
            self.stop()
            return False
        
        return True
    
    def stop(self):
        """Stop all services"""
        logger.info("Stopping Agentic AI System...")
        self.running = False
        
        try:
            self.data_collector.stop_collection()
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
        """Show system status with real financial data information"""
        from models.database import SessionLocal, MCPData, AIInsight
        
        logger.info("=== Agentic AI System Status (Real Fi MCP Data) ===")
        
        db = SessionLocal()
        try:
            # Data statistics
            total_data = db.query(MCPData).count()
            unprocessed_data = db.query(MCPData).filter(MCPData.processed == False).count()
            total_insights = db.query(AIInsight).count()
            
            logger.info(f"Data Source: Real Fi MCP")
            logger.info(f"MCP Data Records: {total_data}")
            logger.info(f"Unprocessed Records: {unprocessed_data}")
            logger.info(f"Generated Insights: {total_insights}")
            
            # Show real financial data breakdown
            logger.info("\n📊 Real Financial Data Breakdown:")
            real_data_types = ["net_worth", "bank_transactions", "epf_details", "credit_report"]
            for data_type in real_data_types:
                count = db.query(MCPData).filter(MCPData.data_type == data_type).count()
                if count > 0:
                    logger.info(f"   {data_type}: {count} records")
            
            # Show latest financial summary
            summary = self.data_collector.get_latest_financial_summary()
            logger.info(f"\n💰 Latest Financial Summary:")
            for key, value in summary.items():
                if value != "N/A":
                    logger.info(f"   {key.replace('_', ' ').title()}: {value}")
            
            # Recent activity
            recent_data = db.query(MCPData).order_by(MCPData.timestamp.desc()).first()
            recent_insight = db.query(AIInsight).order_by(AIInsight.created_at.desc()).first()
            
            if recent_data:
                logger.info(f"Last Data Collection: {recent_data.timestamp}")
            else:
                logger.info("Last Data Collection: Never")
                
            if recent_insight:
                logger.info(f"Last Insight Generated: {recent_insight.created_at}")
                logger.info(f"Latest Insight: {recent_insight.title}")
            else:
                logger.info("Last Insight Generated: Never")
                
        except Exception as e:
            logger.error(f"Error checking status: {e}")
        finally:
            db.close()
    
    def collect_now(self):
        """Trigger immediate data collection"""
        logger.info("Triggering immediate real data collection...")
        
        # Test connection first
        if not real_data_collector.test_mcp_connection():
            logger.error("Cannot collect data - Fi MCP server connection failed")
            return False
        
        self.data_collector.collect_data()
        logger.info("Data collection completed")
        return True
    
    def generate_now(self):
        """Trigger immediate insight generation"""
        logger.info("Triggering immediate insight generation...")
        insight_generator.generate_insights()
        logger.info("Insight generation completed")
    
    def test_connection(self):
        """Test Fi MCP server connection"""
        logger.info("Testing Fi MCP server connection...")
        return real_data_collector.test_mcp_connection()

def main():
    """Main entry point with enhanced CLI interface"""
    parser = argparse.ArgumentParser(description="Agentic AI Financial Insights System with Real Fi MCP Data")
    parser.add_argument('command', nargs='?', default='start',
                       choices=['start', 'stop', 'status', 'collect', 'generate', 'dashboard', 'test'],
                       help='Command to execute')
    parser.add_argument('--no-collector', action='store_true',
                       help='Start without data collector')
    parser.add_argument('--no-generator', action='store_true',
                       help='Start without insight generator')
    
    args = parser.parse_args()
    
    system = AgenticAISystem()
    
    if args.command == 'start':
        try:
            success = system.start(
                start_collector=not args.no_collector,
                start_generator=not args.no_generator
            )
            if not success:
                sys.exit(1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            system.stop()
    
    elif args.command == 'status':
        system.status()
    
    elif args.command == 'collect':
        success = system.collect_now()
        if not success:
            sys.exit(1)
    
    elif args.command == 'generate':
        system.generate_now()
    
    elif args.command == 'test':
        logger.info("Testing Fi MCP server connection...")
        if system.test_connection():
            logger.info("✅ Fi MCP connection successful")
        else:
            logger.error("❌ Fi MCP connection failed")
            sys.exit(1)
    
    elif args.command == 'dashboard':
        logger.info("Starting financial insights dashboard...")
        logger.info("Run: streamlit run dashboard/app.py")
        import subprocess
        subprocess.run(["streamlit", "run", "dashboard/app.py"])
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 