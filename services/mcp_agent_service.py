"""
MCP Agent Service
Manages the MCP Periodic AI Agent lifecycle and startup
"""

import logging
import time
import threading
from typing import Dict, Any

from adk_agents.mcp_periodic_ai_agent import mcp_periodic_ai_agent
from services.logger_config import get_logger

logger = get_logger('mcp.agent.service')

class MCPAgentService:
    """Service to manage the MCP Periodic AI Agent"""
    
    def __init__(self):
        self.agent = mcp_periodic_ai_agent
        self.running = False
        self.startup_thread = None
        
    def start_agent_service(self, auto_start_collection: bool = True):
        """Start the MCP Agent Service"""
        try:
            logger.info("Starting MCP Agent Service...")
            self.running = True
            
            # Test MCP connection first
            if self.agent.test_mcp_connection():
                logger.info("✅ MCP connection successful")
            else:
                logger.warning("⚠️ MCP connection failed - agent will retry later")
            
            # Start periodic collection if requested
            if auto_start_collection:
                logger.info("Starting periodic data collection...")
                self.agent.start_periodic_collection()
                
                # Wait a moment and perform initial data collection
                self._perform_initial_collection()
            
            logger.info("✅ MCP Agent Service started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start MCP Agent Service: {e}")
            return False
    
    def stop_agent_service(self):
        """Stop the MCP Agent Service"""
        try:
            logger.info("Stopping MCP Agent Service...")
            self.running = False
            
            # Stop periodic collection
            self.agent.stop_periodic_collection()
            
            # Wait for any ongoing operations to complete
            if self.startup_thread and self.startup_thread.is_alive():
                self.startup_thread.join(timeout=10)
            
            logger.info("✅ MCP Agent Service stopped")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error stopping MCP Agent Service: {e}")
            return False
    
    def _perform_initial_collection(self):
        """Perform initial data collection in a separate thread"""
        def initial_collection():
            try:
                # Wait a bit for the agent to fully initialize
                time.sleep(5)
                
                logger.info("Performing initial data collection...")
                result = self.agent.collect_mcp_data()
                
                if result.get("success"):
                    logger.info(f"✅ Initial collection successful: {result['records_stored']} records")
                    
                    # Wait a bit more and try initial AI analysis
                    time.sleep(3)
                    analysis_result = self.agent.generate_ai_analysis()
                    
                    if analysis_result.get("success"):
                        logger.info(f"✅ Initial AI analysis successful: {analysis_result['insights_generated']} insights")
                    else:
                        logger.info(f"ℹ️ Initial AI analysis skipped: {analysis_result.get('error', 'Unknown reason')}")
                else:
                    logger.warning(f"⚠️ Initial collection failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"❌ Error in initial collection: {e}")
        
        self.startup_thread = threading.Thread(target=initial_collection, daemon=True)
        self.startup_thread.start()
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get the current service status"""
        agent_status = self.agent.get_agent_status()
        
        return {
            "service_running": self.running,
            "agent_status": agent_status,
            "mcp_connection": agent_status.get("mcp_connection", False),
            "periodic_collection_active": agent_status.get("running", False),
            "last_collection": agent_status.get("stats", {}).get("last_collection_time"),
            "last_analysis": agent_status.get("stats", {}).get("last_analysis_time"),
            "total_collections": agent_status.get("stats", {}).get("total_collections", 0),
            "analysis_count": agent_status.get("stats", {}).get("analysis_count", 0)
        }
    
    def collect_data_now(self) -> Dict[str, Any]:
        """Trigger immediate data collection"""
        try:
            logger.info("Manual data collection triggered")
            return self.agent.collect_mcp_data()
        except Exception as e:
            logger.error(f"Error in manual data collection: {e}")
            return {"success": False, "error": str(e)}
    
    def run_ai_analysis_now(self) -> Dict[str, Any]:
        """Trigger immediate AI analysis"""
        try:
            logger.info("Manual AI analysis triggered")
            return self.agent.generate_ai_analysis(force=True)
        except Exception as e:
            logger.error(f"Error in manual AI analysis: {e}")
            return {"success": False, "error": str(e)}

# Singleton instance
mcp_agent_service = MCPAgentService() 