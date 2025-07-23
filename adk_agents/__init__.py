"""
ADK Agents Package - Google Cloud Agent Development Kit Multi-Agent System
Financial intelligence through coordinated AI agents powered by Google Gemini
"""

from .agent_config import adk_config
from .ai_analysis_base import AIAnalysisBase
from .financial_data_collector import financial_data_collector_agent
from .risk_assessment_agent import risk_assessment_agent 
from .market_analysis_agent import market_analysis_agent
from .adk_orchestrator import adk_orchestrator

__all__ = [
    'adk_config',
    'AIAnalysisBase',
    'financial_data_collector_agent',
    'risk_assessment_agent',
    'market_analysis_agent', 
    'adk_orchestrator'
]

__version__ = "2.0.0"
__author__ = "Google Cloud ADK Multi-Agent System with AI Analysis"
__description__ = "Financial intelligence through coordinated AI agents using Google Cloud ADK and Gemini AI" 