#!/usr/bin/env python3
"""
Subscription Tracking Agent
Analyzes transaction data to identify subscriptions and provide insights
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from .ai_analysis_base import AIAnalysisBase


class SubscriptionCategory(Enum):
    """Categories for different types of subscriptions"""
    STREAMING = "streaming"
    SOFTWARE = "software"
    FITNESS = "fitness"
    FOOD_DELIVERY = "food_delivery"
    SHOPPING = "shopping"
    EDUCATION = "education"
    GAMING = "gaming"
    PRODUCTIVITY = "productivity"
    SECURITY = "security"
    FINANCE = "finance"
    HEALTH = "health"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    OTHER = "other"


@dataclass
class Subscription:
    """Data class for subscription information"""
    name: str
    category: SubscriptionCategory
    amount: float
    frequency: str  # monthly, yearly, quarterly, etc.
    merchant: str
    last_charge_date: datetime
    next_charge_date: datetime
    description: str
    is_active: bool = True
    usage_frequency: Optional[str] = None  # high, medium, low, none
    annual_cost: Optional[float] = None
    savings_potential: Optional[float] = None
    ai_confidence: Optional[float] = None  # AI classification confidence
    entities: Optional[Dict[str, List[str]]] = None
    semantic_analysis: Optional[str] = None
    reasoning: Optional[str] = None


class SubscriptionTrackingAgent(AIAnalysisBase):
    """
    Agent for tracking and analyzing subscription services with AI-powered categorization
    """

    def __init__(self, agent_id: str = "subscription_tracking_agent", agent_config: Dict[str, Any] = None):
        # Use ADK configuration if not provided
        if agent_config is None:
            from .agent_config import AGENT_CONFIGS
            agent_config = AGENT_CONFIGS.get("subscription_tracking_agent", {})

        super().__init__(agent_id, agent_config)
        self.logger = logging.getLogger(__name__)

    async def analyze_subscriptions(self, transaction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze transaction data to identify and categorize subscriptions

        Args:
            transaction_data: List of transaction dictionaries

        Returns:
            Dictionary containing subscription analysis results
        """
        try:
            self.logger.info("Starting subscription analysis")

            # Extract potential subscriptions
            subscriptions = self._identify_subscriptions(transaction_data)

            # Categorize subscriptions
            categorized_subs = self._categorize_subscriptions(subscriptions)

            # Analyze usage patterns
            usage_analysis = self._analyze_usage_patterns(categorized_subs, transaction_data)

            # Calculate costs and savings
            cost_analysis = self._calculate_costs_and_savings(categorized_subs)

            # Generate recommendations
            recommendations = await self._generate_recommendations(categorized_subs, usage_analysis, cost_analysis)

            return {
                'subscriptions': [self._subscription_to_dict(sub) for sub in categorized_subs],
                'usage_analysis': usage_analysis,
                'cost_analysis': cost_analysis,
                'recommendations': recommendations,
                'summary': self._generate_summary(categorized_subs, cost_analysis),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error in subscription analysis: {e}")
            return {
                'error': str(e),
                'subscriptions': [],
                'usage_analysis': {},
                'cost_analysis': {},
                'recommendations': [],
                'summary': {}
            }

    def _identify_subscriptions(self, transactions: List[Dict[str, Any]]) -> List[Subscription]:
        """Identify potential subscriptions from transaction data"""
        subscriptions = []

        # Group transactions by merchant
        merchant_groups = {}
        for transaction in transactions:
            merchant = transaction.get('merchant', '').lower()
            amount = transaction.get('amount', 0)
            date = transaction.get('date')

            if merchant not in merchant_groups:
                merchant_groups[merchant] = []
            merchant_groups[merchant].append({
                'amount': amount,
                'date': date,
                'description': transaction.get('description', '')
            })

        # Analyze each merchant for subscription patterns
        for merchant, transactions_list in merchant_groups.items():
            if len(transactions_list) >= 2:  # At least 2 transactions to be a subscription
                # Check for recurring amounts
                amounts = [t['amount'] for t in transactions_list]
                if self._is_recurring_amount(amounts):
                    # Calculate frequency
                    frequency = self._calculate_frequency(transactions_list)

                    # Get latest transaction
                    latest_txn = max(transactions_list, key=lambda x: x['date'])

                    # Create subscription object
                    subscription = Subscription(
                        name=self._extract_subscription_name(merchant, transactions_list),
                        category=SubscriptionCategory.OTHER,  # Will be categorized later
                        amount=amounts[-1],  # Latest amount
                        frequency=frequency,
                        merchant=merchant,
                        last_charge_date=latest_txn['date'],
                        next_charge_date=self._calculate_next_charge_date(latest_txn['date'], frequency),
                        description=latest_txn['description']
                    )

                    subscriptions.append(subscription)

        return subscriptions

    def _is_recurring_amount(self, amounts: List[float]) -> bool:
        """Check if amounts are recurring (similar amounts)"""
        if len(amounts) < 2:
            return False

        # Check if amounts are similar (within 10% variance)
        avg_amount = sum(amounts) / len(amounts)
        variance_threshold = avg_amount * 0.1

        for amount in amounts:
            if abs(amount - avg_amount) > variance_threshold:
                return False

        return True

    def _calculate_frequency(self, transactions: List[Dict[str, Any]]) -> str:
        """Calculate the frequency of transactions"""
        if len(transactions) < 2:
            return "unknown"

        # Sort by date
        sorted_txns = sorted(transactions, key=lambda x: x['date'])

        # Calculate average interval
        intervals = []
        for i in range(1, len(sorted_txns)):
            interval = (sorted_txns[i]['date'] - sorted_txns[i-1]['date']).days
            intervals.append(interval)

        avg_interval = sum(intervals) / len(intervals)

        # Determine frequency
        if avg_interval <= 7:
            return "weekly"
        elif avg_interval <= 35:
            return "monthly"
        elif avg_interval <= 100:
            return "quarterly"
        elif avg_interval <= 370:
            return "yearly"
        else:
            return "unknown"

    def _calculate_next_charge_date(self, last_date: datetime, frequency: str) -> datetime:
        """Calculate the next charge date based on frequency"""
        if frequency == "weekly":
            return last_date + timedelta(days=7)
        elif frequency == "monthly":
            return last_date + timedelta(days=30)
        elif frequency == "quarterly":
            return last_date + timedelta(days=90)
        elif frequency == "yearly":
            return last_date + timedelta(days=365)
        else:
            return last_date + timedelta(days=30)  # Default to monthly

    def _extract_subscription_name(self, merchant: str, transactions: List[Dict[str, Any]]) -> str:
        """Extract a meaningful name for the subscription"""
        # Try to find a descriptive name from transaction descriptions
        for transaction in transactions:
            desc = transaction['description'].lower()
            if any(keyword in desc for keyword in ['premium', 'pro', 'plus', 'subscription']):
                return transaction['description']

        # Fallback to merchant name
        return merchant.title()

    def _categorize_subscriptions(self, subscriptions: List[Subscription]) -> List[Subscription]:
        """Categorize subscriptions using ADK AI capabilities"""
        for subscription in subscriptions:
            subscription.category = self._determine_category_with_adk(subscription)
        return subscriptions

    def _determine_category_with_adk(self, subscription: Subscription) -> SubscriptionCategory:
        """Use ADK AI to determine subscription category with entity analysis"""
        try:
            # Prepare enhanced context for AI analysis with entity extraction
            context = f"""
            Perform a comprehensive analysis of this subscription transaction to categorize it accurately.

            TASK 1: ENTITY EXTRACTION
            First, identify and extract key entities from the subscription details:
            - Organizations (companies, brands, services)
            - Products (subscription types, service names)
            - Categories (business types, service categories)

            TASK 2: SEMANTIC ANALYSIS
            Analyze the semantic meaning and context:
            - What type of service is this?
            - What industry does it belong to?
            - What is the primary purpose of this subscription?

            TASK 3: CATEGORIZATION
            Based on the entities and semantic analysis, categorize into one of these categories:
            - STREAMING: Video/music streaming services (Netflix, Spotify, Disney+, etc.)
            - SOFTWARE: Software and productivity tools (Adobe, Microsoft, Google Workspace, etc.)
            - FITNESS: Fitness and health apps (Cult Fit, Peloton, MyFitnessPal, etc.)
            - FOOD_DELIVERY: Food delivery and grocery services (Swiggy, Zomato, BigBasket, etc.)
            - SHOPPING: Shopping memberships (Amazon Prime, Flipkart Plus, Myntra Insider, etc.)
            - EDUCATION: Learning platforms (Coursera, Udemy, Byju's, etc.)
            - GAMING: Gaming subscriptions (Xbox Game Pass, PlayStation Plus, etc.)
            - PRODUCTIVITY: Productivity and note-taking apps (Notion, Slack, Trello, etc.)
            - SECURITY: Security and antivirus software (Norton, McAfee, etc.)
            - FINANCE: Financial management tools (Mint, YNAB, etc.)
            - HEALTH: Health and wellness apps (Noom, Calm, Headspace, etc.)
            - ENTERTAINMENT: General entertainment services
            - UTILITIES: Utility and home services
            - OTHER: Any other category

            SUBSCRIPTION DETAILS TO ANALYZE:
            - Name: {subscription.name}
            - Merchant: {subscription.merchant}
            - Description: {subscription.description}
            - Amount: {subscription.amount}
            - Frequency: {subscription.frequency}

            ANALYSIS INSTRUCTIONS:
            1. Extract key entities (organizations, products, services)
            2. Analyze semantic meaning and context
            3. Determine the most appropriate category
            4. Provide confidence level (0.0-1.0)

            RESPONSE FORMAT:
            Return a JSON object with:
            {{
                "entities": {{
                    "organizations": ["list of identified companies/brands"],
                    "products": ["list of identified products/services"],
                    "categories": ["list of identified business categories"]
                }},
                "semantic_analysis": "brief analysis of what this subscription is for",
                "category": "CATEGORY_NAME",
                "confidence": 0.95,
                "reasoning": "explanation of why this category was chosen"
            }}
            """

            # Use ADK AI to analyze with entity extraction
            response = self.analyze_with_ai(context)

            # Parse the AI response
            if response and isinstance(response, str):
                try:
                    # Try to parse as JSON first
                    import json
                    analysis_result = json.loads(response)

                    # Extract category and confidence
                    category_text = analysis_result.get('category', 'OTHER').upper()
                    confidence = analysis_result.get('confidence', 0.0)

                    # Store additional analysis data
                    subscription.entities = analysis_result.get('entities', {})
                    subscription.semantic_analysis = analysis_result.get('semantic_analysis', '')
                    subscription.reasoning = analysis_result.get('reasoning', '')

                    try:
                        category = SubscriptionCategory(category_text.lower())
                        subscription.ai_confidence = confidence
                        return category
                    except ValueError:
                        self.logger.warning(f"Unknown category from AI: {category_text}")

                except json.JSONDecodeError:
                    # Fallback: try to extract category from plain text
                    category_text = response.strip().upper()
                    try:
                        category = SubscriptionCategory(category_text.lower())
                        subscription.ai_confidence = 0.8  # Medium confidence for text extraction
                        return category
                    except ValueError:
                        self.logger.warning(f"Unknown category from AI text: {category_text}")

            # Fallback to OTHER if AI classification fails
            subscription.ai_confidence = 0.0
            return SubscriptionCategory.OTHER

        except Exception as e:
            self.logger.error(f"Error in ADK AI classification: {e}")
            subscription.ai_confidence = 0.0
            return SubscriptionCategory.OTHER

    def _analyze_usage_patterns(self, subscriptions: List[Subscription], transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze usage patterns for subscriptions"""
        usage_data = {}

        for subscription in subscriptions:
            # This would typically involve analyzing app usage, login patterns, etc.
            # For now, we'll use a simple heuristic based on transaction frequency

            if subscription.frequency == "monthly":
                if len([t for t in transactions if subscription.merchant.lower() in t.get('merchant', '').lower()]) > 3:
                    usage_level = "high"
                elif len([t for t in transactions if subscription.merchant.lower() in t.get('merchant', '').lower()]) > 1:
                    usage_level = "medium"
                else:
                    usage_level = "low"
            else:
                usage_level = "unknown"

            usage_data[subscription.name] = {
                'usage_level': usage_level,
                'transaction_count': len([t for t in transactions if subscription.merchant.lower() in t.get('merchant', '').lower()]),
                'last_used': subscription.last_charge_date.isoformat()
            }

        return usage_data

    def _calculate_costs_and_savings(self, subscriptions: List[Subscription]) -> Dict[str, Any]:
        """Calculate costs and potential savings"""
        total_monthly = 0
        total_yearly = 0
        category_costs = {}

        for subscription in subscriptions:
            # Calculate annual cost
            if subscription.frequency == "monthly":
                annual_cost = subscription.amount * 12
            elif subscription.frequency == "yearly":
                annual_cost = subscription.amount
            elif subscription.frequency == "quarterly":
                annual_cost = subscription.amount * 4
            elif subscription.frequency == "weekly":
                annual_cost = subscription.amount * 52
            else:
                annual_cost = subscription.amount * 12  # Default to monthly

            subscription.annual_cost = annual_cost

            # Add to totals
            monthly_cost = annual_cost / 12
            total_monthly += monthly_cost
            total_yearly += annual_cost

            # Category breakdown
            category = subscription.category.value
            if category not in category_costs:
                category_costs[category] = 0
            category_costs[category] += annual_cost

        return {
            'total_monthly': round(total_monthly, 2),
            'total_yearly': round(total_yearly, 2),
            'category_breakdown': {k: round(v, 2) for k, v in category_costs.items()},
            'subscription_count': len(subscriptions)
        }

    async def _generate_recommendations(self, subscriptions: List[Subscription], usage_analysis: Dict[str, Any], cost_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for subscription management"""
        recommendations = []

        # Find unused or low-usage subscriptions
        for subscription in subscriptions:
            usage_info = usage_analysis.get(subscription.name, {})
            usage_level = usage_info.get('usage_level', 'unknown')

            if usage_level == 'low':
                recommendations.append({
                    'type': 'cancel',
                    'subscription': subscription.name,
                    'reason': 'Low usage detected',
                    'potential_savings': subscription.annual_cost,
                    'priority': 'high'
                })
            elif usage_level == 'unknown':
                recommendations.append({
                    'type': 'review',
                    'subscription': subscription.name,
                    'reason': 'Usage pattern unclear - needs manual review',
                    'potential_savings': subscription.annual_cost,
                    'priority': 'medium'
                })

        # Find duplicate services
        category_groups = {}
        for subscription in subscriptions:
            category = subscription.category.value
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(subscription)

        for category, subs in category_groups.items():
            if len(subs) > 1:
                # Multiple subscriptions in same category
                recommendations.append({
                    'type': 'consolidate',
                    'category': category,
                    'subscriptions': [s.name for s in subs],
                    'reason': f'Multiple {category} subscriptions detected',
                    'potential_savings': sum(s.annual_cost for s in subs[1:]),  # Keep one, cancel others
                    'priority': 'medium'
                })

        # High-cost subscriptions
        high_cost_threshold = cost_analysis['total_yearly'] * 0.1  # 10% of total
        for subscription in subscriptions:
            if subscription.annual_cost > high_cost_threshold:
                recommendations.append({
                    'type': 'review_cost',
                    'subscription': subscription.name,
                    'reason': f'High cost subscription (₹{subscription.annual_cost:.2f}/year)',
                    'current_cost': subscription.annual_cost,
                    'priority': 'high'
                })

        return recommendations

    def _generate_summary(self, subscriptions: List[Subscription], cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of subscription analysis"""
        return {
            'total_subscriptions': len(subscriptions),
            'total_monthly_cost': cost_analysis['total_monthly'],
            'total_yearly_cost': cost_analysis['total_yearly'],
            'categories': list(set(sub.category.value for sub in subscriptions)),
            'most_expensive_category': max(cost_analysis['category_breakdown'].items(), key=lambda x: x[1])[0] if cost_analysis['category_breakdown'] else None,
            'analysis_date': datetime.now().isoformat()
        }

    def _subscription_to_dict(self, subscription: Subscription) -> Dict[str, Any]:
        """Convert subscription object to dictionary"""
        return {
            'name': subscription.name,
            'category': subscription.category.value,
            'amount': subscription.amount,
            'frequency': subscription.frequency,
            'merchant': subscription.merchant,
            'last_charge_date': subscription.last_charge_date.isoformat(),
            'next_charge_date': subscription.next_charge_date.isoformat(),
            'description': subscription.description,
            'is_active': subscription.is_active,
            'annual_cost': subscription.annual_cost,
            'ai_confidence': subscription.ai_confidence,
            'entities': subscription.entities,
            'semantic_analysis': subscription.semantic_analysis,
            'reasoning': subscription.reasoning
        }