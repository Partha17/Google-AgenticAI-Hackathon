"""
Enhanced AI Agent for generating financial insights using Google's Gemini models
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

logger = logging.getLogger(__name__)

class EnhancedAIAgent:
    """Enhanced AI agent for financial analysis using Google's Gemini"""
    
    def __init__(self):
        """Initialize the enhanced AI agent"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.google_api_key,
            temperature=0.3
        )
        logger.info("Enhanced AI Agent initialized with Gemini model")
    
    def generate_market_insight(self, financial_data: Dict[str, Any]) -> str:
        """Generate market insights from financial data"""
        try:
            prompt = f"""
            As a financial analyst, analyze the following financial data and provide insights:
            
            Data: {json.dumps(financial_data, indent=2)}
            
            Please provide:
            1. Key trends and patterns
            2. Risk assessment
            3. Investment recommendations
            4. Market outlook
            
            Keep the analysis concise and actionable.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating market insight: {e}")
            return f"Error generating insight: {str(e)}"
    
    def generate_portfolio_analysis(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate portfolio analysis"""
        try:
            prompt = f"""
            Analyze this portfolio data and provide insights:
            
            Portfolio: {json.dumps(portfolio_data, indent=2)}
            
            Please analyze:
            1. Diversification quality
            2. Risk level assessment
            3. Performance analysis
            4. Rebalancing recommendations
            
            Provide specific, actionable advice.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating portfolio analysis: {e}")
            return f"Error generating portfolio analysis: {str(e)}"
    
    def generate_risk_assessment(self, financial_data: Dict[str, Any]) -> str:
        """Generate risk assessment from financial data"""
        try:
            prompt = f"""
            Perform a comprehensive risk assessment on this financial data:
            
            Data: {json.dumps(financial_data, indent=2)}
            
            Assess:
            1. Market risk exposure
            2. Credit risk factors
            3. Liquidity risks
            4. Operational risks
            5. Mitigation strategies
            
            Provide a detailed risk profile with scores and recommendations.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating risk assessment: {e}")
            return f"Error generating risk assessment: {str(e)}"
    
    def generate_investment_recommendation(self, user_profile: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """Generate personalized investment recommendations"""
        try:
            prompt = f"""
            Based on the user profile and market data, provide investment recommendations:
            
            User Profile: {json.dumps(user_profile, indent=2)}
            Market Data: {json.dumps(market_data, indent=2)}
            
            Provide:
            1. Asset allocation suggestions
            2. Specific investment options
            3. Time horizon considerations
            4. Risk-adjusted recommendations
            5. Entry and exit strategies
            
            Tailor recommendations to the user's risk tolerance and goals.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating investment recommendation: {e}")
            return f"Error generating investment recommendation: {str(e)}"
    
    def analyze_transaction_patterns(self, transactions: List[Dict[str, Any]]) -> str:
        """Analyze transaction patterns and spending habits"""
        try:
            prompt = f"""
            Analyze these transaction patterns:
            
            Transactions: {json.dumps(transactions[:10], indent=2)}  # Limit for prompt size
            Total transactions: {len(transactions)}
            
            Analyze:
            1. Spending patterns and categories
            2. Income vs expenses trends
            3. Unusual or concerning transactions
            4. Budget optimization opportunities
            5. Financial health indicators
            
            Provide actionable insights for better financial management.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error analyzing transaction patterns: {e}")
            return f"Error analyzing transaction patterns: {str(e)}"
    
    def generate_comprehensive_report(self, all_data: Dict[str, Any]) -> str:
        """Generate a comprehensive financial report"""
        try:
            prompt = f"""
            Create a comprehensive financial analysis report:
            
            Financial Data Summary: {json.dumps(all_data, indent=2)[:2000]}...
            
            Structure the report with:
            1. Executive Summary
            2. Current Financial Position
            3. Risk Analysis
            4. Performance Metrics
            5. Strategic Recommendations
            6. Action Items
            
            Make it professional and actionable for financial decision-making.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return f"Error generating comprehensive report: {str(e)}"

# Global instance
enhanced_ai_agent = EnhancedAIAgent() 