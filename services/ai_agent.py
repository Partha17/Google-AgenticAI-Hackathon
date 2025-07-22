import logging
import json
from datetime import datetime
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from sqlalchemy.orm import Session
from models.database import AIInsight, MCPData, SessionLocal
from config import settings

logger = logging.getLogger(__name__)

class AIInsightAgent:
    """LangChain AI agent for generating insights from MCP data using Gemini"""
    
    def __init__(self):
        if not settings.google_api_key:
            raise ValueError("Google API key is required. Please set GOOGLE_API_KEY in your .env file")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.google_api_key,
            temperature=0.7
        )
        
        self.system_prompt = """
        You are a financial AI analyst specializing in market data interpretation and insight generation.
        Your role is to analyze financial data and provide actionable insights for investors and traders.
        
        CRITICAL: You must respond ONLY with valid JSON. Do not include any text before or after the JSON.
        
        Key responsibilities:
        1. Analyze stock prices, volumes, and market trends
        2. Identify patterns in financial metrics and ratios
        3. Assess market sentiment and economic indicators
        4. Generate clear, concise, and actionable insights
        5. Provide confidence scores for your analysis (0-1 scale)
        
        Response format (valid JSON only):
        {
            "insight_type": "trend_analysis",
            "title": "Brief descriptive title",
            "content": "Detailed analysis and recommendation",
            "confidence_score": 0.85,
            "key_factors": ["factor1", "factor2", "factor3"],
            "recommended_actions": ["action1", "action2"]
        }
        
        insight_type must be one of: trend_analysis, risk_assessment, opportunity, market_sentiment
        
        Be specific, data-driven, and focus on actionable intelligence. Respond with JSON only.
        """
    
    def analyze_data_batch(self, mcp_records: List[MCPData]) -> List[Dict[str, Any]]:
        """Analyze a batch of MCP data and generate insights"""
        if not mcp_records:
            return []
        
        try:
            # Prepare data for analysis
            data_summary = self._prepare_data_summary(mcp_records)
            
            # Generate insights using different analysis types
            insights = []
            
            # Market trend analysis
            trend_insight = self._analyze_market_trends(data_summary, mcp_records)
            if trend_insight:
                insights.append(trend_insight)
            
            # Risk assessment
            risk_insight = self._analyze_risks(data_summary, mcp_records)
            if risk_insight:
                insights.append(risk_insight)
            
            # Opportunity identification
            opportunity_insight = self._identify_opportunities(data_summary, mcp_records)
            if opportunity_insight:
                insights.append(opportunity_insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing data batch: {e}")
            return []
    
    def _prepare_data_summary(self, records: List[MCPData]) -> str:
        """Prepare a summary of the data for AI analysis"""
        summary = {
            "total_records": len(records),
            "data_types": {},
            "time_range": {
                "start": min(r.timestamp for r in records).isoformat(),
                "end": max(r.timestamp for r in records).isoformat()
            },
            "sample_data": []
        }
        
        for record in records:
            data_type = record.data_type
            summary["data_types"][data_type] = summary["data_types"].get(data_type, 0) + 1
            
            # Add sample data (limit to prevent token overflow)
            if len(summary["sample_data"]) < 20:
                summary["sample_data"].append(record.get_data())
        
        return json.dumps(summary, indent=2)
    
    def _analyze_market_trends(self, data_summary: str, records: List[MCPData]) -> Dict[str, Any]:
        """Generate market trend analysis"""
        prompt = f"""
        Analyze the following financial data for market trends and patterns:
        
        {data_summary}
        
        Focus on:
        - Stock price movements and volume patterns
        - Market sentiment shifts
        - Economic indicator trends
        - Cross-asset correlations
        
        Provide trend analysis with actionable insights.
        """
        
        return self._generate_insight(prompt, "trend_analysis", records)
    
    def _analyze_risks(self, data_summary: str, records: List[MCPData]) -> Dict[str, Any]:
        """Generate risk assessment"""
        prompt = f"""
        Perform a risk assessment based on the following financial data:
        
        {data_summary}
        
        Identify:
        - Market volatility indicators
        - Economic risk factors
        - Sector-specific risks
        - Liquidity concerns
        - Potential downside scenarios
        
        Provide risk assessment with mitigation strategies.
        """
        
        return self._generate_insight(prompt, "risk_assessment", records)
    
    def _identify_opportunities(self, data_summary: str, records: List[MCPData]) -> Dict[str, Any]:
        """Identify investment opportunities"""
        prompt = f"""
        Identify investment opportunities from the following financial data:
        
        {data_summary}
        
        Look for:
        - Undervalued assets
        - Emerging trends
        - Arbitrage opportunities
        - Sector rotation signals
        - Technical breakout patterns
        
        Provide opportunity analysis with specific recommendations.
        """
        
        return self._generate_insight(prompt, "opportunity", records)
    
    def _generate_insight(self, prompt: str, insight_type: str, records: List[MCPData]) -> Dict[str, Any]:
        """Generate insight using Gemini AI"""
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Clean the response content - remove any markdown formatting
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            logger.info(f"AI Response: {content[:200]}...")  # Log first 200 chars for debugging
            
            # Parse JSON response
            insight_data = json.loads(content)
            
            # Add metadata
            insight_data["source_record_ids"] = [r.id for r in records]
            insight_data["generated_at"] = datetime.utcnow().isoformat()
            insight_data["model"] = "gemini-2.0-flash-exp"
            
            return insight_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Raw response: {response.content}")
            return None
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            return None
    
    def store_insights(self, insights: List[Dict[str, Any]]) -> List[int]:
        """Store generated insights in database"""
        stored_ids = []
        db = SessionLocal()
        
        try:
            for insight_data in insights:
                ai_insight = AIInsight(
                    insight_type=insight_data.get("insight_type", "general"),
                    title=insight_data.get("title", "AI Generated Insight"),
                    content=insight_data.get("content", ""),
                    confidence_score=insight_data.get("confidence_score", 0.0),
                    timestamp=datetime.utcnow()
                )
                
                # Set source IDs
                source_ids = insight_data.get("source_record_ids", [])
                ai_insight.set_source_ids(source_ids)
                
                # Set metadata
                metadata = {
                    "key_factors": insight_data.get("key_factors", []),
                    "recommended_actions": insight_data.get("recommended_actions", []),
                    "model": insight_data.get("model", "unknown"),
                    "generated_at": insight_data.get("generated_at")
                }
                ai_insight.set_metadata(metadata)
                
                db.add(ai_insight)
                db.flush()
                stored_ids.append(ai_insight.id)
            
            db.commit()
            logger.info(f"Stored {len(insights)} insights in database")
            
        except Exception as e:
            logger.error(f"Error storing insights: {e}")
            db.rollback()
        finally:
            db.close()
        
        return stored_ids

# Singleton instance
ai_agent = AIInsightAgent() 