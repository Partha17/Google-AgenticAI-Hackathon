import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any
from config import settings

logger = logging.getLogger(__name__)

class QuotaManager:
    """Manages AI API quota usage to prevent exceeding limits"""
    
    def __init__(self):
        self.quota_file = "ai_quota_usage.json"
        self.usage_data = self._load_usage_data()
    
    def _load_usage_data(self) -> Dict[str, Any]:
        """Load usage data from file"""
        if os.path.exists(self.quota_file):
            try:
                with open(self.quota_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load quota data: {e}")
        
        return {
            "daily_usage": {},
            "hourly_usage": {},
            "last_reset": datetime.now().isoformat()
        }
    
    def _save_usage_data(self):
        """Save usage data to file"""
        try:
            with open(self.quota_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save quota data: {e}")
    
    def _get_date_key(self) -> str:
        """Get current date key for tracking"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def _get_hour_key(self) -> str:
        """Get current hour key for tracking"""
        return datetime.now().strftime("%Y-%m-%d-%H")
    
    def _cleanup_old_data(self):
        """Remove old usage data to keep file size manageable"""
        current_date = datetime.now()
        cutoff_date = current_date - timedelta(days=7)  # Keep 7 days of history
        
        # Clean daily usage
        old_keys = [
            key for key in self.usage_data["daily_usage"].keys()
            if datetime.strptime(key, "%Y-%m-%d") < cutoff_date
        ]
        for key in old_keys:
            del self.usage_data["daily_usage"][key]
        
        # Clean hourly usage (keep only last 24 hours)
        cutoff_hour = current_date - timedelta(hours=24)
        old_keys = [
            key for key in self.usage_data["hourly_usage"].keys()
            if datetime.strptime(key, "%Y-%m-%d-%H") < cutoff_hour
        ]
        for key in old_keys:
            del self.usage_data["hourly_usage"][key]
    
    def check_quota_available(self, requested_requests: int = 1) -> Dict[str, Any]:
        """Check if quota is available for requested number of requests"""
        self._cleanup_old_data()
        
        date_key = self._get_date_key()
        hour_key = self._get_hour_key()
        
        daily_used = self.usage_data["daily_usage"].get(date_key, 0)
        hourly_used = self.usage_data["hourly_usage"].get(hour_key, 0)
        
        daily_remaining = settings.max_daily_ai_requests - daily_used
        hourly_remaining = settings.max_hourly_ai_requests - hourly_used
        
        can_process = (
            daily_remaining >= requested_requests and 
            hourly_remaining >= requested_requests
        )
        
        return {
            "available": can_process,
            "daily_used": daily_used,
            "daily_limit": settings.max_daily_ai_requests,
            "daily_remaining": daily_remaining,
            "hourly_used": hourly_used,
            "hourly_limit": settings.max_hourly_ai_requests,
            "hourly_remaining": hourly_remaining,
            "requested": requested_requests
        }
    
    def record_usage(self, requests_used: int = 1):
        """Record API usage"""
        date_key = self._get_date_key()
        hour_key = self._get_hour_key()
        
        # Update daily usage
        self.usage_data["daily_usage"][date_key] = (
            self.usage_data["daily_usage"].get(date_key, 0) + requests_used
        )
        
        # Update hourly usage
        self.usage_data["hourly_usage"][hour_key] = (
            self.usage_data["hourly_usage"].get(hour_key, 0) + requests_used
        )
        
        self.usage_data["last_usage"] = datetime.now().isoformat()
        self._save_usage_data()
        
        logger.info(f"Recorded {requests_used} AI requests. Daily: {self.usage_data['daily_usage'][date_key]}/{settings.max_daily_ai_requests}, Hourly: {self.usage_data['hourly_usage'][hour_key]}/{settings.max_hourly_ai_requests}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        quota_status = self.check_quota_available()
        
        return {
            "quota_status": quota_status,
            "settings": {
                "max_daily_requests": settings.max_daily_ai_requests,
                "max_hourly_requests": settings.max_hourly_ai_requests,
                "on_demand_only": settings.ai_insights_on_demand_only
            },
            "model": settings.gemini_model
        }
    
    def reset_daily_quota(self):
        """Manually reset daily quota (for testing or admin purposes)"""
        date_key = self._get_date_key()
        self.usage_data["daily_usage"][date_key] = 0
        self._save_usage_data()
        logger.info("Daily quota manually reset")
    
    def reset_hourly_quota(self):
        """Manually reset hourly quota (for testing or admin purposes)"""
        hour_key = self._get_hour_key()
        self.usage_data["hourly_usage"][hour_key] = 0
        self._save_usage_data()
        logger.info("Hourly quota manually reset")

# Singleton instance
quota_manager = QuotaManager() 