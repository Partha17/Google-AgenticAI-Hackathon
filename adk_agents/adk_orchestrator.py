"""
ADK Orchestrator Agent - Multi-Agent System Coordinator
Master orchestrator for the financial multi-agent system using Google Cloud ADK
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from adk_agents.agent_config import adk_config
from adk_agents.financial_data_collector import financial_data_collector_agent
from adk_agents.risk_assessment_agent import risk_assessment_agent
from adk_agents.market_analysis_agent import market_analysis_agent

logger = logging.getLogger(__name__)

class ADKOrchestrator:
    """
    Master Orchestrator Agent for coordinating the financial multi-agent system
    Based on Google Cloud ADK framework patterns
    """
    
    def __init__(self):
        self.agent_id = "orchestrator_agent"
        self.config = adk_config.get_agent_definitions()[self.agent_id]
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
                "total_agents": len(self.available_agents)
            }
            
            # Initialize each agent
            for agent_name, agent_instance in self.available_agents.items():
                try:
                    logger.info(f"Initializing {agent_name}...")
                    
                    if hasattr(agent_instance, 'initialize'):
                        init_result = await agent_instance.initialize()
                        initialization_results["agent_status"][agent_name] = {
                            "status": "ready" if init_result else "failed",
                            "initialized": init_result
                        }
                        if init_result:
                            initialization_results["ready_agents"] += 1
                    else:
                        # Agent doesn't require initialization
                        initialization_results["agent_status"][agent_name] = {
                            "status": "ready",
                            "initialized": True
                        }
                        initialization_results["ready_agents"] += 1
                        
                except Exception as e:
                    error_msg = f"Failed to initialize {agent_name}: {str(e)}"
                    initialization_results["initialization_errors"].append(error_msg)
                    initialization_results["agent_status"][agent_name] = {
                        "status": "error",
                        "error": str(e)
                    }
                    logger.error(error_msg)
            
            # Determine overall system status
            if initialization_results["ready_agents"] == initialization_results["total_agents"]:
                initialization_results["system_status"] = "ready"
                logger.info("✅ All agents initialized successfully")
            elif initialization_results["ready_agents"] > 0:
                initialization_results["system_status"] = "partial"
                logger.warning(f"⚠️ {initialization_results['ready_agents']}/{initialization_results['total_agents']} agents ready")
            else:
                initialization_results["system_status"] = "failed"
                logger.error("❌ System initialization failed")
            
            return initialization_results
            
        except Exception as e:
            logger.error(f"Critical error during system initialization: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "system_status": "critical_error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def execute_comprehensive_analysis(self, user_request: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a comprehensive financial analysis using all agents
        This is the main orchestration workflow
        """
        try:
            logger.info("🚀 Starting comprehensive financial analysis workflow...")
            
            workflow_results = {
                "orchestrator_id": self.agent_id,
                "workflow_id": f"workflow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.utcnow().isoformat(),
                "workflow_status": "in_progress",
                "phases": {},
                "agent_outputs": {},
                "synthesis": {},
                "recommendations": [],
                "execution_time_seconds": 0
            }
            
            start_time = datetime.utcnow()
            
            # Phase 1: Data Collection
            logger.info("📊 Phase 1: Financial Data Collection")
            data_collection_result = await self._execute_data_collection_phase()
            workflow_results["phases"]["data_collection"] = data_collection_result
            workflow_results["agent_outputs"]["financial_data_collector"] = data_collection_result
            
            if not data_collection_result.get("success", False):
                workflow_results["workflow_status"] = "failed"
                workflow_results["error"] = "Data collection phase failed"
                return workflow_results
            
            # Phase 2: Parallel Analysis (Risk Assessment + Market Analysis)
            logger.info("🔍 Phase 2: Parallel Risk and Market Analysis")
            parallel_analysis_results = await self._execute_parallel_analysis_phase(data_collection_result)
            workflow_results["phases"]["parallel_analysis"] = parallel_analysis_results
            
            # Extract individual agent outputs
            workflow_results["agent_outputs"]["risk_assessment_agent"] = parallel_analysis_results.get("risk_analysis", {})
            workflow_results["agent_outputs"]["market_analysis_agent"] = parallel_analysis_results.get("market_analysis", {})
            
            # Phase 3: Synthesis and Insight Generation
            logger.info("💡 Phase 3: Synthesis and Insight Generation")
            synthesis_result = await self._execute_synthesis_phase(workflow_results["agent_outputs"])
            workflow_results["phases"]["synthesis"] = synthesis_result
            workflow_results["synthesis"] = synthesis_result
            
            # Phase 4: Generate Final Recommendations
            logger.info("📋 Phase 4: Final Recommendations")
            recommendations = await self._generate_final_recommendations(workflow_results)
            workflow_results["recommendations"] = recommendations
            
            # Calculate execution time
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()
            workflow_results["execution_time_seconds"] = execution_time
            
            # Final status
            workflow_results["workflow_status"] = "completed"
            
            logger.info(f"✅ Comprehensive analysis completed in {execution_time:.1f} seconds")
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis workflow: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "workflow_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def execute_targeted_analysis(self, analysis_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a targeted analysis using specific agents
        """
        try:
            logger.info(f"🎯 Starting targeted analysis: {analysis_type}")
            
            analysis_results = {
                "orchestrator_id": self.agent_id,
                "analysis_type": analysis_type,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "in_progress",
                "results": {},
                "agents_used": []
            }
            
            # Route analysis to appropriate agents
            if analysis_type == "risk_assessment":
                # First collect data, then analyze risk
                data_result = await financial_data_collector_agent.collect_all_financial_data()
                if data_result.get("success"):
                    risk_result = await risk_assessment_agent.analyze_portfolio_risk(data_result)
                    analysis_results["results"] = risk_result
                    analysis_results["agents_used"] = ["financial_data_collector", "risk_assessment_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "market_analysis":
                # First collect data, then analyze market
                data_result = await financial_data_collector_agent.collect_all_financial_data()
                if data_result.get("success"):
                    market_result = await market_analysis_agent.analyze_market_trends(data_result)
                    analysis_results["results"] = market_result
                    analysis_results["agents_used"] = ["financial_data_collector", "market_analysis_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "opportunity_identification":
                # Collect data and identify opportunities
                data_result = await financial_data_collector_agent.collect_all_financial_data()
                if data_result.get("success"):
                    opportunity_result = await market_analysis_agent.identify_market_opportunities(data_result)
                    analysis_results["results"] = opportunity_result
                    analysis_results["agents_used"] = ["financial_data_collector", "market_analysis_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            elif analysis_type == "stress_testing":
                # Collect data and perform stress testing
                data_result = await financial_data_collector_agent.collect_all_financial_data()
                if data_result.get("success"):
                    stress_result = await risk_assessment_agent.stress_test_portfolio(data_result, parameters.get("scenarios") if parameters else None)
                    analysis_results["results"] = stress_result
                    analysis_results["agents_used"] = ["financial_data_collector", "risk_assessment_agent"]
                else:
                    analysis_results["status"] = "failed"
                    analysis_results["error"] = "Data collection failed"
            
            else:
                analysis_results["status"] = "failed"
                analysis_results["error"] = f"Unknown analysis type: {analysis_type}"
            
            if analysis_results["status"] != "failed":
                analysis_results["status"] = "completed"
            
            logger.info(f"Targeted analysis '{analysis_type}' completed")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in targeted analysis '{analysis_type}': {e}")
            return {
                "orchestrator_id": self.agent_id,
                "analysis_type": analysis_type,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status and health metrics"""
        try:
            logger.info("📊 Checking system status...")
            
            status_report = {
                "orchestrator_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "overall_status": "healthy",
                "agent_health": {},
                "data_source_status": {},
                "performance_metrics": {},
                "recent_activity": [],
                "alerts": []
            }
            
            # Check individual agent health
            for agent_name, agent_instance in self.available_agents.items():
                try:
                    if hasattr(agent_instance, 'validate_data_sources'):
                        health_check = await agent_instance.validate_data_sources()
                        status_report["agent_health"][agent_name] = {
                            "status": health_check.get("overall_health", "unknown"),
                            "last_check": datetime.utcnow().isoformat(),
                            "details": health_check
                        }
                    else:
                        status_report["agent_health"][agent_name] = {
                            "status": "healthy",
                            "last_check": datetime.utcnow().isoformat(),
                            "note": "No health check method available"
                        }
                except Exception as e:
                    status_report["agent_health"][agent_name] = {
                        "status": "error",
                        "error": str(e),
                        "last_check": datetime.utcnow().isoformat()
                    }
            
            # Check data source status (using financial data collector)
            try:
                data_validation = await financial_data_collector_agent.validate_data_sources()
                status_report["data_source_status"] = data_validation
            except Exception as e:
                status_report["data_source_status"] = {"error": str(e)}
            
            # Get collection statistics
            try:
                collection_stats = await financial_data_collector_agent.get_collection_statistics()
                status_report["performance_metrics"]["data_collection"] = collection_stats
            except Exception as e:
                status_report["performance_metrics"]["data_collection"] = {"error": str(e)}
            
            # Determine overall status
            agent_statuses = [agent["status"] for agent in status_report["agent_health"].values()]
            if "error" in agent_statuses:
                status_report["overall_status"] = "degraded"
            elif "unhealthy" in agent_statuses:
                status_report["overall_status"] = "partial"
            else:
                status_report["overall_status"] = "healthy"
            
            # Generate alerts for issues
            alerts = []
            for agent_name, health in status_report["agent_health"].items():
                if health["status"] in ["error", "unhealthy"]:
                    alerts.append(f"Agent '{agent_name}' is {health['status']}")
            
            data_source_health = status_report["data_source_status"].get("overall_health", "unknown")
            if data_source_health in ["unhealthy", "error"]:
                alerts.append(f"Data sources are {data_source_health}")
            
            status_report["alerts"] = alerts
            
            logger.info(f"System status check completed - Overall: {status_report['overall_status']}")
            return status_report
            
        except Exception as e:
            logger.error(f"Error checking system status: {e}")
            return {
                "orchestrator_id": self.agent_id,
                "overall_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_data_collection_phase(self) -> Dict[str, Any]:
        """Execute the data collection phase"""
        try:
            logger.info("Executing data collection phase...")
            
            # Validate data sources first
            validation_result = await financial_data_collector_agent.validate_data_sources()
            
            if validation_result.get("overall_health") not in ["healthy", "partial"]:
                return {
                    "phase": "data_collection",
                    "success": False,
                    "error": "Data sources are unhealthy",
                    "validation_result": validation_result
                }
            
            # Collect comprehensive financial data
            collection_result = await financial_data_collector_agent.collect_all_financial_data()
            
            return {
                "phase": "data_collection",
                "success": collection_result.get("success", False),
                "validation_result": validation_result,
                "collection_result": collection_result,
                "data_quality_score": collection_result.get("data_quality_score", 0.0),
                "total_records": collection_result.get("total_records", 0)
            }
            
        except Exception as e:
            logger.error(f"Error in data collection phase: {e}")
            return {
                "phase": "data_collection",
                "success": False,
                "error": str(e)
            }
    
    async def _execute_parallel_analysis_phase(self, data_collection_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel analysis using multiple agents"""
        try:
            logger.info("Executing parallel analysis phase...")
            
            # Extract collected data
            collected_data = data_collection_result.get("collection_result", {})
            
            # Create analysis tasks
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
                    logger.info(f"Completed {task_name}")
                except Exception as e:
                    logger.error(f"Error in {task_name}: {e}")
                    results[task_name] = {"error": str(e)}
            
            return {
                "phase": "parallel_analysis",
                "success": len(results) > 0,
                "completed_analyses": list(results.keys()),
                **results
            }
            
        except Exception as e:
            logger.error(f"Error in parallel analysis phase: {e}")
            return {
                "phase": "parallel_analysis",
                "success": False,
                "error": str(e)
            }
    
    async def _execute_synthesis_phase(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize outputs from all agents into coherent insights"""
        try:
            logger.info("Executing synthesis phase...")
            
            synthesis = {
                "phase": "synthesis",
                "timestamp": datetime.utcnow().isoformat(),
                "synthesis_quality": "high",
                "key_findings": [],
                "cross_agent_insights": [],
                "confidence_assessment": {},
                "integrated_recommendations": []
            }
            
            # Extract key findings from each agent
            data_collector_output = agent_outputs.get("financial_data_collector", {})
            risk_output = agent_outputs.get("risk_assessment_agent", {})
            market_output = agent_outputs.get("market_analysis_agent", {})
            
            # Data quality findings
            if data_collector_output.get("success"):
                data_quality = data_collector_output.get("data_quality_score", 0)
                synthesis["key_findings"].append({
                    "category": "data_quality",
                    "finding": f"Data collection successful with {data_quality:.1%} quality score",
                    "confidence": 0.9,
                    "source_agent": "financial_data_collector"
                })
            
            # Risk findings
            if "overall_risk_level" in risk_output:
                risk_level = risk_output.get("overall_risk_level", "unknown")
                risk_score = risk_output.get("risk_score", 0)
                synthesis["key_findings"].append({
                    "category": "risk_assessment",
                    "finding": f"Portfolio risk level: {risk_level} (score: {risk_score:.2f})",
                    "confidence": 0.8,
                    "source_agent": "risk_assessment_agent"
                })
            
            # Market findings
            if "market_regime" in market_output:
                market_regime = market_output.get("market_regime", "unknown")
                trend_direction = market_output.get("trend_direction", "unknown")
                synthesis["key_findings"].append({
                    "category": "market_analysis",
                    "finding": f"Market regime: {market_regime}, trend: {trend_direction}",
                    "confidence": market_output.get("confidence_score", 0.5),
                    "source_agent": "market_analysis_agent"
                })
            
            # Generate cross-agent insights
            synthesis["cross_agent_insights"] = self._generate_cross_agent_insights(agent_outputs)
            
            # Assess confidence
            synthesis["confidence_assessment"] = self._assess_synthesis_confidence(agent_outputs)
            
            # Generate integrated recommendations
            synthesis["integrated_recommendations"] = self._generate_integrated_recommendations(agent_outputs)
            
            return synthesis
            
        except Exception as e:
            logger.error(f"Error in synthesis phase: {e}")
            return {
                "phase": "synthesis",
                "error": str(e)
            }
    
    def _generate_cross_agent_insights(self, agent_outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights that span multiple agents"""
        cross_insights = []
        
        try:
            risk_output = agent_outputs.get("risk_assessment_agent", {})
            market_output = agent_outputs.get("market_analysis_agent", {})
            
            # Risk-Market correlation insight
            risk_level = risk_output.get("overall_risk_level", "")
            market_regime = market_output.get("market_regime", "")
            
            if risk_level and market_regime:
                if risk_level == "high" and market_regime == "risk_off":
                    cross_insights.append({
                        "insight": "High portfolio risk aligns with risk-off market environment",
                        "implication": "Consider defensive positioning until market sentiment improves",
                        "confidence": 0.8,
                        "agents_involved": ["risk_assessment_agent", "market_analysis_agent"]
                    })
                elif risk_level == "low" and market_regime == "risk_on":
                    cross_insights.append({
                        "insight": "Low portfolio risk in risk-on market presents opportunity",
                        "implication": "Consider increasing risk exposure to capture market upside",
                        "confidence": 0.7,
                        "agents_involved": ["risk_assessment_agent", "market_analysis_agent"]
                    })
            
            # Data quality vs analysis reliability
            data_output = agent_outputs.get("financial_data_collector", {})
            data_quality = data_output.get("data_quality_score", 0)
            
            if data_quality < 0.7:
                cross_insights.append({
                    "insight": "Lower data quality may affect analysis reliability",
                    "implication": "Treat recommendations with additional caution and seek data validation",
                    "confidence": 0.9,
                    "agents_involved": ["financial_data_collector", "risk_assessment_agent", "market_analysis_agent"]
                })
        
        except Exception as e:
            logger.error(f"Error generating cross-agent insights: {e}")
        
        return cross_insights
    
    def _assess_synthesis_confidence(self, agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the confidence level of the overall synthesis"""
        try:
            confidence_factors = {
                "data_quality": 0.5,
                "agent_consensus": 0.5,
                "completeness": 0.5,
                "overall_confidence": 0.5
            }
            
            # Data quality factor
            data_output = agent_outputs.get("financial_data_collector", {})
            data_quality = data_output.get("data_quality_score", 0)
            confidence_factors["data_quality"] = data_quality
            
            # Agent consensus factor (simplified)
            successful_agents = sum(1 for output in agent_outputs.values() if not output.get("error"))
            total_agents = len(agent_outputs)
            confidence_factors["agent_consensus"] = successful_agents / total_agents if total_agents > 0 else 0
            
            # Completeness factor
            required_outputs = ["financial_data_collector", "risk_assessment_agent", "market_analysis_agent"]
            present_outputs = sum(1 for output in required_outputs if output in agent_outputs)
            confidence_factors["completeness"] = present_outputs / len(required_outputs)
            
            # Overall confidence (weighted average)
            weights = {"data_quality": 0.4, "agent_consensus": 0.3, "completeness": 0.3}
            overall_confidence = sum(confidence_factors[factor] * weights[factor] for factor in weights)
            confidence_factors["overall_confidence"] = overall_confidence
            
            return confidence_factors
            
        except Exception as e:
            logger.error(f"Error assessing synthesis confidence: {e}")
            return {"overall_confidence": 0.3, "error": str(e)}
    
    def _generate_integrated_recommendations(self, agent_outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate integrated recommendations from all agent outputs"""
        integrated_recommendations = []
        
        try:
            risk_output = agent_outputs.get("risk_assessment_agent", {})
            market_output = agent_outputs.get("market_analysis_agent", {})
            data_output = agent_outputs.get("financial_data_collector", {})
            
            # Risk-based recommendations
            if "key_risks" in risk_output:
                key_risks = risk_output.get("key_risks", [])
                for risk in key_risks[:3]:  # Top 3 risks
                    integrated_recommendations.append({
                        "category": "risk_management",
                        "priority": "high" if risk.get("level") == "high" else "medium",
                        "recommendation": f"Address {risk.get('category', 'risk')} identified by risk analysis",
                        "rationale": f"Risk score: {risk.get('score', 0):.2f}",
                        "timeframe": "1-3 months",
                        "source_agents": ["risk_assessment_agent"]
                    })
            
            # Market-based recommendations
            if "key_insights" in market_output:
                market_insights = market_output.get("key_insights", [])
                for insight in market_insights[:2]:  # Top 2 insights
                    if insight.get("actionable", False):
                        integrated_recommendations.append({
                            "category": "market_positioning",
                            "priority": "medium",
                            "recommendation": f"Consider {insight.get('category', 'market')} opportunity",
                            "rationale": insight.get("description", ""),
                            "timeframe": insight.get("timeframe", "medium_term"),
                            "source_agents": ["market_analysis_agent"]
                        })
            
            # Data quality recommendations
            data_quality = data_output.get("data_quality_score", 0)
            if data_quality < 0.8:
                integrated_recommendations.append({
                    "category": "data_improvement",
                    "priority": "medium",
                    "recommendation": "Improve data collection and validation processes",
                    "rationale": f"Current data quality score: {data_quality:.1%}",
                    "timeframe": "1-2 months",
                    "source_agents": ["financial_data_collector"]
                })
            
            # Cross-agent recommendations
            risk_level = risk_output.get("overall_risk_level", "")
            market_regime = market_output.get("market_regime", "")
            
            if risk_level == "high" or market_regime == "risk_off":
                integrated_recommendations.append({
                    "category": "defensive_strategy",
                    "priority": "high",
                    "recommendation": "Implement defensive portfolio strategy",
                    "rationale": f"High risk environment (Risk: {risk_level}, Market: {market_regime})",
                    "timeframe": "immediate",
                    "source_agents": ["risk_assessment_agent", "market_analysis_agent"]
                })
            
            # Sort by priority
            priority_order = {"high": 3, "medium": 2, "low": 1}
            integrated_recommendations.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 0), reverse=True)
            
        except Exception as e:
            logger.error(f"Error generating integrated recommendations: {e}")
        
        return integrated_recommendations
    
    async def _generate_final_recommendations(self, workflow_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate final actionable recommendations"""
        try:
            final_recommendations = []
            
            # Get integrated recommendations from synthesis
            synthesis = workflow_results.get("synthesis", {})
            integrated_recs = synthesis.get("integrated_recommendations", [])
            
            # Add orchestrator-level recommendations
            orchestrator_recs = []
            
            # System performance recommendation
            execution_time = workflow_results.get("execution_time_seconds", 0)
            if execution_time > 60:
                orchestrator_recs.append({
                    "category": "system_optimization",
                    "priority": "low",
                    "recommendation": "Optimize system performance to reduce analysis time",
                    "rationale": f"Current analysis takes {execution_time:.1f} seconds",
                    "timeframe": "next_sprint",
                    "source": "orchestrator"
                })
            
            # Workflow completeness recommendation
            completed_phases = len([p for p in workflow_results.get("phases", {}).values() if p.get("success", False)])
            total_phases = len(workflow_results.get("phases", {}))
            
            if completed_phases < total_phases:
                orchestrator_recs.append({
                    "category": "workflow_improvement",
                    "priority": "medium",
                    "recommendation": "Investigate and resolve workflow phase failures",
                    "rationale": f"Only {completed_phases}/{total_phases} phases completed successfully",
                    "timeframe": "immediate",
                    "source": "orchestrator"
                })
            
            # Combine all recommendations
            final_recommendations = integrated_recs + orchestrator_recs
            
            # Ensure we have at least some recommendations
            if not final_recommendations:
                final_recommendations.append({
                    "category": "general",
                    "priority": "low",
                    "recommendation": "Continue monitoring portfolio and market conditions",
                    "rationale": "Regular monitoring is essential for financial health",
                    "timeframe": "ongoing",
                    "source": "orchestrator"
                })
            
            return final_recommendations[:10]  # Limit to top 10 recommendations
            
        except Exception as e:
            logger.error(f"Error generating final recommendations: {e}")
            return [{
                "category": "error",
                "priority": "high",
                "recommendation": "Investigate system errors in recommendation generation",
                "rationale": str(e),
                "timeframe": "immediate",
                "source": "orchestrator"
            }]

# Global orchestrator instance
adk_orchestrator = ADKOrchestrator() 