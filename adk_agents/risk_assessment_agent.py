"""
Risk Assessment Agent - ADK Implementation
Specialized agent for comprehensive financial risk analysis and management
"""

import asyncio
import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from adk_agents.agent_config import adk_config

logger = logging.getLogger(__name__)

class RiskAssessmentAgent:
    """ADK-based Risk Assessment Agent for financial risk analysis"""
    
    def __init__(self):
        self.agent_id = "risk_assessment_agent"
        self.config = adk_config.get_agent_definitions()[self.agent_id]
        
    async def analyze_portfolio_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive portfolio risk analysis
        Main tool function for risk assessment
        """
        try:
            logger.info("Starting comprehensive portfolio risk analysis...")
            
            risk_analysis = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "overall_risk_level": "medium",
                "risk_score": 0.5,
                "risk_categories": {},
                "key_risks": [],
                "mitigation_strategies": [],
                "monitoring_alerts": []
            }
            
            # Extract financial metrics from data
            metrics = self._extract_financial_metrics(financial_data)
            
            # Perform different types of risk analysis
            market_risk = await self._analyze_market_risk(metrics)
            credit_risk = await self._analyze_credit_risk(metrics)
            liquidity_risk = await self._analyze_liquidity_risk(metrics)
            concentration_risk = await self._analyze_concentration_risk(metrics)
            
            # Compile risk categories
            risk_analysis["risk_categories"] = {
                "market_risk": market_risk,
                "credit_risk": credit_risk,
                "liquidity_risk": liquidity_risk,
                "concentration_risk": concentration_risk
            }
            
            # Calculate overall risk score and level
            overall_score = self._calculate_overall_risk_score(risk_analysis["risk_categories"])
            risk_analysis["risk_score"] = overall_score
            risk_analysis["overall_risk_level"] = self._determine_risk_level(overall_score)
            
            # Identify key risks
            risk_analysis["key_risks"] = self._identify_key_risks(risk_analysis["risk_categories"])
            
            # Generate mitigation strategies
            risk_analysis["mitigation_strategies"] = self._generate_mitigation_strategies(
                risk_analysis["key_risks"], metrics
            )
            
            # Set up monitoring alerts
            risk_analysis["monitoring_alerts"] = self._setup_monitoring_alerts(
                risk_analysis["risk_categories"]
            )
            
            logger.info(f"Risk analysis completed - Overall risk level: {risk_analysis['overall_risk_level']}")
            return risk_analysis
            
        except Exception as e:
            logger.error(f"Error in portfolio risk analysis: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def stress_test_portfolio(self, financial_data: Dict[str, Any], 
                                   scenarios: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform stress testing on the portfolio under various market scenarios
        """
        try:
            logger.info("Starting portfolio stress testing...")
            
            if scenarios is None:
                scenarios = self._get_default_stress_scenarios()
            
            stress_results = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "scenarios_tested": len(scenarios),
                "worst_case_loss": 0.0,
                "best_case_gain": 0.0,
                "scenario_results": [],
                "risk_tolerance_assessment": "unknown"
            }
            
            metrics = self._extract_financial_metrics(financial_data)
            base_portfolio_value = metrics.get("total_net_worth", 0)
            
            scenario_outcomes = []
            
            # Run each stress scenario
            for scenario in scenarios:
                outcome = await self._run_stress_scenario(metrics, scenario)
                scenario_outcomes.append(outcome)
                stress_results["scenario_results"].append(outcome)
            
            # Calculate aggregate stress test results
            if scenario_outcomes:
                losses = [o["portfolio_impact"] for o in scenario_outcomes if o["portfolio_impact"] < 0]
                gains = [o["portfolio_impact"] for o in scenario_outcomes if o["portfolio_impact"] > 0]
                
                stress_results["worst_case_loss"] = min(losses) if losses else 0.0
                stress_results["best_case_gain"] = max(gains) if gains else 0.0
                
                # Assess risk tolerance
                max_loss_pct = abs(stress_results["worst_case_loss"]) / base_portfolio_value if base_portfolio_value > 0 else 0
                stress_results["risk_tolerance_assessment"] = self._assess_risk_tolerance(max_loss_pct)
            
            logger.info("Portfolio stress testing completed")
            return stress_results
            
        except Exception as e:
            logger.error(f"Error in stress testing: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def monitor_risk_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor key risk metrics and generate alerts for threshold breaches
        """
        try:
            logger.info("Monitoring risk metrics...")
            
            monitoring_results = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "metrics_monitored": 0,
                "alerts_triggered": 0,
                "metric_status": {},
                "active_alerts": [],
                "recommendations": []
            }
            
            metrics = self._extract_financial_metrics(financial_data)
            
            # Define risk thresholds and current values
            risk_thresholds = self._get_risk_thresholds()
            
            for metric_name, threshold_config in risk_thresholds.items():
                current_value = metrics.get(metric_name, 0)
                threshold_value = threshold_config["threshold"]
                operator = threshold_config["operator"]  # "greater", "less", "between"
                
                # Check if threshold is breached
                breach_detected = self._check_threshold_breach(
                    current_value, threshold_value, operator
                )
                
                status = {
                    "current_value": current_value,
                    "threshold": threshold_value,
                    "status": "alert" if breach_detected else "normal",
                    "severity": threshold_config.get("severity", "medium")
                }
                
                monitoring_results["metric_status"][metric_name] = status
                monitoring_results["metrics_monitored"] += 1
                
                if breach_detected:
                    alert = {
                        "metric": metric_name,
                        "current_value": current_value,
                        "threshold": threshold_value,
                        "severity": threshold_config.get("severity", "medium"),
                        "message": threshold_config.get("message", f"{metric_name} threshold breached"),
                        "recommended_action": threshold_config.get("action", "Review and adjust")
                    }
                    monitoring_results["active_alerts"].append(alert)
                    monitoring_results["alerts_triggered"] += 1
            
            # Generate recommendations based on alerts
            monitoring_results["recommendations"] = self._generate_monitoring_recommendations(
                monitoring_results["active_alerts"]
            )
            
            logger.info(f"Risk monitoring completed - {monitoring_results['alerts_triggered']} alerts triggered")
            return monitoring_results
            
        except Exception as e:
            logger.error(f"Error in risk monitoring: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extract_financial_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant financial metrics from collected data"""
        metrics = {
            "total_net_worth": 0,
            "total_assets": 0,
            "total_liabilities": 0,
            "debt_to_asset_ratio": 0,
            "credit_score": 0,
            "epf_balance": 0,
            "monthly_transactions": 0,
            "asset_diversification": 0
        }
        
        try:
            # Extract from data sources
            data_sources = financial_data.get("data_sources", [])
            
            for source in data_sources:
                if not source.get("success", False):
                    continue
                
                source_type = source.get("type", "")
                
                # Process net worth data
                if source_type == "net_worth" and "data" in financial_data:
                    net_worth_data = financial_data["data"]
                    metrics["total_net_worth"] = net_worth_data.get("total_net_worth", 0)
                    metrics["total_assets"] = net_worth_data.get("total_assets", 0)
                    metrics["total_liabilities"] = net_worth_data.get("total_liabilities", 0)
                    
                    # Calculate debt-to-asset ratio
                    if metrics["total_assets"] > 0:
                        metrics["debt_to_asset_ratio"] = metrics["total_liabilities"] / metrics["total_assets"]
                
                # Process credit report
                elif source_type == "credit_report" and "data" in financial_data:
                    credit_data = financial_data["data"]
                    metrics["credit_score"] = credit_data.get("credit_score", 0)
                
                # Process EPF data
                elif source_type == "epf_details" and "data" in financial_data:
                    epf_data = financial_data["data"]
                    metrics["epf_balance"] = epf_data.get("epf_balance", 0)
                
                # Process transaction data
                elif source_type == "bank_transactions" and "data" in financial_data:
                    txn_data = financial_data["data"]
                    metrics["monthly_transactions"] = txn_data.get("transaction_count", 0)
            
            # Calculate asset diversification (simple heuristic)
            if metrics["total_assets"] > 0:
                # Simplified diversification score based on multiple asset types
                asset_types = ["epf_balance", "total_net_worth"]
                non_zero_assets = sum(1 for asset in asset_types if metrics.get(asset, 0) > 0)
                metrics["asset_diversification"] = non_zero_assets / len(asset_types)
            
        except Exception as e:
            logger.error(f"Error extracting financial metrics: {e}")
        
        return metrics
    
    async def _analyze_market_risk(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market risk exposure"""
        try:
            market_risk = {
                "risk_level": "medium",
                "risk_score": 0.5,
                "key_factors": [],
                "recommendations": []
            }
            
            # Assess based on asset concentration and diversification
            diversification = metrics.get("asset_diversification", 0)
            
            if diversification < 0.3:
                market_risk["risk_level"] = "high"
                market_risk["risk_score"] = 0.8
                market_risk["key_factors"].append("Low asset diversification")
                market_risk["recommendations"].append("Diversify across more asset classes")
            elif diversification < 0.6:
                market_risk["risk_level"] = "medium"
                market_risk["risk_score"] = 0.5
                market_risk["key_factors"].append("Moderate asset diversification")
            else:
                market_risk["risk_level"] = "low"
                market_risk["risk_score"] = 0.3
                market_risk["key_factors"].append("Good asset diversification")
            
            return market_risk
            
        except Exception as e:
            logger.error(f"Error in market risk analysis: {e}")
            return {"risk_level": "unknown", "risk_score": 0.5, "error": str(e)}
    
    async def _analyze_credit_risk(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze credit risk based on credit score and debt levels"""
        try:
            credit_risk = {
                "risk_level": "medium",
                "risk_score": 0.5,
                "key_factors": [],
                "recommendations": []
            }
            
            credit_score = metrics.get("credit_score", 0)
            debt_ratio = metrics.get("debt_to_asset_ratio", 0)
            
            # Assess credit score risk
            if credit_score > 0:
                if credit_score >= 750:
                    credit_risk["risk_level"] = "low"
                    credit_risk["risk_score"] = 0.2
                    credit_risk["key_factors"].append(f"Excellent credit score: {credit_score}")
                elif credit_score >= 700:
                    credit_risk["risk_level"] = "medium"
                    credit_risk["risk_score"] = 0.4
                    credit_risk["key_factors"].append(f"Good credit score: {credit_score}")
                else:
                    credit_risk["risk_level"] = "high"
                    credit_risk["risk_score"] = 0.7
                    credit_risk["key_factors"].append(f"Below-average credit score: {credit_score}")
                    credit_risk["recommendations"].append("Work to improve credit score")
            
            # Assess debt-to-asset ratio
            if debt_ratio > 0.5:
                credit_risk["risk_level"] = "high"
                credit_risk["risk_score"] = max(credit_risk["risk_score"], 0.8)
                credit_risk["key_factors"].append(f"High debt-to-asset ratio: {debt_ratio:.1%}")
                credit_risk["recommendations"].append("Consider debt reduction strategies")
            elif debt_ratio > 0.3:
                credit_risk["risk_score"] = max(credit_risk["risk_score"], 0.5)
                credit_risk["key_factors"].append(f"Moderate debt levels: {debt_ratio:.1%}")
            
            return credit_risk
            
        except Exception as e:
            logger.error(f"Error in credit risk analysis: {e}")
            return {"risk_level": "unknown", "risk_score": 0.5, "error": str(e)}
    
    async def _analyze_liquidity_risk(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze liquidity risk based on cash flow and asset liquidity"""
        try:
            liquidity_risk = {
                "risk_level": "medium",
                "risk_score": 0.5,
                "key_factors": [],
                "recommendations": []
            }
            
            # Simple liquidity assessment based on available metrics
            monthly_transactions = metrics.get("monthly_transactions", 0)
            
            if monthly_transactions > 50:
                liquidity_risk["key_factors"].append("High transaction activity suggests good liquidity")
                liquidity_risk["risk_level"] = "low"
                liquidity_risk["risk_score"] = 0.3
            elif monthly_transactions > 20:
                liquidity_risk["key_factors"].append("Moderate transaction activity")
            else:
                liquidity_risk["key_factors"].append("Low transaction activity may indicate liquidity constraints")
                liquidity_risk["risk_level"] = "medium"
                liquidity_risk["risk_score"] = 0.6
                liquidity_risk["recommendations"].append("Ensure adequate emergency fund")
            
            return liquidity_risk
            
        except Exception as e:
            logger.error(f"Error in liquidity risk analysis: {e}")
            return {"risk_level": "unknown", "risk_score": 0.5, "error": str(e)}
    
    async def _analyze_concentration_risk(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze concentration risk in asset allocation"""
        try:
            concentration_risk = {
                "risk_level": "medium",
                "risk_score": 0.5,
                "key_factors": [],
                "recommendations": []
            }
            
            diversification = metrics.get("asset_diversification", 0)
            
            if diversification < 0.3:
                concentration_risk["risk_level"] = "high"
                concentration_risk["risk_score"] = 0.8
                concentration_risk["key_factors"].append("High concentration in few asset types")
                concentration_risk["recommendations"].append("Diversify across more asset classes")
            elif diversification < 0.6:
                concentration_risk["risk_level"] = "medium"
                concentration_risk["risk_score"] = 0.5
                concentration_risk["key_factors"].append("Moderate asset concentration")
            else:
                concentration_risk["risk_level"] = "low"
                concentration_risk["risk_score"] = 0.3
                concentration_risk["key_factors"].append("Well-diversified portfolio")
            
            return concentration_risk
            
        except Exception as e:
            logger.error(f"Error in concentration risk analysis: {e}")
            return {"risk_level": "unknown", "risk_score": 0.5, "error": str(e)}
    
    def _calculate_overall_risk_score(self, risk_categories: Dict[str, Any]) -> float:
        """Calculate weighted overall risk score"""
        try:
            weights = {
                "market_risk": 0.3,
                "credit_risk": 0.3,
                "liquidity_risk": 0.2,
                "concentration_risk": 0.2
            }
            
            total_score = 0.0
            total_weight = 0.0
            
            for category, weight in weights.items():
                if category in risk_categories and "risk_score" in risk_categories[category]:
                    total_score += risk_categories[category]["risk_score"] * weight
                    total_weight += weight
            
            return total_score / total_weight if total_weight > 0 else 0.5
            
        except Exception:
            return 0.5
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level from numeric score"""
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _identify_key_risks(self, risk_categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify the most significant risks"""
        key_risks = []
        
        for category, analysis in risk_categories.items():
            if analysis.get("risk_level") == "high" or analysis.get("risk_score", 0) >= 0.7:
                key_risks.append({
                    "category": category,
                    "level": analysis.get("risk_level", "unknown"),
                    "score": analysis.get("risk_score", 0),
                    "factors": analysis.get("key_factors", [])
                })
        
        # Sort by risk score descending
        key_risks.sort(key=lambda x: x.get("score", 0), reverse=True)
        return key_risks[:5]  # Top 5 risks
    
    def _generate_mitigation_strategies(self, key_risks: List[Dict[str, Any]], 
                                      metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific mitigation strategies for identified risks"""
        strategies = []
        
        for risk in key_risks:
            category = risk["category"]
            
            if category == "credit_risk":
                strategies.append({
                    "risk_category": category,
                    "strategy": "Credit Score Improvement",
                    "actions": [
                        "Pay all bills on time",
                        "Reduce credit utilization below 30%",
                        "Avoid opening new credit accounts",
                        "Monitor credit report regularly"
                    ],
                    "timeline": "6-12 months",
                    "priority": "high"
                })
            
            elif category == "concentration_risk":
                strategies.append({
                    "risk_category": category,
                    "strategy": "Portfolio Diversification",
                    "actions": [
                        "Invest in different asset classes",
                        "Consider international exposure",
                        "Balance between equity and fixed income",
                        "Implement systematic rebalancing"
                    ],
                    "timeline": "3-6 months",
                    "priority": "medium"
                })
            
            elif category == "liquidity_risk":
                strategies.append({
                    "risk_category": category,
                    "strategy": "Liquidity Enhancement",
                    "actions": [
                        "Build emergency fund (6 months expenses)",
                        "Keep some investments in liquid assets",
                        "Establish credit lines for emergencies",
                        "Review and optimize cash flow"
                    ],
                    "timeline": "1-3 months",
                    "priority": "high"
                })
        
        return strategies
    
    def _setup_monitoring_alerts(self, risk_categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Set up monitoring alerts for key risk metrics"""
        alerts = []
        
        for category, analysis in risk_categories.items():
            if analysis.get("risk_score", 0) >= 0.5:
                alerts.append({
                    "category": category,
                    "metric": f"{category}_score",
                    "current_value": analysis.get("risk_score", 0),
                    "threshold": 0.7,
                    "frequency": "weekly",
                    "action": f"Review {category} factors and implement mitigation strategies"
                })
        
        return alerts
    
    def _get_default_stress_scenarios(self) -> List[Dict[str, Any]]:
        """Get default stress testing scenarios"""
        return [
            {
                "name": "Market Crash",
                "description": "30% market decline",
                "equity_impact": -0.30,
                "probability": 0.05
            },
            {
                "name": "Economic Recession",
                "description": "Mild recession scenario",
                "equity_impact": -0.15,
                "income_impact": -0.10,
                "probability": 0.15
            },
            {
                "name": "Interest Rate Shock",
                "description": "Rapid interest rate increase",
                "bond_impact": -0.10,
                "equity_impact": -0.05,
                "probability": 0.20
            }
        ]
    
    async def _run_stress_scenario(self, metrics: Dict[str, Any], 
                                  scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single stress test scenario"""
        try:
            base_value = metrics.get("total_net_worth", 0)
            
            # Apply scenario impacts
            equity_impact = scenario.get("equity_impact", 0)
            bond_impact = scenario.get("bond_impact", 0)
            income_impact = scenario.get("income_impact", 0)
            
            # Simplified calculation assuming 70% equity, 30% bonds
            portfolio_impact = (0.7 * equity_impact + 0.3 * bond_impact) * base_value
            
            return {
                "scenario_name": scenario.get("name", "Unknown"),
                "description": scenario.get("description", ""),
                "portfolio_impact": portfolio_impact,
                "impact_percentage": portfolio_impact / base_value if base_value > 0 else 0,
                "probability": scenario.get("probability", 0),
                "expected_loss": portfolio_impact * scenario.get("probability", 0)
            }
            
        except Exception as e:
            return {
                "scenario_name": scenario.get("name", "Unknown"),
                "error": str(e),
                "portfolio_impact": 0
            }
    
    def _assess_risk_tolerance(self, max_loss_percentage: float) -> str:
        """Assess risk tolerance based on maximum loss scenarios"""
        if max_loss_percentage > 0.3:
            return "low"
        elif max_loss_percentage > 0.15:
            return "moderate"
        else:
            return "high"
    
    def _get_risk_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Get risk monitoring thresholds"""
        return {
            "debt_to_asset_ratio": {
                "threshold": 0.5,
                "operator": "greater",
                "severity": "high",
                "message": "Debt-to-asset ratio exceeds 50%",
                "action": "Consider debt reduction strategies"
            },
            "credit_score": {
                "threshold": 650,
                "operator": "less",
                "severity": "medium",
                "message": "Credit score below 650",
                "action": "Focus on credit improvement"
            },
            "asset_diversification": {
                "threshold": 0.3,
                "operator": "less",
                "severity": "medium",
                "message": "Low portfolio diversification",
                "action": "Increase asset diversification"
            }
        }
    
    def _check_threshold_breach(self, current_value: float, threshold: float, 
                               operator: str) -> bool:
        """Check if a threshold has been breached"""
        if operator == "greater":
            return current_value > threshold
        elif operator == "less":
            return current_value < threshold
        elif operator == "between":
            # threshold should be a tuple for between
            if isinstance(threshold, (list, tuple)) and len(threshold) == 2:
                return not (threshold[0] <= current_value <= threshold[1])
        return False
    
    def _generate_monitoring_recommendations(self, alerts: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on triggered alerts"""
        recommendations = []
        
        high_severity_alerts = [a for a in alerts if a.get("severity") == "high"]
        medium_severity_alerts = [a for a in alerts if a.get("severity") == "medium"]
        
        if high_severity_alerts:
            recommendations.append("Address high-severity risk alerts immediately")
            
        if len(alerts) > 3:
            recommendations.append("Multiple risk thresholds breached - comprehensive review needed")
            
        if medium_severity_alerts:
            recommendations.append("Monitor medium-severity alerts and plan corrective actions")
            
        return recommendations

# Global agent instance
risk_assessment_agent = RiskAssessmentAgent() 