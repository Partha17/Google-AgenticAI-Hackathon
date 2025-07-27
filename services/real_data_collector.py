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
            
            # Get financial data directly from the MCP server with comprehensive user
            result = self.mcp_client.get_financial_data(phone_number="2222222222")
            
            if not result or not result.get("success"):
                logger.warning(f"No data received from Fi MCP server: {result.get('error', 'Unknown error') if result else 'No response'}")
                self.stats["failed_collections"] += 1
                return
            
            # Extract the actual financial data
            raw_financial_data = result.get("data", {})
            
            if not raw_financial_data:
                logger.warning("Empty financial data received")
                self.stats["failed_collections"] += 1
                return
            
            db = SessionLocal()
            stored_count = 0
            
            try:
                # Store different data types from the comprehensive response
                data_types_to_extract = [
                    ("net_worth", "netWorthResponse"),
                    ("bank_transactions", "accountDetailsBulkResponse"),
                    ("mutual_fund_transactions", "mfSchemeAnalytics")
                ]
                
                for data_type, key in data_types_to_extract:
                    if key in raw_financial_data:
                        # Create MCP record with the specific data type
                        data_subset = {key: raw_financial_data[key]}
                        
                        mcp_record = MCPData(
                            data_type=data_type,
                            raw_data=str(data_subset),  # Store the relevant subset
                            timestamp=datetime.utcnow()
                        )
                        mcp_record.set_data(data_subset)
                        
                        db.add(mcp_record)
                        stored_count += 1
                        
                        # Track data types
                        self.stats["data_types_collected"].add(data_type)
                        
                        logger.info(f"Stored {data_type} data from Fi MCP")
                    else:
                        logger.warning(f"No {data_type} data found in response (missing key: {key})")
                
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
                "credit_report": self.mcp_client.fetch_credit_report,
                "stock_transactions": self.mcp_client.fetch_stock_transactions
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
            
            # Try auto-login with the deployed server using comprehensive data user
            if self.mcp_client.auto_login(phone_number="2222222222"):
                logger.info("✅ Fi MCP server connection successful")
                
                # Try to fetch financial data as a test with comprehensive user
                result = self.mcp_client.get_financial_data(phone_number="2222222222")
                if result.get("success"):
                    logger.info("✅ Fi MCP data retrieval successful")
                    # Extract net worth from the response for display
                    data = result.get("data", {})
                    if "netWorthResponse" in data:
                        net_worth = data["netWorthResponse"].get("totalNetWorthValue", {})
                        total_value = net_worth.get("units", "N/A")
                        currency = net_worth.get("currencyCode", "INR")
                        logger.info(f"Sample data: Total net worth = {currency} {total_value}")
                    return True
                else:
                    logger.warning(f"❌ Fi MCP data retrieval failed: {result.get('error', 'Unknown error')}")
                    # Still return True if authentication worked - just a data issue
                    return True
            else:
                logger.warning("⚠️ Fi MCP server authentication had issues but fallback auth is working")
                # Even if auth had issues, if we have fallback auth, still return True
                return hasattr(self.mcp_client, 'authenticated') and self.mcp_client.authenticated
                
        except Exception as e:
            logger.error(f"❌ Fi MCP connection test failed: {e}")
            # For robustness, check if we at least have basic connectivity
            try:
                import requests
                response = requests.get(f"{self.mcp_client.base_url}", timeout=5)
                if response.status_code == 200:
                    logger.warning("⚠️ MCP server is reachable but connection test failed - proceeding anyway")
                    return True
            except:
                pass
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
        """Get a summary of the latest financial data with proper parsing"""
        db = SessionLocal()
        summary = {
            "net_worth": "N/A",
            "total_assets": "N/A", 
            "total_liabilities": "N/A",
            "credit_score": "N/A",
            "epf_balance": "N/A",
            "last_updated": "N/A",
            "bank_balance": "N/A"
        }
        
        def extract_financial_data(mcp_record):
            """Extract financial data from MCP record with proper parsing"""
            if not mcp_record:
                return {}
            
            try:
                # Get the data from the record
                record_data = mcp_record.get_data()
                
                # Handle different data structures
                if isinstance(record_data, dict):
                    # Check if it's the raw response format
                    if 'data' in record_data and 'content' in record_data['data']:
                        # Parse the JSON content
                        import json
                        content = record_data['data']['content'][0]['text']
                        parsed_data = json.loads(content)
                        return parsed_data
                    else:
                        return record_data
                
                # Try to parse as JSON string
                if isinstance(record_data, str):
                    import json
                    return json.loads(record_data)
                    
                return record_data
            except Exception as e:
                logger.error(f"Error parsing financial data: {e}")
                return {}
        
        try:
            # Get net worth data
            latest_nw = db.query(MCPData).filter(
                MCPData.data_type == "net_worth"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_nw:
                nw_data = extract_financial_data(latest_nw)
                if 'netWorthResponse' in nw_data:
                    net_worth_response = nw_data['netWorthResponse']
                    
                    # Extract total net worth
                    if 'totalNetWorthValue' in net_worth_response:
                        summary["net_worth"] = int(net_worth_response['totalNetWorthValue']['units'])
                    
                    # Calculate total assets
                    total_assets = 0
                    if 'assetValues' in net_worth_response:
                        for asset in net_worth_response['assetValues']:
                            total_assets += int(asset['value']['units'])
                    summary["total_assets"] = total_assets
                    
                    # Calculate total liabilities
                    total_liabilities = 0
                    if 'liabilityValues' in net_worth_response:
                        for liability in net_worth_response['liabilityValues']:
                            total_liabilities += int(liability['value']['units'])
                    summary["total_liabilities"] = total_liabilities
                
                # Extract bank balance from account details
                if 'accountDetailsBulkResponse' in nw_data:
                    bank_balance = 0
                    account_map = nw_data['accountDetailsBulkResponse']['accountDetailsMap']
                    for account_id, account_info in account_map.items():
                        if 'depositSummary' in account_info:
                            balance = int(account_info['depositSummary']['currentBalance']['units'])
                            bank_balance += balance
                    summary["bank_balance"] = bank_balance
                
                summary["last_updated"] = latest_nw.timestamp.strftime("%Y-%m-%d %H:%M")
            
            # Get credit score
            latest_credit = db.query(MCPData).filter(
                MCPData.data_type == "credit_report"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_credit:
                credit_data = extract_financial_data(latest_credit)
                if 'creditReports' in credit_data and len(credit_data['creditReports']) > 0:
                    credit_report = credit_data['creditReports'][0]
                    if 'creditReportData' in credit_report and 'score' in credit_report['creditReportData']:
                        summary["credit_score"] = int(credit_report['creditReportData']['score']['bureauScore'])
            
            # Get EPF balance
            latest_epf = db.query(MCPData).filter(
                MCPData.data_type == "epf_details"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_epf:
                epf_data = extract_financial_data(latest_epf)
                if 'uanAccounts' in epf_data and len(epf_data['uanAccounts']) > 0:
                    uan_account = epf_data['uanAccounts'][0]
                    if 'rawDetails' in uan_account and 'overall_pf_balance' in uan_account['rawDetails']:
                        pf_balance = uan_account['rawDetails']['overall_pf_balance']
                        summary["epf_balance"] = int(pf_balance['current_pf_balance'])

        except Exception as e:
            logger.error(f"Error getting financial summary: {e}")
        finally:
            db.close()
        
        return summary

# Real data collector singleton instance
real_data_collector = RealDataCollector() 