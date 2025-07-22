import logging
import schedule
import time
import threading
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import MCPData, SessionLocal, create_tables
from services.fi_mcp_client import fi_mcp_client
from config import settings

logger = logging.getLogger(__name__)

class RealDataCollector:
    """Service to collect real financial data from Fi MCP server and store in database"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        create_tables()  # Ensure tables exist
        
        # Fi MCP client
        self.mcp_client = fi_mcp_client
        
        # Track collection statistics
        self.stats = {
            "total_collections": 0,
            "successful_collections": 0,
            "failed_collections": 0,
            "last_collection_time": None,
            "data_types_collected": set()
        }
    
    def collect_data(self):
        """Collect real financial data from Fi MCP and store in database"""
        try:
            logger.info("Starting real data collection from Fi MCP...")
            self.stats["total_collections"] += 1
            
            # Get all financial data from Fi MCP
            financial_data = self.mcp_client.get_all_financial_data()
            
            if not financial_data:
                logger.warning("No data received from Fi MCP server")
                self.stats["failed_collections"] += 1
                return
            
            db = SessionLocal()
            stored_count = 0
            
            try:
                for data_item in financial_data:
                    if data_item.get("success"):
                        # Create MCP record with real financial data
                        mcp_record = MCPData(
                            data_type=data_item.get("type", "unknown"),
                            raw_data=str(data_item),  # Store the complete response
                            timestamp=datetime.utcnow()
                        )
                        mcp_record.set_data(data_item)
                        
                        db.add(mcp_record)
                        stored_count += 1
                        
                        # Track data types
                        self.stats["data_types_collected"].add(data_item.get("type"))
                        
                        logger.info(f"Stored {data_item.get('type')} data from Fi MCP")
                    else:
                        logger.warning(f"Skipped failed data: {data_item.get('error', 'Unknown error')}")
                
                db.commit()
                
                self.stats["successful_collections"] += 1
                self.stats["last_collection_time"] = datetime.utcnow()
                
                logger.info(f"Successfully stored {stored_count} real financial records from Fi MCP")
                
            except Exception as e:
                logger.error(f"Database error during real data collection: {e}")
                db.rollback()
                self.stats["failed_collections"] += 1
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error during real data collection: {e}")
            self.stats["failed_collections"] += 1
    
    def collect_specific_data_type(self, data_type: str):
        """Collect a specific type of financial data"""
        try:
            logger.info(f"Collecting specific data type: {data_type}")
            
            # Map data types to client methods
            data_fetchers = {
                "net_worth": self.mcp_client.fetch_net_worth,
                "bank_transactions": self.mcp_client.fetch_bank_transactions,
                "mutual_fund_transactions": self.mcp_client.fetch_mutual_fund_transactions,
                "epf_details": self.mcp_client.fetch_epf_details,
                "credit_report": self.mcp_client.fetch_credit_report
            }
            
            if data_type not in data_fetchers:
                logger.error(f"Unknown data type: {data_type}")
                return False
            
            # Fetch the specific data
            fetcher = data_fetchers[data_type]
            result = fetcher()
            
            if result.get("success"):
                # Store in database
                db = SessionLocal()
                try:
                    mcp_record = MCPData(
                        data_type=data_type,
                        raw_data=str(result),
                        timestamp=datetime.utcnow()
                    )
                    mcp_record.set_data(result)
                    
                    db.add(mcp_record)
                    db.commit()
                    
                    logger.info(f"Successfully collected and stored {data_type}")
                    return True
                    
                except Exception as e:
                    logger.error(f"Database error storing {data_type}: {e}")
                    db.rollback()
                    return False
                finally:
                    db.close()
            else:
                logger.error(f"Failed to fetch {data_type}: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error collecting {data_type}: {e}")
            return False
    
    def test_mcp_connection(self) -> bool:
        """Test connection to Fi MCP server"""
        try:
            logger.info("Testing Fi MCP server connection...")
            
            # Try to authenticate
            if self.mcp_client.authenticate():
                logger.info("✅ Fi MCP server connection successful")
                
                # Try to fetch net worth as a test
                result = self.mcp_client.fetch_net_worth()
                if result.get("success"):
                    logger.info("✅ Fi MCP data retrieval successful")
                    logger.info(f"Sample data: Total net worth = {result.get('total_net_worth', 'N/A')}")
                    return True
                else:
                    logger.warning(f"❌ Fi MCP data retrieval failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                logger.error("❌ Fi MCP server authentication failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Fi MCP connection test failed: {e}")
            return False
    
    def start_collection(self):
        """Start periodic real data collection"""
        if self.running:
            logger.warning("Real data collection is already running")
            return
        
        # Test connection first
        if not self.test_mcp_connection():
            logger.error("Cannot start collection - Fi MCP server connection failed")
            return
        
        self.running = True
        
        # Schedule periodic collection
        schedule.every(settings.collection_interval_minutes).minutes.do(self.collect_data)
        
        # Run initial collection
        self.collect_data()
        
        # Start scheduler in separate thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info(f"Real data collection started with {settings.collection_interval_minutes} minute intervals")
        logger.info("Collecting data from Fi MCP server with real financial information")
    
    def stop_collection(self):
        """Stop real data collection"""
        self.running = False
        schedule.clear()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info("Real data collection stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def get_unprocessed_data(self) -> list:
        """Get unprocessed real MCP data for AI analysis"""
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
    
    def get_collection_stats(self) -> dict:
        """Get collection statistics"""
        stats = self.stats.copy()
        stats["data_types_collected"] = list(stats["data_types_collected"])
        stats["success_rate"] = (
            stats["successful_collections"] / max(1, stats["total_collections"]) * 100
        )
        
        # Get database statistics
        db = SessionLocal()
        try:
            stats["total_records_in_db"] = db.query(MCPData).count()
            stats["unprocessed_records"] = db.query(MCPData).filter(MCPData.processed == False).count()
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            stats["total_records_in_db"] = 0
            stats["unprocessed_records"] = 0
        finally:
            db.close()
        
        return stats
    
    def get_latest_financial_summary(self) -> dict:
        """Get a summary of the latest financial data"""
        db = SessionLocal()
        summary = {
            "net_worth": "N/A",
            "total_assets": "N/A", 
            "total_liabilities": "N/A",
            "credit_score": "N/A",
            "epf_balance": "N/A",
            "last_updated": "N/A"
        }
        
        try:
            # Get latest net worth data
            latest_nw = db.query(MCPData).filter(
                MCPData.data_type == "net_worth"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_nw:
                nw_data = latest_nw.get_data()
                summary["net_worth"] = nw_data.get("total_net_worth", "N/A")
                summary["total_assets"] = nw_data.get("total_assets", "N/A")
                summary["total_liabilities"] = nw_data.get("total_liabilities", "N/A")
                summary["last_updated"] = latest_nw.timestamp.strftime("%Y-%m-%d %H:%M")
            
            # Get latest credit report
            latest_credit = db.query(MCPData).filter(
                MCPData.data_type == "credit_report"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_credit:
                credit_data = latest_credit.get_data()
                summary["credit_score"] = credit_data.get("credit_score", "N/A")
            
            # Get latest EPF data
            latest_epf = db.query(MCPData).filter(
                MCPData.data_type == "epf_details"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_epf:
                epf_data = latest_epf.get_data()
                summary["epf_balance"] = epf_data.get("epf_balance", "N/A")
            
        except Exception as e:
            logger.error(f"Error getting financial summary: {e}")
        finally:
            db.close()
        
        return summary

# Real data collector singleton instance
real_data_collector = RealDataCollector() 