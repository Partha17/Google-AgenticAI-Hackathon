"""
ADK Agent Definition - Financial Assistant Agent
This file defines the Financial Assistant Agent for Google Cloud ADK
Based on: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
"""

import asyncio
import json
from main_adk import financial_assistant

# Agent configuration for ADK
AGENT_CONFIG = {
    "agent_name": "financial_assistant",
    "model": "gemini-1.5-flash",
    "system_instruction": """
You are an elite Financial Assistant Agent powered by a sophisticated multi-agent system. You provide comprehensive financial intelligence through coordinated AI agents specializing in different aspects of financial analysis.

CORE CAPABILITIES:
- Comprehensive Financial Analysis: Complete portfolio and financial health assessment
- Risk Assessment: Advanced portfolio risk analysis and stress testing
- Market Analysis: Technical analysis, market trends, and regime identification  
- Opportunity Identification: Investment opportunities and strategic recommendations
- Real-time Data Integration: Live financial data from Fi MCP server

MULTI-AGENT ARCHITECTURE:
Your responses are powered by specialized agents:
1. Financial Data Collector Agent: Gathers real-time financial data
2. Risk Assessment Agent: Analyzes portfolio risks and stress scenarios
3. Market Analysis Agent: Performs technical and fundamental analysis
4. Orchestrator Agent: Coordinates multi-agent workflows

RESPONSE STYLE:
- Professional yet accessible financial guidance
- Data-driven insights with confidence levels
- Actionable recommendations with timeframes
- Clear explanations of complex financial concepts
- Structured responses with priorities and next steps

FINANCIAL EXPERTISE:
- Portfolio optimization and diversification
- Risk management and stress testing
- Market regime analysis and trend identification
- Investment opportunity evaluation
- Performance attribution and benchmarking

Always provide specific, actionable financial guidance based on real data analysis from your multi-agent system.
    """,
    "tools": [
        {
            "name": "comprehensive_analysis",
            "description": "Execute comprehensive financial analysis using all agents",
            "function": "comprehensive_financial_analysis"
        },
        {
            "name": "risk_assessment", 
            "description": "Perform detailed portfolio risk assessment",
            "function": "risk_assessment_analysis"
        },
        {
            "name": "market_analysis",
            "description": "Analyze market trends and conditions",
            "function": "market_trend_analysis"
        },
        {
            "name": "opportunity_identification",
            "description": "Identify investment opportunities",
            "function": "investment_opportunity_analysis"
        },
        {
            "name": "stress_testing",
            "description": "Perform portfolio stress testing",
            "function": "portfolio_stress_testing"
        },
        {
            "name": "system_status",
            "description": "Check multi-agent system health",
            "function": "system_health_check"
        }
    ]
}

async def comprehensive_financial_analysis(params=None):
    """Tool function for comprehensive financial analysis"""
    try:
        response = await financial_assistant.handle_message("comprehensive analysis")
        return {"result": response, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

async def risk_assessment_analysis(params=None):
    """Tool function for risk assessment"""
    try:
        response = await financial_assistant.handle_message("risk assessment")
        return {"result": response, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

async def market_trend_analysis(params=None):
    """Tool function for market analysis"""
    try:
        response = await financial_assistant.handle_message("market analysis")
        return {"result": response, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

async def investment_opportunity_analysis(params=None):
    """Tool function for opportunity identification"""
    try:
        response = await financial_assistant.handle_message("investment opportunities")
        return {"result": response, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

async def portfolio_stress_testing(params=None):
    """Tool function for stress testing"""
    try:
        response = await financial_assistant.handle_message("stress test")
        return {"result": response, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

async def system_health_check(params=None):
    """Tool function for system status"""
    try:
        response = await financial_assistant.handle_message("system status")
        return {"result": response, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

# Main handler function for ADK
async def handle_message(message: str, context: dict = None):
    """Main message handler for ADK integration"""
    try:
        # Initialize if not already done
        if not financial_assistant.system_initialized:
            await financial_assistant.initialize()
        
        # Handle the message using our multi-agent system
        response = await financial_assistant.handle_message(message, context)
        return response
    
    except Exception as e:
        return f"I encountered an error: {str(e)}. Please try again or check system status."

# Export for ADK
def get_agent_config():
    """Get agent configuration for ADK"""
    return AGENT_CONFIG

# For ADK compatibility
if __name__ == "__main__":
    # This would be used by ADK to run the agent
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        asyncio.run(financial_assistant.initialize())
    else:
        print("Financial Assistant Agent - ADK Multi-Agent System")
        print("Use 'adk run financial_assistant' to start the agent") 