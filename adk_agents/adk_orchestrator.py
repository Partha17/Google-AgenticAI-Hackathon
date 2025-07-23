"""
ADK Orchestrator Agent - Multi-Agent System Coordinator with AI-Powered Synthesis
Master orchestrator for the financial multi-agent system using Google Cloud ADK and Gemini AI
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from adk_agents.agent_config import adk_config
from adk_agents.ai_analysis_base import AIAnalysisBase
from adk_agents.financial_data_collector import financial_data_collector_agent
from adk_agents.risk_assessment_agent import risk_assessment_agent
from adk_agents.market_analysis_agent import market_analysis_agent

logger = logging.getLogger(__name__)

class ADKOrchestrator(AIAnalysisBase):
    """
    Master Orchestrator Agent powered by Gemini AI for coordinating the financial multi-agent system
    """
    
    def __init__(self):
        self.agent_id = "orchestrator_agent"
        config = adk_config.get_agent_definitions()[self.agent_id]
        super().__init__(self.agent_id, config)
        self.active_agents = {}
        self.workflow_state = {}
        self.max_concurrent_agents = 5
        
        # Register available agents
        self.available_agents = {
            "financial_data_collector": financial_data_collector_agent,
            "risk_assessment_agent": risk_assessment_agent,
            "market_analysis_agent": market_analysis_agent
        }
        
    async def initialize_system(self) -> Dict[str, Any]:
        """Initialize the entire multi-agent system"""
        try:
            logger.info("Initializing ADK Multi-Agent Financial System...")
            
            initialization_results = {
                "orchestrator_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "system_status": "initializing",
                "agent_status": {},
                "initialization_errors": [],
                "ready_agents": 0,
                "system_health": "unknown"
            }
            
            # Initialize each agent
            for agent_name, agent_instance in self.available_agents.items():
                try:
                    logger.info(f"Initializing {agent_name}...")
                    
                    # Basic health check for each agent
                    agent_health = {
                        "agent_name": agent_name,
                        "status": "ready",
                        "timestamp": datetime.utcnow().isoformat(),
                        "capabilities": []
                    }
                    
                    # Check agent capabilities
                    if hasattr(agent_instance, 'ai_analyze'):
                        agent_health["capabilities"].append("ai_analysis")
                    if hasattr(agent_instance, 'agent_id'):
                        agent_health["capabilities"].append("adk_compliant")
                    
                    initialization_results["agent_status"][agent_name] = agent_health
                    initialization_results["ready_agents"] += 1
                    
                    logger.info(f"✅ {agent_name} initialized successfully")
                    
                except Exception as e:
                    error_msg = f"Failed to initialize {agent_name}: {str(e)}"
                    logger.error(error_msg)
                    initialization_results["initialization_errors"].append(error_msg)
                    initialization_results["agent_status"][agent_name] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            # Determine system health
            total_agents = len(self.available_agents)
            if initialization_results["ready_agents"] == total_agents:
                initialization_results["system_status"] = "ready"
                initialization_results["system_health"] = "excellent"
            elif initialization_results["ready_agents"] > total_agents / 2:
                initialization_results["system_status"] = "partial"
                initialization_results["system_health"] = "good"
            else:
                initialization_results["system_status"] = "degraded"
                initialization_results["system_health"] = "poor"
            
            logger.info(f"System initialization completed: {initialization_results['ready_agents']}/{total_agents} agents ready")
            return initialization_results
            
        except Exception as e:
            logger.error(f"Error initializing system: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "system_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def execute_comprehensive_analysis(self, user_request: Dict[str, Any] = None, phone_number: str = None) -> Dict[str, Any]:
        """
        Execute a comprehensive financial analysis using all agents with AI-powered synthesis
        """
        try:
            logger.info("🚀 Starting AI-powered comprehensive financial analysis workflow...")
            
            workflow_results = {
                "orchestrator_id": self.agent_id,
                "workflow_id": f"workflow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.utcnow().isoformat(),
                "workflow_status": "in_progress",
                "phases": {},
                "agent_outputs": {},
                "ai_synthesis": {},
                "final_recommendations": [],
                "execution_time_seconds": 0,
                "user_request": user_request or {}
            }
            
            start_time = datetime.utcnow()
            
            # Phase 1: Data Collection
            logger.info("📊 Phase 1: AI-Powered Financial Data Collection")
            data_collection_result = await self._execute_data_collection_phase(phone_number)
            workflow_results["phases"]["data_collection"] = data_collection_result
            workflow_results["agent_outputs"]["financial_data_collector"] = data_collection_result
            
            if not data_collection_result.get("success", False):
                workflow_results["workflow_status"] = "failed"
                workflow_results["error"] = "Data collection phase failed"
                return workflow_results
            
            # Phase 2: Parallel Analysis (Risk Assessment + Market Analysis)
            logger.info("🔍 Phase 2: Parallel AI-Powered Risk and Market Analysis")
            parallel_analysis_results = await self._execute_parallel_analysis_phase(data_collection_result)
            workflow_results["phases"]["parallel_analysis"] = parallel_analysis_results
            
            # Extract individual agent outputs
            workflow_results["agent_outputs"]["risk_assessment_agent"] = parallel_analysis_results.get("risk_analysis", {})
            workflow_results["agent_outputs"]["market_analysis_agent"] = parallel_analysis_results.get("market_analysis", {})
            
            # Phase 3: AI-Powered Cross-Agent Synthesis
            logger.info("🧠 Phase 3: AI-Powered Cross-Agent Synthesis and Insight Generation")
            synthesis_result = await self._execute_ai_synthesis_phase(workflow_results["agent_outputs"], user_request)
            workflow_results["phases"]["ai_synthesis"] = synthesis_result
            workflow_results["ai_synthesis"] = synthesis_result
            
            # Phase 4: AI-Generated Final Recommendations
            logger.info("📋 Phase 4: AI-Generated Strategic Recommendations")
            recommendations = await self._generate_ai_recommendations(workflow_results, user_request)
            workflow_results["final_recommendations"] = recommendations
            
            # Calculate execution time
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()
            workflow_results["execution_time_seconds"] = execution_time
            
            # Final status
            workflow_results["workflow_status"] = "completed"
            
            logger.info(f"✅ AI-powered comprehensive analysis completed in {execution_time:.1f} seconds")
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error in AI-powered comprehensive analysis workflow: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "workflow_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def execute_targeted_analysis(self, analysis_type: str, parameters: Dict[str, Any] = None, phone_number: str = None) -> Dict[str, Any]:
        """
        Execute a targeted analysis using specific agents with AI enhancement
        """
        try:
            logger.info(f"🎯 Starting AI-powered targeted analysis: {analysis_type}")
            
            analysis_results = {
                "orchestrator_id": self.agent_id,
                "analysis_type": analysis_type,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "in_progress",
                "results": {},
                "agents_used": [],
                "ai_enhancements": {}
            }
            
            # Route analysis to appropriate agents with AI enhancement
            if analysis_type == "risk_assessment":
                # AI-powered risk assessment workflow
                data_result = await financial_data_collector_agent.collect_all_financial_data(phone_number)
                if data_result.get("success"):
                    risk_result = await risk_assessment_agent.analyze_portfolio_risk(data_result)
                    analysis_results["results"] = risk_result
                    analysis_results["agents_used"] = ["financial_data_collector", "risk_assessment_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "market_analysis":
                # AI-powered market analysis workflow
                data_result = await financial_data_collector_agent.collect_all_financial_data(phone_number)
                if data_result.get("success"):
                    market_result = await market_analysis_agent.analyze_market_trends(data_result)
                    analysis_results["results"] = market_result
                    analysis_results["agents_used"] = ["financial_data_collector", "market_analysis_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "opportunity_identification":
                # AI-powered opportunity identification
                data_result = await financial_data_collector_agent.collect_all_financial_data(phone_number)
                if data_result.get("success"):
                    opportunity_result = await market_analysis_agent.identify_market_opportunities(data_result)
                    analysis_results["results"] = opportunity_result
                    analysis_results["agents_used"] = ["financial_data_collector", "market_analysis_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "stress_testing":
                # AI-powered stress testing
                data_result = await financial_data_collector_agent.collect_all_financial_data(phone_number)
                if data_result.get("success"):
                    scenarios = parameters.get("scenarios") if parameters else None
                    stress_result = await risk_assessment_agent.stress_test_portfolio(data_result, scenarios)
                    analysis_results["results"] = stress_result
                    analysis_results["agents_used"] = ["financial_data_collector", "risk_assessment_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "data_quality_assessment":
                # AI-powered data quality assessment
                data_result = await financial_data_collector_agent.collect_all_financial_data(phone_number)
                if data_result.get("success"):
                    quality_result = await financial_data_collector_agent.validate_data_quality(data_result)
                    analysis_results["results"] = quality_result
                    analysis_results["agents_used"] = ["financial_data_collector"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            else:
                analysis_results["status"] = "failed"
                analysis_results["error"] = f"Unknown analysis type: {analysis_type}"
            
            if analysis_results["status"] != "failed":
                analysis_results["status"] = "completed"
            
            logger.info(f"AI-powered targeted analysis '{analysis_type}' completed")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in AI-powered targeted analysis '{analysis_type}': {e}")
            return {
                "orchestrator_id": self.agent_id,
                "analysis_type": analysis_type,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_data_collection_phase(self, phone_number: str = None) -> Dict[str, Any]:
        """Execute AI-powered data collection phase"""
        try:
            logger.info("Executing AI-powered data collection phase...")
            
            # Use the AI-enhanced data collector
            collection_result = await financial_data_collector_agent.collect_all_financial_data(phone_number)
            
            return {
                "phase": "data_collection",
                "success": collection_result.get("success", False),
                "agent_used": "financial_data_collector",
                "collection_result": collection_result,
                "data_quality_score": collection_result.get("data_quality_score", 0.0),
                "ai_insights": collection_result.get("ai_insights", {})
            }
            
        except Exception as e:
            logger.error(f"Error in data collection phase: {e}")
            return {
                "phase": "data_collection",
                "success": False,
                "error": str(e)
            }
    
    async def _execute_parallel_analysis_phase(self, data_collection_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel AI-powered analysis using multiple agents"""
        try:
            logger.info("Executing parallel AI-powered analysis phase...")
            
            # Extract collected data
            collected_data = data_collection_result.get("collection_result", {})
            
            # Create AI-powered analysis tasks
            analysis_tasks = {
                "risk_analysis": risk_assessment_agent.analyze_portfolio_risk(collected_data),
                "market_analysis": market_analysis_agent.analyze_market_trends(collected_data)
            }
            
            # Execute tasks in parallel
            results = {}
            for task_name, task_coroutine in analysis_tasks.items():
                try:
                    result = await task_coroutine
                    results[task_name] = result
                    logger.info(f"Completed AI-powered {task_name}")
                except Exception as e:
                    logger.error(f"Error in AI-powered {task_name}: {e}")
                    results[task_name] = {"error": str(e)}
            
            return {
                "phase": "parallel_ai_analysis",
                "success": len(results) > 0,
                "completed_analyses": list(results.keys()),
                "analysis_method": "ai_powered",
                **results
            }
            
        except Exception as e:
            logger.error(f"Error in parallel AI analysis phase: {e}")
            return {
                "phase": "parallel_ai_analysis",
                "success": False,
                "error": str(e)
            }
    
    async def _execute_ai_synthesis_phase(self, agent_outputs: Dict[str, Any], user_request: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute AI-powered synthesis phase using Gemini for cross-agent analysis"""
        try:
            logger.info("Executing AI-powered cross-agent synthesis phase...")
            
            # Use AI synthesis from base class
            synthesis_focus = "comprehensive"
            if user_request:
                # Customize synthesis based on user request
                request_type = user_request.get("type", "")
                if "risk" in request_type.lower():
                    synthesis_focus = "risk_focused"
                elif "opportunity" in request_type.lower() or "investment" in request_type.lower():
                    synthesis_focus = "opportunity_focused"
                elif "performance" in request_type.lower():
                    synthesis_focus = "performance_focused"
            
            # Use the AI synthesis method from base class
            ai_synthesis_result = await self.ai_synthesize_insights(agent_outputs, synthesis_focus)
            
            # Enhance with orchestrator-specific analysis
            enhanced_synthesis = {
                "phase": "ai_powered_synthesis",
                "synthesis_method": "gemini_ai",
                "focus": synthesis_focus,
                "timestamp": datetime.utcnow().isoformat(),
                **ai_synthesis_result
            }
            
            # Add workflow coordination insights
            enhanced_synthesis["workflow_insights"] = await self._generate_workflow_insights(agent_outputs)
            
            return enhanced_synthesis
            
        except Exception as e:
            logger.error(f"Error in AI synthesis phase: {e}")
            return {
                "phase": "ai_powered_synthesis",
                "error": str(e),
                "fallback_synthesis": "AI synthesis failed, using basic aggregation"
            }
    
    async def _generate_ai_recommendations(self, workflow_results: Dict[str, Any], user_request: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate AI-powered final recommendations based on all analysis results"""
        try:
            logger.info("Generating AI-powered strategic recommendations...")
            
            specific_instructions = f"""
            Generate comprehensive strategic recommendations based on the complete multi-agent analysis:
            
            User Request Context: {json.dumps(user_request or {}, indent=2)}
            
            Analysis Framework:
            1. **Strategic Recommendations**:
               - Long-term financial strategy optimization
               - Portfolio positioning and allocation guidance
               - Risk management strategy recommendations
               - Growth and opportunity prioritization
               
            2. **Tactical Recommendations**:
               - Short-term action items with timelines
               - Immediate risk mitigation steps
               - Quick wins and optimization opportunities
               - Performance improvement tactics
               
            3. **Implementation Guidance**:
               - Step-by-step implementation plans
               - Resource requirements and constraints
               - Timeline and milestone definitions
               - Success metrics and monitoring
               
            4. **Risk Considerations**:
               - Implementation risks and mitigation
               - Market timing considerations
               - Regulatory and compliance factors
               - Contingency planning
               
            5. **Personalization**:
               - Tailor recommendations to user's specific situation
               - Consider risk tolerance and objectives
               - Account for constraints and preferences
               - Provide alternatives and options
            
            Provide specific, actionable recommendations with clear rationale,
            implementation timelines, and expected outcomes.
            """
            
            recommendations_data = {
                "workflow_results": workflow_results,
                "agent_outputs": workflow_results.get("agent_outputs", {}),
                "synthesis_results": workflow_results.get("ai_synthesis", {}),
                "user_context": user_request or {}
            }
            
            ai_recommendations = await self.ai_analyze(
                analysis_type="strategic_recommendations_generation",
                data=recommendations_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Structure recommendations properly
            if "error" not in ai_recommendations:
                recommendations = ai_recommendations.get("recommendations", [])
                if not isinstance(recommendations, list):
                    recommendations = ai_recommendations.get("strategic_recommendations", [])
                    if not isinstance(recommendations, list):
                        # Try to extract recommendations from the response
                        recommendations = []
                        for key, value in ai_recommendations.items():
                            if "recommendation" in key.lower() and isinstance(value, list):
                                recommendations.extend(value)
                                break
                
                # Ensure each recommendation has required fields
                structured_recommendations = []
                for i, rec in enumerate(recommendations):
                    if isinstance(rec, str):
                        rec = {"recommendation": rec, "priority": "medium", "category": "general"}
                    
                    structured_rec = {
                        "id": f"rec_{i+1}",
                        "category": rec.get("category", "financial_strategy"),
                        "recommendation": rec.get("recommendation", str(rec)),
                        "priority": rec.get("priority", "medium"),
                        "timeframe": rec.get("timeframe", "medium_term"),
                        "expected_impact": rec.get("expected_impact", "moderate"),
                        "implementation_steps": rec.get("implementation_steps", []),
                        "ai_confidence": rec.get("confidence", 0.8),
                        "source_analysis": rec.get("supporting_analysis", "multi_agent_synthesis")
                    }
                    structured_recommendations.append(structured_rec)
                
                return structured_recommendations
            
            return []
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
            return [{
                "category": "system_error",
                "recommendation": "AI recommendation generation failed. Please review agent outputs manually.",
                "priority": "high",
                "error": str(e)
            }]
    
    async def _generate_workflow_insights(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights about the workflow execution and agent coordination"""
        try:
            insights = {
                "workflow_efficiency": "high",
                "agent_coordination": "successful",
                "data_flow_analysis": {},
                "quality_assessment": {},
                "performance_metrics": {}
            }
            
            # Analyze data quality across agents
            data_quality_scores = []
            for agent_name, output in agent_outputs.items():
                if isinstance(output, dict):
                    if "data_quality_score" in output:
                        data_quality_scores.append(output["data_quality_score"])
                    elif "ai_analysis_metadata" in output:
                        confidence = output["ai_analysis_metadata"].get("confidence_indicators", {}).get("overall_confidence", 0.5)
                        data_quality_scores.append(confidence)
            
            if data_quality_scores:
                avg_quality = sum(data_quality_scores) / len(data_quality_scores)
                insights["quality_assessment"] = {
                    "average_quality_score": avg_quality,
                    "quality_distribution": data_quality_scores,
                    "quality_level": "high" if avg_quality > 0.8 else "medium" if avg_quality > 0.6 else "low"
                }
            
            # Analyze workflow performance
            successful_agents = len([output for output in agent_outputs.values() 
                                   if isinstance(output, dict) and not output.get("error")])
            total_agents = len(agent_outputs)
            
            insights["performance_metrics"] = {
                "successful_agents": successful_agents,
                "total_agents": total_agents,
                "success_rate": successful_agents / total_agents if total_agents > 0 else 0,
                "workflow_completion": "complete" if successful_agents == total_agents else "partial"
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating workflow insights: {e}")
            return {"error": str(e)}

# Create global instance
adk_orchestrator = ADKOrchestrator() 