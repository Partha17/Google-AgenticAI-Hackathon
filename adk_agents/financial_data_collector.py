"""
Financial Data Collector Agent - ADK Implementation
Specialized agent for collecting and processing financial data from Fi MCP server
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from services.fi_mcp_client import fi_mcp_client
from services.real_data_collector import real_data_collector
from adk_agents.agent_config import adk_config

logger = logging.getLogger(__name__)

class FinancialDataCollectorAgent:
    """ADK-based Financial Data Collection Agent"""
    
    def __init__(self):
        self.agent_id = "financial_data_collector"
        self.config = adk_config.get_agent_definitions()[self.agent_id]
        self.fi_client = fi_mcp_client
        self.data_collector = real_data_collector
        self.session_active = False
        
    async def initialize(self) -> bool:
        """Initialize the agent and establish connections"""
        try:
            logger.info(f"Initializing {self.agent_id} agent...")
            
            # Test Fi MCP connection
            if not self.fi_client.authenticate():
                logger.error("Failed to authenticate with Fi MCP server")
                return False
            
            self.session_active = True
            logger.info("Financial Data Collector Agent initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            return False
    
    async def collect_all_financial_data(self) -> Dict[str, Any]:
        """
        Collect comprehensive financial data from all available sources
        This is the main tool function for this agent
        """
        if not self.session_active:
            await self.initialize()
        
        try:
            logger.info("Starting comprehensive financial data collection...")
            
            # Collect all types of financial data
            collection_results = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data_sources": [],
                "total_records": 0,
                "data_quality_score": 0.0,
                "success": False,
                "errors": []
            }
            
            # Define data collection tasks
            data_tasks = [
                ("net_worth", self.fi_client.fetch_net_worth),
                ("bank_transactions", self.fi_client.fetch_bank_transactions),
                ("mutual_fund_transactions", self.fi_client.fetch_mutual_fund_transactions),
                ("epf_details", self.fi_client.fetch_epf_details),
                ("credit_report", self.fi_client.fetch_credit_report)
            ]
            
            collected_data = []
            successful_collections = 0
            
            # Execute data collection tasks
            for data_type, collector_func in data_tasks:
                try:
                    logger.info(f"Collecting {data_type} data...")
                    result = collector_func()
                    
                    if result.get("success"):
                        collected_data.append(result)
                        successful_collections += 1
                        
                        # Store in database using existing collector
                        self.data_collector._store_mcp_data(
                            data_type, 
                            result.get("data", {}),
                            result.get("raw_response", {})
                        )
                        
                        collection_results["data_sources"].append({
                            "type": data_type,
                            "success": True,
                            "records": 1,
                            "quality_score": self._assess_data_quality(result)
                        })
                        
                        logger.info(f"Successfully collected {data_type} data")
                    else:
                        error_msg = result.get("error", "Unknown error")
                        collection_results["errors"].append(f"{data_type}: {error_msg}")
                        collection_results["data_sources"].append({
                            "type": data_type,
                            "success": False,
                            "error": error_msg
                        })
                        logger.warning(f"Failed to collect {data_type}: {error_msg}")
                        
                except Exception as e:
                    error_msg = str(e)
                    collection_results["errors"].append(f"{data_type}: {error_msg}")
                    logger.error(f"Error collecting {data_type}: {e}")
            
            # Calculate overall metrics
            collection_results["total_records"] = len(collected_data)
            collection_results["success"] = successful_collections > 0
            collection_results["data_quality_score"] = self._calculate_overall_quality(collection_results["data_sources"])
            
            # Generate summary
            collection_results["summary"] = self._generate_collection_summary(collection_results)
            
            logger.info(f"Data collection completed: {successful_collections}/{len(data_tasks)} sources successful")
            return collection_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive data collection: {e}")
            return {
                "agent_id": self.agent_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def validate_data_sources(self) -> Dict[str, Any]:
        """Validate the health and availability of data sources"""
        try:
            logger.info("Validating data source health...")
            
            validation_results = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "fi_mcp_server": {
                    "available": False,
                    "response_time_ms": 0,
                    "authenticated": False
                },
                "database": {
                    "accessible": False,
                    "connection_status": "unknown"
                },
                "overall_health": "unhealthy"
            }
            
            # Test Fi MCP server
            start_time = datetime.utcnow()
            mcp_available = self.data_collector.test_mcp_connection()
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            validation_results["fi_mcp_server"] = {
                "available": mcp_available,
                "response_time_ms": response_time,
                "authenticated": self.fi_client.authenticated
            }
            
            # Test database connection
            try:
                from models.database import SessionLocal
                db = SessionLocal()
                db.execute("SELECT 1")
                db.close()
                validation_results["database"] = {
                    "accessible": True,
                    "connection_status": "healthy"
                }
            except Exception as e:
                validation_results["database"] = {
                    "accessible": False,
                    "connection_status": f"error: {str(e)}"
                }
            
            # Determine overall health
            if (validation_results["fi_mcp_server"]["available"] and 
                validation_results["database"]["accessible"]):
                validation_results["overall_health"] = "healthy"
            elif (validation_results["fi_mcp_server"]["available"] or 
                  validation_results["database"]["accessible"]):
                validation_results["overall_health"] = "partial"
            else:
                validation_results["overall_health"] = "unhealthy"
            
            logger.info(f"Data source validation completed: {validation_results['overall_health']}")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating data sources: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "overall_health": "error",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_collection_statistics(self) -> Dict[str, Any]:
        """Get statistics about recent data collection activities"""
        try:
            from models.database import SessionLocal, MCPData
            from sqlalchemy import func, desc
            
            db = SessionLocal()
            try:
                # Get collection statistics
                stats = {
                    "agent_id": self.agent_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "total_records": 0,
                    "records_by_type": {},
                    "recent_collections": [],
                    "data_quality_trends": {}
                }
                
                # Total records
                stats["total_records"] = db.query(MCPData).count()
                
                # Records by type
                type_counts = db.query(
                    MCPData.data_type,
                    func.count(MCPData.id).label('count')
                ).group_by(MCPData.data_type).all()
                
                stats["records_by_type"] = {
                    result.data_type: result.count for result in type_counts
                }
                
                # Recent collections (last 10)
                recent = db.query(MCPData).order_by(desc(MCPData.timestamp)).limit(10).all()
                stats["recent_collections"] = [
                    {
                        "type": record.data_type,
                        "timestamp": record.timestamp.isoformat() if record.timestamp else None,
                        "processed": record.processed
                    }
                    for record in recent
                ]
                
                logger.info("Collection statistics retrieved successfully")
                return stats
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error getting collection statistics: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _assess_data_quality(self, data_result: Dict[str, Any]) -> float:
        """Assess the quality of collected data"""
        try:
            quality_score = 0.0
            
            # Check basic structure
            if data_result.get("success", False):
                quality_score += 0.3
            
            # Check data presence
            data = data_result.get("data", {})
            if data:
                quality_score += 0.3
                
                # Check data richness
                if len(data) > 5:  # Has multiple fields
                    quality_score += 0.2
                
                # Check for numeric data
                numeric_fields = sum(1 for v in data.values() if isinstance(v, (int, float)))
                if numeric_fields > 0:
                    quality_score += 0.2
            
            return min(quality_score, 1.0)
            
        except Exception:
            return 0.0
    
    def _calculate_overall_quality(self, data_sources: List[Dict[str, Any]]) -> float:
        """Calculate overall data quality score"""
        if not data_sources:
            return 0.0
        
        successful_sources = [src for src in data_sources if src.get("success", False)]
        if not successful_sources:
            return 0.0
        
        quality_scores = [src.get("quality_score", 0.0) for src in successful_sources]
        return sum(quality_scores) / len(quality_scores)
    
    def _generate_collection_summary(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable summary of collection results"""
        total_sources = len(results.get("data_sources", []))
        successful = len([src for src in results.get("data_sources", []) if src.get("success", False)])
        quality = results.get("data_quality_score", 0.0)
        
        summary = f"Collected data from {successful}/{total_sources} sources "
        summary += f"with {quality:.1%} average quality. "
        
        if results.get("errors"):
            summary += f"Encountered {len(results['errors'])} errors."
        else:
            summary += "No errors encountered."
        
        return summary

# Global agent instance
financial_data_collector_agent = FinancialDataCollectorAgent() 