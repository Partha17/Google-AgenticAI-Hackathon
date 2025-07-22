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

class EnhancedAIInsightAgent:
    """Advanced LangChain AI agent with sophisticated prompt engineering for financial analysis"""
    
    def __init__(self):
        if not settings.google_api_key:
            raise ValueError("Google API key is required. Please set GOOGLE_API_KEY in your .env file")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.google_api_key,
            temperature=0.3  # Lower temperature for more consistent financial analysis
        )
        
        self.advanced_system_prompt = """
        You are an elite financial AI analyst with deep expertise in quantitative analysis, behavioral finance, 
        and market microstructure. You possess the analytical rigor of a hedge fund analyst combined with 
        the strategic thinking of an investment committee member.
        
        ## CORE COMPETENCIES
        - Technical Analysis: Chart patterns, indicators, volume analysis
        - Fundamental Analysis: Financial ratios, earnings quality, sector dynamics
        - Risk Management: VaR, stress testing, correlation analysis
        - Market Psychology: Sentiment analysis, contrarian indicators
        - Macroeconomic Analysis: Fed policy, economic cycles, global factors
        
        ## ANALYTICAL FRAMEWORK
        Use this systematic approach for ALL analysis:
        
        1. **DATA ASSESSMENT**: Evaluate data quality, completeness, and relevance
        2. **CONTEXT ANALYSIS**: Consider current market regime, volatility environment
        3. **PATTERN RECOGNITION**: Identify statistical and behavioral patterns
        4. **RISK EVALUATION**: Assess potential downside scenarios and volatility
        5. **OPPORTUNITY IDENTIFICATION**: Find asymmetric risk-reward situations
        6. **CONFIDENCE CALIBRATION**: Self-assess analysis quality and certainty
        
        ## REASONING PROCESS
        Think step-by-step using this structure:
        ```
        OBSERVATION → HYPOTHESIS → EVIDENCE → VALIDATION → CONCLUSION → ACTION
        ```
        
        ## FINANCIAL EXPERTISE INJECTION
        Consider these key factors in your analysis:
        - **Market Regime**: Bull/bear/sideways, volatility clustering
        - **Sector Rotation**: Growth vs value, cyclical vs defensive
        - **Risk Environment**: Risk-on vs risk-off sentiment
        - **Liquidity Conditions**: Bid-ask spreads, volume patterns
        - **Temporal Factors**: Time of day, day of week, seasonal effects
        - **Correlation Dynamics**: Asset class relationships, diversification breakdown
        
        ## CONFIDENCE CALIBRATION GUIDE
        - 0.9-1.0: High conviction with multiple confirming signals
        - 0.7-0.89: Good confidence with clear patterns
        - 0.5-0.69: Moderate confidence with mixed signals
        - 0.3-0.49: Low confidence due to conflicting data
        - 0.1-0.29: Very uncertain, more data needed
        
        ## OUTPUT REQUIREMENTS
        CRITICAL: Respond ONLY with valid JSON. No explanatory text outside JSON.
        
        Response format:
        {
            "insight_type": "trend_analysis",
            "title": "Specific, actionable title (max 80 chars)",
            "content": "Detailed analysis with reasoning chain and specific evidence",
            "confidence_score": 0.85,
            "key_factors": ["Factor 1 with data", "Factor 2 with context", "Factor 3 with significance"],
            "recommended_actions": ["Specific action with timeframe", "Risk management step"],
            "reasoning_chain": ["Step 1: Observation", "Step 2: Analysis", "Step 3: Conclusion"],
            "risk_assessment": "Primary risks and mitigation strategies",
            "data_quality": "Assessment of input data reliability",
            "market_context": "Current market regime and relevance",
            "timeframe": "Short/Medium/Long-term analysis horizon"
        }
        
        ## EXAMPLE HIGH-QUALITY ANALYSIS
        Example of excellent financial insight:
        {
            "insight_type": "trend_analysis",
            "title": "Tech Sector Momentum Divergence Signals Rotation Risk",
            "content": "Analysis reveals a dangerous divergence in tech sector momentum. While headline indices remain elevated, underlying breadth has deteriorated with 60% of tech stocks below their 20-day moving averages. Volume patterns show distribution rather than accumulation, with smart money flows rotating toward defensive sectors. This technical breakdown, combined with elevated valuation metrics (avg P/E of 28x vs historical 22x), suggests a potential 10-15% correction risk over the next 3-6 weeks.",
            "confidence_score": 0.78,
            "key_factors": [
                "Breadth deterioration: 60% of tech stocks below 20-day MA",
                "Volume analysis: Distribution pattern in leading tech names",
                "Valuation concern: Sector P/E 27% above historical average"
            ],
            "recommended_actions": [
                "Reduce tech overweight by 25% over next 2 weeks",
                "Implement protective puts on QQQ (3-month duration)",
                "Rotate 15% allocation to defensive sectors (utilities, staples)"
            ],
            "reasoning_chain": [
                "Observed: Tech index vs breadth divergence",
                "Analyzed: Volume patterns suggest institutional selling",
                "Validated: Historical precedent for 15% corrections after similar setups",
                "Concluded: High probability of near-term weakness",
                "Action: Defensive repositioning with specific steps"
            ],
            "risk_assessment": "Primary risk: Continued momentum despite technical warnings. Mitigation: Gradual position reduction rather than wholesale exit.",
            "data_quality": "High confidence in breadth and volume data, moderate confidence in flow data",
            "market_context": "Late-cycle bull market with elevated volatility regime",
            "timeframe": "Medium-term (3-6 weeks) with long-term implications"
        }
        
        Analyze with this level of depth, specificity, and actionability.
        """
    
    def analyze_data_batch(self, mcp_records: List[MCPData]) -> List[Dict[str, Any]]:
        """Analyze a batch of MCP data with enhanced intelligence"""
        if not mcp_records:
            return []
        
        try:
            # Enhanced data preparation with market context
            data_analysis = self._prepare_enhanced_data_analysis(mcp_records)
            market_context = self._assess_market_context(mcp_records)
            
            insights = []
            
            # Generate sophisticated insights with context awareness
            trend_insight = self._advanced_trend_analysis(data_analysis, market_context, mcp_records)
            if trend_insight:
                insights.append(trend_insight)
            
            risk_insight = self._advanced_risk_assessment(data_analysis, market_context, mcp_records)
            if risk_insight:
                insights.append(risk_insight)
            
            opportunity_insight = self._advanced_opportunity_analysis(data_analysis, market_context, mcp_records)
            if opportunity_insight:
                insights.append(opportunity_insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error in enhanced analysis: {e}")
            return []
    
    def _prepare_enhanced_data_analysis(self, records: List[MCPData]) -> Dict[str, Any]:
        """Prepare sophisticated data analysis with statistical insights"""
        from collections import defaultdict
        import statistics
        
        analysis = {
            "total_records": len(records),
            "data_types": defaultdict(int),
            "time_span_hours": 0,
            "data_quality_score": 0,
            "statistical_summary": {},
            "pattern_indicators": {},
            "sample_data": []
        }
        
        # Enhanced data processing
        stock_prices = []
        volumes = []
        sentiment_scores = []
        
        for record in records:
            data = record.get_data()
            analysis["data_types"][record.data_type] += 1
            
            # Extract numerical data for statistical analysis
            if "price" in data:
                stock_prices.append(float(data["price"]))
            if "volume" in data:
                volumes.append(float(data["volume"]))
            if "sentiment_score" in data:
                sentiment_scores.append(float(data["sentiment_score"]))
            
            if len(analysis["sample_data"]) < 15:
                analysis["sample_data"].append(data)
        
        # Calculate statistical insights
        if stock_prices:
            analysis["statistical_summary"]["price_stats"] = {
                "mean": statistics.mean(stock_prices),
                "median": statistics.median(stock_prices),
                "stdev": statistics.stdev(stock_prices) if len(stock_prices) > 1 else 0,
                "range": max(stock_prices) - min(stock_prices)
            }
        
        if volumes:
            analysis["statistical_summary"]["volume_stats"] = {
                "mean": statistics.mean(volumes),
                "median": statistics.median(volumes),
                "volume_concentration": max(volumes) / statistics.mean(volumes) if volumes else 0
            }
        
        if sentiment_scores:
            analysis["statistical_summary"]["sentiment_stats"] = {
                "mean": statistics.mean(sentiment_scores),
                "extreme_readings": sum(1 for s in sentiment_scores if abs(s) > 0.7) / len(sentiment_scores)
            }
        
        # Calculate data quality score
        completeness = len([r for r in records if r.get_data()]) / len(records)
        timeliness = 1.0  # Assume recent data
        analysis["data_quality_score"] = (completeness + timeliness) / 2
        
        return analysis
    
    def _assess_market_context(self, records: List[MCPData]) -> Dict[str, Any]:
        """Assess current market context and regime"""
        context = {
            "market_regime": "unknown",
            "volatility_environment": "moderate",
            "dominant_themes": [],
            "risk_appetite": "neutral",
            "sector_dynamics": {},
            "temporal_factors": {}
        }
        
        # Analyze market regime based on data patterns
        sentiment_readings = []
        volatility_indicators = []
        
        for record in records:
            data = record.get_data()
            if "sentiment_score" in data:
                sentiment_readings.append(data["sentiment_score"])
            if "change_percent" in data:
                volatility_indicators.append(abs(data["change_percent"]))
        
        # Determine market regime
        if sentiment_readings:
            avg_sentiment = sum(sentiment_readings) / len(sentiment_readings)
            if avg_sentiment > 0.3:
                context["market_regime"] = "risk_on"
                context["risk_appetite"] = "high"
            elif avg_sentiment < -0.3:
                context["market_regime"] = "risk_off"
                context["risk_appetite"] = "low"
            else:
                context["market_regime"] = "neutral"
        
        # Assess volatility environment
        if volatility_indicators:
            avg_vol = sum(volatility_indicators) / len(volatility_indicators)
            if avg_vol > 3:
                context["volatility_environment"] = "high"
            elif avg_vol > 1.5:
                context["volatility_environment"] = "moderate"
            else:
                context["volatility_environment"] = "low"
        
        return context
    
    def _advanced_trend_analysis(self, data_analysis: Dict, market_context: Dict, records: List[MCPData]) -> Dict[str, Any]:
        """Generate sophisticated trend analysis with chain-of-thought reasoning"""
        prompt = f"""
        ## ADVANCED TREND ANALYSIS REQUEST
        
        Perform elite-level trend analysis using the systematic framework. Think like a senior portfolio manager.
        
        ### DATA ANALYSIS
        {json.dumps(data_analysis, indent=2)}
        
        ### MARKET CONTEXT
        {json.dumps(market_context, indent=2)}
        
        ### ANALYSIS REQUIREMENTS
        1. **Pattern Recognition**: Identify significant price/volume/sentiment patterns
        2. **Momentum Assessment**: Evaluate trend strength and sustainability
        3. **Divergence Analysis**: Look for warning signs or confirmation signals
        4. **Sector/Asset Rotation**: Identify shifting market leadership
        5. **Risk-Adjusted Perspective**: Consider volatility and drawdown risks
        
        ### THINKING PROCESS
        Follow the reasoning chain: OBSERVE → HYPOTHESIZE → VALIDATE → CONCLUDE → ACT
        
        ### FOCUS AREAS
        - Technical momentum and breadth indicators
        - Fundamental trend confirmation or divergence
        - Sentiment extreme readings and contrarian signals
        - Volume pattern analysis and institutional activity
        - Temporal context and seasonal factors
        
        Provide actionable trend analysis with specific evidence and quantified confidence.
        """
        
        return self._generate_enhanced_insight(prompt, "trend_analysis", records)
    
    def _advanced_risk_assessment(self, data_analysis: Dict, market_context: Dict, records: List[MCPData]) -> Dict[str, Any]:
        """Generate sophisticated risk assessment"""
        prompt = f"""
        ## COMPREHENSIVE RISK ASSESSMENT
        
        Conduct institutional-grade risk analysis. Think like a risk management committee.
        
        ### DATA FOR RISK ANALYSIS
        {json.dumps(data_analysis, indent=2)}
        
        ### MARKET RISK CONTEXT
        {json.dumps(market_context, indent=2)}
        
        ### RISK ASSESSMENT FRAMEWORK
        1. **Market Risk**: Directional exposure, beta sensitivity, correlation breakdown
        2. **Liquidity Risk**: Bid-ask spreads, market depth, stress scenarios
        3. **Volatility Risk**: Implied vs realized vol, volatility clustering
        4. **Concentration Risk**: Sector/geographic/factor concentration
        5. **Tail Risk**: Black swan events, fat-tail distributions
        6. **Behavioral Risk**: Sentiment extremes, crowding, positioning
        
        ### RISK QUANTIFICATION
        - Identify specific risk factors with probability estimates
        - Quantify potential downside scenarios (10th percentile outcomes)
        - Assess risk-reward asymmetry
        - Recommend hedging strategies and position sizing
        
        Focus on actionable risk management with specific mitigation strategies.
        """
        
        return self._generate_enhanced_insight(prompt, "risk_assessment", records)
    
    def _advanced_opportunity_analysis(self, data_analysis: Dict, market_context: Dict, records: List[MCPData]) -> Dict[str, Any]:
        """Generate sophisticated opportunity identification"""
        prompt = f"""
        ## SOPHISTICATED OPPORTUNITY ANALYSIS
        
        Identify alpha-generating opportunities like an institutional research team.
        
        ### OPPORTUNITY DATA
        {json.dumps(data_analysis, indent=2)}
        
        ### MARKET OPPORTUNITY CONTEXT
        {json.dumps(market_context, indent=2)}
        
        ### OPPORTUNITY FRAMEWORK
        1. **Value Opportunities**: Fundamental mispricing, ratio analysis
        2. **Momentum Opportunities**: Trend continuation, breakout setups
        3. **Mean Reversion**: Oversold/overbought extremes, sentiment reversals
        4. **Arbitrage**: Statistical arbitrage, pairs trading, calendar spreads
        5. **Thematic Opportunities**: Sector rotation, macro trends, policy changes
        6. **Volatility Opportunities**: Vol trading, option strategies
        
        ### OPPORTUNITY CRITERIA
        - Risk-adjusted return potential (Sharpe ratio > 1.5)
        - Probability of success (>60% historical hit rate)
        - Time horizon and catalyst identification
        - Position sizing and risk management
        - Exit strategy and profit-taking levels
        
        Focus on asymmetric risk-reward opportunities with specific entry/exit criteria.
        """
        
        return self._generate_enhanced_insight(prompt, "opportunity", records)
    
    def _generate_enhanced_insight(self, prompt: str, insight_type: str, records: List[MCPData]) -> Dict[str, Any]:
        """Generate insight with enhanced reasoning and validation"""
        try:
            messages = [
                SystemMessage(content=self.advanced_system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Enhanced response processing
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            logger.info(f"Enhanced AI Response ({insight_type}): {content[:200]}...")
            
            # Parse and validate enhanced JSON structure
            insight_data = json.loads(content)
            
            # Validate required enhanced fields
            required_fields = ["reasoning_chain", "risk_assessment", "data_quality", "market_context", "timeframe"]
            for field in required_fields:
                if field not in insight_data:
                    insight_data[field] = f"Not specified for {field}"
            
            # Add enhanced metadata
            insight_data["source_record_ids"] = [r.id for r in records]
            insight_data["generated_at"] = datetime.utcnow().isoformat()
            insight_data["model"] = "gemini-2.0-flash-exp-enhanced"
            insight_data["analysis_version"] = "2.0_advanced"
            
            return insight_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Enhanced agent JSON parsing error: {e}")
            logger.error(f"Raw enhanced response: {response.content}")
            return None
        except Exception as e:
            logger.error(f"Enhanced agent error: {e}")
            return None
    
    def store_enhanced_insights(self, insights: List[Dict[str, Any]]) -> List[int]:
        """Store enhanced insights with additional metadata"""
        stored_ids = []
        db = SessionLocal()
        
        try:
            for insight_data in insights:
                ai_insight = AIInsight(
                    insight_type=insight_data.get("insight_type", "general"),
                    title=insight_data.get("title", "Enhanced AI Generated Insight"),
                    content=insight_data.get("content", ""),
                    confidence_score=insight_data.get("confidence_score", 0.0),
                    timestamp=datetime.utcnow()
                )
                
                # Set source IDs
                source_ids = insight_data.get("source_record_ids", [])
                ai_insight.set_source_ids(source_ids)
                
                # Enhanced metadata with new fields
                metadata = {
                    "key_factors": insight_data.get("key_factors", []),
                    "recommended_actions": insight_data.get("recommended_actions", []),
                    "reasoning_chain": insight_data.get("reasoning_chain", []),
                    "risk_assessment": insight_data.get("risk_assessment", ""),
                    "data_quality": insight_data.get("data_quality", ""),
                    "market_context": insight_data.get("market_context", ""),
                    "timeframe": insight_data.get("timeframe", ""),
                    "model": insight_data.get("model", "unknown"),
                    "analysis_version": insight_data.get("analysis_version", "1.0"),
                    "generated_at": insight_data.get("generated_at")
                }
                ai_insight.set_metadata(metadata)
                
                db.add(ai_insight)
                db.flush()
                stored_ids.append(ai_insight.id)
            
            db.commit()
            logger.info(f"Stored {len(insights)} enhanced insights in database")
            
        except Exception as e:
            logger.error(f"Error storing enhanced insights: {e}")
            db.rollback()
        finally:
            db.close()
        
        return stored_ids

# Enhanced singleton instance
enhanced_ai_agent = EnhancedAIInsightAgent() 