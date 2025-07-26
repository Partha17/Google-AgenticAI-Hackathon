"""
Market Analysis Agent - ADK Implementation with AI-Powered Analysis
Sophisticated agent for technical and fundamental market analysis using Google Gemini
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from adk_agents.agent_config import adk_config
from adk_agents.ai_analysis_base import AIAnalysisBase

logger = logging.getLogger(__name__)

class MarketAnalysisAgent(AIAnalysisBase):
    """ADK-based Market Analysis Agent powered by Gemini AI for comprehensive market intelligence"""
    
    def __init__(self):
        self.agent_id = "market_analysis_agent"
        config = adk_config.get_agent_definitions()[self.agent_id]
        super().__init__(self.agent_id, config)
        
    async def analyze_market_trends(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered comprehensive market trend analysis using Gemini
        """
        try:
            logger.info("Starting AI-powered comprehensive market trend analysis...")
            
            specific_instructions = """
            Perform comprehensive market trend analysis focusing on:
            
            1. **Technical Analysis**:
               - Price trend identification and direction
               - Momentum indicators and strength assessment
               - Support and resistance level analysis
               - Volume analysis and market participation
               - Chart pattern recognition
            
            2. **Market Regime Analysis**:
               - Current market environment assessment (bull/bear/sideways)
               - Market volatility evaluation
               - Risk-on vs risk-off sentiment
               - Market cycle positioning
               - Trend sustainability assessment
            
            3. **Sector and Asset Analysis**:
               - Sector rotation patterns
               - Asset class performance comparison
               - Relative strength analysis
               - Correlation analysis between assets
               - Diversification effectiveness
            
            4. **Market Intelligence**:
               - Economic cycle positioning
               - Central bank policy impact
               - Geopolitical risk assessment
               - Market sentiment indicators
               - Forward-looking market outlook
            
            5. **Investment Opportunities**:
               - Undervalued sectors/assets identification
               - Growth opportunity assessment
               - Risk-adjusted return analysis
               - Timing considerations
               - Entry/exit strategy recommendations
            
            Provide specific market regime classification, trend strength scores (0.0-1.0),
            confidence assessments, and actionable investment insights.
            """
            
            analysis_results = await self.ai_analyze(
                analysis_type="comprehensive_market_analysis",
                data=financial_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for market analysis
            if "error" not in analysis_results:
                analysis_results = self._enhance_market_analysis_structure(analysis_results)
            
            logger.info("AI-powered market trend analysis completed")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in AI market trend analysis: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "fallback_analysis": "AI analysis failed, manual intervention required"
            }
    
    async def analyze_portfolio_performance(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered portfolio performance analysis and attribution
        """
        try:
            logger.info("Starting AI-powered portfolio performance analysis...")
            
            specific_instructions = """
            Perform comprehensive portfolio performance analysis focusing on:
            
            1. **Performance Metrics Calculation**:
               - Total return analysis (absolute and annualized)
               - Risk-adjusted return metrics (Sharpe ratio, Sortino ratio)
               - Volatility and downside risk assessment
               - Maximum drawdown analysis
               - Performance consistency evaluation
            
            2. **Attribution Analysis**:
               - Asset allocation contribution
               - Security selection impact
               - Sector/style attribution
               - Geographic allocation effects
               - Currency impact analysis
            
            3. **Benchmark Comparison**:
               - Relative performance vs appropriate benchmarks
               - Active vs passive performance analysis
               - Alpha generation assessment
               - Beta and correlation analysis
               - Tracking error evaluation
            
            4. **Risk-Return Profile**:
               - Efficient frontier positioning
               - Risk budgeting analysis
               - Concentration risk assessment
               - Liquidity analysis
               - Stress test performance
            
            5. **Performance Improvement Recommendations**:
               - Underperforming asset identification
               - Rebalancing opportunities
               - Cost optimization suggestions
               - Risk management improvements
               - Portfolio optimization strategies
            
            Provide detailed performance metrics, attribution analysis,
            and specific recommendations for portfolio enhancement.
            """
            
            performance_analysis = await self.ai_analyze(
                analysis_type="portfolio_performance_analysis",
                data=financial_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for performance analysis
            if "error" not in performance_analysis:
                performance_analysis = self._enhance_performance_structure(performance_analysis)
            
            logger.info("AI-powered portfolio performance analysis completed")
            return performance_analysis
            
        except Exception as e:
            logger.error(f"Error in AI portfolio performance analysis: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def identify_market_opportunities(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered market opportunity identification and investment recommendations
        """
        try:
            logger.info("Starting AI-powered market opportunity identification...")
            
            specific_instructions = """
            Identify and analyze market opportunities focusing on:
            
            1. **Growth Opportunities**:
               - Emerging market trends and themes
               - Sector rotation opportunities
               - Undervalued asset identification
               - Growth vs value positioning
               - Technology and innovation trends
            
            2. **Income Opportunities**:
               - Dividend growth opportunities
               - Fixed income positioning
               - REIT and infrastructure investments
               - High-yield opportunities with acceptable risk
               - Income sustainability analysis
            
            3. **Tactical Opportunities**:
               - Short-term market inefficiencies
               - Seasonal patterns and cycles
               - Event-driven opportunities
               - Volatility trading opportunities
               - Arbitrage possibilities
            
            4. **Strategic Positioning**:
               - Long-term secular trends
               - Demographic and social changes
               - ESG and sustainability themes
               - Currency and commodity positioning
               - Geographic allocation opportunities
            
            5. **Risk-Opportunity Assessment**:
               - Risk-adjusted opportunity ranking
               - Implementation feasibility
               - Timing considerations
               - Position sizing recommendations
               - Exit strategy definition
            
            Provide specific opportunity recommendations with rationale,
            risk assessment, expected returns, and implementation guidance.
            """
            
            opportunity_analysis = await self.ai_analyze(
                analysis_type="market_opportunity_identification",
                data=financial_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for opportunity analysis
            if "error" not in opportunity_analysis:
                opportunity_analysis = self._enhance_opportunity_structure(opportunity_analysis)
            
            logger.info("AI-powered market opportunity identification completed")
            return opportunity_analysis
            
        except Exception as e:
            logger.error(f"Error in AI opportunity identification: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def generate_market_outlook(self, financial_data: Dict[str, Any], time_horizon: str = "medium_term") -> Dict[str, Any]:
        """
        AI-powered comprehensive market outlook and forecasting
        """
        try:
            logger.info(f"Starting AI-powered market outlook generation for {time_horizon}...")
            
            specific_instructions = f"""
            Generate comprehensive market outlook for {time_horizon} horizon focusing on:
            
            1. **Economic Environment Assessment**:
               - GDP growth expectations
               - Inflation outlook and central bank policy
               - Employment and consumer spending trends
               - Corporate earnings environment
               - Economic cycle positioning
            
            2. **Market Regime Forecasting**:
               - Expected market volatility levels
               - Risk sentiment evolutionhy2ty
               - Sector leadership expectations
               - Style preferences (growth vs value)
               - Geographic market performance expectations
            
            3. **Asset Class Outlook**:
               - Equity market expectations by region/sector
               - Fixed income outlook and yield curve expectations
               - Alternative investment opportunities
               - Currency and commodity outlook
               - Real estate and infrastructure prospects
            
            4. **Risk Factor Analysis**:
               - Key downside risks and tail events
               - Geopolitical risk assessment
               - Policy and regulatory risks
               - Market structure and liquidity risks
               - Black swan event considerations
            
            5. **Strategic Recommendations**:
               - Asset allocation guidance
               - Hedging and protection strategies
               - Opportunistic positioning recommendations
               - Risk management priorities
               - Portfolio positioning for different scenarios
            
            Time Horizon: {time_horizon}
            - short_term: 1-3 months
            - medium_term: 3-12 months  
            - long_term: 1-3 years
            
            Provide specific forecasts with probability assessments,
            scenario analysis, and actionable investment guidance.
            """
            
            outlook_analysis = await self.ai_analyze(
                analysis_type="market_outlook_forecasting",
                data={"financial_data": financial_data, "time_horizon": time_horizon},
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for outlook analysis
            if "error" not in outlook_analysis:
                outlook_analysis = self._enhance_outlook_structure(outlook_analysis, time_horizon)
            
            logger.info("AI-powered market outlook generation completed")
            return outlook_analysis
            
        except Exception as e:
            logger.error(f"Error in AI market outlook generation: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _enhance_market_analysis_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response with required structure for market analysis"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_market_analysis",
            **ai_response
        }
        
        # Ensure required fields exist with defaults
        if "market_regime" not in enhanced:
            enhanced["market_regime"] = enhanced.get("regime", "neutral")
        
        if "trend_direction" not in enhanced:
            enhanced["trend_direction"] = enhanced.get("trend", "sideways")
        
        if "trend_strength" not in enhanced:
            enhanced["trend_strength"] = enhanced.get("strength", 0.5)
        
        if "confidence_score" not in enhanced:
            enhanced["confidence_score"] = enhanced.get("confidence", 0.5)
        
        if "technical_indicators" not in enhanced:
            enhanced["technical_indicators"] = enhanced.get("technical_analysis", {})
        
        if "fundamental_metrics" not in enhanced:
            enhanced["fundamental_metrics"] = enhanced.get("fundamental_analysis", {})
        
        if "sector_analysis" not in enhanced:
            enhanced["sector_analysis"] = enhanced.get("sector_breakdown", {})
        
        if "market_outlook" not in enhanced:
            enhanced["market_outlook"] = enhanced.get("outlook", {})
        
        if "key_insights" not in enhanced:
            enhanced["key_insights"] = enhanced.get("insights", [])
        
        return enhanced
    
    def _enhance_performance_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response structure for performance analysis"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_performance_analysis",
            **ai_response
        }
        
        # Ensure required fields
        if "performance_metrics" not in enhanced:
            enhanced["performance_metrics"] = enhanced.get("metrics", {})
        
        if "attribution_analysis" not in enhanced:
            enhanced["attribution_analysis"] = enhanced.get("attribution", {})
        
        if "benchmark_comparison" not in enhanced:
            enhanced["benchmark_comparison"] = enhanced.get("benchmark", {})
        
        if "risk_adjusted_returns" not in enhanced:
            enhanced["risk_adjusted_returns"] = enhanced.get("risk_metrics", {})
        
        if "recommendations" not in enhanced:
            enhanced["recommendations"] = enhanced.get("improvement_recommendations", [])
        
        return enhanced
    
    def _enhance_opportunity_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response structure for opportunity analysis"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_opportunity_identification",
            **ai_response
        }
        
        # Ensure required fields
        if "opportunities" not in enhanced:
            enhanced["opportunities"] = enhanced.get("identified_opportunities", [])
        
        if "growth_opportunities" not in enhanced:
            enhanced["growth_opportunities"] = enhanced.get("growth", [])
        
        if "income_opportunities" not in enhanced:
            enhanced["income_opportunities"] = enhanced.get("income", [])
        
        if "tactical_opportunities" not in enhanced:
            enhanced["tactical_opportunities"] = enhanced.get("tactical", [])
        
        if "risk_assessment" not in enhanced:
            enhanced["risk_assessment"] = enhanced.get("risks", {})
        
        return enhanced
    
    def _enhance_outlook_structure(self, ai_response: Dict[str, Any], time_horizon: str) -> Dict[str, Any]:
        """Enhance AI response structure for outlook analysis"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_market_outlook",
            "time_horizon": time_horizon,
            **ai_response
        }
        
        # Ensure required fields
        if "economic_outlook" not in enhanced:
            enhanced["economic_outlook"] = enhanced.get("economic_environment", {})
        
        if "market_forecasts" not in enhanced:
            enhanced["market_forecasts"] = enhanced.get("forecasts", {})
        
        if "asset_class_outlook" not in enhanced:
            enhanced["asset_class_outlook"] = enhanced.get("asset_outlook", {})
        
        if "risk_factors" not in enhanced:
            enhanced["risk_factors"] = enhanced.get("risks", [])
        
        if "strategic_recommendations" not in enhanced:
            enhanced["strategic_recommendations"] = enhanced.get("recommendations", [])
        
        if "scenarios" not in enhanced:
            enhanced["scenarios"] = enhanced.get("scenario_analysis", [])
        
        return enhanced

# Create global instance
market_analysis_agent = MarketAnalysisAgent() 