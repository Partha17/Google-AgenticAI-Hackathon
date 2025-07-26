"""
Enhanced ADK Orchestrator with Complete Google Cloud Integration
Master orchestrator leveraging all Google Cloud services for superior financial intelligence
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import existing ADK components
from adk_agents.adk_orchestrator import ADKOrchestrator
from adk_agents.agent_config import adk_config
from adk_agents.ai_analysis_base import AIAnalysisBase

# Import all Google Cloud services
from services.google_cloud_manager import google_cloud_manager
from services.google_vertex_ai_enhanced import vertex_ai_enhanced
from services.google_auth_manager import google_auth_manager
from services.google_scheduler_manager import google_scheduler_manager
from services.google_cloud_functions_manager import google_cloud_functions_manager

logger = logging.getLogger(__name__)

class EnhancedADKOrchestrator(ADKOrchestrator):
    """
    Enhanced ADK Orchestrator with complete Google Cloud Platform integration
    Provides enterprise-grade financial intelligence through coordinated cloud services
    """
    
    def __init__(self):
        super().__init__()
        self.agent_id = "enhanced_orchestrator_agent"
        
        # Google Cloud service managers
        self.cloud_manager = google_cloud_manager
        self.vertex_ai = vertex_ai_enhanced
        self.auth_manager = google_auth_manager
        self.scheduler = google_scheduler_manager
        self.functions_manager = google_cloud_functions_manager
        
        # Enhanced capabilities
        self.cloud_functions_enabled = True
        self.real_time_monitoring = True
        self.multi_language_support = True
        self.voice_capabilities = True
        
        # Workflow templates
        self.enhanced_workflows = {
            "comprehensive_cloud_analysis": {
                "description": "Full-stack financial analysis using all Google Cloud services",
                "phases": [
                    "cloud_data_collection",
                    "serverless_processing", 
                    "ai_enhanced_analysis",
                    "real_time_monitoring",
                    "intelligent_recommendations"
                ]
            },
            "real_time_risk_monitoring": {
                "description": "Continuous risk monitoring with instant alerts",
                "phases": [
                    "streaming_data_ingestion",
                    "real_time_risk_calculation",
                    "predictive_analytics",
                    "automated_alerting"
                ]
            },
            "intelligent_portfolio_optimization": {
                "description": "AI-powered portfolio optimization with advanced forecasting",
                "phases": [
                    "deep_portfolio_analysis",
                    "market_sentiment_analysis",
                    "optimization_modeling", 
                    "implementation_planning"
                ]
            }
        }
        
        logger.info("✅ Enhanced ADK Orchestrator initialized with full Google Cloud integration")
    
    # === Enhanced System Initialization ===
    
    async def initialize_enhanced_system(self) -> Dict[str, Any]:
        """Initialize the complete enhanced system with all Google Cloud services"""
        try:
            logger.info("🚀 Initializing Enhanced ADK Multi-Agent System with Google Cloud...")
            
            initialization_results = {
                "orchestrator_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "system_status": "initializing",
                "google_cloud_services": {},
                "adk_agents": {},
                "serverless_functions": {},
                "scheduled_workflows": {},
                "system_health": "unknown",
                "capabilities": []
            }
            
            # Initialize base ADK system
            base_init = await super().initialize_system()
            initialization_results["adk_agents"] = base_init.get("agent_status", {})
            
            # Initialize Google Cloud services
            cloud_status = await self.cloud_manager.get_comprehensive_status()
            initialization_results["google_cloud_services"] = cloud_status.get("services", {})
            
            # Initialize serverless functions
            functions_result = await self._initialize_cloud_functions()
            initialization_results["serverless_functions"] = functions_result
            
            # Setup automated workflows
            workflows_result = await self._setup_automated_workflows()
            initialization_results["scheduled_workflows"] = workflows_result
            
            # Determine system capabilities
            capabilities = await self._assess_system_capabilities()
            initialization_results["capabilities"] = capabilities
            
            # Calculate overall health
            health_score = self._calculate_system_health(initialization_results)
            initialization_results["system_health"] = health_score
            initialization_results["system_status"] = "ready" if health_score >= 0.8 else "partial"
            
            logger.info(f"✅ Enhanced system initialization completed - Health: {health_score:.1%}")
            return initialization_results
            
        except Exception as e:
            logger.error(f"Error in enhanced system initialization: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "system_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _initialize_cloud_functions(self) -> Dict[str, Any]:
        """Initialize Google Cloud Functions for serverless agent execution"""
        try:
            logger.info("⚡ Initializing Cloud Functions...")
            
            # Deploy financial functions
            deployment_result = await self.functions_manager.deploy_all_financial_functions()
            
            if deployment_result.get("success"):
                deployed_count = deployment_result.get("deployed_functions", 0)
                total_count = deployment_result.get("total_functions", 0)
                
                return {
                    "status": "ready",
                    "deployed_functions": deployed_count,
                    "total_functions": total_count,
                    "success_rate": deployed_count / total_count if total_count > 0 else 0
                }
            else:
                return {
                    "status": "error",
                    "error": deployment_result.get("error"),
                    "deployed_functions": 0
                }
                
        except Exception as e:
            logger.error(f"Error initializing cloud functions: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _setup_automated_workflows(self) -> Dict[str, Any]:
        """Setup automated financial workflows with Cloud Scheduler"""
        try:
            logger.info("⏰ Setting up automated workflows...")
            
            # Setup financial workflows
            workflows_result = await self.scheduler.setup_financial_workflows()
            
            if workflows_result.get("success"):
                created_count = workflows_result.get("workflows_created", 0)
                total_count = workflows_result.get("total_workflows", 0)
                
                return {
                    "status": "ready",
                    "created_workflows": created_count,
                    "total_workflows": total_count,
                    "success_rate": created_count / total_count if total_count > 0 else 0
                }
            else:
                return {
                    "status": "error", 
                    "error": workflows_result.get("error"),
                    "created_workflows": 0
                }
                
        except Exception as e:
            logger.error(f"Error setting up workflows: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _assess_system_capabilities(self) -> List[str]:
        """Assess enhanced system capabilities"""
        capabilities = []
        
        try:
            # Check Vertex AI capabilities
            vertex_status = await self.vertex_ai.get_service_status()
            if vertex_status.get("vertex_ai_initialized"):
                capabilities.extend([
                    "advanced_ai_analysis",
                    "market_sentiment_analysis", 
                    "ai_portfolio_optimization",
                    "financial_forecasting"
                ])
            
            # Check translation capabilities
            if vertex_status.get("additional_services", {}).get("translation"):
                capabilities.append("multi_language_support")
            
            # Check speech capabilities
            if vertex_status.get("additional_services", {}).get("speech_recognition"):
                capabilities.extend(["voice_commands", "speech_to_text"])
            
            if vertex_status.get("additional_services", {}).get("text_to_speech"):
                capabilities.append("text_to_speech")
            
            # Check cloud services
            if self.cloud_manager.initialized_services.get("firestore"):
                capabilities.append("real_time_data_sync")
            
            if self.cloud_manager.initialized_services.get("bigquery"):
                capabilities.append("advanced_analytics")
            
            if self.cloud_manager.initialized_services.get("monitoring"):
                capabilities.append("system_monitoring")
            
            if self.cloud_manager.initialized_services.get("pubsub"):
                capabilities.append("real_time_events")
            
            # Check functions
            if self.cloud_functions_enabled:
                capabilities.append("serverless_execution")
            
        except Exception as e:
            logger.error(f"Error assessing capabilities: {e}")
        
        return capabilities
    
    def _calculate_system_health(self, init_results: Dict[str, Any]) -> float:
        """Calculate overall system health score"""
        try:
            health_factors = []
            
            # ADK agents health
            adk_agents = init_results.get("adk_agents", {})
            ready_agents = sum(1 for agent in adk_agents.values() if agent.get("status") == "ready")
            total_agents = len(adk_agents)
            if total_agents > 0:
                health_factors.append(ready_agents / total_agents)
            
            # Google Cloud services health
            cloud_services = init_results.get("google_cloud_services", {})
            healthy_services = sum(1 for service in cloud_services.values() if service.get("status") == "healthy")
            total_services = len(cloud_services)
            if total_services > 0:
                health_factors.append(healthy_services / total_services)
            
            # Serverless functions health
            functions_info = init_results.get("serverless_functions", {})
            if functions_info.get("status") == "ready":
                health_factors.append(functions_info.get("success_rate", 0))
            else:
                health_factors.append(0)
            
            # Workflows health
            workflows_info = init_results.get("scheduled_workflows", {})
            if workflows_info.get("status") == "ready":
                health_factors.append(workflows_info.get("success_rate", 0))
            else:
                health_factors.append(0)
            
            # Calculate average
            return sum(health_factors) / len(health_factors) if health_factors else 0
            
        except Exception as e:
            logger.error(f"Error calculating system health: {e}")
            return 0
    
    # === Enhanced Analysis Workflows ===
    
    async def execute_comprehensive_cloud_analysis(self, user_request: Dict[str, Any] = None, phone_number: str = None) -> Dict[str, Any]:
        """Execute comprehensive analysis using all Google Cloud capabilities"""
        try:
            logger.info("🌟 Starting comprehensive cloud-powered financial analysis...")
            
            workflow_results = {
                "orchestrator_id": self.agent_id,
                "workflow_id": f"cloud_workflow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.utcnow().isoformat(),
                "workflow_type": "comprehensive_cloud_analysis",
                "status": "in_progress",
                "phases": {},
                "google_cloud_services_used": [],
                "ai_enhancements": {},
                "real_time_monitoring": {},
                "final_recommendations": [],
                "execution_time_seconds": 0
            }
            
            start_time = datetime.utcnow()
            
            # Phase 1: Cloud-powered data collection
            logger.info("📥 Phase 1: Cloud-powered Data Collection")
            data_phase = await self._execute_cloud_data_collection_phase(phone_number)
            workflow_results["phases"]["cloud_data_collection"] = data_phase
            workflow_results["google_cloud_services_used"].extend(["firestore", "cloud_storage", "pubsub"])
            
            # Phase 2: Serverless processing
            logger.info("⚡ Phase 2: Serverless Agent Processing")
            serverless_phase = await self._execute_serverless_processing_phase(data_phase)
            workflow_results["phases"]["serverless_processing"] = serverless_phase
            workflow_results["google_cloud_services_used"].extend(["cloud_functions"])
            
            # Phase 3: AI-enhanced analysis
            logger.info("🧠 Phase 3: AI-Enhanced Analysis with Vertex AI")
            ai_phase = await self._execute_ai_enhanced_analysis_phase(data_phase, user_request)
            workflow_results["phases"]["ai_enhanced_analysis"] = ai_phase
            workflow_results["ai_enhancements"] = ai_phase.get("ai_results", {})
            workflow_results["google_cloud_services_used"].extend(["vertex_ai", "translation", "speech"])
            
            # Phase 4: Real-time monitoring setup
            logger.info("📊 Phase 4: Real-time Monitoring & Analytics")
            monitoring_phase = await self._execute_monitoring_phase(workflow_results)
            workflow_results["phases"]["real_time_monitoring"] = monitoring_phase
            workflow_results["real_time_monitoring"] = monitoring_phase.get("monitoring_config", {})
            workflow_results["google_cloud_services_used"].extend(["cloud_monitoring", "bigquery"])
            
            # Phase 5: Intelligent recommendations
            logger.info("💡 Phase 5: Intelligent Recommendations Generation")
            recommendations_phase = await self._generate_intelligent_recommendations(workflow_results, user_request)
            workflow_results["phases"]["intelligent_recommendations"] = recommendations_phase
            workflow_results["final_recommendations"] = recommendations_phase.get("recommendations", [])
            
            # Calculate execution time
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()
            workflow_results["execution_time_seconds"] = execution_time
            workflow_results["status"] = "completed"
            
            # Store results in cloud storage
            await self._store_workflow_results(workflow_results)
            
            logger.info(f"✅ Comprehensive cloud analysis completed in {execution_time:.1f} seconds")
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive cloud analysis: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "workflow_type": "comprehensive_cloud_analysis",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_cloud_data_collection_phase(self, phone_number: str = None) -> Dict[str, Any]:
        """Execute cloud-powered data collection with real-time sync"""
        try:
            # Use cloud functions for data processing
            if phone_number:
                function_result = await self.functions_manager.invoke_function(
                    "financial_data_processor",
                    {"phone_number": phone_number}
                )
            else:
                function_result = {"success": False, "error": "No phone number provided"}
            
            # Store data in Firestore for real-time access
            if function_result.get("success"):
                cloud_storage_result = await self.cloud_manager.store_financial_data(
                    phone_number or "demo_user",
                    {"collection_method": "cloud_function", "timestamp": datetime.utcnow().isoformat()}
                )
            else:
                cloud_storage_result = False
            
            return {
                "phase": "cloud_data_collection",
                "success": function_result.get("success", False),
                "function_invocation": function_result,
                "cloud_storage": cloud_storage_result,
                "real_time_sync": True,
                "data_quality_enhanced": True
            }
            
        except Exception as e:
            logger.error(f"Error in cloud data collection: {e}")
            return {"phase": "cloud_data_collection", "success": False, "error": str(e)}
    
    async def _execute_serverless_processing_phase(self, data_phase: Dict[str, Any]) -> Dict[str, Any]:
        """Execute serverless processing using Cloud Functions"""
        try:
            processing_results = {}
            
            # Invoke portfolio analyzer function
            portfolio_result = await self.functions_manager.invoke_function(
                "portfolio_analyzer",
                {"analysis_type": "comprehensive", "data_source": "firestore"}
            )
            processing_results["portfolio_analysis"] = portfolio_result
            
            # Invoke risk calculator function  
            risk_result = await self.functions_manager.invoke_function(
                "risk_calculator",
                {"calculation_type": "advanced", "include_stress_test": True}
            )
            processing_results["risk_calculation"] = risk_result
            
            return {
                "phase": "serverless_processing",
                "success": True,
                "processing_results": processing_results,
                "serverless_execution": True,
                "scalable_processing": True
            }
            
        except Exception as e:
            logger.error(f"Error in serverless processing: {e}")
            return {"phase": "serverless_processing", "success": False, "error": str(e)}
    
    async def _execute_ai_enhanced_analysis_phase(self, data_phase: Dict[str, Any], user_request: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute AI-enhanced analysis using Vertex AI"""
        try:
            ai_results = {}
            
            # Market sentiment analysis
            sample_market_data = [
                "Technology stocks showing strong momentum",
                "Financial sector experiencing volatility", 
                "Healthcare sector remains stable with growth potential"
            ]
            sentiment_result = await self.vertex_ai.analyze_market_sentiment(sample_market_data)
            ai_results["market_sentiment"] = sentiment_result
            
            # AI portfolio optimization
            sample_portfolio = {
                "stocks": 60,
                "bonds": 30, 
                "alternatives": 10
            }
            sample_objectives = {
                "risk_tolerance": "moderate",
                "time_horizon": "long_term",
                "income_needs": "low"
            }
            optimization_result = await self.vertex_ai.optimize_portfolio_ai(sample_portfolio, sample_objectives)
            ai_results["portfolio_optimization"] = optimization_result
            
            # Financial forecasting
            sample_historical_data = {
                "returns": [0.08, 0.12, -0.05, 0.15, 0.09],
                "volatility": [0.15, 0.18, 0.22, 0.16, 0.14]
            }
            forecast_result = await self.vertex_ai.generate_financial_forecast(sample_historical_data, "6_months")
            ai_results["financial_forecast"] = forecast_result
            
            # Multi-language support (if requested)
            if user_request and user_request.get("language") and user_request["language"] != "en":
                translation_result = await self.vertex_ai.translate_financial_report(
                    "Portfolio analysis complete with positive outlook",
                    user_request["language"]
                )
                ai_results["translation"] = translation_result
            
            return {
                "phase": "ai_enhanced_analysis",
                "success": True,
                "ai_results": ai_results,
                "advanced_ai_processing": True,
                "multi_language_support": user_request.get("language") is not None
            }
            
        except Exception as e:
            logger.error(f"Error in AI-enhanced analysis: {e}")
            return {"phase": "ai_enhanced_analysis", "success": False, "error": str(e)}
    
    async def _execute_monitoring_phase(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Setup real-time monitoring and analytics"""
        try:
            # Record workflow metrics
            workflow_metric = await self.cloud_manager.record_custom_metric(
                "workflow_execution",
                workflow_results.get("execution_time_seconds", 0),
                {
                    "workflow_type": workflow_results.get("workflow_type"),
                    "status": workflow_results.get("status"),
                    "services_used": str(len(workflow_results.get("google_cloud_services_used", [])))
                }
            )
            
            # Store analytics in BigQuery
            analytics_data = {
                "workflow_id": workflow_results.get("workflow_id"),
                "timestamp": workflow_results.get("timestamp"),
                "execution_time": workflow_results.get("execution_time_seconds", 0),
                "services_used": len(workflow_results.get("google_cloud_services_used", [])),
                "success": workflow_results.get("status") == "completed"
            }
            bigquery_result = await self.cloud_manager.store_agent_metrics(analytics_data)
            
            monitoring_config = {
                "real_time_metrics": workflow_metric,
                "analytics_storage": bigquery_result,
                "monitoring_enabled": True,
                "alert_thresholds": {
                    "execution_time_warning": 300,  # 5 minutes
                    "error_rate_threshold": 0.1
                }
            }
            
            return {
                "phase": "real_time_monitoring",
                "success": True,
                "monitoring_config": monitoring_config,
                "real_time_analytics": True
            }
            
        except Exception as e:
            logger.error(f"Error in monitoring phase: {e}")
            return {"phase": "real_time_monitoring", "success": False, "error": str(e)}
    
    async def _generate_intelligent_recommendations(self, workflow_results: Dict[str, Any], user_request: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate intelligent recommendations using all analysis results"""
        try:
            # Extract insights from all phases
            all_insights = []
            
            for phase_name, phase_result in workflow_results.get("phases", {}).items():
                if phase_result.get("success"):
                    all_insights.append(f"✅ {phase_name}: Successfully completed")
                else:
                    all_insights.append(f"⚠️ {phase_name}: {phase_result.get('error', 'Unknown error')}")
            
            # AI-powered recommendation generation
            ai_recommendations = await self.ai_analyze(
                analysis_type="comprehensive_recommendations",
                data={
                    "workflow_results": workflow_results,
                    "all_insights": all_insights,
                    "user_request": user_request or {}
                },
                specific_instructions="""
                Generate comprehensive financial recommendations based on the complete cloud-powered analysis.
                
                Consider:
                1. Cloud-scale data processing results
                2. AI-enhanced market insights  
                3. Real-time monitoring capabilities
                4. Serverless execution efficiency
                5. Multi-service integration benefits
                
                Provide specific, actionable recommendations with implementation priorities.
                """,
                output_format="json"
            )
            
            # Structure recommendations
            recommendations = []
            if "error" not in ai_recommendations:
                ai_recs = ai_recommendations.get("recommendations", [])
                for i, rec in enumerate(ai_recs[:10]):  # Limit to top 10
                    recommendation = {
                        "id": f"cloud_rec_{i+1}",
                        "category": "cloud_enhanced_strategy",
                        "recommendation": rec if isinstance(rec, str) else rec.get("recommendation", str(rec)),
                        "priority": "high" if i < 3 else "medium",
                        "implementation": "cloud_native",
                        "ai_confidence": 0.9,
                        "cloud_services_utilized": workflow_results.get("google_cloud_services_used", [])
                    }
                    recommendations.append(recommendation)
            
            # Add system-specific recommendations
            system_recommendations = [
                {
                    "id": "cloud_monitoring",
                    "category": "system_optimization",
                    "recommendation": "Leverage real-time monitoring for continuous portfolio optimization",
                    "priority": "high",
                    "implementation": "automated",
                    "cloud_services_utilized": ["cloud_monitoring", "bigquery"]
                },
                {
                    "id": "serverless_scaling",
                    "category": "performance_enhancement", 
                    "recommendation": "Utilize serverless functions for scalable analysis during market volatility",
                    "priority": "medium",
                    "implementation": "on_demand",
                    "cloud_services_utilized": ["cloud_functions"]
                }
            ]
            
            recommendations.extend(system_recommendations)
            
            return {
                "phase": "intelligent_recommendations",
                "success": True,
                "recommendations": recommendations,
                "total_recommendations": len(recommendations),
                "ai_powered": True,
                "cloud_native": True
            }
            
        except Exception as e:
            logger.error(f"Error generating intelligent recommendations: {e}")
            return {"phase": "intelligent_recommendations", "success": False, "error": str(e)}
    
    async def _store_workflow_results(self, workflow_results: Dict[str, Any]):
        """Store workflow results in cloud storage for future reference"""
        try:
            workflow_id = workflow_results.get("workflow_id")
            
            # Store in Cloud Storage
            await self.cloud_manager.upload_file(
                f"workflows/{workflow_id}",
                f"{workflow_id}_results.json",
                json.dumps(workflow_results, indent=2)
            )
            
            # Store summary in Firestore
            summary = {
                "workflow_id": workflow_id,
                "timestamp": workflow_results.get("timestamp"),
                "status": workflow_results.get("status"),
                "execution_time": workflow_results.get("execution_time_seconds"),
                "services_used": workflow_results.get("google_cloud_services_used", []),
                "recommendations_count": len(workflow_results.get("final_recommendations", []))
            }
            
            await self.cloud_manager.store_financial_data(f"workflow_{workflow_id}", summary)
            
        except Exception as e:
            logger.error(f"Error storing workflow results: {e}")
    
    # === Enhanced System Status ===
    
    async def get_enhanced_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the enhanced system"""
        try:
            # Get base system status
            base_status = await super().get_system_status() if hasattr(super(), 'get_system_status') else {}
            
            # Get Google Cloud status
            cloud_status = await self.cloud_manager.get_comprehensive_status()
            
            # Get Vertex AI status
            vertex_status = await self.vertex_ai.get_service_status()
            
            # Get functions status
            functions_status = await self.functions_manager.get_functions_status()
            
            # Get scheduler status
            scheduler_status = await self.scheduler.get_scheduler_status()
            
            # Get authentication status
            auth_status = self.auth_manager.get_auth_status()
            
            enhanced_status = {
                "system_type": "enhanced_adk_multi_agent",
                "timestamp": datetime.utcnow().isoformat(),
                "overall_health": "healthy",
                "base_adk_system": base_status,
                "google_cloud_services": cloud_status,
                "vertex_ai_services": vertex_status,
                "cloud_functions": functions_status,
                "cloud_scheduler": scheduler_status,
                "authentication": auth_status,
                "enhanced_capabilities": await self._assess_system_capabilities(),
                "performance_metrics": {
                    "total_services": 8,
                    "active_services": len([s for s in cloud_status.get("services", {}).values() if s.get("status") == "healthy"]),
                    "cloud_functions_deployed": functions_status.get("total_functions", 0),
                    "scheduled_workflows": scheduler_status.get("total_jobs", 0)
                }
            }
            
            # Calculate overall health
            health_factors = []
            if cloud_status.get("overall_health") == "healthy":
                health_factors.append(1.0)
            elif cloud_status.get("overall_health") == "degraded":
                health_factors.append(0.7)
            else:
                health_factors.append(0.3)
            
            if vertex_status.get("vertex_ai_initialized"):
                health_factors.append(1.0)
            else:
                health_factors.append(0.5)
            
            if functions_status.get("success"):
                health_factors.append(1.0)
            else:
                health_factors.append(0.6)
            
            overall_health_score = sum(health_factors) / len(health_factors) if health_factors else 0
            
            if overall_health_score >= 0.9:
                enhanced_status["overall_health"] = "excellent"
            elif overall_health_score >= 0.7:
                enhanced_status["overall_health"] = "good"
            elif overall_health_score >= 0.5:
                enhanced_status["overall_health"] = "degraded"
            else:
                enhanced_status["overall_health"] = "poor"
            
            return enhanced_status
            
        except Exception as e:
            logger.error(f"Error getting enhanced system status: {e}")
            return {
                "system_type": "enhanced_adk_multi_agent",
                "overall_health": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Create enhanced global instance
enhanced_adk_orchestrator = EnhancedADKOrchestrator() 