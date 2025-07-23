"""
Risk Assessment Agent - ADK Implementation with AI-Powered Analysis
Specialized agent for comprehensive financial risk analysis using Google Gemini
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from adk_agents.agent_config import adk_config
from adk_agents.ai_analysis_base import AIAnalysisBase

logger = logging.getLogger(__name__)

class RiskAssessmentAgent(AIAnalysisBase):
    """ADK-based Risk Assessment Agent powered by Gemini AI for financial risk analysis"""
    
    def __init__(self):
        self.agent_id = "risk_assessment_agent"
        config = adk_config.get_agent_definitions()[self.agent_id]
        super().__init__(self.agent_id, config)
        
    async def analyze_portfolio_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered comprehensive portfolio risk analysis using Gemini
        """
        try:
            logger.info("Starting AI-powered comprehensive portfolio risk analysis...")
            
            specific_instructions = """
            Perform a comprehensive portfolio risk analysis focusing on:
            
            1. **Market Risk Assessment**:
               - Asset concentration and diversification analysis
               - Market volatility exposure
               - Sector and geographic concentration risks
               - Correlation analysis between holdings
            
            2. **Credit Risk Evaluation**:
               - Credit score assessment and implications
               - Debt-to-asset ratio analysis
               - Payment history and credit utilization
               - Default probability estimation
            
            3. **Liquidity Risk Analysis**:
               - Cash flow adequacy assessment
               - Asset liquidity evaluation
               - Emergency fund sufficiency
               - Short-term funding risks
            
            4. **Concentration Risk Assessment**:
               - Portfolio diversification measurement
               - Single-asset exposure limits
               - Industry/sector concentration
               - Geographic concentration analysis
            
            5. **Overall Risk Profile**:
               - Integrated risk score calculation
               - Risk level categorization (low/medium/high)
               - Key risk factors identification
               - Risk mitigation recommendations
            
            Provide specific numerical risk scores (0.0-1.0), detailed explanations,
            and actionable mitigation strategies for each risk category.
            """
            
            # Use AI analysis instead of mathematical formulas
            risk_analysis = await self.ai_analyze(
                analysis_type="portfolio_risk_assessment",
                data=financial_data,
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Ensure required fields are present with AI-generated values
            if "error" not in risk_analysis:
                # Validate and enhance AI response structure
                risk_analysis = self._enhance_risk_analysis_structure(risk_analysis)
            
            logger.info("AI-powered portfolio risk analysis completed")
            return risk_analysis
            
        except Exception as e:
            logger.error(f"Error in AI portfolio risk analysis: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "fallback_analysis": "AI analysis failed, manual intervention required"
            }
    
    async def stress_test_portfolio(self, financial_data: Dict[str, Any], scenarios: List[Dict] = None) -> Dict[str, Any]:
        """
        AI-powered portfolio stress testing using various economic scenarios
        """
        try:
            logger.info("Starting AI-powered portfolio stress testing...")
            
            # Define stress test scenarios if not provided
            if scenarios is None:
                scenarios = [
                    {"name": "Market Crash", "market_decline": 30, "interest_rate_change": 2.0},
                    {"name": "Economic Recession", "gdp_decline": 5, "unemployment_increase": 4},
                    {"name": "Interest Rate Spike", "interest_rate_change": 3.0, "bond_decline": 15},
                    {"name": "Inflation Surge", "inflation_increase": 4, "real_return_impact": -2},
                    {"name": "Credit Crisis", "credit_spread_widening": 300, "liquidity_crunch": True}
                ]
            
            specific_instructions = f"""
            Perform comprehensive portfolio stress testing using these scenarios:
            {json.dumps(scenarios, indent=2)}
            
            For each scenario, analyze:
            
            1. **Portfolio Impact Assessment**:
               - Estimated portfolio value decline/gain
               - Asset-specific impacts by category
               - Recovery timeline estimation
               - Worst-case loss calculation
            
            2. **Liquidity Stress Analysis**:
               - Cash flow impact under stress
               - Asset liquidation requirements
               - Time to liquidity for different assets
               - Emergency fund adequacy
            
            3. **Risk Tolerance Evaluation**:
               - Current portfolio vs. stress scenarios
               - Maximum tolerable loss assessment
               - Recovery capacity analysis
               - Psychological impact factors
            
            4. **Scenario-Specific Recommendations**:
               - Protective strategies for each scenario
               - Portfolio adjustments needed
               - Risk mitigation priorities
               - Contingency planning
            
            Provide detailed numerical impact assessments, probability estimates,
            and specific action plans for each stress scenario.
            """
            
            stress_results = await self.ai_analyze(
                analysis_type="portfolio_stress_testing",
                data={"financial_data": financial_data, "stress_scenarios": scenarios},
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for stress test results
            if "error" not in stress_results:
                stress_results = self._enhance_stress_test_structure(stress_results, scenarios)
            
            logger.info("AI-powered portfolio stress testing completed")
            return stress_results
            
        except Exception as e:
            logger.error(f"Error in AI stress testing: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def monitor_risk_alerts(self, current_data: Dict[str, Any], alert_thresholds: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        AI-powered continuous risk monitoring and alert system
        """
        try:
            logger.info("Starting AI-powered risk monitoring...")
            
            if alert_thresholds is None:
                alert_thresholds = {
                    "max_portfolio_risk_score": 0.7,
                    "min_diversification_score": 0.6,
                    "max_debt_to_asset_ratio": 0.4,
                    "min_credit_score": 650,
                    "min_liquidity_ratio": 0.1
                }
            
            specific_instructions = f"""
            Perform continuous risk monitoring and alert analysis with these thresholds:
            {json.dumps(alert_thresholds, indent=2)}
            
            Analyze and report:
            
            1. **Risk Threshold Monitoring**:
               - Current vs. threshold comparisons
               - Trend analysis for key metrics
               - Early warning indicators
               - Breach probability assessment
            
            2. **Dynamic Risk Assessment**:
               - Real-time risk level evaluation
               - Market condition impact
               - Portfolio drift analysis
               - Concentration creep detection
            
            3. **Alert Prioritization**:
               - Critical alerts (immediate action needed)
               - Warning alerts (monitor closely)
               - Informational alerts (awareness only)
               - False positive filtering
            
            4. **Recommended Actions**:
               - Immediate interventions required
               - Monitoring adjustments needed
               - Threshold recalibrations
               - Preventive measures
            
            Generate specific alerts with urgency levels, affected metrics,
            and recommended response actions.
            """
            
            monitoring_results = await self.ai_analyze(
                analysis_type="risk_monitoring_and_alerts",
                data={"current_data": current_data, "alert_thresholds": alert_thresholds},
                specific_instructions=specific_instructions,
                output_format="json"
            )
            
            # Enhance structure for monitoring results
            if "error" not in monitoring_results:
                monitoring_results = self._enhance_monitoring_structure(monitoring_results)
            
            logger.info("AI-powered risk monitoring completed")
            return monitoring_results
            
        except Exception as e:
            logger.error(f"Error in AI risk monitoring: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _enhance_risk_analysis_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response with required structure for risk analysis"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_risk_assessment",
            **ai_response
        }
        
        # Ensure required fields exist with defaults
        if "overall_risk_level" not in enhanced:
            enhanced["overall_risk_level"] = enhanced.get("risk_level", "medium")
        
        if "risk_score" not in enhanced:
            enhanced["risk_score"] = enhanced.get("overall_risk_score", 0.5)
        
        if "risk_categories" not in enhanced:
            enhanced["risk_categories"] = {
                "market_risk": enhanced.get("market_risk", {}),
                "credit_risk": enhanced.get("credit_risk", {}),
                "liquidity_risk": enhanced.get("liquidity_risk", {}),
                "concentration_risk": enhanced.get("concentration_risk", {})
            }
        
        if "key_risks" not in enhanced:
            enhanced["key_risks"] = enhanced.get("key_risk_factors", [])
        
        if "mitigation_strategies" not in enhanced:
            enhanced["mitigation_strategies"] = enhanced.get("recommendations", [])
        
        return enhanced
    
    def _enhance_stress_test_structure(self, ai_response: Dict[str, Any], scenarios: List[Dict]) -> Dict[str, Any]:
        """Enhance AI response structure for stress test results"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_stress_testing",
            "scenarios_tested": len(scenarios),
            **ai_response
        }
        
        # Ensure required fields
        if "worst_case_loss" not in enhanced:
            enhanced["worst_case_loss"] = enhanced.get("maximum_loss", 0.0)
        
        if "best_case_gain" not in enhanced:
            enhanced["best_case_gain"] = enhanced.get("maximum_gain", 0.0)
        
        if "scenario_results" not in enhanced:
            enhanced["scenario_results"] = enhanced.get("scenario_analysis", [])
        
        if "risk_tolerance_assessment" not in enhanced:
            enhanced["risk_tolerance_assessment"] = enhanced.get("risk_tolerance", "medium")
        
        return enhanced
    
    def _enhance_monitoring_structure(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance AI response structure for monitoring results"""
        enhanced = {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_type": "ai_powered_risk_monitoring",
            **ai_response
        }
        
        # Ensure required fields
        if "alerts_triggered" not in enhanced:
            enhanced["alerts_triggered"] = len(enhanced.get("alerts", []))
        
        if "monitoring_status" not in enhanced:
            enhanced["monitoring_status"] = "active"
        
        if "risk_trend" not in enhanced:
            enhanced["risk_trend"] = enhanced.get("trend_analysis", "stable")
        
        return enhanced

# Create global instance
risk_assessment_agent = RiskAssessmentAgent() 