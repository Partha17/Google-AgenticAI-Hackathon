"""
Main ADK Application - Financial Multi-Agent System
Entry point for the Google Cloud ADK-based financial intelligence system
Based on: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import centralized logging
from services.logger_config import setup_logging, get_adk_logger, log_startup, log_shutdown, log_error

# Setup centralized logging
setup_logging()
logger = get_adk_logger()

# Import ADK agents
try:
    from adk_agents import (
        adk_orchestrator,
        financial_data_collector_agent,
        risk_assessment_agent,
        market_analysis_agent,
        adk_config
    )
    logger.info("✅ ADK agents imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import ADK agents: {e}")
    raise

class FinancialAssistantAgent:
    """
    Main Financial Assistant Agent compatible with Google Cloud ADK
    This serves as the primary interface for the multi-agent system
    """
    
    def __init__(self):
        self.agent_name = "financial_assistant"
        self.orchestrator = adk_orchestrator
        self.system_initialized = False
        
        # Agent capabilities
        self.capabilities = [
            "comprehensive_financial_analysis",
            "risk_assessment", 
            "market_analysis",
            "opportunity_identification",
            "portfolio_optimization",
            "stress_testing",
            "system_monitoring"
        ]
        
        logger.info(f"🤖 Financial Assistant Agent initialized with {len(self.capabilities)} capabilities")
    
    async def initialize(self) -> bool:
        """Initialize the multi-agent system"""
        try:
            logger.info("🚀 Initializing Financial Multi-Agent System...")
            
            # Initialize the orchestrator and all sub-agents
            init_result = await self.orchestrator.initialize_system()
            
            if init_result.get("system_status") in ["ready", "partial"]:
                self.system_initialized = True
                ready_agents = init_result.get("ready_agents", 0)
                total_agents = init_result.get("total_agents", 0)
                
                logger.info(f"✅ System initialized successfully!")
                logger.info(f"📊 Agents ready: {ready_agents}/{total_agents}")
                
                if init_result.get("initialization_errors"):
                    logger.warning("⚠️ Some initialization warnings:")
                    for error in init_result["initialization_errors"]:
                        logger.warning(f"  - {error}")
                
                return True
            else:
                logger.error(f"❌ System initialization failed: {init_result.get('system_status')}")
                return False
                
        except Exception as e:
            logger.error(f"💥 Critical error during initialization: {e}")
            return False
    
    async def handle_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Main message handler for the financial assistant
        This is the primary interface that ADK will call
        """
        try:
            if not self.system_initialized:
                await self.initialize()
            
            logger.info(f"💬 Received message: {message[:100]}...")
            
            # Parse user intent
            intent = self._parse_user_intent(message)
            logger.info(f"🎯 Detected intent: {intent['action']}")
            
            # Route to appropriate handler
            if intent["action"] == "comprehensive_analysis":
                response = await self._handle_comprehensive_analysis(intent, context)
            elif intent["action"] == "risk_assessment":
                response = await self._handle_risk_assessment(intent, context)
            elif intent["action"] == "market_analysis":
                response = await self._handle_market_analysis(intent, context)
            elif intent["action"] == "opportunity_identification":
                response = await self._handle_opportunity_identification(intent, context)
            elif intent["action"] == "stress_testing":
                response = await self._handle_stress_testing(intent, context)
            elif intent["action"] == "system_status":
                response = await self._handle_system_status(intent, context)
            elif intent["action"] == "help":
                response = self._handle_help_request(intent, context)
            else:
                response = await self._handle_general_query(intent, context)
            
            logger.info("✅ Response generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error handling message: {e}")
            return self._format_error_response(str(e))
    
    def _parse_user_intent(self, message: str) -> Dict[str, Any]:
        """Parse user message to determine intent and extract parameters"""
        message_lower = message.lower()
        
        # Define intent patterns
        intent_patterns = {
            "comprehensive_analysis": [
                "comprehensive analysis", "full analysis", "complete analysis",
                "analyze everything", "analyze portfolio", "financial analysis"
            ],
            "risk_assessment": [
                "risk", "risk assessment", "risk analysis", "assess risk",
                "portfolio risk", "how risky", "risk level"
            ],
            "market_analysis": [
                "market", "market analysis", "market trends", "market conditions",
                "market outlook", "analyze market"
            ],
            "opportunity_identification": [
                "opportunities", "opportunity", "investment opportunities",
                "find opportunities", "what to invest", "investment ideas"
            ],
            "stress_testing": [
                "stress test", "stress testing", "scenario analysis",
                "what if", "market crash", "worst case"
            ],
            "system_status": [
                "status", "system status", "health", "how are you",
                "system health", "check system"
            ],
            "help": [
                "help", "what can you do", "capabilities", "commands",
                "how to use", "instructions"
            ]
        }
        
        # Match patterns
        for action, patterns in intent_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return {
                    "action": action,
                    "original_message": message,
                    "confidence": 0.8
                }
        
        # Default to general query
        return {
            "action": "general_query",
            "original_message": message,
            "confidence": 0.5
        }
    
    async def _handle_comprehensive_analysis(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle comprehensive financial analysis request"""
        try:
            logger.info("🔍 Starting comprehensive financial analysis...")
            
            # Execute comprehensive workflow
            analysis_result = await self.orchestrator.execute_comprehensive_analysis()
            
            if analysis_result.get("workflow_status") == "completed":
                return self._format_comprehensive_analysis_response(analysis_result)
            else:
                error_msg = analysis_result.get("error", "Analysis workflow failed")
                return f"I encountered an issue during the comprehensive analysis: {error_msg}. Please try again or check the system status."
                
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return f"I'm sorry, but I encountered an error during the comprehensive analysis: {str(e)}"
    
    async def _handle_risk_assessment(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle risk assessment request"""
        try:
            logger.info("⚖️ Starting risk assessment...")
            
            analysis_result = await self.orchestrator.execute_targeted_analysis("risk_assessment")
            
            if analysis_result.get("status") == "completed":
                return self._format_risk_assessment_response(analysis_result)
            else:
                error_msg = analysis_result.get("error", "Risk assessment failed")
                return f"I couldn't complete the risk assessment: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return f"I encountered an error during risk assessment: {str(e)}"
    
    async def _handle_market_analysis(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle market analysis request"""
        try:
            logger.info("📈 Starting market analysis...")
            
            analysis_result = await self.orchestrator.execute_targeted_analysis("market_analysis")
            
            if analysis_result.get("status") == "completed":
                return self._format_market_analysis_response(analysis_result)
            else:
                error_msg = analysis_result.get("error", "Market analysis failed")
                return f"I couldn't complete the market analysis: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return f"I encountered an error during market analysis: {str(e)}"
    
    async def _handle_opportunity_identification(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle opportunity identification request"""
        try:
            logger.info("💡 Identifying investment opportunities...")
            
            analysis_result = await self.orchestrator.execute_targeted_analysis("opportunity_identification")
            
            if analysis_result.get("status") == "completed":
                return self._format_opportunity_response(analysis_result)
            else:
                error_msg = analysis_result.get("error", "Opportunity identification failed")
                return f"I couldn't identify opportunities: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error in opportunity identification: {e}")
            return f"I encountered an error while identifying opportunities: {str(e)}"
    
    async def _handle_stress_testing(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle stress testing request"""
        try:
            logger.info("🧪 Starting stress testing...")
            
            analysis_result = await self.orchestrator.execute_targeted_analysis("stress_testing")
            
            if analysis_result.get("status") == "completed":
                return self._format_stress_test_response(analysis_result)
            else:
                error_msg = analysis_result.get("error", "Stress testing failed")
                return f"I couldn't complete the stress testing: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error in stress testing: {e}")
            return f"I encountered an error during stress testing: {str(e)}"
    
    async def _handle_system_status(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle system status request"""
        try:
            logger.info("📊 Checking system status...")
            
            status_result = await self.orchestrator.get_system_status()
            return self._format_system_status_response(status_result)
            
        except Exception as e:
            logger.error(f"Error checking system status: {e}")
            return f"I encountered an error while checking system status: {str(e)}"
    
    def _handle_help_request(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle help request"""
        help_text = """
🤖 **Financial Assistant Agent - Multi-Agent System**

I'm powered by a sophisticated multi-agent system that can help you with comprehensive financial analysis. Here's what I can do:

**📊 Core Capabilities:**
• **Comprehensive Analysis** - Complete financial health assessment
• **Risk Assessment** - Portfolio risk analysis and stress testing  
• **Market Analysis** - Market trends and technical analysis
• **Opportunity Identification** - Investment opportunities and recommendations
• **System Monitoring** - Real-time system health and performance

**💬 How to interact with me:**
• "Analyze my portfolio" - Get comprehensive financial analysis
• "What's my risk level?" - Get detailed risk assessment
• "Show me market trends" - Get market analysis and outlook
• "Find investment opportunities" - Get investment recommendations
• "Run stress test" - Analyze portfolio under stress scenarios
• "System status" - Check system health and performance

**🔧 Powered by:**
• Financial Data Collector Agent
• Risk Assessment Agent  
• Market Analysis Agent
• ADK Orchestrator Agent

**📈 Data Sources:**
• Real-time Fi MCP server data
• Bank transactions, net worth, EPF details
• Credit reports and mutual fund data

Ready to help with your financial intelligence needs! Just ask me anything about your financial situation.
        """
        return help_text.strip()
    
    async def _handle_general_query(self, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle general queries that don't match specific intents"""
        return """
I'm a specialized financial assistant powered by multiple AI agents. I can help you with:

• **Financial Analysis** - Comprehensive portfolio and financial health assessment
• **Risk Assessment** - Understanding and managing your investment risks
• **Market Analysis** - Current market conditions and trends
• **Investment Opportunities** - Finding and evaluating investment options

Please ask me something specific like:
- "Analyze my financial situation"
- "What's my risk level?"
- "Show me market opportunities"
- "Help" for more detailed instructions

What would you like to know about your finances?
        """
    
    # Response formatting methods
    
    def _format_comprehensive_analysis_response(self, analysis_result: Dict[str, Any]) -> str:
        """Format comprehensive analysis response"""
        try:
            execution_time = analysis_result.get("execution_time_seconds", 0)
            synthesis = analysis_result.get("synthesis", {})
            recommendations = analysis_result.get("recommendations", [])
            
            response = f"""
🎯 **Comprehensive Financial Analysis Complete** ⏱️ {execution_time:.1f}s

"""
            
            # Key findings
            key_findings = synthesis.get("key_findings", [])
            if key_findings:
                response += "📊 **Key Findings:**\n"
                for finding in key_findings[:3]:  # Top 3 findings
                    confidence = finding.get("confidence", 0)
                    response += f"• {finding.get('finding', 'N/A')} (Confidence: {confidence:.0%})\n"
                response += "\n"
            
            # Cross-agent insights
            cross_insights = synthesis.get("cross_agent_insights", [])
            if cross_insights:
                response += "🔍 **Key Insights:**\n"
                for insight in cross_insights[:2]:  # Top 2 insights
                    response += f"• {insight.get('insight', 'N/A')}\n"
                    response += f"  *Implication: {insight.get('implication', 'N/A')}*\n"
                response += "\n"
            
            # Top recommendations
            if recommendations:
                response += "📋 **Priority Recommendations:**\n"
                for rec in recommendations[:3]:  # Top 3 recommendations
                    priority = rec.get("priority", "medium")
                    category = rec.get("category", "general")
                    recommendation = rec.get("recommendation", "N/A")
                    timeframe = rec.get("timeframe", "N/A")
                    
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                    response += f"{priority_emoji} **{category.title()}** ({timeframe})\n"
                    response += f"   {recommendation}\n"
                response += "\n"
            
            # Overall confidence
            confidence_assessment = synthesis.get("confidence_assessment", {})
            overall_confidence = confidence_assessment.get("overall_confidence", 0.5)
            response += f"📈 **Analysis Confidence:** {overall_confidence:.0%}\n"
            
            response += "\n💡 *Ask me for specific details about any area: risk, market conditions, or opportunities.*"
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting comprehensive analysis response: {e}")
            return "✅ Comprehensive analysis completed, but I had trouble formatting the results. Please ask for specific details."
    
    def _format_risk_assessment_response(self, analysis_result: Dict[str, Any]) -> str:
        """Format risk assessment response"""
        try:
            results = analysis_result.get("results", {})
            risk_level = results.get("overall_risk_level", "unknown")
            risk_score = results.get("risk_score", 0)
            
            risk_emoji = {
                "low": "🟢",
                "medium": "🟡", 
                "high": "🔴"
            }.get(risk_level, "⚪")
            
            response = f"""
⚖️ **Portfolio Risk Assessment**

{risk_emoji} **Overall Risk Level:** {risk_level.title()} (Score: {risk_score:.2f})

"""
            
            # Key risks
            key_risks = results.get("key_risks", [])
            if key_risks:
                response += "🚨 **Key Risks Identified:**\n"
                for risk in key_risks[:3]:
                    category = risk.get("category", "Unknown")
                    risk_level = risk.get("level", "medium")
                    factors = risk.get("factors", [])
                    
                    response += f"• **{category.replace('_', ' ').title()}** ({risk_level})\n"
                    if factors:
                        response += f"  {factors[0]}\n"
                response += "\n"
            
            # Mitigation strategies
            mitigation_strategies = results.get("mitigation_strategies", [])
            if mitigation_strategies:
                response += "🛡️ **Recommended Actions:**\n"
                for strategy in mitigation_strategies[:2]:
                    strategy_name = strategy.get("strategy", "Risk Management")
                    timeline = strategy.get("timeline", "Medium-term")
                    priority = strategy.get("priority", "medium")
                    
                    response += f"• **{strategy_name}** ({timeline}, {priority} priority)\n"
                    actions = strategy.get("actions", [])
                    if actions:
                        response += f"  {actions[0]}\n"
                response += "\n"
            
            response += "💡 *Ask me about stress testing or specific risk mitigation strategies for more details.*"
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting risk assessment response: {e}")
            return "✅ Risk assessment completed, but I had trouble formatting the results."
    
    def _format_market_analysis_response(self, analysis_result: Dict[str, Any]) -> str:
        """Format market analysis response"""
        try:
            results = analysis_result.get("results", {})
            market_regime = results.get("market_regime", "neutral")
            trend_direction = results.get("trend_direction", "sideways")
            confidence_score = results.get("confidence_score", 0.5)
            
            regime_emoji = {
                "risk_on": "🚀",
                "risk_off": "🛡️",
                "neutral": "⚖️"
            }.get(market_regime, "📊")
            
            trend_emoji = {
                "up": "📈",
                "down": "📉", 
                "sideways": "↔️"
            }.get(trend_direction, "📊")
            
            response = f"""
📈 **Market Analysis**

{regime_emoji} **Market Regime:** {market_regime.replace('_', ' ').title()}
{trend_emoji} **Trend Direction:** {trend_direction.title()}
📊 **Confidence:** {confidence_score:.0%}

"""
            
            # Key insights
            key_insights = results.get("key_insights", [])
            if key_insights:
                response += "🔍 **Market Insights:**\n"
                for insight in key_insights[:3]:
                    title = insight.get("title", "Market Insight")
                    timeframe = insight.get("timeframe", "current")
                    confidence = insight.get("confidence", 0.5)
                    
                    response += f"• **{title}** ({timeframe})\n"
                    response += f"  Confidence: {confidence:.0%}\n"
                response += "\n"
            
            # Market outlook
            market_outlook = results.get("market_outlook", {})
            if market_outlook:
                short_term = market_outlook.get("short_term", {})
                if short_term:
                    outlook = short_term.get("outlook", "neutral")
                    timeframe = short_term.get("timeframe", "1-3 months")
                    
                    response += f"🔮 **Short-term Outlook ({timeframe}):** {outlook.title()}\n"
                
                # Key themes
                key_themes = market_outlook.get("key_themes", [])
                if key_themes:
                    response += f"📋 **Key Themes:** {', '.join(key_themes[:3])}\n"
                response += "\n"
            
            response += "💡 *Ask me about investment opportunities or specific market sectors for more details.*"
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting market analysis response: {e}")
            return "✅ Market analysis completed, but I had trouble formatting the results."
    
    def _format_opportunity_response(self, analysis_result: Dict[str, Any]) -> str:
        """Format opportunity identification response"""
        try:
            results = analysis_result.get("results", {})
            opportunities_count = results.get("opportunities_identified", 0)
            
            response = f"""
💡 **Investment Opportunities Identified: {opportunities_count}**

"""
            
            # Tactical opportunities
            tactical_opportunities = results.get("tactical_opportunities", [])
            if tactical_opportunities:
                response += "⚡ **Short-term Opportunities (6-12 months):**\n"
                for opp in tactical_opportunities[:2]:
                    opportunity = opp.get("opportunity", "Investment opportunity")
                    expected_return = opp.get("expected_return", "N/A")
                    
                    response += f"• {opportunity}\n"
                    response += f"  Expected return: {expected_return}\n"
                response += "\n"
            
            # Strategic opportunities
            strategic_opportunities = results.get("strategic_opportunities", [])
            if strategic_opportunities:
                response += "🎯 **Long-term Opportunities (2+ years):**\n"
                for opp in strategic_opportunities[:2]:
                    opportunity = opp.get("opportunity", "Investment opportunity")
                    expected_return = opp.get("expected_return", "N/A")
                    
                    response += f"• {opportunity}\n"
                    response += f"  Expected return: {expected_return}\n"
                response += "\n"
            
            # Investment themes
            investment_themes = results.get("investment_themes", [])
            if investment_themes:
                response += f"📈 **Key Investment Themes:** {', '.join(investment_themes[:4])}\n\n"
            
            # Risk-reward assessment
            risk_reward = results.get("risk_reward_assessment", {})
            if risk_reward:
                overall_risk = risk_reward.get("overall_risk_level", "medium")
                expected_return = risk_reward.get("expected_return_range", "N/A")
                
                response += f"⚖️ **Risk-Return Profile:** {overall_risk.title()} risk, {expected_return} expected returns\n\n"
            
            response += "💡 *Ask me for detailed analysis of any specific opportunity or investment theme.*"
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting opportunity response: {e}")
            return "✅ Opportunity identification completed, but I had trouble formatting the results."
    
    def _format_stress_test_response(self, analysis_result: Dict[str, Any]) -> str:
        """Format stress test response"""
        try:
            results = analysis_result.get("results", {})
            scenarios_tested = results.get("scenarios_tested", 0)
            worst_case_loss = results.get("worst_case_loss", 0)
            risk_tolerance = results.get("risk_tolerance_assessment", "unknown")
            
            response = f"""
🧪 **Portfolio Stress Test Results**

📊 **Scenarios Tested:** {scenarios_tested}
📉 **Worst Case Loss:** {worst_case_loss:,.0f} ({abs(worst_case_loss/1000000*100):.1f}% if portfolio is ₹10L)
⚖️ **Risk Tolerance:** {risk_tolerance.title()}

"""
            
            # Scenario results
            scenario_results = results.get("scenario_results", [])
            if scenario_results:
                response += "📋 **Scenario Analysis:**\n"
                for scenario in scenario_results[:3]:
                    name = scenario.get("scenario_name", "Unknown")
                    impact = scenario.get("portfolio_impact", 0)
                    probability = scenario.get("probability", 0)
                    
                    if impact < 0:
                        impact_emoji = "📉"
                        impact_text = f"Loss: ₹{abs(impact):,.0f}"
                    else:
                        impact_emoji = "📈"
                        impact_text = f"Gain: ₹{impact:,.0f}"
                    
                    response += f"{impact_emoji} **{name}** (Probability: {probability:.0%})\n"
                    response += f"   {impact_text}\n"
                response += "\n"
            
            # Risk tolerance guidance
            if risk_tolerance == "low":
                response += "🛡️ **Recommendation:** Consider more defensive positioning given stress test results.\n"
            elif risk_tolerance == "high":
                response += "🚀 **Recommendation:** Portfolio shows good resilience, can maintain current risk level.\n"
            else:
                response += "⚖️ **Recommendation:** Balanced approach recommended based on stress test results.\n"
            
            response += "\n💡 *Ask me about risk mitigation strategies or scenario-specific advice.*"
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting stress test response: {e}")
            return "✅ Stress testing completed, but I had trouble formatting the results."
    
    def _format_system_status_response(self, status_result: Dict[str, Any]) -> str:
        """Format system status response"""
        try:
            overall_status = status_result.get("overall_status", "unknown")
            agent_health = status_result.get("agent_health", {})
            alerts = status_result.get("alerts", [])
            
            status_emoji = {
                "healthy": "🟢",
                "partial": "🟡",
                "degraded": "🟠", 
                "error": "🔴"
            }.get(overall_status, "⚪")
            
            response = f"""
📊 **System Status Report**

{status_emoji} **Overall Status:** {overall_status.title()}

🤖 **Agent Status:**
"""
            
            for agent_name, health in agent_health.items():
                agent_status = health.get("status", "unknown")
                agent_emoji = {
                    "healthy": "✅",
                    "partial": "⚠️",
                    "error": "❌",
                    "unhealthy": "🚫"
                }.get(agent_status, "❓")
                
                friendly_name = agent_name.replace("_", " ").title()
                response += f"{agent_emoji} {friendly_name}: {agent_status.title()}\n"
            
            response += "\n"
            
            # Performance metrics
            performance_metrics = status_result.get("performance_metrics", {})
            data_collection = performance_metrics.get("data_collection", {})
            if data_collection and not data_collection.get("error"):
                total_records = data_collection.get("total_records", 0)
                response += f"📈 **Data Records:** {total_records:,} total collected\n"
            
            # Alerts
            if alerts:
                response += f"\n🚨 **Active Alerts ({len(alerts)}):**\n"
                for alert in alerts[:3]:  # Show top 3 alerts
                    response += f"• {alert}\n"
            else:
                response += "\n✅ **No active alerts**\n"
            
            response += "\n💡 *All systems operational and ready for financial analysis.*"
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting system status response: {e}")
            return "✅ System status checked, but I had trouble formatting the results."
    
    def _format_error_response(self, error_message: str) -> str:
        """Format error response"""
        return f"""
❌ **I encountered an error:**

{error_message}

🔧 **What you can try:**
• Check if the Fi MCP server is running (port 8080)
• Try asking for system status: "system status"
• Use a simpler request like "help"
• Contact support if the issue persists

💡 *I'm still learning and improving. Thank you for your patience!*
        """

# Global agent instance for ADK
financial_assistant = FinancialAssistantAgent()

# ADK compatibility functions
async def main():
    """Main function for ADK compatibility"""
    try:
        log_startup('ADK.System', 'Financial Assistant Agent starting')
        logger.info("🚀 Starting Financial Assistant Agent...")
        
        # Initialize the agent
        if await financial_assistant.initialize():
            logger.info("✅ Financial Assistant Agent ready!")
            log_startup('ADK.Agent', 'Financial Assistant Agent initialized successfully')
            
            # Keep the agent running
            while True:
                try:
                    # In a real ADK setup, this would be handled by the ADK framework
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    log_shutdown('ADK.Agent', 'Shutdown signal received')
                    logger.info("👋 Shutting down Financial Assistant Agent...")
                    break
        else:
            logger.error("❌ Failed to initialize Financial Assistant Agent")
            
    except Exception as e:
        logger.error(f"💥 Critical error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 