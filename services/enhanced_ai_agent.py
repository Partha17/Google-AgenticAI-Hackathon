"""
Enhanced AI Agent for generating financial insights using Google's Gemini models
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from services.logger_config import get_ai_logger, log_error

# Use centralized logger
logger = get_ai_logger()

class EnhancedAIAgent:
    """Enhanced AI agent for financial analysis using Google's Gemini"""
    
    def __init__(self):
        """Initialize the enhanced AI agent"""
        try:
            # Get API key from environment or settings
            api_key = os.getenv("GOOGLE_API_KEY") or settings.google_api_key
            
            if not api_key:
                logger.error("No Google API key found. Please set GOOGLE_API_KEY environment variable.")
                raise ValueError("Google API key is required")
            
            # Initialize the LLM with explicit configuration
            self.llm = ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=api_key,
                temperature=0.3,
                max_output_tokens=2048,
                top_p=0.8,
                top_k=40
            )
            
            logger.info(f"Enhanced AI Agent initialized with {settings.gemini_model} model")
            
        except Exception as e:
            logger.error(f"Failed to initialize Enhanced AI Agent: {e}")
            raise
    
    def analyze_data_batch(self, data_records: List[Any]) -> List[Dict[str, Any]]:
        """Analyze a batch of MCP data records and generate insights"""
        try:
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                logger.warning("LLM not initialized, skipping data analysis")
                return []
            
            logger.info(f"Analyzing batch of {len(data_records)} data records")
            
            insights = []
            
            # Extract financial data from records
            financial_data = {}
            for record in data_records:
                if hasattr(record, 'data_type') and hasattr(record, 'raw_data'):
                    try:
                        # Parse the raw data
                        if isinstance(record.raw_data, str):
                            import ast
                            parsed_data = ast.literal_eval(record.raw_data)
                        else:
                            parsed_data = record.raw_data
                        
                        financial_data[record.data_type] = parsed_data
                    except Exception as e:
                        logger.warning(f"Error parsing data for {record.data_type}: {e}")
                        continue
            
            if not financial_data:
                logger.warning("No valid financial data found in batch")
                return []
            
            # Generate different types of insights
            insight_types = [
                ("trend_analysis", "Market Trend Analysis"),
                ("risk_assessment", "Risk Assessment"),
                ("opportunity", "Investment Opportunities")
            ]
            
            for insight_type, title in insight_types:
                try:
                    # Generate insight based on type
                    if insight_type == "trend_analysis":
                        content = self.generate_market_insight(financial_data)
                    elif insight_type == "risk_assessment":
                        content = self.generate_risk_assessment(financial_data)
                    elif insight_type == "opportunity":
                        content = self.generate_investment_recommendation(
                            {"financial_data": financial_data}, 
                            financial_data
                        )
                    else:
                        content = self.generate_market_insight(financial_data)
                    
                    # Create insight object
                    insight = {
                        "title": f"{title} - {datetime.now().strftime('%Y-%m-%d')}",
                        "content": content,
                        "insight_type": insight_type,
                        "confidence_score": 0.8,  # Default confidence
                        "created_at": datetime.now(),
                        "data_sources": list(financial_data.keys())
                    }
                    
                    insights.append(insight)
                    logger.info(f"Generated {insight_type} insight")
                    
                except Exception as e:
                    logger.error(f"Error generating {insight_type} insight: {e}")
                    continue
            
            logger.info(f"Generated {len(insights)} insights from batch")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing data batch: {e}")
            return []
    
    def store_enhanced_insights(self, insights: List[Dict[str, Any]]) -> List[int]:
        """Store enhanced insights in the database"""
        try:
            from models.database import SessionLocal, AIInsight
            
            db = SessionLocal()
            stored_ids = []
            
            try:
                for insight_data in insights:
                    # Create AIInsight object
                    ai_insight = AIInsight(
                        title=insight_data["title"],
                        content=insight_data["content"],
                        insight_type=insight_data["insight_type"],
                        confidence_score=insight_data["confidence_score"],
                        created_at=insight_data["created_at"],
                        data_sources=",".join(insight_data.get("data_sources", []))
                    )
                    
                    db.add(ai_insight)
                    db.flush()  # Get the ID
                    stored_ids.append(ai_insight.id)
                
                db.commit()
                logger.info(f"Stored {len(stored_ids)} enhanced insights")
                
            except Exception as e:
                db.rollback()
                logger.error(f"Error storing insights: {e}")
                raise
            
            finally:
                db.close()
            
            return stored_ids
            
        except Exception as e:
            logger.error(f"Error in store_enhanced_insights: {e}")
            return []

    def generate_market_insight(self, financial_data: Dict[str, Any]) -> str:
        """Generate market insights from financial data"""
        try:
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                return "AI insights not available - API key not configured"
            
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
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                return "AI insights not available - API key not configured"
            
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
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                return "AI insights not available - API key not configured"
            
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
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                return "AI insights not available - API key not configured"
            
            # Check if API key is available
            api_key = os.getenv("GOOGLE_API_KEY") or settings.google_api_key
            if not api_key:
                return "Error: Google API key not configured. Please set GOOGLE_API_KEY environment variable."
            
            # Create a simplified prompt to reduce token usage
            prompt = f"""
            Generate investment recommendations based on this financial data:
            
            User Profile: {json.dumps(user_profile, indent=2)[:1000]}
            Market Data: {json.dumps(market_data, indent=2)[:1000]}
            
            Provide brief recommendations for:
            1. Asset allocation
            2. Investment options
            3. Risk considerations
            
            Keep response concise and actionable.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating investment recommendation: {error_msg}")
            
            # Check for specific authentication errors
            if "ACCESS_TOKEN_SCOPE_INSUFFICIENT" in error_msg or "403" in error_msg:
                return "Error: API key authentication failed. Please check Google API key configuration and ensure it has access to Generative Language API."
            elif "quota" in error_msg.lower():
                return "Error: API quota exceeded. Please try again later or check quota limits."
            else:
                return f"Error generating investment recommendation: {error_msg}"
    
    def analyze_transaction_patterns(self, transactions: List[Dict[str, Any]]) -> str:
        """Analyze transaction patterns and spending habits"""
        try:
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                return "AI insights not available - API key not configured"
            
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
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                return "AI insights not available - API key not configured"
            
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

    def test_api_connection(self) -> bool:
        """Test the API connection and key validity"""
        try:
            # Check if LLM is available
            if not hasattr(self, 'llm') or self.llm is None:
                logger.error("❌ LLM not initialized")
                return False
            
            # Simple test prompt
            test_prompt = "Hello, this is a test message. Please respond with 'API connection successful'."
            response = self.llm.invoke(test_prompt)
            
            if response and response.content:
                logger.info("✅ API connection test successful")
                return True
            else:
                logger.error("❌ API connection test failed: No response")
                return False
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ API connection test failed: {error_msg}")
            
            if "ACCESS_TOKEN_SCOPE_INSUFFICIENT" in error_msg:
                logger.error("🔑 API key scope issue: Ensure the API key has access to Generative Language API")
            elif "403" in error_msg:
                logger.error("🔑 API key authentication failed: Check API key validity")
            elif "quota" in error_msg.lower():
                logger.error("📊 API quota exceeded: Check usage limits")
            
            return False

# Global instance with lazy initialization
_enhanced_ai_agent_instance = None

def get_enhanced_ai_agent():
    """Get the singleton instance of EnhancedAIAgent with lazy initialization"""
    global _enhanced_ai_agent_instance
    
    if _enhanced_ai_agent_instance is None:
        try:
            _enhanced_ai_agent_instance = EnhancedAIAgent()
            logger.info("✅ Enhanced AI Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Enhanced AI Agent: {e}")
            # Create a fallback instance that handles errors gracefully
            _enhanced_ai_agent_instance = EnhancedAIAgent.__new__(EnhancedAIAgent)
            _enhanced_ai_agent_instance.llm = None
            _enhanced_ai_agent_instance._initialized = False
    
    return _enhanced_ai_agent_instance

# For backward compatibility
enhanced_ai_agent = get_enhanced_ai_agent() 