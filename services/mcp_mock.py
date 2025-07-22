import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class MockMCPService:
    """Mock MCP service that generates realistic financial data"""
    
    def __init__(self):
        self.companies = [
            "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", 
            "META", "NVDA", "NFLX", "UBER", "SPOT"
        ]
        self.metrics = [
            "stock_price", "volume", "market_cap", "pe_ratio", 
            "earnings", "revenue", "debt_ratio", "roi"
        ]
    
    def generate_stock_data(self) -> Dict[str, Any]:
        """Generate mock stock market data"""
        company = random.choice(self.companies)
        base_price = random.uniform(50, 500)
        
        return {
            "type": "stock_data",
            "symbol": company,
            "price": round(base_price + random.uniform(-10, 10), 2),
            "volume": random.randint(1000000, 50000000),
            "change": round(random.uniform(-5, 5), 2),
            "change_percent": round(random.uniform(-3, 3), 2),
            "market_cap": round(base_price * random.randint(1000, 10000), 2),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_financial_metrics(self) -> Dict[str, Any]:
        """Generate mock financial metrics"""
        company = random.choice(self.companies)
        
        return {
            "type": "financial_metrics",
            "symbol": company,
            "pe_ratio": round(random.uniform(10, 35), 2),
            "eps": round(random.uniform(1, 15), 2),
            "revenue": round(random.uniform(10000, 100000), 2),
            "net_income": round(random.uniform(1000, 20000), 2),
            "debt_to_equity": round(random.uniform(0.1, 2.0), 2),
            "roi": round(random.uniform(5, 25), 2),
            "quarter": f"Q{random.randint(1, 4)} 2024",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_market_sentiment(self) -> Dict[str, Any]:
        """Generate mock market sentiment data"""
        sentiments = ["bullish", "bearish", "neutral"]
        sectors = ["technology", "healthcare", "finance", "energy", "consumer"]
        
        return {
            "type": "market_sentiment",
            "overall_sentiment": random.choice(sentiments),
            "sentiment_score": round(random.uniform(-1, 1), 3),
            "sector": random.choice(sectors),
            "news_volume": random.randint(50, 500),
            "social_mentions": random.randint(1000, 10000),
            "analyst_rating": round(random.uniform(1, 5), 1),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_economic_indicators(self) -> Dict[str, Any]:
        """Generate mock economic indicators"""
        indicators = [
            "inflation_rate", "unemployment_rate", "gdp_growth", 
            "interest_rate", "consumer_confidence"
        ]
        
        return {
            "type": "economic_indicators",
            "indicator": random.choice(indicators),
            "value": round(random.uniform(0, 10), 2),
            "previous_value": round(random.uniform(0, 10), 2),
            "change": round(random.uniform(-2, 2), 2),
            "period": "monthly",
            "country": "US",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_random_data(self) -> Dict[str, Any]:
        """Get a random piece of mock data"""
        generators = [
            self.generate_stock_data,
            self.generate_financial_metrics,
            self.generate_market_sentiment,
            self.generate_economic_indicators
        ]
        
        generator = random.choice(generators)
        return generator()
    
    def get_batch_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get a batch of mock data"""
        return [self.get_random_data() for _ in range(count)]

# Singleton instance
mock_mcp = MockMCPService() 