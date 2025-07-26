"""
MCP Periodic AI Agent
Combines automated data collection from Fi MCP with AI-powered analysis
"""

import asyncio
import json
import logging
import schedule
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

# Add langchain imports for AI analysis
from langchain.schema import HumanMessage, SystemMessage

from .ai_analysis_base import AIAnalysisBase
from .agent_config import AGENT_CONFIGS
from models.database import MCPData, AIInsight, SessionLocal, create_tables
from services.fi_mcp_client import fi_mcp_client
from services.logger_config import get_adk_logger, log_error
from services.quota_manager import quota_manager

logger = get_adk_logger()

class MCPPeriodicAIAgent(AIAnalysisBase):
    """
    Agent that periodically collects data from Fi MCP server and performs AI analysis
    Features:
    - Automated periodic data collection
    - On-demand AI analysis
    - Financial insights generation
    - Portfolio performance tracking
    - Risk assessment
    """
    
    def __init__(self):
        # Initialize with agent config
        agent_config = AGENT_CONFIGS.get("mcp_periodic_ai_agent", {
            "model": "gemini-1.5-flash",
            "generation_config": {
                "temperature": 0.3,
                "max_output_tokens": 2048,
                "top_p": 0.8
            },
            "collection_interval_minutes": 60,  # Collect data every hour
            "analysis_triggers": {
                "data_freshness_hours": 2,  # Trigger analysis if data is older than 2 hours
                "significant_change_threshold": 0.05  # 5% change threshold
            }
        })
        
        super().__init__("mcp_periodic_ai_agent", agent_config)
        
        # Initialize components
        self.mcp_client = fi_mcp_client
        self.running = False
        self.scheduler_thread = None
        
        # Collection stats
        self.stats = {
            "total_collections": 0,
            "successful_collections": 0,
            "failed_collections": 0,
            "last_collection_time": None,
            "last_analysis_time": None,
            "data_types_collected": set(),
            "analysis_count": 0
        }
        
        # Ensure database tables exist
        create_tables()
        
        logger.info("MCP Periodic AI Agent initialized")
    
    def start_periodic_collection(self):
        """Start the periodic data collection scheduler"""
        if self.running:
            logger.warning("Periodic collection already running")
            return
        
        self.running = True
        
        # Schedule data collection
        collection_interval = self.config.get("collection_interval_minutes", 60)
        schedule.every(collection_interval).minutes.do(self._scheduled_collection)
        
        # Start scheduler in separate thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info(f"Started periodic collection every {collection_interval} minutes")
    
    def stop_periodic_collection(self):
        """Stop the periodic data collection"""
        self.running = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        logger.info("Stopped periodic collection")
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)
    
    def _scheduled_collection(self):
        """Scheduled data collection task"""
        try:
            logger.info("Running scheduled data collection...")
            self.collect_mcp_data()
            
            # Check if analysis should be triggered
            if self._should_trigger_analysis():
                self.generate_ai_analysis()
                
        except Exception as e:
            logger.error(f"Scheduled collection error: {e}")
            log_error('mcp.periodic.agent', e, "Scheduled data collection")
    
    def collect_mcp_data(self) -> Dict[str, Any]:
        """Collect data from Fi MCP server and store in database"""
        try:
            logger.info("Starting MCP data collection...")
            self.stats["total_collections"] += 1
            
            # Get all financial data from Fi MCP
            financial_data = self.mcp_client.get_all_financial_data()
            
            if not financial_data:
                logger.warning("No data received from Fi MCP server")
                self.stats["failed_collections"] += 1
                return {"success": False, "error": "No data received"}
            
            db = SessionLocal()
            stored_count = 0
            
            try:
                for data_item in financial_data:
                    if data_item.get("success"):
                        # Create MCP data record
                        mcp_record = MCPData(
                            data_type=data_item["type"],
                            raw_data=json.dumps(data_item),
                            timestamp=datetime.utcnow(),
                            phone_number=getattr(self.mcp_client, 'current_phone', '2222222222'),
                            session_id=getattr(self.mcp_client, 'session_id', 'unknown')
                        )
                        
                        db.add(mcp_record)
                        stored_count += 1
                        self.stats["data_types_collected"].add(data_item["type"])
                
                db.commit()
                self.stats["successful_collections"] += 1
                self.stats["last_collection_time"] = datetime.utcnow()
                
                logger.info(f"Successfully stored {stored_count} data records")
                
                return {
                    "success": True,
                    "records_stored": stored_count,
                    "data_types": list(self.stats["data_types_collected"]),
                    "timestamp": self.stats["last_collection_time"].isoformat()
                }
                
            except Exception as e:
                db.rollback()
                logger.error(f"Database error during collection: {e}")
                self.stats["failed_collections"] += 1
                return {"success": False, "error": f"Database error: {str(e)}"}
            
            finally:
                db.close()
        
        except Exception as e:
            logger.error(f"MCP data collection error: {e}")
            log_error('mcp.periodic.agent', e, "MCP data collection")
            self.stats["failed_collections"] += 1
            return {"success": False, "error": str(e)}
    
    def _should_trigger_analysis(self) -> bool:
        """Determine if AI analysis should be triggered"""
        try:
            # Check quota availability
            if not quota_manager.check_quota_available(3)["available"]:
                logger.info("Skipping analysis - quota exceeded")
                return False
            
            # Check data freshness
            data_freshness_hours = self.config.get("analysis_triggers", {}).get("data_freshness_hours", 2)
            
            if self.stats["last_analysis_time"]:
                time_since_analysis = datetime.utcnow() - self.stats["last_analysis_time"]
                if time_since_analysis < timedelta(hours=data_freshness_hours):
                    logger.info("Skipping analysis - too recent")
                    return False
            
            # Check if we have fresh data
            db = SessionLocal()
            try:
                recent_data = db.query(MCPData).filter(
                    MCPData.timestamp > datetime.utcnow() - timedelta(hours=1)
                ).count()
                
                return recent_data > 0
            finally:
                db.close()
        
        except Exception as e:
            logger.error(f"Error checking analysis triggers: {e}")
            return False
    
    def generate_ai_analysis(self, force: bool = False) -> Dict[str, Any]:
        """Generate AI analysis of collected financial data"""
        try:
            # Check quota unless forced
            if not force:
                quota_check = quota_manager.check_quota_available(5)
                if not quota_check["available"]:
                    return {
                        "success": False, 
                        "error": "Quota exceeded",
                        "quota_status": quota_check
                    }
            
            logger.info("Starting AI analysis of financial data...")
            
            # Get recent financial data
            db = SessionLocal()
            try:
                # Get latest data from each type
                latest_data = {}
                data_types = ["net_worth", "credit_report", "epf_details", "bank_transactions", "mutual_fund_transactions"]
                
                for data_type in data_types:
                    latest_record = db.query(MCPData).filter(
                        MCPData.data_type == data_type
                    ).order_by(MCPData.timestamp.desc()).first()
                    
                    if latest_record:
                        latest_data[data_type] = json.loads(latest_record.raw_data)
                
                if not latest_data:
                    return {"success": False, "error": "No financial data available for analysis"}
                
                # Generate comprehensive financial analysis
                analysis_results = []
                
                # 1. Portfolio Analysis
                if "net_worth" in latest_data:
                    portfolio_analysis = self._analyze_portfolio(latest_data["net_worth"])
                    if portfolio_analysis:
                        analysis_results.append(portfolio_analysis)
                
                # 2. Risk Assessment
                if "credit_report" in latest_data:
                    risk_analysis = self._analyze_credit_risk(latest_data["credit_report"])
                    if risk_analysis:
                        analysis_results.append(risk_analysis)
                
                # 3. Financial Health Analysis
                health_analysis = self._analyze_financial_health(latest_data)
                if health_analysis:
                    analysis_results.append(health_analysis)
                
                # 4. Investment Opportunities
                opportunity_analysis = self._analyze_opportunities(latest_data)
                if opportunity_analysis:
                    analysis_results.append(opportunity_analysis)
                
                # Store insights in database
                stored_insights = []
                for insight_data in analysis_results:
                    if insight_data:
                        insight = AIInsight(
                            title=insight_data["title"],
                            content=insight_data["content"],
                            insight_type=insight_data["type"],
                            confidence_score=insight_data.get("confidence", 0.8),
                            data_sources=json.dumps(insight_data.get("sources", [])),
                            created_at=datetime.utcnow()
                        )
                        db.add(insight)
                        stored_insights.append(insight_data)
                
                db.commit()
                self.stats["analysis_count"] += 1
                self.stats["last_analysis_time"] = datetime.utcnow()
                
                logger.info(f"Generated {len(stored_insights)} AI insights")
                
                return {
                    "success": True,
                    "insights_generated": len(stored_insights),
                    "insights": stored_insights,
                    "timestamp": self.stats["last_analysis_time"].isoformat()
                }
            
            finally:
                db.close()
        
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            log_error('mcp.periodic.agent', e, "AI analysis generation")
            return {"success": False, "error": str(e)}
    
    def _analyze_portfolio(self, net_worth_data: Dict) -> Optional[Dict]:
        """Analyze portfolio composition and performance"""
        try:
            if not net_worth_data.get("success") or "data" not in net_worth_data:
                return None
            
            # Extract portfolio data
            portfolio_context = self._extract_portfolio_metrics(net_worth_data)
            
            prompt = f"""
            Analyze this portfolio composition and provide investment insights:
            
            Portfolio Data:
            {json.dumps(portfolio_context, indent=2)}
            
            Please provide:
            1. Asset allocation analysis
            2. Diversification assessment
            3. Risk level evaluation
            4. Specific recommendations for improvement
            
            Keep the analysis practical and actionable.
            """
            
            messages = [
                SystemMessage(content="You are a financial advisor specializing in portfolio analysis. Provide clear, actionable insights based on the data."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "title": "Portfolio Composition Analysis",
                "content": response.content,
                "type": "portfolio_analysis",
                "confidence": 0.85,
                "sources": ["net_worth"]
            }
        
        except Exception as e:
            logger.error(f"Portfolio analysis error: {e}")
            return None
    
    def _analyze_credit_risk(self, credit_data: Dict) -> Optional[Dict]:
        """Analyze credit profile and risk factors"""
        try:
            if not credit_data.get("success") or "data" not in credit_data:
                return None
            
            # Extract credit metrics
            credit_context = self._extract_credit_metrics(credit_data)
            
            prompt = f"""
            Analyze this credit profile and assess financial risk:
            
            Credit Data:
            {json.dumps(credit_context, indent=2)}
            
            Please provide:
            1. Credit score interpretation
            2. Risk factors identified
            3. Credit improvement strategies
            4. Debt management recommendations
            
            Focus on actionable steps for credit improvement.
            """
            
            messages = [
                SystemMessage(content="You are a credit counselor providing risk assessment and improvement strategies. Be specific and practical."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "title": "Credit Risk Assessment",
                "content": response.content,
                "type": "risk_assessment",
                "confidence": 0.9,
                "sources": ["credit_report"]
            }
        
        except Exception as e:
            logger.error(f"Credit risk analysis error: {e}")
            return None
    
    def _analyze_financial_health(self, all_data: Dict) -> Optional[Dict]:
        """Analyze overall financial health"""
        try:
            # Compile comprehensive financial picture
            financial_summary = {}
            
            for data_type, data in all_data.items():
                if data.get("success"):
                    financial_summary[data_type] = self._extract_key_metrics(data, data_type)
            
            prompt = f"""
            Analyze the overall financial health based on this comprehensive data:
            
            Financial Summary:
            {json.dumps(financial_summary, indent=2)}
            
            Please provide:
            1. Overall financial health score (1-10)
            2. Strengths in the financial profile
            3. Areas needing improvement
            4. Priority actions for financial wellness
            
            Provide a balanced assessment with specific recommendations.
            """
            
            messages = [
                SystemMessage(content="You are a financial wellness advisor. Provide holistic financial health assessment with prioritized recommendations."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "title": "Financial Health Analysis",
                "content": response.content,
                "type": "financial_health_analysis",
                "confidence": 0.88,
                "sources": list(all_data.keys())
            }
        
        except Exception as e:
            logger.error(f"Financial health analysis error: {e}")
            return None
    
    def _analyze_opportunities(self, all_data: Dict) -> Optional[Dict]:
        """Identify investment and financial opportunities"""
        try:
            # Extract opportunity indicators
            opportunity_context = {}
            
            for data_type, data in all_data.items():
                if data.get("success"):
                    opportunity_context[data_type] = self._extract_opportunity_metrics(data, data_type)
            
            prompt = f"""
            Identify financial opportunities based on this data:
            
            Financial Data:
            {json.dumps(opportunity_context, indent=2)}
            
            Please identify:
            1. Investment opportunities based on current allocation
            2. Tax optimization strategies
            3. Income enhancement possibilities
            4. Cost reduction opportunities
            
            Focus on specific, actionable opportunities with clear benefits.
            """
            
            messages = [
                SystemMessage(content="You are an investment advisor focused on identifying growth opportunities. Provide specific, actionable recommendations."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "title": "Financial Opportunities Analysis",
                "content": response.content,
                "type": "opportunity",
                "confidence": 0.82,
                "sources": list(all_data.keys())
            }
        
        except Exception as e:
            logger.error(f"Opportunities analysis error: {e}")
            return None
    
    def _extract_portfolio_metrics(self, data: Dict) -> Dict:
        """Extract portfolio metrics for analysis"""
        try:
            content = data.get("data", {}).get("content", [{}])[0].get("text", "{}")
            parsed_data = json.loads(content)
            
            if "netWorthResponse" in parsed_data:
                nw_response = parsed_data["netWorthResponse"]
                
                # Calculate asset allocation
                assets = {}
                total_assets = 0
                
                for asset in nw_response.get("assetValues", []):
                    asset_type = asset["netWorthAttribute"]
                    value = int(asset["value"]["units"])
                    assets[asset_type] = value
                    total_assets += value
                
                # Calculate asset percentages
                asset_allocation = {}
                for asset_type, value in assets.items():
                    percentage = (value / total_assets * 100) if total_assets > 0 else 0
                    asset_allocation[asset_type] = {
                        "value": value,
                        "percentage": round(percentage, 2)
                    }
                
                return {
                    "total_assets": total_assets,
                    "asset_allocation": asset_allocation,
                    "diversification_score": len(assets),
                    "currency": "INR"
                }
        
        except Exception as e:
            logger.error(f"Error extracting portfolio metrics: {e}")
        
        return {}
    
    def _extract_credit_metrics(self, data: Dict) -> Dict:
        """Extract credit metrics for analysis"""
        try:
            content = data.get("data", {}).get("content", [{}])[0].get("text", "{}")
            parsed_data = json.loads(content)
            
            if "creditReports" in parsed_data and len(parsed_data["creditReports"]) > 0:
                credit_report = parsed_data["creditReports"][0]["creditReportData"]
                
                metrics = {}
                
                # Credit score
                if "score" in credit_report:
                    metrics["credit_score"] = int(credit_report["score"]["bureauScore"])
                
                # Account summary
                if "creditAccount" in credit_report:
                    account_summary = credit_report["creditAccount"].get("creditAccountSummary", {})
                    if "account" in account_summary:
                        metrics["accounts"] = account_summary["account"]
                    
                    if "totalOutstandingBalance" in account_summary:
                        balance = account_summary["totalOutstandingBalance"]
                        metrics["outstanding_debt"] = {
                            "secured": int(balance.get("outstandingBalanceSecured", 0)),
                            "unsecured": int(balance.get("outstandingBalanceUnSecured", 0))
                        }
                
                return metrics
        
        except Exception as e:
            logger.error(f"Error extracting credit metrics: {e}")
        
        return {}
    
    def _extract_key_metrics(self, data: Dict, data_type: str) -> Dict:
        """Extract key metrics based on data type"""
        try:
            if data_type == "net_worth":
                return self._extract_portfolio_metrics(data)
            elif data_type == "credit_report":
                return self._extract_credit_metrics(data)
            elif data_type == "epf_details":
                return self._extract_epf_metrics(data)
            else:
                return {"data_type": data_type, "available": True}
        
        except Exception:
            return {"data_type": data_type, "available": False}
    
    def _extract_epf_metrics(self, data: Dict) -> Dict:
        """Extract EPF metrics for analysis"""
        try:
            content = data.get("data", {}).get("content", [{}])[0].get("text", "{}")
            parsed_data = json.loads(content)
            
            if "uanAccounts" in parsed_data and len(parsed_data["uanAccounts"]) > 0:
                uan_account = parsed_data["uanAccounts"][0]
                
                metrics = {}
                
                if "rawDetails" in uan_account:
                    raw_details = uan_account["rawDetails"]
                    if "overall_pf_balance" in raw_details:
                        pf_balance = raw_details["overall_pf_balance"]
                        metrics["current_balance"] = int(pf_balance.get("current_pf_balance", 0))
                        metrics["employee_contribution"] = int(pf_balance.get("employee_contribution", 0))
                        metrics["employer_contribution"] = int(pf_balance.get("employer_contribution", 0))
                
                return metrics
        
        except Exception as e:
            logger.error(f"Error extracting EPF metrics: {e}")
        
        return {}
    
    def _extract_opportunity_metrics(self, data: Dict, data_type: str) -> Dict:
        """Extract metrics relevant to identifying opportunities"""
        return self._extract_key_metrics(data, data_type)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and statistics"""
        return {
            "agent_id": self.agent_id,
            "running": self.running,
            "stats": self.stats.copy(),
            "config": self.config,
            "mcp_connection": self.test_mcp_connection(),
            "last_update": datetime.utcnow().isoformat()
        }
    
    def test_mcp_connection(self) -> bool:
        """Test connection to Fi MCP server"""
        try:
            # Use the new thread-safe authentication
            if self.mcp_client.ensure_authenticated():
                # Try to get some data to verify connection works
                test_data = self.mcp_client.get_financial_data()
                return test_data.get("success", False)
            return False
        except Exception as e:
            logger.error(f"MCP connection test failed: {e}")
            return False

# Singleton instance
mcp_periodic_ai_agent = MCPPeriodicAIAgent() 