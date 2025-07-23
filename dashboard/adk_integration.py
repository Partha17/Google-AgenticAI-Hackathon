"""
Dashboard Integration with ADK Multi-Agent System
Provides seamless integration between Streamlit dashboard and ADK agents
"""

import asyncio
import logging
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Import ADK agents
try:
    from adk_agents import adk_orchestrator
    from main_adk import financial_assistant
    ADK_AVAILABLE = True
except ImportError as e:
    logging.warning(f"ADK agents not available: {e}")
    ADK_AVAILABLE = False

logger = logging.getLogger(__name__)

class ADKDashboardIntegration:
    """Integration layer between Streamlit dashboard and ADK multi-agent system"""
    
    def __init__(self):
        self.adk_available = ADK_AVAILABLE
        self.financial_assistant = financial_assistant if ADK_AVAILABLE else None
        self.orchestrator = adk_orchestrator if ADK_AVAILABLE else None
        self.initialized = False
        
    async def initialize_adk_system(self) -> bool:
        """Initialize the ADK multi-agent system"""
        if not self.adk_available:
            return False
        
        try:
            if not self.initialized:
                success = await self.financial_assistant.initialize()
                self.initialized = success
                return success
            return True
        except Exception as e:
            logger.error(f"Failed to initialize ADK system: {e}")
            return False
    
    def is_adk_available(self) -> bool:
        """Check if ADK system is available and initialized"""
        return self.adk_available and self.initialized
    
    async def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """Get comprehensive financial analysis from ADK system"""
        if not self.adk_available:
            return {"error": "ADK system not available"}
        
        try:
            if not self.initialized:
                await self.initialize_adk_system()
            
            # Execute comprehensive analysis through orchestrator
            result = await self.orchestrator.execute_comprehensive_analysis()
            return self._process_analysis_result(result)
            
        except Exception as e:
            logger.error(f"Error getting comprehensive analysis: {e}")
            return {"error": str(e)}
    
    async def get_risk_assessment(self) -> Dict[str, Any]:
        """Get risk assessment from ADK system"""
        if not self.adk_available:
            return {"error": "ADK system not available"}
        
        try:
            result = await self.orchestrator.execute_targeted_analysis("risk_assessment")
            return self._process_risk_result(result)
            
        except Exception as e:
            logger.error(f"Error getting risk assessment: {e}")
            return {"error": str(e)}
    
    async def get_market_analysis(self) -> Dict[str, Any]:
        """Get market analysis from ADK system"""
        if not self.adk_available:
            return {"error": "ADK system not available"}
        
        try:
            result = await self.orchestrator.execute_targeted_analysis("market_analysis")
            return self._process_market_result(result)
            
        except Exception as e:
            logger.error(f"Error getting market analysis: {e}")
            return {"error": str(e)}
    
    async def get_opportunities(self) -> Dict[str, Any]:
        """Get investment opportunities from ADK system"""
        if not self.adk_available:
            return {"error": "ADK system not available"}
        
        try:
            result = await self.orchestrator.execute_targeted_analysis("opportunity_identification")
            return self._process_opportunity_result(result)
            
        except Exception as e:
            logger.error(f"Error getting opportunities: {e}")
            return {"error": str(e)}
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get ADK system status"""
        if not self.adk_available:
            return {"error": "ADK system not available"}
        
        try:
            result = await self.orchestrator.get_system_status()
            return result
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    async def chat_with_assistant(self, message: str) -> str:
        """Chat with the financial assistant"""
        if not self.adk_available:
            return "ADK multi-agent system is not available. Please check the installation."
        
        try:
            if not self.initialized:
                await self.initialize_adk_system()
            
            response = await self.financial_assistant.handle_message(message)
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"I encountered an error: {str(e)}. Please try again."
    
    def _process_analysis_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process comprehensive analysis result for dashboard display"""
        processed = {
            "status": result.get("workflow_status", "unknown"),
            "execution_time": result.get("execution_time_seconds", 0),
            "data_quality": 0.0,
            "key_findings": [],
            "recommendations": [],
            "confidence": 0.5,
            "risk_level": "unknown",
            "market_regime": "unknown"
        }
        
        try:
            # Extract synthesis information
            synthesis = result.get("synthesis", {})
            processed["key_findings"] = synthesis.get("key_findings", [])
            processed["recommendations"] = result.get("recommendations", [])
            
            confidence_assessment = synthesis.get("confidence_assessment", {})
            processed["confidence"] = confidence_assessment.get("overall_confidence", 0.5)
            
            # Extract agent outputs
            agent_outputs = result.get("agent_outputs", {})
            
            # Data quality from collector
            data_collector_output = agent_outputs.get("financial_data_collector", {})
            processed["data_quality"] = data_collector_output.get("data_quality_score", 0.0)
            
            # Risk level from risk agent
            risk_output = agent_outputs.get("risk_assessment_agent", {})
            processed["risk_level"] = risk_output.get("overall_risk_level", "unknown")
            
            # Market regime from market agent
            market_output = agent_outputs.get("market_analysis_agent", {})
            processed["market_regime"] = market_output.get("market_regime", "unknown")
            
        except Exception as e:
            logger.error(f"Error processing analysis result: {e}")
        
        return processed
    
    def _process_risk_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process risk assessment result for dashboard display"""
        risk_data = result.get("results", {})
        
        return {
            "risk_level": risk_data.get("overall_risk_level", "unknown"),
            "risk_score": risk_data.get("risk_score", 0.0),
            "key_risks": risk_data.get("key_risks", []),
            "mitigation_strategies": risk_data.get("mitigation_strategies", []),
            "risk_categories": risk_data.get("risk_categories", {})
        }
    
    def _process_market_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process market analysis result for dashboard display"""
        market_data = result.get("results", {})
        
        return {
            "market_regime": market_data.get("market_regime", "unknown"),
            "trend_direction": market_data.get("trend_direction", "sideways"),
            "confidence_score": market_data.get("confidence_score", 0.5),
            "key_insights": market_data.get("key_insights", []),
            "market_outlook": market_data.get("market_outlook", {}),
            "technical_indicators": market_data.get("technical_indicators", {})
        }
    
    def _process_opportunity_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process opportunity identification result for dashboard display"""
        opp_data = result.get("results", {})
        
        return {
            "opportunities_count": opp_data.get("opportunities_identified", 0),
            "tactical_opportunities": opp_data.get("tactical_opportunities", []),
            "strategic_opportunities": opp_data.get("strategic_opportunities", []),
            "investment_themes": opp_data.get("investment_themes", []),
            "risk_reward_assessment": opp_data.get("risk_reward_assessment", {})
        }

# Global integration instance
adk_integration = ADKDashboardIntegration()

# Streamlit helper functions for ADK integration

def display_adk_status():
    """Display ADK system status in sidebar"""
    with st.sidebar:
        st.subheader("🤖 ADK Multi-Agent System")
        
        if adk_integration.is_adk_available():
            st.success("✅ ADK System Active")
            
            # Show system status
            if st.button("🔍 Check System Status"):
                with st.spinner("Checking system status..."):
                    status = asyncio.run(adk_integration.get_system_status())
                    
                    if "error" not in status:
                        overall_status = status.get("overall_status", "unknown")
                        if overall_status == "healthy":
                            st.success(f"System Status: {overall_status.title()}")
                        elif overall_status in ["partial", "degraded"]:
                            st.warning(f"System Status: {overall_status.title()}")
                        else:
                            st.error(f"System Status: {overall_status.title()}")
                        
                        # Show agent health
                        agent_health = status.get("agent_health", {})
                        for agent, health in agent_health.items():
                            agent_name = agent.replace("_", " ").title()
                            health_status = health.get("status", "unknown")
                            
                            if health_status == "healthy":
                                st.success(f"✅ {agent_name}")
                            elif health_status in ["partial", "degraded"]:
                                st.warning(f"⚠️ {agent_name}")
                            else:
                                st.error(f"❌ {agent_name}")
                    else:
                        st.error(f"Status Check Failed: {status.get('error')}")
            
        else:
            st.warning("⚠️ ADK System Unavailable")
            st.caption("Using legacy single-agent system")

def create_adk_chat_interface():
    """Create chat interface for ADK financial assistant"""
    st.subheader("💬 Chat with Financial Assistant")
    st.caption("Powered by ADK Multi-Agent System")
    
    if not adk_integration.is_adk_available():
        st.error("ADK multi-agent system is not available. Please check the installation.")
        return
    
    # Initialize chat history
    if "adk_chat_history" not in st.session_state:
        st.session_state.adk_chat_history = []
    
    # Display chat history
    for message in st.session_state.adk_chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your finances..."):
        # Add user message to history
        st.session_state.adk_chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing with multi-agent system..."):
                response = asyncio.run(adk_integration.chat_with_assistant(prompt))
                st.write(response)
                
                # Add assistant response to history
                st.session_state.adk_chat_history.append({"role": "assistant", "content": response})

def create_adk_analysis_dashboard():
    """Create analysis dashboard using ADK system"""
    st.subheader("📊 ADK Multi-Agent Analysis Dashboard")
    
    if not adk_integration.is_adk_available():
        st.error("ADK multi-agent system is not available.")
        return
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type:",
        ["Comprehensive Analysis", "Risk Assessment", "Market Analysis", "Investment Opportunities"]
    )
    
    if st.button(f"🚀 Run {analysis_type}"):
        with st.spinner(f"Running {analysis_type.lower()} with multi-agent system..."):
            try:
                if analysis_type == "Comprehensive Analysis":
                    result = asyncio.run(adk_integration.get_comprehensive_analysis())
                    display_comprehensive_analysis(result)
                    
                elif analysis_type == "Risk Assessment":
                    result = asyncio.run(adk_integration.get_risk_assessment())
                    display_risk_assessment(result)
                    
                elif analysis_type == "Market Analysis":
                    result = asyncio.run(adk_integration.get_market_analysis())
                    display_market_analysis(result)
                    
                elif analysis_type == "Investment Opportunities":
                    result = asyncio.run(adk_integration.get_opportunities())
                    display_opportunities(result)
                    
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

def display_comprehensive_analysis(result: Dict[str, Any]):
    """Display comprehensive analysis results"""
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Analysis Status", result.get("status", "Unknown"))
    
    with col2:
        execution_time = result.get("execution_time", 0)
        st.metric("Execution Time", f"{execution_time:.1f}s")
    
    with col3:
        data_quality = result.get("data_quality", 0)
        st.metric("Data Quality", f"{data_quality:.1%}")
    
    with col4:
        confidence = result.get("confidence", 0)
        st.metric("Confidence", f"{confidence:.1%}")
    
    # Key findings
    key_findings = result.get("key_findings", [])
    if key_findings:
        st.subheader("🔍 Key Findings")
        for finding in key_findings:
            category = finding.get("category", "General")
            finding_text = finding.get("finding", "N/A")
            confidence = finding.get("confidence", 0)
            
            st.write(f"**{category.title()}:** {finding_text} (Confidence: {confidence:.0%})")
    
    # Recommendations
    recommendations = result.get("recommendations", [])
    if recommendations:
        st.subheader("📋 Recommendations")
        for rec in recommendations[:5]:
            priority = rec.get("priority", "medium")
            category = rec.get("category", "general")
            recommendation = rec.get("recommendation", "N/A")
            timeframe = rec.get("timeframe", "N/A")
            
            priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
            st.write(f"{priority_color} **{category.title()}** ({timeframe}): {recommendation}")

def display_risk_assessment(result: Dict[str, Any]):
    """Display risk assessment results"""
    if "error" in result:
        st.error(f"Risk assessment failed: {result['error']}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_level = result.get("risk_level", "unknown")
        risk_color = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk_level, "⚪")
        st.metric("Risk Level", f"{risk_color} {risk_level.title()}")
    
    with col2:
        risk_score = result.get("risk_score", 0)
        st.metric("Risk Score", f"{risk_score:.2f}")
    
    # Key risks
    key_risks = result.get("key_risks", [])
    if key_risks:
        st.subheader("🚨 Key Risks")
        for risk in key_risks:
            category = risk.get("category", "Unknown")
            level = risk.get("level", "medium")
            score = risk.get("score", 0)
            st.write(f"**{category.replace('_', ' ').title()}:** {level} risk (Score: {score:.2f})")

def display_market_analysis(result: Dict[str, Any]):
    """Display market analysis results"""
    if "error" in result:
        st.error(f"Market analysis failed: {result['error']}")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        market_regime = result.get("market_regime", "neutral")
        regime_emoji = {"risk_on": "🚀", "risk_off": "🛡️", "neutral": "⚖️"}.get(market_regime, "📊")
        st.metric("Market Regime", f"{regime_emoji} {market_regime.replace('_', ' ').title()}")
    
    with col2:
        trend_direction = result.get("trend_direction", "sideways")
        trend_emoji = {"up": "📈", "down": "📉", "sideways": "↔️"}.get(trend_direction, "📊")
        st.metric("Trend", f"{trend_emoji} {trend_direction.title()}")
    
    with col3:
        confidence = result.get("confidence_score", 0)
        st.metric("Confidence", f"{confidence:.1%}")
    
    # Key insights
    key_insights = result.get("key_insights", [])
    if key_insights:
        st.subheader("🔍 Market Insights")
        for insight in key_insights:
            title = insight.get("title", "Market Insight")
            timeframe = insight.get("timeframe", "current")
            confidence = insight.get("confidence", 0)
            st.write(f"**{title}** ({timeframe}) - Confidence: {confidence:.0%}")

def display_opportunities(result: Dict[str, Any]):
    """Display investment opportunities"""
    if "error" in result:
        st.error(f"Opportunity analysis failed: {result['error']}")
        return
    
    opportunities_count = result.get("opportunities_count", 0)
    st.metric("Opportunities Identified", opportunities_count)
    
    # Tactical opportunities
    tactical_opportunities = result.get("tactical_opportunities", [])
    if tactical_opportunities:
        st.subheader("⚡ Short-term Opportunities")
        for opp in tactical_opportunities:
            opportunity = opp.get("opportunity", "Investment opportunity")
            expected_return = opp.get("expected_return", "N/A")
            st.write(f"• **{opportunity}** - Expected return: {expected_return}")
    
    # Strategic opportunities
    strategic_opportunities = result.get("strategic_opportunities", [])
    if strategic_opportunities:
        st.subheader("🎯 Long-term Opportunities")
        for opp in strategic_opportunities:
            opportunity = opp.get("opportunity", "Investment opportunity")
            expected_return = opp.get("expected_return", "N/A")
            st.write(f"• **{opportunity}** - Expected return: {expected_return}")
    
    # Investment themes
    investment_themes = result.get("investment_themes", [])
    if investment_themes:
        st.subheader("📈 Investment Themes")
        st.write(", ".join(investment_themes)) 