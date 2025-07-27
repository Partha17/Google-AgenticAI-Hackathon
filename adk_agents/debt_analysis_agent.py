#!/usr/bin/env python3
"""
Debt Analysis & Budget Optimization Agent
Analyzes debt patterns and suggests budget optimizations using MCP data
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from sqlalchemy.orm import Session

from .ai_analysis_base import AIAnalysisBase
from .agent_config import AGENT_CONFIGS
from models.database import MCPData, SessionLocal
from services.logger_config import get_adk_logger

logger = get_adk_logger()


class DebtType(Enum):
    """Types of debt"""
    CREDIT_CARD = "credit_card"
    PERSONAL_LOAN = "personal_loan"
    HOME_LOAN = "home_loan"
    VEHICLE_LOAN = "vehicle_loan"
    STUDENT_LOAN = "student_loan"
    BUSINESS_LOAN = "business_loan"
    OTHER = "other"


class ExpenseCategory(Enum):
    """Expense categories for budget analysis"""
    HOUSING = "housing"
    TRANSPORTATION = "transportation"
    FOOD = "food"
    UTILITIES = "utilities"
    INSURANCE = "insurance"
    HEALTHCARE = "healthcare"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    EDUCATION = "education"
    SUBSCRIPTIONS = "subscriptions"
    DEBT_PAYMENTS = "debt_payments"
    SAVINGS = "savings"
    OTHER = "other"


@dataclass
class Debt:
    """Data class for debt information"""
    name: str
    type: DebtType
    amount: float
    interest_rate: float
    monthly_payment: float
    remaining_balance: float
    due_date: datetime
    lender: str
    is_active: bool = True
    priority: Optional[str] = None  # high, medium, low


@dataclass
class BudgetItem:
    """Data class for budget items"""
    category: ExpenseCategory
    amount: float
    frequency: str  # monthly, yearly, etc.
    description: str
    is_essential: bool = True
    optimization_potential: Optional[float] = None


class DebtAnalysisAgent(AIAnalysisBase):
    """
    Agent for analyzing debt patterns and suggesting budget optimizations using MCP data
    """

    def __init__(self, agent_id: str = "debt_analysis_agent", agent_config: Dict[str, Any] = None):
        # Use ADK configuration if not provided
        if agent_config is None:
            agent_config = AGENT_CONFIGS.get("debt_analysis_agent", {})

        super().__init__(agent_id, agent_config)
        self.logger = logging.getLogger(__name__)

    async def analyze_debt_and_budget(self, phone_number: str = None) -> Dict[str, Any]:
        """
        Analyze debt patterns and budget using MCP data from database

        Args:
            phone_number: Phone number to filter data (optional)

        Returns:
            Dictionary containing comprehensive debt and budget analysis
        """
        try:
            self.logger.info("Starting debt and budget analysis using MCP data")

            # Get MCP data from database
            mcp_data = self._get_mcp_data_from_db(phone_number)

            if not mcp_data:
                return {
                    'error': 'No MCP data found in database',
                    'debt_summary': {},
                    'budget_analysis': {},
                    'recommendations': [],
                    'timestamp': datetime.now().isoformat()
                }

            # Extract and analyze debt information
            debt_analysis = await self._analyze_debt_patterns(mcp_data)

            # Analyze budget and spending patterns
            budget_analysis = await self._analyze_budget_patterns(mcp_data)

            # Generate optimization recommendations
            recommendations = await self._generate_optimization_recommendations(
                debt_analysis, budget_analysis
            )

            # Calculate financial health metrics
            health_metrics = self._calculate_financial_health_metrics(debt_analysis, budget_analysis)

            return {
                'debt_summary': debt_analysis,
                'budget_analysis': budget_analysis,
                'financial_health_metrics': health_metrics,
                'optimization_recommendations': recommendations,
                'repayment_plan': self._generate_repayment_plan(debt_analysis),
                'emergency_fund_strategy': self._generate_emergency_fund_strategy(budget_analysis),
                'risk_assessment': self._assess_financial_risk(debt_analysis, budget_analysis),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error in debt and budget analysis: {e}")
            return {
                'error': str(e),
                'debt_summary': {},
                'budget_analysis': {},
                'recommendations': [],
                'timestamp': datetime.now().isoformat()
            }

    def _get_mcp_data_from_db(self, phone_number: str = None) -> Dict[str, Any]:
        """Retrieve MCP data from database"""
        try:
            db = SessionLocal()

            # Query for recent MCP data
            query = db.query(MCPData).filter(
                MCPData.timestamp > datetime.utcnow() - timedelta(days=30)
            )

            if phone_number:
                query = query.filter(MCPData.phone_number == phone_number)

            mcp_records = query.order_by(MCPData.timestamp.desc()).all()

            # Organize data by type
            organized_data = {}
            for record in mcp_records:
                data_type = record.data_type
                if data_type not in organized_data:
                    organized_data[data_type] = []

                # Get the processed data from the record
                record_data = record.get_data()

                # The data is stored as the processed response from MCP client
                # It has structure: {"success": True, "data": {...}, "data_type": "...", ...}
                if isinstance(record_data, dict) and "success" in record_data and "data" in record_data:
                    # Extract the actual data portion
                    organized_data[data_type].append(record_data["data"])
                else:
                    # Fallback: use the record data as is
                    organized_data[data_type].append(record_data)

            db.close()
            return organized_data

        except Exception as e:
            self.logger.error(f"Error retrieving MCP data from database: {e}")
            return {}

    async def _analyze_debt_patterns(self, mcp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze debt patterns from MCP data"""
        try:
            # Extract debt-related data
            credit_data = mcp_data.get('credit_report', [])
            bank_transactions = mcp_data.get('bank_transactions', [])

            # Prepare context for AI analysis
            context = f"""
            Analyze the debt patterns from the following financial data:

            CREDIT REPORT DATA:
            {json.dumps(credit_data, indent=2)}

            BANK TRANSACTIONS:
            {json.dumps(bank_transactions[:50], indent=2)}  # First 50 transactions for analysis

            TASK: Perform comprehensive debt analysis including:
            1. **Debt Identification**: Identify all types of debt (credit cards, loans, etc.)
            2. **Debt Classification**: Categorize by type (credit card, personal loan, home loan, etc.)
            3. **Debt Metrics**: Calculate amounts, interest rates, monthly payments
            4. **Debt Health**: Assess debt-to-income ratio, credit utilization
            5. **Risk Assessment**: Identify high-risk debt patterns

            RESPONSE FORMAT:
            Return a JSON object with:
            {{
                "total_debt": 0.0,
                "debt_by_type": {{
                    "credit_card": {{"amount": 0.0, "count": 0, "avg_interest": 0.0}},
                    "personal_loan": {{"amount": 0.0, "count": 0, "avg_interest": 0.0}},
                    "home_loan": {{"amount": 0.0, "count": 0, "avg_interest": 0.0}},
                    "vehicle_loan": {{"amount": 0.0, "count": 0, "avg_interest": 0.0}},
                    "student_loan": {{"amount": 0.0, "count": 0, "avg_interest": 0.0}},
                    "other": {{"amount": 0.0, "count": 0, "avg_interest": 0.0}}
                }},
                "debt_health_metrics": {{
                    "debt_to_income_ratio": 0.0,
                    "credit_utilization_ratio": 0.0,
                    "total_monthly_payments": 0.0,
                    "highest_interest_debt": "description",
                    "debt_priority": "high/medium/low"
                }},
                "individual_debts": [
                    {{
                        "name": "debt name",
                        "type": "debt type",
                        "amount": 0.0,
                        "interest_rate": 0.0,
                        "monthly_payment": 0.0,
                        "lender": "lender name",
                        "priority": "high/medium/low"
                    }}
                ]
            }}
            """

            # Use ADK AI for debt analysis
            response = await self.ai_analyze(
                analysis_type="debt_analysis",
                data=mcp_data,
                specific_instructions="Analyze debt patterns and provide structured analysis",
                output_format="json"
            )

            if response and isinstance(response, dict):
                return response
            elif response and isinstance(response, str):
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse AI response as JSON")

            # Fallback analysis
            return self._fallback_debt_analysis(mcp_data)

        except Exception as e:
            self.logger.error(f"Error in debt pattern analysis: {e}")
            return {}

    async def _analyze_budget_patterns(self, mcp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze budget patterns from MCP data"""
        try:
            # Extract budget-related data
            bank_transactions = mcp_data.get('bank_transactions', [])
            net_worth_data = mcp_data.get('net_worth', [])

            # Prepare context for AI analysis
            context = f"""
            Analyze the budget patterns from the following financial data:

            BANK TRANSACTIONS:
            {json.dumps(bank_transactions[:100], indent=2)}  # First 100 transactions for analysis

            NET WORTH DATA:
            {json.dumps(net_worth_data, indent=2)}

            TASK: Perform comprehensive budget analysis including:
            1. **Expense Categorization**: Categorize expenses by type (housing, food, transportation, etc.)
            2. **Income Analysis**: Analyze income sources and patterns
            3. **Budget Allocation**: Assess current budget allocation across categories
            4. **Spending Patterns**: Identify spending trends and patterns
            5. **Optimization Opportunities**: Find areas for budget optimization

            RESPONSE FORMAT:
            Return a JSON object with:
            {{
                "total_income": 0.0,
                "total_expenses": 0.0,
                "savings_rate": 0.0,
                "expense_categories": {{
                    "housing": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "food": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "transportation": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "utilities": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "entertainment": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "shopping": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "healthcare": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "education": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}},
                    "other": {{"amount": 0.0, "percentage": 0.0, "trend": "increasing/decreasing/stable"}}
                }},
                "budget_health_metrics": {{
                    "income_stability": "high/medium/low",
                    "expense_volatility": "high/medium/low",
                    "savings_consistency": "high/medium/low",
                    "budget_adherence": "high/medium/low"
                }},
                "spending_insights": [
                    {{
                        "category": "category name",
                        "insight": "insight description",
                        "recommendation": "recommendation text",
                        "potential_savings": 0.0
                    }}
                ]
            }}
            """

            # Use ADK AI for budget analysis
            response = await self.ai_analyze(
                analysis_type="budget_analysis",
                data=mcp_data,
                specific_instructions="Analyze budget patterns and provide structured analysis",
                output_format="json"
            )

            if response and isinstance(response, dict):
                return response
            elif response and isinstance(response, str):
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse AI response as JSON")

            # Fallback analysis
            return self._fallback_budget_analysis(mcp_data)

        except Exception as e:
            self.logger.error(f"Error in budget pattern analysis: {e}")
            return {}

    async def _generate_optimization_recommendations(
        self, debt_analysis: Dict[str, Any], budget_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate optimization recommendations based on debt and budget analysis"""
        try:
            context = f"""
            Generate comprehensive optimization recommendations based on:

            DEBT ANALYSIS:
            {json.dumps(debt_analysis, indent=2)}

            BUDGET ANALYSIS:
            {json.dumps(budget_analysis, indent=2)}

            TASK: Generate actionable optimization recommendations including:
            1. **Debt Repayment Strategies**: Suggest optimal debt repayment approaches
            2. **Budget Optimization**: Recommend spending reductions and reallocations
            3. **Emergency Fund Planning**: Suggest emergency fund strategies
            4. **Income Enhancement**: Suggest ways to increase income
            5. **Risk Mitigation**: Suggest ways to reduce financial risk

            RESPONSE FORMAT:
            Return a JSON array of recommendations:
            [
                {{
                    "type": "debt_repayment/budget_optimization/emergency_fund/income_enhancement/risk_mitigation",
                    "priority": "high/medium/low",
                    "title": "recommendation title",
                    "description": "detailed description",
                    "potential_impact": "quantified impact",
                    "implementation_steps": ["step 1", "step 2", "step 3"],
                    "timeline": "immediate/short_term/long_term"
                }}
            ]
            """

            # Use ADK AI for recommendations
            response = await self.ai_analyze(
                analysis_type="optimization_recommendations",
                data={"debt_analysis": debt_analysis, "budget_analysis": budget_analysis},
                specific_instructions="Generate optimization recommendations based on debt and budget analysis",
                output_format="json"
            )

            if response and isinstance(response, dict):
                return response
            elif response and isinstance(response, str):
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse AI response as JSON")

            # Fallback recommendations
            return self._fallback_recommendations(debt_analysis, budget_analysis)

        except Exception as e:
            self.logger.error(f"Error generating optimization recommendations: {e}")
            return []

    def _calculate_financial_health_metrics(
        self, debt_analysis: Dict[str, Any], budget_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate financial health metrics"""
        try:
            total_debt = debt_analysis.get('total_debt', 0)
            monthly_income = budget_analysis.get('monthly_income', 0)
            monthly_expenses = budget_analysis.get('monthly_expenses', 0)

            # Calculate key metrics
            debt_to_income_ratio = (total_debt / monthly_income * 12) if monthly_income > 0 else 0
            savings_rate = ((monthly_income - monthly_expenses) / monthly_income) if monthly_income > 0 else 0

            return {
                'debt_to_income_ratio': round(debt_to_income_ratio, 2),
                'savings_rate': round(savings_rate * 100, 2),
                'monthly_cash_flow': round(monthly_income - monthly_expenses, 2),
                'financial_health_score': self._calculate_health_score(debt_to_income_ratio, savings_rate),
                'risk_level': self._determine_risk_level(debt_to_income_ratio, savings_rate)
            }
        except Exception as e:
            self.logger.error(f"Error calculating financial health metrics: {e}")
            return {}

    def _generate_repayment_plan(self, debt_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured debt repayment plan"""
        try:
            individual_debts = debt_analysis.get('individual_debts', [])

            # Sort by priority and interest rate
            sorted_debts = sorted(
                individual_debts,
                key=lambda x: (
                    {'high': 3, 'medium': 2, 'low': 1}.get(x.get('priority', 'low'), 1),
                    x.get('interest_rate', 0)
                ),
                reverse=True
            )

            return {
                'repayment_strategy': 'avalanche' if sorted_debts else 'none',
                'total_repayment_time': self._calculate_repayment_time(sorted_debts),
                'monthly_payment_required': sum(d.get('monthly_payment', 0) for d in sorted_debts),
                'debt_repayment_order': [d.get('name', 'Unknown') for d in sorted_debts],
                'estimated_completion': self._estimate_completion_date(sorted_debts)
            }
        except Exception as e:
            self.logger.error(f"Error generating repayment plan: {e}")
            return {}

    def _generate_emergency_fund_strategy(self, budget_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate emergency fund strategy"""
        try:
            monthly_expenses = budget_analysis.get('monthly_expenses', 0)
            monthly_income = budget_analysis.get('monthly_income', 0)

            # Calculate emergency fund target (3-6 months of expenses)
            emergency_fund_target = monthly_expenses * 6
            monthly_savings = monthly_income - monthly_expenses

            return {
                'emergency_fund_target': round(emergency_fund_target, 2),
                'monthly_savings_needed': round(emergency_fund_target / 12, 2),
                'time_to_target': round(emergency_fund_target / monthly_savings, 1) if monthly_savings > 0 else 0,
                'recommended_monthly_contribution': round(monthly_savings * 0.3, 2),
                'strategy': 'Build emergency fund before aggressive debt repayment'
            }
        except Exception as e:
            self.logger.error(f"Error generating emergency fund strategy: {e}")
            return {}

    def _assess_financial_risk(
        self, debt_analysis: Dict[str, Any], budget_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess overall financial risk"""
        try:
            debt_to_income_ratio = debt_analysis.get('debt_health_metrics', {}).get('debt_to_income_ratio', 0)
            savings_rate = budget_analysis.get('savings_rate', 0)

            risk_factors = []
            risk_level = 'low'

            if debt_to_income_ratio > 0.4:
                risk_factors.append('High debt-to-income ratio')
                risk_level = 'high'
            elif debt_to_income_ratio > 0.2:
                risk_factors.append('Moderate debt-to-income ratio')
                risk_level = 'medium'

            if savings_rate < 10:
                risk_factors.append('Low savings rate')
                risk_level = 'high' if risk_level == 'high' else 'medium'

            return {
                'overall_risk_level': risk_level,
                'risk_factors': risk_factors,
                'risk_score': self._calculate_risk_score(debt_to_income_ratio, savings_rate),
                'mitigation_strategies': self._get_risk_mitigation_strategies(risk_factors)
            }
        except Exception as e:
            self.logger.error(f"Error assessing financial risk: {e}")
            return {}

    # Helper methods for fallback analysis
    def _fallback_debt_analysis(self, mcp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback debt analysis when AI analysis fails"""
        return {
            'total_debt': 0.0,
            'debt_by_type': {},
            'debt_health_metrics': {},
            'individual_debts': []
        }

    def _fallback_budget_analysis(self, mcp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback budget analysis when AI analysis fails"""
        return {
            'monthly_income': 0.0,
            'monthly_expenses': 0.0,
            'savings_rate': 0.0,
            'expense_categories': {},
            'spending_analysis': {},
            'budget_recommendations': []
        }

    def _fallback_recommendations(
        self, debt_analysis: Dict[str, Any], budget_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Fallback recommendations when AI analysis fails"""
        return [
            {
                'type': 'general',
                'priority': 'medium',
                'title': 'Review Financial Data',
                'description': 'Please review your financial data manually for optimization opportunities',
                'potential_impact': 'Unknown',
                'implementation_steps': ['Review bank statements', 'Analyze spending patterns', 'Identify savings opportunities'],
                'timeline': 'short_term'
            }
        ]

    def _calculate_health_score(self, debt_to_income_ratio: float, savings_rate: float) -> float:
        """Calculate overall financial health score (0-100)"""
        # Simple scoring algorithm
        debt_score = max(0, 100 - (debt_to_income_ratio * 100))
        savings_score = min(100, savings_rate * 10)
        return round((debt_score + savings_score) / 2, 1)

    def _determine_risk_level(self, debt_to_income_ratio: float, savings_rate: float) -> str:
        """Determine overall risk level"""
        if debt_to_income_ratio > 0.4 or savings_rate < 5:
            return 'high'
        elif debt_to_income_ratio > 0.2 or savings_rate < 10:
            return 'medium'
        else:
            return 'low'

    def _calculate_repayment_time(self, debts: List[Dict[str, Any]]) -> int:
        """Calculate estimated repayment time in months"""
        total_debt = sum(d.get('amount', 0) for d in debts)
        monthly_payment = sum(d.get('monthly_payment', 0) for d in debts)
        return round(total_debt / monthly_payment) if monthly_payment > 0 else 0

    def _estimate_completion_date(self, debts: List[Dict[str, Any]]) -> str:
        """Estimate debt repayment completion date"""
        months_to_completion = self._calculate_repayment_time(debts)
        completion_date = datetime.now() + timedelta(days=months_to_completion * 30)
        return completion_date.strftime('%Y-%m-%d')

    def _calculate_risk_score(self, debt_to_income_ratio: float, savings_rate: float) -> float:
        """Calculate risk score (0-100, higher = more risky)"""
        debt_risk = min(100, debt_to_income_ratio * 100)
        savings_risk = max(0, 100 - (savings_rate * 10))
        return round((debt_risk + savings_risk) / 2, 1)

    def _get_risk_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Get strategies to mitigate identified risks"""
        strategies = []
        for factor in risk_factors:
            if 'debt-to-income' in factor.lower():
                strategies.append('Focus on debt reduction and income increase')
            if 'savings' in factor.lower():
                strategies.append('Increase savings rate and build emergency fund')
        return strategies if strategies else ['Review financial plan regularly']


# Global instance
debt_analysis_agent = DebtAnalysisAgent()