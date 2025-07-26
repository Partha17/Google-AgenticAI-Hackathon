"""
Enhanced Financial Multi-Agent System - Main Application
Complete Google Cloud Platform integration with ADK multi-agent architecture
"""

import asyncio
import logging
import sys
import signal
from datetime import datetime
from typing import Dict, Any, Optional

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_financial_system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import enhanced orchestrator and all Google Cloud services
try:
    from adk_agents.enhanced_adk_orchestrator import enhanced_adk_orchestrator
    from services.google_cloud_manager import google_cloud_manager
    from services.google_vertex_ai_enhanced import vertex_ai_enhanced
    from services.google_auth_manager import google_auth_manager
    from services.google_scheduler_manager import google_scheduler_manager
    from services.google_cloud_functions_manager import google_cloud_functions_manager
    from config import settings
    
    logger.info("✅ All enhanced components imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import enhanced components: {e}")
    sys.exit(1)

class EnhancedFinancialSystem:
    """
    Enhanced Financial Multi-Agent System with complete Google Cloud integration
    Enterprise-grade financial intelligence platform
    """
    
    def __init__(self):
        self.system_name = "Enhanced Financial Multi-Agent System"
        self.version = "2.0.0"
        self.orchestrator = enhanced_adk_orchestrator
        
        # Google Cloud service managers
        self.cloud_manager = google_cloud_manager
        self.vertex_ai = vertex_ai_enhanced
        self.auth_manager = google_auth_manager
        self.scheduler = google_scheduler_manager
        self.functions_manager = google_cloud_functions_manager
        
        # System state
        self.is_running = False
        self.initialization_complete = False
        self.system_health = "unknown"
        
        # Performance tracking
        self.startup_time = None
        self.total_analyses_completed = 0
        self.total_cloud_operations = 0
        
        logger.info(f"🚀 {self.system_name} v{self.version} initialized")
    
    async def startup(self) -> Dict[str, Any]:
        """Complete system startup with all Google Cloud services"""
        try:
            startup_start = datetime.utcnow()
            logger.info(f"🌟 Starting {self.system_name} with Google Cloud Platform...")
            
            # Display startup banner
            self._display_startup_banner()
            
            # Initialize enhanced system
            logger.info("🔧 Initializing enhanced multi-agent system...")
            init_result = await self.orchestrator.initialize_enhanced_system()
            
            if init_result.get("system_status") in ["ready", "partial"]:
                self.initialization_complete = True
                self.system_health = init_result.get("system_health", "unknown")
                
                # Calculate startup time
                startup_end = datetime.utcnow()
                self.startup_time = (startup_end - startup_start).total_seconds()
                
                # Display system status
                await self._display_system_status(init_result)
                
                # Setup signal handlers for graceful shutdown
                self._setup_signal_handlers()
                
                self.is_running = True
                
                logger.info(f"✅ System startup completed in {self.startup_time:.1f} seconds")
                logger.info(f"🎯 System health: {self.system_health}")
                
                return {
                    "success": True,
                    "startup_time_seconds": self.startup_time,
                    "system_health": self.system_health,
                    "initialization_result": init_result
                }
            else:
                error_msg = init_result.get("error", "System initialization failed")
                logger.error(f"❌ System startup failed: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "initialization_result": init_result
                }
                
        except Exception as e:
            logger.error(f"❌ Critical error during startup: {e}")
            return {"success": False, "error": str(e)}
    
    def _display_startup_banner(self):
        """Display enhanced startup banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🚀 Enhanced Financial Multi-Agent System v{self.version}                     ║
║                                                                              ║
║    🤖 Multi-Agent ADK Architecture                                          ║
║    ☁️  Complete Google Cloud Platform Integration                           ║
║    🧠 Advanced AI with Vertex AI & Gemini                                   ║
║    ⚡ Serverless Computing with Cloud Functions                             ║
║    📊 Real-time Analytics with BigQuery & Monitoring                        ║
║    🔐 Enterprise Security with Google Authentication                         ║
║    🌐 Multi-language & Voice AI Capabilities                                ║
║                                                                              ║
║    🎯 Comprehensive Financial Intelligence Platform                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        logger.info("System banner displayed")
    
    async def _display_system_status(self, init_result: Dict[str, Any]):
        """Display comprehensive system status"""
        try:
            logger.info("📊 System Status Summary:")
            logger.info(f"   └─ Overall Health: {init_result.get('system_health', 'unknown')}")
            
            # ADK Agents Status
            adk_agents = init_result.get("adk_agents", {})
            logger.info(f"🤖 ADK Agents: {len(adk_agents)} agents")
            for agent_name, agent_status in adk_agents.items():
                status_icon = "✅" if agent_status.get("status") == "ready" else "❌"
                agent_display = agent_name.replace("_", " ").title()
                logger.info(f"   └─ {status_icon} {agent_display}")
            
            # Google Cloud Services Status
            cloud_services = init_result.get("google_cloud_services", {})
            logger.info(f"☁️  Google Cloud Services: {len(cloud_services)} services")
            for service_name, service_status in cloud_services.items():
                if service_status.get("status") == "healthy":
                    status_icon = "✅"
                elif service_status.get("status") == "degraded":
                    status_icon = "⚠️"
                else:
                    status_icon = "❌"
                service_display = service_name.replace("_", " ").title()
                logger.info(f"   └─ {status_icon} {service_display}")
            
            # Serverless Functions Status
            functions_info = init_result.get("serverless_functions", {})
            if functions_info.get("status") == "ready":
                deployed = functions_info.get("deployed_functions", 0)
                total = functions_info.get("total_functions", 0)
                logger.info(f"⚡ Cloud Functions: {deployed}/{total} deployed")
            else:
                logger.info(f"⚡ Cloud Functions: ❌ Not ready")
            
            # Automated Workflows Status
            workflows_info = init_result.get("scheduled_workflows", {})
            if workflows_info.get("status") == "ready":
                created = workflows_info.get("created_workflows", 0)
                total = workflows_info.get("total_workflows", 0)
                logger.info(f"⏰ Scheduled Workflows: {created}/{total} active")
            else:
                logger.info(f"⏰ Scheduled Workflows: ❌ Not ready")
            
            # Enhanced Capabilities
            capabilities = init_result.get("capabilities", [])
            logger.info(f"🎯 Enhanced Capabilities: {len(capabilities)} active")
            for capability in capabilities[:5]:  # Show first 5
                logger.info(f"   └─ ✨ {capability.replace('_', ' ').title()}")
            
        except Exception as e:
            logger.error(f"Error displaying system status: {e}")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"📡 Received signal {signum}, initiating graceful shutdown...")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    # === Interactive System Operations ===
    
    async def run_interactive_demo(self):
        """Run an interactive demonstration of system capabilities"""
        try:
            if not self.initialization_complete:
                logger.error("❌ System not properly initialized")
                return
            
            logger.info("🎮 Starting Interactive System Demonstration")
            
            demo_scenarios = [
                {
                    "name": "Comprehensive Cloud Analysis",
                    "description": "Full-stack financial analysis using all Google Cloud services",
                    "function": self._demo_comprehensive_analysis
                },
                {
                    "name": "AI-Powered Market Intelligence",
                    "description": "Advanced market analysis using Vertex AI",
                    "function": self._demo_ai_market_intelligence
                },
                {
                    "name": "Real-time Risk Monitoring",
                    "description": "Live risk assessment with Cloud Monitoring",
                    "function": self._demo_real_time_monitoring
                },
                {
                    "name": "Multi-language Financial Reports", 
                    "description": "Financial reports in multiple languages",
                    "function": self._demo_multilingual_reports
                },
                {
                    "name": "Serverless Portfolio Analysis",
                    "description": "Scalable portfolio analysis using Cloud Functions",
                    "function": self._demo_serverless_analysis
                }
            ]
            
            logger.info("📋 Available Demo Scenarios:")
            for i, scenario in enumerate(demo_scenarios, 1):
                logger.info(f"   {i}. {scenario['name']}: {scenario['description']}")
            
            # Run all demos
            for scenario in demo_scenarios:
                logger.info(f"🚀 Running Demo: {scenario['name']}")
                try:
                    result = await scenario['function']()
                    if result.get("success"):
                        logger.info(f"✅ Demo completed: {scenario['name']}")
                    else:
                        logger.warning(f"⚠️ Demo had issues: {scenario['name']} - {result.get('error')}")
                except Exception as e:
                    logger.error(f"❌ Demo failed: {scenario['name']} - {str(e)}")
                
                # Small delay between demos
                await asyncio.sleep(2)
            
            logger.info("🎉 Interactive demonstration completed!")
            
        except Exception as e:
            logger.error(f"❌ Error in interactive demo: {e}")
    
    async def _demo_comprehensive_analysis(self) -> Dict[str, Any]:
        """Demo comprehensive cloud-powered analysis"""
        try:
            logger.info("   🔍 Executing comprehensive cloud analysis...")
            
            result = await self.orchestrator.execute_comprehensive_cloud_analysis(
                user_request={"analysis_type": "comprehensive", "priority": "high"},
                phone_number="demo_user_12345"
            )
            
            if result.get("status") == "completed":
                services_used = len(result.get("google_cloud_services_used", []))
                execution_time = result.get("execution_time_seconds", 0)
                recommendations_count = len(result.get("final_recommendations", []))
                
                logger.info(f"   ✨ Analysis completed using {services_used} Google Cloud services")
                logger.info(f"   ⏱️ Execution time: {execution_time:.1f} seconds")
                logger.info(f"   💡 Generated {recommendations_count} intelligent recommendations")
                
                self.total_analyses_completed += 1
                self.total_cloud_operations += services_used
                
                return {"success": True, "result": result}
            else:
                return {"success": False, "error": result.get("error")}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _demo_ai_market_intelligence(self) -> Dict[str, Any]:
        """Demo AI-powered market intelligence"""
        try:
            logger.info("   🧠 Running AI market intelligence analysis...")
            
            # Market sentiment analysis
            market_news = [
                "Technology sector shows strong growth momentum with AI innovations",
                "Federal Reserve maintains dovish stance supporting market optimism",
                "Healthcare sector benefits from breakthrough drug approvals"
            ]
            
            sentiment_result = await self.vertex_ai.analyze_market_sentiment(market_news)
            
            if sentiment_result.get("success"):
                sentiment = sentiment_result["sentiment_analysis"]
                logger.info(f"   📈 Market sentiment: {sentiment.get('overall_sentiment', 'neutral').upper()}")
                logger.info(f"   🎯 Confidence: {sentiment.get('confidence', 0.5)*100:.1f}%")
                
                # Financial forecasting
                historical_data = {
                    "returns": [0.08, 0.12, -0.05, 0.15, 0.09, 0.07],
                    "volatility": [0.15, 0.18, 0.22, 0.16, 0.14, 0.13]
                }
                
                forecast_result = await self.vertex_ai.generate_financial_forecast(historical_data, "3_months")
                
                if forecast_result.get("success"):
                    logger.info("   🔮 Financial forecast generated successfully")
                    
                return {"success": True}
            else:
                return {"success": False, "error": sentiment_result.get("error")}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _demo_real_time_monitoring(self) -> Dict[str, Any]:
        """Demo real-time monitoring capabilities"""
        try:
            logger.info("   📊 Setting up real-time monitoring...")
            
            # Record system metrics
            metrics_recorded = 0
            
            # Portfolio performance metric
            portfolio_metric = await self.cloud_manager.record_custom_metric(
                "portfolio_performance", 
                85.7, 
                {"demo": "true", "metric_type": "performance"}
            )
            if portfolio_metric:
                metrics_recorded += 1
            
            # Risk level metric
            risk_metric = await self.cloud_manager.record_custom_metric(
                "risk_level", 
                65.2, 
                {"demo": "true", "metric_type": "risk"}
            )
            if risk_metric:
                metrics_recorded += 1
            
            # System health metric
            health_metric = await self.cloud_manager.record_custom_metric(
                "system_health", 
                92.1, 
                {"demo": "true", "metric_type": "system"}
            )
            if health_metric:
                metrics_recorded += 1
            
            logger.info(f"   📈 Recorded {metrics_recorded} real-time metrics")
            
            # Retrieve recent metrics
            recent_metrics = await self.cloud_manager.get_system_metrics(hours_back=1)
            logger.info(f"   📋 Retrieved {len(recent_metrics)} metric series")
            
            return {"success": True, "metrics_recorded": metrics_recorded}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _demo_multilingual_reports(self) -> Dict[str, Any]:
        """Demo multi-language financial reports"""
        try:
            logger.info("   🌐 Generating multi-language financial reports...")
            
            base_report = "Portfolio analysis shows strong performance with 15% annual return. Risk level is moderate. Recommend increasing diversification in emerging markets."
            
            languages = ["es", "fr", "de", "ja"]
            translations_completed = 0
            
            for lang in languages:
                try:
                    translation_result = await self.vertex_ai.translate_financial_report(base_report, lang)
                    if translation_result.get("success"):
                        translations_completed += 1
                        lang_name = {"es": "Spanish", "fr": "French", "de": "German", "ja": "Japanese"}.get(lang, lang)
                        logger.info(f"   ✅ Report translated to {lang_name}")
                    
                except Exception as e:
                    logger.warning(f"   ⚠️ Translation to {lang} failed: {e}")
            
            logger.info(f"   🌍 Completed {translations_completed}/{len(languages)} translations")
            
            return {"success": True, "translations": translations_completed}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _demo_serverless_analysis(self) -> Dict[str, Any]:
        """Demo serverless portfolio analysis"""
        try:
            logger.info("   ⚡ Running serverless portfolio analysis...")
            
            # Invoke portfolio analyzer function
            portfolio_result = await self.functions_manager.invoke_function(
                "portfolio_analyzer",
                {
                    "portfolio_id": "demo_portfolio_001",
                    "analysis_depth": "comprehensive",
                    "include_optimization": True
                }
            )
            
            if portfolio_result.get("success"):
                logger.info("   ✅ Serverless portfolio analysis triggered")
                
                # Invoke risk calculator function
                risk_result = await self.functions_manager.invoke_function(
                    "risk_calculator",
                    {
                        "portfolio_id": "demo_portfolio_001",
                        "risk_models": ["var", "cvar", "monte_carlo"],
                        "confidence_level": 0.95
                    }
                )
                
                if risk_result.get("success"):
                    logger.info("   ✅ Serverless risk calculation triggered")
                    return {"success": True}
                else:
                    return {"success": False, "error": "Risk calculation failed"}
            else:
                return {"success": False, "error": "Portfolio analysis failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # === System Management ===
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system performance metrics"""
        try:
            # Get enhanced system status
            system_status = await self.orchestrator.get_enhanced_system_status()
            
            # Calculate uptime
            uptime = (datetime.utcnow() - datetime.fromisoformat(system_status.get("timestamp", datetime.utcnow().isoformat()))).total_seconds() if self.startup_time else 0
            
            metrics = {
                "system_info": {
                    "name": self.system_name,
                    "version": self.version,
                    "uptime_seconds": uptime,
                    "startup_time_seconds": self.startup_time,
                    "system_health": self.system_health
                },
                "performance_counters": {
                    "total_analyses_completed": self.total_analyses_completed,
                    "total_cloud_operations": self.total_cloud_operations,
                    "initialization_complete": self.initialization_complete,
                    "is_running": self.is_running
                },
                "enhanced_system_status": system_status,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e)}
    
    async def shutdown(self):
        """Graceful system shutdown"""
        try:
            logger.info("🔄 Initiating graceful system shutdown...")
            
            # Stop accepting new requests
            self.is_running = False
            
            # Clean up authentication sessions
            self.auth_manager.cleanup_expired_sessions()
            logger.info("✅ Authentication sessions cleaned up")
            
            # Log final metrics
            final_metrics = await self.get_system_metrics()
            logger.info(f"📊 Final system metrics: {self.total_analyses_completed} analyses, {self.total_cloud_operations} cloud operations")
            
            # Log shutdown completion
            total_uptime = final_metrics.get("system_info", {}).get("uptime_seconds", 0)
            logger.info(f"✅ System shutdown completed. Total uptime: {total_uptime:.1f} seconds")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")

# === Main Application Entry Point ===

async def main():
    """Main application entry point"""
    try:
        # Create enhanced system instance
        financial_system = EnhancedFinancialSystem()
        
        # Startup system
        startup_result = await financial_system.startup()
        
        if not startup_result.get("success"):
            logger.error("❌ System startup failed")
            sys.exit(1)
        
        # Run interactive demonstration
        await financial_system.run_interactive_demo()
        
        # Keep system running
        logger.info("🔄 System is running... Press Ctrl+C to shutdown")
        
        try:
            while financial_system.is_running:
                # Periodic health check
                await asyncio.sleep(30)
                
                # Get system metrics
                metrics = await financial_system.get_system_metrics()
                health = metrics.get("system_info", {}).get("system_health", "unknown")
                
                if health in ["poor", "error"]:
                    logger.warning(f"⚠️ System health degraded: {health}")
                
        except KeyboardInterrupt:
            logger.info("📡 Received shutdown signal")
        
        # Graceful shutdown
        await financial_system.shutdown()
        
    except Exception as e:
        logger.error(f"❌ Critical system error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the enhanced financial system
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Application terminated by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1) 