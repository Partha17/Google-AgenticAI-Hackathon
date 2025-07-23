"""
Market Analysis Agent - ADK Implementation
Sophisticated agent for technical and fundamental market analysis
"""

import asyncio
import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from adk_agents.agent_config import adk_config

logger = logging.getLogger(__name__)

class MarketAnalysisAgent:
    """ADK-based Market Analysis Agent for comprehensive market intelligence"""
    
    def __init__(self):
        self.agent_id = "market_analysis_agent"
        self.config = adk_config.get_agent_definitions()[self.agent_id]
        
    async def analyze_market_trends(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive market trend analysis
        Main tool function for market analysis
        """
        try:
            logger.info("Starting comprehensive market trend analysis...")
            
            analysis_results = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "market_regime": "neutral",
                "trend_direction": "sideways",
                "trend_strength": 0.5,
                "confidence_score": 0.5,
                "technical_indicators": {},
                "fundamental_metrics": {},
                "sector_analysis": {},
                "market_outlook": {},
                "key_insights": []
            }
            
            # Extract market data from financial information
            market_data = self._extract_market_data(financial_data)
            
            # Perform technical analysis
            technical_analysis = await self._perform_technical_analysis(market_data)
            analysis_results["technical_indicators"] = technical_analysis
            
            # Perform fundamental analysis
            fundamental_analysis = await self._perform_fundamental_analysis(market_data)
            analysis_results["fundamental_metrics"] = fundamental_analysis
            
            # Analyze sector dynamics
            sector_analysis = await self._analyze_sector_dynamics(market_data)
            analysis_results["sector_analysis"] = sector_analysis
            
            # Determine market regime and trend
            market_regime = self._determine_market_regime(technical_analysis, fundamental_analysis)
            analysis_results["market_regime"] = market_regime["regime"]
            analysis_results["trend_direction"] = market_regime["trend"]
            analysis_results["trend_strength"] = market_regime["strength"]
            analysis_results["confidence_score"] = market_regime["confidence"]
            
            # Generate market outlook
            outlook = await self._generate_market_outlook(analysis_results)
            analysis_results["market_outlook"] = outlook
            
            # Synthesize key insights
            insights = self._synthesize_key_insights(analysis_results)
            analysis_results["key_insights"] = insights
            
            logger.info(f"Market analysis completed - Regime: {analysis_results['market_regime']}, Trend: {analysis_results['trend_direction']}")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in market trend analysis: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def analyze_portfolio_performance(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze portfolio performance metrics and attribution
        """
        try:
            logger.info("Starting portfolio performance analysis...")
            
            performance_analysis = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "performance_metrics": {},
                "attribution_analysis": {},
                "benchmark_comparison": {},
                "risk_adjusted_returns": {},
                "recommendations": []
            }
            
            # Extract portfolio data
            portfolio_data = self._extract_portfolio_data(financial_data)
            
            # Calculate performance metrics
            performance_metrics = await self._calculate_performance_metrics(portfolio_data)
            performance_analysis["performance_metrics"] = performance_metrics
            
            # Perform attribution analysis
            attribution = await self._perform_attribution_analysis(portfolio_data)
            performance_analysis["attribution_analysis"] = attribution
            
            # Benchmark comparison
            benchmark_comparison = await self._compare_to_benchmarks(performance_metrics)
            performance_analysis["benchmark_comparison"] = benchmark_comparison
            
            # Risk-adjusted returns
            risk_adjusted = await self._calculate_risk_adjusted_returns(portfolio_data)
            performance_analysis["risk_adjusted_returns"] = risk_adjusted
            
            # Generate recommendations
            recommendations = self._generate_performance_recommendations(performance_analysis)
            performance_analysis["recommendations"] = recommendations
            
            logger.info("Portfolio performance analysis completed")
            return performance_analysis
            
        except Exception as e:
            logger.error(f"Error in portfolio performance analysis: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def identify_market_opportunities(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify market opportunities and investment ideas
        """
        try:
            logger.info("Identifying market opportunities...")
            
            opportunity_analysis = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "opportunities_identified": 0,
                "opportunity_categories": {},
                "investment_themes": [],
                "tactical_opportunities": [],
                "strategic_opportunities": [],
                "risk_reward_assessment": {}
            }
            
            market_data = self._extract_market_data(financial_data)
            
            # Identify value opportunities
            value_opportunities = await self._identify_value_opportunities(market_data)
            opportunity_analysis["opportunity_categories"]["value"] = value_opportunities
            
            # Identify momentum opportunities
            momentum_opportunities = await self._identify_momentum_opportunities(market_data)
            opportunity_analysis["opportunity_categories"]["momentum"] = momentum_opportunities
            
            # Identify thematic opportunities
            thematic_opportunities = await self._identify_thematic_opportunities(market_data)
            opportunity_analysis["opportunity_categories"]["thematic"] = thematic_opportunities
            
            # Categorize by timeframe
            tactical_ops, strategic_ops = self._categorize_by_timeframe(opportunity_analysis["opportunity_categories"])
            opportunity_analysis["tactical_opportunities"] = tactical_ops
            opportunity_analysis["strategic_opportunities"] = strategic_ops
            
            # Investment themes
            themes = self._extract_investment_themes(opportunity_analysis["opportunity_categories"])
            opportunity_analysis["investment_themes"] = themes
            
            # Risk-reward assessment
            risk_reward = await self._assess_opportunity_risk_reward(opportunity_analysis)
            opportunity_analysis["risk_reward_assessment"] = risk_reward
            
            # Count total opportunities
            total_opportunities = sum(len(cat.get("opportunities", [])) for cat in opportunity_analysis["opportunity_categories"].values())
            opportunity_analysis["opportunities_identified"] = total_opportunities
            
            logger.info(f"Identified {total_opportunities} market opportunities")
            return opportunity_analysis
            
        except Exception as e:
            logger.error(f"Error identifying market opportunities: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extract_market_data(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market-relevant data from financial information"""
        market_data = {
            "net_worth_trend": [],
            "transaction_patterns": {},
            "asset_allocation": {},
            "performance_indicators": {},
            "volatility_measures": {}
        }
        
        try:
            data_sources = financial_data.get("data_sources", [])
            
            for source in data_sources:
                if not source.get("success", False):
                    continue
                
                source_type = source.get("type", "")
                
                # Extract net worth data for trend analysis
                if source_type == "net_worth" and "data" in financial_data:
                    nw_data = financial_data["data"]
                    market_data["net_worth_trend"].append({
                        "timestamp": datetime.utcnow().isoformat(),
                        "value": nw_data.get("total_net_worth", 0),
                        "assets": nw_data.get("total_assets", 0),
                        "liabilities": nw_data.get("total_liabilities", 0)
                    })
                    
                    # Asset allocation analysis
                    if "assets" in nw_data:
                        market_data["asset_allocation"] = nw_data["assets"]
                
                # Extract transaction patterns
                elif source_type == "bank_transactions" and "data" in financial_data:
                    txn_data = financial_data["data"]
                    market_data["transaction_patterns"] = {
                        "monthly_volume": txn_data.get("total_amount", 0),
                        "transaction_count": txn_data.get("transaction_count", 0),
                        "average_transaction": txn_data.get("total_amount", 0) / max(txn_data.get("transaction_count", 1), 1)
                    }
                
                # Extract mutual fund performance
                elif source_type == "mutual_fund_transactions" and "data" in financial_data:
                    mf_data = financial_data["data"]
                    market_data["performance_indicators"]["mutual_funds"] = {
                        "fund_count": mf_data.get("fund_count", 0),
                        "total_investment": mf_data.get("total_investment", 0)
                    }
        
        except Exception as e:
            logger.error(f"Error extracting market data: {e}")
        
        return market_data
    
    def _extract_portfolio_data(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract portfolio-specific data for performance analysis"""
        portfolio_data = {
            "current_value": 0,
            "asset_breakdown": {},
            "historical_values": [],
            "cash_flows": [],
            "holdings": {}
        }
        
        try:
            data_sources = financial_data.get("data_sources", [])
            
            for source in data_sources:
                if not source.get("success", False):
                    continue
                
                source_type = source.get("type", "")
                
                if source_type == "net_worth" and "data" in financial_data:
                    nw_data = financial_data["data"]
                    portfolio_data["current_value"] = nw_data.get("total_net_worth", 0)
                    portfolio_data["asset_breakdown"] = nw_data.get("assets", {})
                
                elif source_type == "mutual_fund_transactions" and "data" in financial_data:
                    mf_data = financial_data["data"]
                    portfolio_data["holdings"]["mutual_funds"] = mf_data
                
                elif source_type == "epf_details" and "data" in financial_data:
                    epf_data = financial_data["data"]
                    portfolio_data["holdings"]["epf"] = epf_data
        
        except Exception as e:
            logger.error(f"Error extracting portfolio data: {e}")
        
        return portfolio_data
    
    async def _perform_technical_analysis(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform technical analysis on market data"""
        try:
            technical_indicators = {
                "trend_indicators": {},
                "momentum_indicators": {},
                "volatility_indicators": {},
                "volume_indicators": {}
            }
            
            # Trend analysis based on net worth progression
            net_worth_trend = market_data.get("net_worth_trend", [])
            if net_worth_trend:
                values = [point.get("value", 0) for point in net_worth_trend]
                if len(values) > 1:
                    # Simple trend calculation
                    trend_slope = (values[-1] - values[0]) / len(values) if len(values) > 1 else 0
                    trend_direction = "up" if trend_slope > 0 else "down" if trend_slope < 0 else "sideways"
                    
                    technical_indicators["trend_indicators"] = {
                        "slope": trend_slope,
                        "direction": trend_direction,
                        "strength": abs(trend_slope) / max(values) if max(values) > 0 else 0
                    }
            
            # Momentum analysis based on transaction patterns
            transaction_patterns = market_data.get("transaction_patterns", {})
            if transaction_patterns:
                avg_transaction = transaction_patterns.get("average_transaction", 0)
                monthly_volume = transaction_patterns.get("monthly_volume", 0)
                
                momentum_score = 0.5  # Neutral
                if avg_transaction > 10000:  # High value transactions
                    momentum_score += 0.2
                if monthly_volume > 100000:  # High volume
                    momentum_score += 0.2
                
                technical_indicators["momentum_indicators"] = {
                    "momentum_score": min(momentum_score, 1.0),
                    "transaction_velocity": transaction_patterns.get("transaction_count", 0),
                    "volume_trend": "increasing" if monthly_volume > 50000 else "stable"
                }
            
            # Volatility analysis
            if net_worth_trend and len(net_worth_trend) > 1:
                values = [point.get("value", 0) for point in net_worth_trend]
                if len(values) > 1:
                    volatility = statistics.stdev(values) / statistics.mean(values) if statistics.mean(values) > 0 else 0
                    technical_indicators["volatility_indicators"] = {
                        "volatility": volatility,
                        "stability": "high" if volatility < 0.1 else "medium" if volatility < 0.3 else "low"
                    }
            
            return technical_indicators
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return {"error": str(e)}
    
    async def _perform_fundamental_analysis(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform fundamental analysis on financial data"""
        try:
            fundamental_metrics = {
                "valuation_metrics": {},
                "quality_metrics": {},
                "growth_metrics": {},
                "financial_strength": {}
            }
            
            # Asset allocation analysis
            asset_allocation = market_data.get("asset_allocation", {})
            if asset_allocation:
                total_assets = sum(asset_allocation.values())
                
                # Calculate diversification score
                if total_assets > 0:
                    # Herfindahl-Hirschman Index for concentration
                    hhi = sum((value / total_assets) ** 2 for value in asset_allocation.values())
                    diversification_score = 1 - hhi
                    
                    fundamental_metrics["quality_metrics"] = {
                        "diversification_score": diversification_score,
                        "concentration_risk": "low" if hhi < 0.3 else "medium" if hhi < 0.6 else "high",
                        "asset_count": len(asset_allocation)
                    }
            
            # Financial strength metrics
            transaction_patterns = market_data.get("transaction_patterns", {})
            if transaction_patterns:
                monthly_volume = transaction_patterns.get("monthly_volume", 0)
                transaction_count = transaction_patterns.get("transaction_count", 0)
                
                # Liquidity assessment
                liquidity_score = min(transaction_count / 50, 1.0)  # Normalized to 50 transactions
                
                fundamental_metrics["financial_strength"] = {
                    "liquidity_score": liquidity_score,
                    "activity_level": "high" if transaction_count > 30 else "medium" if transaction_count > 10 else "low",
                    "cash_flow_stability": "stable" if monthly_volume > 20000 else "variable"
                }
            
            # Growth metrics
            net_worth_trend = market_data.get("net_worth_trend", [])
            if len(net_worth_trend) > 1:
                initial_value = net_worth_trend[0].get("value", 0)
                current_value = net_worth_trend[-1].get("value", 0)
                
                if initial_value > 0:
                    growth_rate = (current_value - initial_value) / initial_value
                    fundamental_metrics["growth_metrics"] = {
                        "net_worth_growth": growth_rate,
                        "growth_trend": "positive" if growth_rate > 0 else "negative" if growth_rate < 0 else "flat"
                    }
            
            return fundamental_metrics
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis: {e}")
            return {"error": str(e)}
    
    async def _analyze_sector_dynamics(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sector-specific dynamics and allocation"""
        try:
            sector_analysis = {
                "sector_allocation": {},
                "sector_performance": {},
                "rotation_signals": {},
                "recommendations": []
            }
            
            # Analyze asset allocation by sector/type
            asset_allocation = market_data.get("asset_allocation", {})
            performance_indicators = market_data.get("performance_indicators", {})
            
            if asset_allocation:
                total_assets = sum(asset_allocation.values())
                
                # Map assets to sectors (simplified)
                sector_mapping = {
                    "equity": ["stocks", "equity_mutual_funds", "shares"],
                    "fixed_income": ["bonds", "fixed_deposits", "debt_funds"],
                    "alternative": ["real_estate", "commodities", "crypto"],
                    "cash": ["savings", "current_account", "liquid_funds"]
                }
                
                sector_allocation = {}
                for sector, asset_types in sector_mapping.items():
                    sector_value = sum(asset_allocation.get(asset_type, 0) for asset_type in asset_types)
                    if total_assets > 0:
                        sector_allocation[sector] = sector_value / total_assets
                
                sector_analysis["sector_allocation"] = sector_allocation
                
                # Generate sector recommendations
                recommendations = []
                if sector_allocation.get("cash", 0) > 0.3:
                    recommendations.append("Consider reducing cash allocation and investing in growth assets")
                if sector_allocation.get("equity", 0) < 0.4:
                    recommendations.append("Consider increasing equity allocation for long-term growth")
                if sector_allocation.get("fixed_income", 0) > 0.5:
                    recommendations.append("Review fixed income allocation for optimal risk-return balance")
                
                sector_analysis["recommendations"] = recommendations
            
            return sector_analysis
            
        except Exception as e:
            logger.error(f"Error in sector analysis: {e}")
            return {"error": str(e)}
    
    def _determine_market_regime(self, technical_analysis: Dict[str, Any], 
                                fundamental_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Determine overall market regime and trend"""
        try:
            regime_analysis = {
                "regime": "neutral",
                "trend": "sideways",
                "strength": 0.5,
                "confidence": 0.5
            }
            
            # Extract key indicators
            trend_indicators = technical_analysis.get("trend_indicators", {})
            momentum_indicators = technical_analysis.get("momentum_indicators", {})
            quality_metrics = fundamental_analysis.get("quality_metrics", {})
            
            # Determine trend direction
            trend_direction = trend_indicators.get("direction", "sideways")
            trend_strength = trend_indicators.get("strength", 0.5)
            momentum_score = momentum_indicators.get("momentum_score", 0.5)
            
            regime_analysis["trend"] = trend_direction
            regime_analysis["strength"] = trend_strength
            
            # Determine market regime
            if momentum_score > 0.7 and trend_strength > 0.3:
                regime_analysis["regime"] = "risk_on"
                regime_analysis["confidence"] = 0.8
            elif momentum_score < 0.3 or trend_strength < 0.1:
                regime_analysis["regime"] = "risk_off"
                regime_analysis["confidence"] = 0.7
            else:
                regime_analysis["regime"] = "neutral"
                regime_analysis["confidence"] = 0.6
            
            return regime_analysis
            
        except Exception as e:
            logger.error(f"Error determining market regime: {e}")
            return {
                "regime": "unknown",
                "trend": "unknown",
                "strength": 0.5,
                "confidence": 0.3,
                "error": str(e)
            }
    
    async def _generate_market_outlook(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate forward-looking market outlook"""
        try:
            outlook = {
                "short_term": {"timeframe": "1-3 months", "outlook": "neutral", "key_factors": []},
                "medium_term": {"timeframe": "3-12 months", "outlook": "neutral", "key_factors": []},
                "long_term": {"timeframe": "1-3 years", "outlook": "neutral", "key_factors": []},
                "key_themes": [],
                "risk_factors": [],
                "opportunity_areas": []
            }
            
            market_regime = analysis_results.get("market_regime", "neutral")
            trend_direction = analysis_results.get("trend_direction", "sideways")
            trend_strength = analysis_results.get("trend_strength", 0.5)
            
            # Short-term outlook
            if market_regime == "risk_on" and trend_direction == "up":
                outlook["short_term"]["outlook"] = "positive"
                outlook["short_term"]["key_factors"] = ["Strong momentum", "Positive trend"]
            elif market_regime == "risk_off" or trend_direction == "down":
                outlook["short_term"]["outlook"] = "cautious"
                outlook["short_term"]["key_factors"] = ["Risk-off sentiment", "Downward pressure"]
            else:
                outlook["short_term"]["key_factors"] = ["Mixed signals", "Range-bound movement"]
            
            # Medium-term outlook based on fundamentals
            fundamental_metrics = analysis_results.get("fundamental_metrics", {})
            quality_metrics = fundamental_metrics.get("quality_metrics", {})
            
            if quality_metrics.get("diversification_score", 0) > 0.6:
                outlook["medium_term"]["outlook"] = "positive"
                outlook["medium_term"]["key_factors"] = ["Good diversification", "Quality fundamentals"]
            else:
                outlook["medium_term"]["outlook"] = "neutral"
                outlook["medium_term"]["key_factors"] = ["Need for improved diversification"]
            
            # Long-term outlook
            growth_metrics = fundamental_metrics.get("growth_metrics", {})
            if growth_metrics.get("net_worth_growth", 0) > 0:
                outlook["long_term"]["outlook"] = "positive"
                outlook["long_term"]["key_factors"] = ["Positive growth trajectory", "Wealth accumulation"]
            else:
                outlook["long_term"]["outlook"] = "neutral"
                outlook["long_term"]["key_factors"] = ["Focus on growth acceleration needed"]
            
            # Key themes
            outlook["key_themes"] = [
                "Portfolio optimization and diversification",
                "Risk-adjusted return enhancement",
                "Systematic wealth building"
            ]
            
            # Risk factors
            outlook["risk_factors"] = [
                "Market volatility",
                "Concentration risk",
                "Liquidity constraints"
            ]
            
            # Opportunity areas
            outlook["opportunity_areas"] = [
                "Asset class diversification",
                "Systematic investment planning",
                "Risk management optimization"
            ]
            
            return outlook
            
        except Exception as e:
            logger.error(f"Error generating market outlook: {e}")
            return {"error": str(e)}
    
    def _synthesize_key_insights(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Synthesize key insights from all analysis components"""
        try:
            insights = []
            
            # Market regime insight
            market_regime = analysis_results.get("market_regime", "neutral")
            trend_direction = analysis_results.get("trend_direction", "sideways")
            confidence = analysis_results.get("confidence_score", 0.5)
            
            insights.append({
                "category": "market_regime",
                "title": f"Current Market Environment: {market_regime.title()}",
                "description": f"Market is in {market_regime} regime with {trend_direction} trend",
                "confidence": confidence,
                "actionable": True,
                "timeframe": "current"
            })
            
            # Technical analysis insights
            technical_indicators = analysis_results.get("technical_indicators", {})
            momentum_indicators = technical_indicators.get("momentum_indicators", {})
            
            if momentum_indicators:
                momentum_score = momentum_indicators.get("momentum_score", 0.5)
                volume_trend = momentum_indicators.get("volume_trend", "stable")
                
                insights.append({
                    "category": "momentum",
                    "title": f"Momentum Analysis: {volume_trend.title()} Activity",
                    "description": f"Current momentum score: {momentum_score:.1%}, volume trend: {volume_trend}",
                    "confidence": 0.7,
                    "actionable": True,
                    "timeframe": "short_term"
                })
            
            # Fundamental insights
            fundamental_metrics = analysis_results.get("fundamental_metrics", {})
            quality_metrics = fundamental_metrics.get("quality_metrics", {})
            
            if quality_metrics:
                diversification_score = quality_metrics.get("diversification_score", 0)
                concentration_risk = quality_metrics.get("concentration_risk", "medium")
                
                insights.append({
                    "category": "diversification",
                    "title": f"Portfolio Diversification: {concentration_risk.title()} Risk",
                    "description": f"Diversification score: {diversification_score:.1%}, concentration risk: {concentration_risk}",
                    "confidence": 0.8,
                    "actionable": True,
                    "timeframe": "medium_term"
                })
            
            # Sector analysis insights
            sector_analysis = analysis_results.get("sector_analysis", {})
            sector_recommendations = sector_analysis.get("recommendations", [])
            
            if sector_recommendations:
                insights.append({
                    "category": "sector_allocation",
                    "title": "Sector Allocation Optimization",
                    "description": f"Key recommendations: {', '.join(sector_recommendations[:2])}",
                    "confidence": 0.7,
                    "actionable": True,
                    "timeframe": "medium_term"
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error synthesizing insights: {e}")
            return []
    
    # Additional methods for portfolio performance and opportunity identification
    
    async def _calculate_performance_metrics(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate key portfolio performance metrics"""
        try:
            metrics = {
                "total_return": 0.0,
                "annualized_return": 0.0,
                "volatility": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0
            }
            
            current_value = portfolio_data.get("current_value", 0)
            historical_values = portfolio_data.get("historical_values", [])
            
            if historical_values and len(historical_values) > 1:
                initial_value = historical_values[0]
                if initial_value > 0:
                    total_return = (current_value - initial_value) / initial_value
                    metrics["total_return"] = total_return
                    
                    # Simple annualized return calculation
                    periods = len(historical_values)
                    if periods > 1:
                        metrics["annualized_return"] = ((1 + total_return) ** (12 / periods)) - 1
                
                # Calculate volatility
                if len(historical_values) > 2:
                    returns = []
                    for i in range(1, len(historical_values)):
                        if historical_values[i-1] > 0:
                            returns.append((historical_values[i] - historical_values[i-1]) / historical_values[i-1])
                    
                    if returns:
                        metrics["volatility"] = statistics.stdev(returns) if len(returns) > 1 else 0
                        
                        # Simple Sharpe ratio calculation (assuming 3% risk-free rate)
                        excess_return = metrics["annualized_return"] - 0.03
                        if metrics["volatility"] > 0:
                            metrics["sharpe_ratio"] = excess_return / metrics["volatility"]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {"error": str(e)}
    
    async def _perform_attribution_analysis(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform performance attribution analysis"""
        try:
            attribution = {
                "asset_class_contribution": {},
                "security_selection": {},
                "allocation_effect": {},
                "interaction_effect": {}
            }
            
            asset_breakdown = portfolio_data.get("asset_breakdown", {})
            if asset_breakdown:
                total_value = sum(asset_breakdown.values())
                
                # Calculate asset class contributions
                for asset_class, value in asset_breakdown.items():
                    weight = value / total_value if total_value > 0 else 0
                    # Simplified contribution calculation
                    attribution["asset_class_contribution"][asset_class] = {
                        "weight": weight,
                        "contribution": weight * 0.08  # Assumed 8% average return
                    }
            
            return attribution
            
        except Exception as e:
            logger.error(f"Error in attribution analysis: {e}")
            return {"error": str(e)}
    
    async def _compare_to_benchmarks(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Compare portfolio performance to relevant benchmarks"""
        try:
            # Simplified benchmark comparison
            benchmarks = {
                "nifty_50": {"return": 0.12, "volatility": 0.18},
                "balanced_fund": {"return": 0.10, "volatility": 0.12},
                "fixed_deposit": {"return": 0.06, "volatility": 0.02}
            }
            
            comparison = {}
            portfolio_return = performance_metrics.get("annualized_return", 0)
            portfolio_vol = performance_metrics.get("volatility", 0)
            
            for benchmark_name, benchmark_metrics in benchmarks.items():
                comparison[benchmark_name] = {
                    "return_difference": portfolio_return - benchmark_metrics["return"],
                    "volatility_difference": portfolio_vol - benchmark_metrics["volatility"],
                    "risk_adjusted_outperformance": (portfolio_return - benchmark_metrics["return"]) / max(benchmark_metrics["volatility"], 0.01)
                }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error in benchmark comparison: {e}")
            return {"error": str(e)}
    
    async def _calculate_risk_adjusted_returns(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate various risk-adjusted return metrics"""
        try:
            risk_adjusted = {
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0,
                "information_ratio": 0.0,
                "calmar_ratio": 0.0
            }
            
            # This would require more historical data for proper calculation
            # Placeholder implementation
            current_value = portfolio_data.get("current_value", 0)
            if current_value > 0:
                risk_adjusted["sharpe_ratio"] = 0.5  # Placeholder
                risk_adjusted["sortino_ratio"] = 0.6  # Placeholder
            
            return risk_adjusted
            
        except Exception as e:
            logger.error(f"Error calculating risk-adjusted returns: {e}")
            return {"error": str(e)}
    
    def _generate_performance_recommendations(self, performance_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on performance analysis"""
        recommendations = []
        
        try:
            performance_metrics = performance_analysis.get("performance_metrics", {})
            benchmark_comparison = performance_analysis.get("benchmark_comparison", {})
            
            # Performance-based recommendations
            total_return = performance_metrics.get("total_return", 0)
            volatility = performance_metrics.get("volatility", 0)
            sharpe_ratio = performance_metrics.get("sharpe_ratio", 0)
            
            if total_return < 0:
                recommendations.append({
                    "category": "performance",
                    "priority": "high",
                    "recommendation": "Review portfolio allocation and consider rebalancing",
                    "rationale": "Negative returns indicate need for portfolio optimization"
                })
            
            if volatility > 0.25:
                recommendations.append({
                    "category": "risk",
                    "priority": "medium",
                    "recommendation": "Consider reducing portfolio volatility through diversification",
                    "rationale": "High volatility may indicate concentrated positions"
                })
            
            if sharpe_ratio < 0.5:
                recommendations.append({
                    "category": "efficiency",
                    "priority": "medium",
                    "recommendation": "Improve risk-adjusted returns through better asset selection",
                    "rationale": "Low Sharpe ratio suggests suboptimal risk-return profile"
                })
            
            # Benchmark comparison recommendations
            for benchmark, comparison in benchmark_comparison.items():
                return_diff = comparison.get("return_difference", 0)
                if return_diff < -0.02:  # Underperforming by more than 2%
                    recommendations.append({
                        "category": "benchmark",
                        "priority": "medium",
                        "recommendation": f"Consider indexing strategy or factor exposure to match {benchmark}",
                        "rationale": f"Underperforming {benchmark} by {return_diff:.1%}"
                    })
        
        except Exception as e:
            logger.error(f"Error generating performance recommendations: {e}")
        
        return recommendations
    
    # Opportunity identification methods
    
    async def _identify_value_opportunities(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify value-based investment opportunities"""
        try:
            value_opportunities = {
                "opportunities": [],
                "screening_criteria": ["undervalued assets", "high dividend yield", "low price-to-book"],
                "risk_level": "medium"
            }
            
            # Simplified value opportunity identification
            asset_allocation = market_data.get("asset_allocation", {})
            
            # If heavily allocated to cash, suggest value investing
            if asset_allocation:
                total_assets = sum(asset_allocation.values())
                cash_allocation = asset_allocation.get("cash", 0) / total_assets if total_assets > 0 else 0
                
                if cash_allocation > 0.3:
                    value_opportunities["opportunities"].append({
                        "opportunity": "Deploy excess cash in undervalued equity positions",
                        "rationale": f"High cash allocation ({cash_allocation:.1%}) suggests opportunity to invest in value stocks",
                        "expected_return": "8-12% annually",
                        "timeframe": "12-24 months"
                    })
            
            return value_opportunities
            
        except Exception as e:
            logger.error(f"Error identifying value opportunities: {e}")
            return {"error": str(e)}
    
    async def _identify_momentum_opportunities(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify momentum-based opportunities"""
        try:
            momentum_opportunities = {
                "opportunities": [],
                "screening_criteria": ["price momentum", "earnings momentum", "sector rotation"],
                "risk_level": "medium_high"
            }
            
            # Analyze transaction patterns for momentum signals
            transaction_patterns = market_data.get("transaction_patterns", {})
            
            if transaction_patterns.get("transaction_count", 0) > 20:
                momentum_opportunities["opportunities"].append({
                    "opportunity": "Capitalize on high activity momentum",
                    "rationale": "High transaction activity suggests momentum in financial behavior",
                    "expected_return": "10-15% annually",
                    "timeframe": "6-12 months"
                })
            
            return momentum_opportunities
            
        except Exception as e:
            logger.error(f"Error identifying momentum opportunities: {e}")
            return {"error": str(e)}
    
    async def _identify_thematic_opportunities(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify thematic investment opportunities"""
        try:
            thematic_opportunities = {
                "opportunities": [],
                "themes": ["technology", "healthcare", "sustainability", "emerging_markets"],
                "risk_level": "medium"
            }
            
            # Suggest thematic opportunities based on portfolio gaps
            thematic_opportunities["opportunities"].extend([
                {
                    "opportunity": "Technology sector exposure",
                    "rationale": "Digital transformation theme continues to drive growth",
                    "expected_return": "12-18% annually",
                    "timeframe": "24-36 months"
                },
                {
                    "opportunity": "ESG-focused investments",
                    "rationale": "Sustainability theme gaining momentum in Indian markets",
                    "expected_return": "8-14% annually",
                    "timeframe": "36-60 months"
                }
            ])
            
            return thematic_opportunities
            
        except Exception as e:
            logger.error(f"Error identifying thematic opportunities: {e}")
            return {"error": str(e)}
    
    def _categorize_by_timeframe(self, opportunity_categories: Dict[str, Any]) -> tuple:
        """Categorize opportunities by timeframe"""
        tactical_opportunities = []
        strategic_opportunities = []
        
        try:
            for category, category_data in opportunity_categories.items():
                opportunities = category_data.get("opportunities", [])
                
                for opp in opportunities:
                    timeframe = opp.get("timeframe", "")
                    
                    if "6" in timeframe or "12" in timeframe:
                        tactical_opportunities.append({
                            "category": category,
                            "opportunity": opp.get("opportunity", ""),
                            "timeframe": timeframe,
                            "expected_return": opp.get("expected_return", "")
                        })
                    else:
                        strategic_opportunities.append({
                            "category": category,
                            "opportunity": opp.get("opportunity", ""),
                            "timeframe": timeframe,
                            "expected_return": opp.get("expected_return", "")
                        })
        
        except Exception as e:
            logger.error(f"Error categorizing opportunities by timeframe: {e}")
        
        return tactical_opportunities, strategic_opportunities
    
    def _extract_investment_themes(self, opportunity_categories: Dict[str, Any]) -> List[str]:
        """Extract dominant investment themes"""
        themes = []
        
        try:
            # Extract themes from thematic opportunities
            thematic_data = opportunity_categories.get("thematic", {})
            theme_list = thematic_data.get("themes", [])
            themes.extend(theme_list)
            
            # Add themes based on other categories
            if "value" in opportunity_categories:
                themes.append("value_investing")
            if "momentum" in opportunity_categories:
                themes.append("momentum_strategies")
            
            # Remove duplicates and limit to top themes
            themes = list(set(themes))[:5]
        
        except Exception as e:
            logger.error(f"Error extracting investment themes: {e}")
        
        return themes
    
    async def _assess_opportunity_risk_reward(self, opportunity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk-reward profile of identified opportunities"""
        try:
            risk_reward = {
                "overall_risk_level": "medium",
                "expected_return_range": "8-12%",
                "risk_factors": [],
                "return_drivers": [],
                "correlation_analysis": {}
            }
            
            # Analyze opportunity categories
            opportunity_categories = opportunity_analysis.get("opportunity_categories", {})
            
            risk_levels = []
            return_estimates = []
            
            for category, category_data in opportunity_categories.items():
                risk_level = category_data.get("risk_level", "medium")
                risk_levels.append(risk_level)
                
                opportunities = category_data.get("opportunities", [])
                for opp in opportunities:
                    expected_return = opp.get("expected_return", "")
                    if "%" in expected_return:
                        # Extract numeric range
                        import re
                        numbers = re.findall(r'\d+', expected_return)
                        if numbers:
                            return_estimates.extend([int(n) for n in numbers])
            
            # Determine overall risk level
            if "high" in risk_levels:
                risk_reward["overall_risk_level"] = "medium_high"
            elif "low" in risk_levels:
                risk_reward["overall_risk_level"] = "medium_low"
            
            # Calculate expected return range
            if return_estimates:
                min_return = min(return_estimates)
                max_return = max(return_estimates)
                risk_reward["expected_return_range"] = f"{min_return}-{max_return}%"
            
            # Risk factors
            risk_reward["risk_factors"] = [
                "Market volatility",
                "Sector concentration",
                "Execution risk",
                "Timing risk"
            ]
            
            # Return drivers
            risk_reward["return_drivers"] = [
                "Asset allocation optimization",
                "Market timing benefits",
                "Thematic growth trends",
                "Diversification benefits"
            ]
            
            return risk_reward
            
        except Exception as e:
            logger.error(f"Error assessing opportunity risk-reward: {e}")
            return {"error": str(e)}

# Global agent instance
market_analysis_agent = MarketAnalysisAgent() 