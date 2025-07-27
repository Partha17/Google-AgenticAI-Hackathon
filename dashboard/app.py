import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sys
import os
import random
from typing import Dict, Any, List
from difflib import get_close_matches

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import logging
from services.logger_config import get_dashboard_logger, log_error

from models.database import SessionLocal, AIInsight, MCPData, create_tables

# Stock analysis functionality is now built into the dashboard
# No external import needed

# Optional imports - wrap in try-except to handle missing credentials
try:
    from services.insight_generator import insight_generator
    from services.real_data_collector import real_data_collector
    from services.quota_manager import quota_manager
    from adk_agents.mcp_periodic_ai_agent import mcp_periodic_ai_agent
    AI_SERVICES_AVAILABLE = True
except Exception as e:
    print(f"Warning: AI services not available: {e}")
    AI_SERVICES_AVAILABLE = False
    # Create dummy objects for compatibility
    class DummyInsightGenerator:
        def get_recent_insights(self, limit=10):
            return []
        def generate_insights(self, force=False):
            return {"success": False, "error": "AI services not available"}

    class DummyQuotaManager:
        def check_quota_available(self, requests=1):
            return {"available": False, "daily_used": 0, "daily_limit": 0}
        def get_usage_stats(self):
            return {"quota_status": {"available": False}}

    class DummyMCPAgent:
        def get_agent_status(self):
            return {"running": False, "mcp_connection": False, "stats": {}}
        def start_periodic_collection(self):
            return {"success": False, "error": "AI services not available"}
        def stop_periodic_collection(self):
            return {"success": False, "error": "AI services not available"}
        def collect_mcp_data(self):
            return {"success": False, "error": "AI services not available"}
        def generate_ai_analysis(self, force=False):
            return {"success": False, "error": "AI services not available"}

    class DummyDataCollector:
        def test_mcp_connection(self):
            return False
        def collect_data(self):
            return {"success": False, "error": "AI services not available"}

    insight_generator = DummyInsightGenerator()
    quota_manager = DummyQuotaManager()
    mcp_periodic_ai_agent = DummyMCPAgent()
    real_data_collector = DummyDataCollector()

# Page configuration
st.set_page_config(
    page_title="🤖 FinGenie - AI Financial Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed by default for mobile
)

# FinGenie Logo Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem 2rem;
    margin: -1rem -2rem 1rem -2rem;
    border-radius: 0 0 15px 15px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3), 0 0 30px rgba(102, 126, 234, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    "></div>
    <div class="header-logo">
        <span class="logo-icon">🤖</span>
        <span class="logo-text">FinGenie</span>
        <span style="font-size: 1rem; opacity: 0.8; margin-left: 0.5rem;">AI Financial Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Custom CSS for comprehensive responsive design
st.markdown("""
<style>
    /* FinGenie Logo and Header */
    .header-logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .logo-icon {
        font-size: 2rem;
        animation: pulse 2s infinite;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .logo-icon:hover {
        animation: bounce 0.6s ease-in-out;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }

    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .logo-text {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }

    /* Mobile logo adjustments */
    @media (max-width: 768px) {
        .header-logo {
            font-size: 1.2rem;
        }
        .logo-icon {
            font-size: 1.5rem;
        }
    }

    /* Metrics Grid Styling */
    .metrics-grid .row-widget.stHorizontal {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0.5rem !important;
        flex-wrap: wrap !important;
    }

    .metrics-grid .row-widget.stHorizontal > div {
        width: 100% !important;
        flex: none !important;
        min-width: 0 !important;
    }

    /* Override any conflicting styles */
    .metrics-grid .row-widget.stHorizontal > div:nth-child(1),
    .metrics-grid .row-widget.stHorizontal > div:nth-child(2),
    .metrics-grid .row-widget.stHorizontal > div:nth-child(3),
    .metrics-grid .row-widget.stHorizontal > div:nth-child(4) {
        width: 100% !important;
        flex: 0 0 calc(50% - 0.25rem) !important;
    }

    @media (max-width: 768px) {
        .metrics-grid .row-widget.stHorizontal {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }
    /* Mobile-first responsive design */
    .main > div {
        padding-top: 1rem;
    }

    /* Responsive metrics */
    .stMetric > div > div > div > div {
        font-size: 1rem;
    }

    /* Responsive cards */
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        width: 100%;
        box-sizing: border-box;
    }

    .insight-high {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .insight-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .insight-low {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
    }

    .financial-summary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        width: 100%;
        box-sizing: border-box;
    }

    .status-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 0.75rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        width: 100%;
        box-sizing: border-box;
    }
    .status-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 0.75rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        width: 100%;
        box-sizing: border-box;
    }
    .status-error {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 0.75rem;
        border-radius: 10px;
        color: #333;
        text-align: center;
        margin: 0.5rem 0;
        width: 100%;
        box-sizing: border-box;
    }

    /* Responsive Streamlit Components */

    /* Make columns stack on mobile */
    .row-widget.stHorizontal > div {
        flex-wrap: wrap;
    }

    /* Responsive tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        scrollbar-width: thin;
        scrollbar-color: #667eea #f0f0f0;
        padding-bottom: 8px; /* Space for scrollbar */
        margin-bottom: 0.5rem; /* Space below tabs */
    }

    /* Custom scrollbar for webkit browsers */
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 8px;
    }

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 4px;
    }

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
    }

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
    }

    .stTabs [data-baseweb="tab"] {
        height: auto;
        white-space: nowrap;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        flex-shrink: 0;
    }

    /* Responsive expanders */
    .streamlit-expanderHeader {
        font-size: 1rem;
        padding: 0.75rem;
    }

    /* Responsive dataframes */
    .stDataFrame {
        overflow-x: auto;
        font-size: 0.9rem;
    }

    /* Responsive plotly charts */
    .js-plotly-plot {
        width: 100% !important;
        height: auto !important;
    }

    /* Responsive sidebar */
    .css-1d391kg {
        width: 100% !important;
    }

    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .main > div {
            padding-top: 0.5rem;
        }

        .stMetric > div > div > div > div {
            font-size: 0.9rem;
        }

        .insight-card {
            padding: 0.75rem;
            margin: 0.25rem 0;
        }

        .financial-summary {
            padding: 1rem;
            margin: 0.5rem 0;
        }

        .status-good, .status-warning, .status-error {
            padding: 0.5rem;
            margin: 0.25rem 0;
        }

        /* Force columns to stack on mobile (but not for 4-column layouts) */
        .row-widget.stHorizontal > div:not(:nth-child(4n+1)):not(:nth-child(4n+2)):not(:nth-child(4n+3)):not(:nth-child(4n+4)) {
            flex-direction: column !important;
        }

        .row-widget.stHorizontal > div:not(:nth-child(4n+1)):not(:nth-child(4n+2)):not(:nth-child(4n+3)):not(:nth-child(4n+4)) > div {
            width: 100% !important;
            margin-bottom: 0.5rem;
        }

        /* Make 4-column layouts into 2x2 grid on mobile */
        .row-widget.stHorizontal > div:nth-child(4n+1),
        .row-widget.stHorizontal > div:nth-child(4n+2),
        .row-widget.stHorizontal > div:nth-child(4n+3),
        .row-widget.stHorizontal > div:nth-child(4n+4) {
            width: 50% !important;
            flex: 0 0 50% !important;
            flex-direction: row !important;
        }

        /* Ensure metric cards in 4-column layouts don't stack */
        .row-widget.stHorizontal > div:nth-child(4n+1) > div,
        .row-widget.stHorizontal > div:nth-child(4n+2) > div,
        .row-widget.stHorizontal > div:nth-child(4n+3) > div,
        .row-widget.stHorizontal > div:nth-child(4n+4) > div {
            width: 100% !important;
            margin-bottom: 0 !important;
        }

        /* Ensure proper spacing for 2x2 grid */
        .row-widget.stHorizontal > div:nth-child(odd) {
            padding-right: 0.25rem;
        }

        .row-widget.stHorizontal > div:nth-child(even) {
            padding-left: 0.25rem;
        }

        /* Force 4-column layouts to wrap into 2x2 grid */
        .row-widget.stHorizontal > div:nth-child(4n+1),
        .row-widget.stHorizontal > div:nth-child(4n+2) {
            margin-bottom: 0.5rem;
        }

        /* Ensure the container allows wrapping */
        .row-widget.stHorizontal {
            flex-wrap: wrap !important;
            display: flex !important;
        }

        /* Specific styling for 4-column metric containers */
        .row-widget.stHorizontal:has(> div:nth-child(4)) {
            gap: 0.5rem;
        }

        /* Adjust tabs for mobile */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            scrollbar-width: thin;
            scrollbar-color: #667eea #f0f0f0;
            padding-bottom: 10px; /* More space for scrollbar */
            margin-bottom: 0.5rem; /* Space below tabs */
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 6px;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 4px;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        }

        /* Ensure tab container has proper positioning */
        .stTabs [data-baseweb="tab-list"] {
            position: relative;
        }

        /* Add spacing between tabs and content */
        .stTabs [data-baseweb="tab-panel"] {
            margin-top: 0.5rem !important;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.1rem 0.4rem 0.3rem 0.4rem;
            font-size: 0.8rem;
            min-width: auto;
            flex-shrink: 0 !important;
            white-space: nowrap !important;
            height: auto !important;
            min-height: 28px !important;
        }

        /* Hover effects for tabs */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(102, 126, 234, 0.05) !important;
            transition: background-color 0.2s ease;
        }

        /* Focus states for accessibility */
        .stTabs [data-baseweb="tab"]:focus {
            outline: 2px solid #667eea !important;
            outline-offset: 2px !important;
        }

        /* Adjust expanders for mobile */
        .streamlit-expanderHeader {
            font-size: 0.9rem;
            padding: 0.5rem;
        }

        /* Adjust dataframes for mobile */
        .stDataFrame {
            font-size: 0.8rem;
        }

        /* Ensure proper viewport */
        .stApp {
            max-width: 100vw;
            overflow-x: hidden;
        }

        /* Adjust metric cards for mobile */
        .stMetric {
            margin-bottom: 0.5rem;
        }

        /* Make buttons more touch-friendly */
        .stButton > button {
            min-height: 44px;
            padding: 0.5rem 1rem;
        }

        /* Center align buttons when there are 1-2 buttons */
        .stHorizontal > div:has(.stButton):only-child,
        .stHorizontal > div:has(.stButton):nth-child(1):nth-last-child(2),
        .stHorizontal > div:has(.stButton):nth-child(2):nth-last-child(1) {
            display: flex;
            justify-content: center;
        }

        /* Center single buttons */
        .stButton:only-child {
            display: flex;
            justify-content: center;
        }

        /* Adjust text inputs for mobile */
        .stTextInput > div > div > input {
            font-size: 16px; /* Prevents zoom on iOS */
        }
    }

    /* Tablet responsive adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main > div {
            padding-top: 1.5rem;
        }

        .insight-card {
            padding: 1.25rem;
        }

        .financial-summary {
            padding: 1.75rem;
        }

        /* Adjust columns for tablet */
        .row-widget.stHorizontal > div > div {
            margin-bottom: 0.75rem;
        }
    }

    /* Large screen optimizations */
    @media (min-width: 1025px) {
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.5rem;
            font-size: 1.125rem; /* Increased by 2 points (1rem = 16px, 1.125rem = 18px) */
        }

        .streamlit-expanderHeader {
            font-size: 1.125rem; /* Increased by 2 points */
            padding: 1rem;
        }

        /* Increase metric font sizes on desktop */
        .stMetric > div > div > div > div {
            font-size: 1.125rem; /* Increased by 2 points */
        }

        /* Increase insight card font sizes on desktop */
        .insight-card {
            font-size: 1.125rem; /* Increased by 2 points */
        }

        /* Increase financial summary font sizes on desktop */
        .financial-summary {
            font-size: 1.125rem; /* Increased by 2 points */
        }
    }

    /* Ensure charts are responsive */
    .element-container {
        width: 100% !important;
    }

    /* Improve touch targets on mobile */
    @media (max-width: 768px) {
        .stSelectbox > div > div {
            min-height: 44px;
        }

        .stCheckbox > div > div {
            min-height: 44px;
        }

        .stRadio > div > div {
            min-height: 44px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Responsive layout helper functions
def responsive_columns(ratios, gap=1):
    """
    Create responsive columns that stack on mobile devices
    Args:
        ratios: List of column ratios (e.g., [2, 1] for 2:1 ratio)
        gap: Gap between columns in rem
    """
    # Use st.columns for desktop layout
    return st.columns(ratios)

def is_mobile_device():
    """
    Detect if the user is on a mobile device
    Returns True if mobile, False otherwise
    """
    # This is a simple detection based on user agent
    # In a real implementation, you might want to use JavaScript
    return False  # Default to desktop for now

class ModernFinancialDashboard:
    def __init__(self):
        self.logger = get_dashboard_logger()
        self.logger.info("Dashboard initialized")
        create_tables()

        # Disable Fi MCP authentication for this use case
        self.mcp_enabled = False
        self.logger.info("Fi MCP authentication disabled - using mock data mode")

    def extract_financial_data(self, mcp_record) -> Dict[str, Any]:
        """Extract financial data from MCP record with proper parsing"""
        if not mcp_record:
            return {}

        try:
            # Get the data from the record
            record_data = mcp_record.get_data()

            # Handle different data structures
            if isinstance(record_data, dict):
                # Check if it's the raw response format
                if 'data' in record_data and 'content' in record_data['data']:
                    # Parse the JSON content
                    content = record_data['data']['content'][0]['text']
                    parsed_data = json.loads(content)
                    return parsed_data
                else:
                    return record_data
            # Try to parse as JSON string
            if isinstance(record_data, str):
                return json.loads(record_data)

            return record_data
        except Exception as e:
            st.error(f"Error parsing financial data: {e}")
            return {}

    def get_parsed_financial_summary(self) -> Dict[str, Any]:
        """Get financial summary - uses mock data when MCP is disabled"""
        if not self.mcp_enabled:
            # Return mock data when MCP is disabled
            return {
                "net_worth": 2500000,
                "total_assets": 3200000,
                "total_liabilities": 700000,
                "credit_score": 785,
                "epf_balance": 450000,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "bank_balance": 180000
            }

        # Original MCP data logic
        db = SessionLocal()
        summary = {
            "net_worth": "N/A",
            "total_assets": "N/A",
            "total_liabilities": "N/A",
            "credit_score": "N/A",
            "epf_balance": "N/A",
            "last_updated": "N/A",
            "bank_balance": "N/A"
        }

        try:
            # Get net worth data
            latest_nw = db.query(MCPData).filter(
                MCPData.data_type == "net_worth"
            ).order_by(MCPData.timestamp.desc()).first()

            if latest_nw:
                nw_data = self.extract_financial_data(latest_nw)
                if 'netWorthResponse' in nw_data:
                    net_worth_response = nw_data['netWorthResponse']

                    # Extract total net worth
                    if 'totalNetWorthValue' in net_worth_response:
                        summary["net_worth"] = int(net_worth_response['totalNetWorthValue']['units'])

                    # Calculate total assets
                    total_assets = 0
                    if 'assetValues' in net_worth_response:
                        for asset in net_worth_response['assetValues']:
                            total_assets += int(asset['value']['units'])
                    summary["total_assets"] = total_assets

                    # Calculate total liabilities
                    total_liabilities = 0
                    if 'liabilityValues' in net_worth_response:
                        for liability in net_worth_response['liabilityValues']:
                            total_liabilities += int(liability['value']['units'])
                    summary["total_liabilities"] = total_liabilities

                # Extract bank balance from account details
                bank_balance = 0

                # First try to get bank balance from net worth data
                if 'accountDetailsBulkResponse' in nw_data:
                    account_map = nw_data['accountDetailsBulkResponse']['accountDetailsMap']
                    for account_id, account_info in account_map.items():
                        if 'depositSummary' in account_info:
                            balance = int(account_info['depositSummary']['currentBalance']['units'])
                            bank_balance += balance

                # If no bank balance found in net worth data, try bank_transactions data
                if bank_balance == 0:
                    latest_bank = db.query(MCPData).filter(
                        MCPData.data_type == "bank_transactions"
                    ).order_by(MCPData.timestamp.desc()).first()

                    if latest_bank:
                        bank_data = self.extract_financial_data(latest_bank)
                        if 'accountDetailsBulkResponse' in bank_data:
                            account_map = bank_data['accountDetailsBulkResponse']['accountDetailsMap']
                            for account_id, account_info in account_map.items():
                                if 'depositSummary' in account_info:
                                    balance = int(account_info['depositSummary']['currentBalance']['units'])
                                    bank_balance += balance

                summary["bank_balance"] = bank_balance if bank_balance > 0 else "Not Available"

                summary["last_updated"] = latest_nw.timestamp.strftime("%Y-%m-%d %H:%M")

            # Get credit score (currently not available in MCP response)
            latest_credit = db.query(MCPData).filter(
                MCPData.data_type == "credit_report"
            ).order_by(MCPData.timestamp.desc()).first()

            if latest_credit:
                credit_data = self.extract_financial_data(latest_credit)
                if 'creditReports' in credit_data and len(credit_data['creditReports']) > 0:
                    credit_report = credit_data['creditReports'][0]
                    if 'creditReportData' in credit_report and 'score' in credit_report['creditReportData']:
                        summary["credit_score"] = int(credit_report['creditReportData']['score']['bureauScore'])
            else:
                # Credit score not available in current MCP response
                summary["credit_score"] = "Not Available"

            # Get EPF balance (currently not available in MCP response)
            latest_epf = db.query(MCPData).filter(
                MCPData.data_type == "epf_details"
            ).order_by(MCPData.timestamp.desc()).first()

            if latest_epf:
                epf_data = self.extract_financial_data(latest_epf)
                if 'uanAccounts' in epf_data and len(epf_data['uanAccounts']) > 0:
                    uan_account = epf_data['uanAccounts'][0]
                    if 'rawDetails' in uan_account and 'overall_pf_balance' in uan_account['rawDetails']:
                        pf_balance = uan_account['rawDetails']['overall_pf_balance']
                        summary["epf_balance"] = int(pf_balance['current_pf_balance'])
            else:
                # EPF balance not available in current MCP response
                summary["epf_balance"] = "Not Available"
        except Exception as e:
            st.error(f"Error getting financial summary: {e}")
        finally:
            db.close()

        return summary

    def main(self):
        """Main dashboard interface"""
        # Header with modern design
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("💰 Fi Financial AI Dashboard")
            st.markdown("**Real-time financial analysis powered by AI agents and Fi MCP data**")
        with col2:
            if st.button("🔄 Refresh Data", type="primary", key="main_refresh_data"):
                st.rerun()

        # Financial Overview with real data
        self.render_financial_overview()

                # Main content tabs with modern styling
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🧠 AI Insights",
            "📈 Portfolio Analysis",
            "📊 Stock Tracker",
            "📱 Subscription Tracker",
            "💳 Credit & Debt",
            "🤖 MCP AI Agent",
            "⚙️ System Status"
        ])

        with tab1:
            self.render_modern_insights()

        with tab2:
            self.render_portfolio_analysis()

        with tab3:
            self.render_stock_tracker()

        with tab4:
            self.render_subscription_tracker()

        with tab5:
            self.render_credit_analysis()

        with tab6:
            self.render_mcp_ai_agent()

        with tab7:
            self.render_system_status()

    def render_financial_overview(self):
        """Render modern financial overview"""
        summary = self.get_parsed_financial_summary()

        # Key metrics in cards
        st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            net_worth = summary.get('net_worth', 'N/A')
            if isinstance(net_worth, (int, float)):
                st.metric("💰 Net Worth", f"₹{net_worth:,}", delta=None)
            else:
                st.metric("💰 Net Worth", net_worth)

        with col2:
            credit_score = summary.get('credit_score', 'N/A')
            if isinstance(credit_score, (int, float)):
                delta_color = "normal"
                if credit_score >= 750:
                    delta_color = "inverse"
                st.metric("📊 Credit Score", credit_score, delta=f"{'Excellent' if credit_score >= 750 else 'Good' if credit_score >= 700 else 'Fair'}")
            else:
                st.metric("📊 Credit Score", credit_score)

        with col3:
            epf_balance = summary.get('epf_balance', 'N/A')
            if isinstance(epf_balance, (int, float)):
                st.metric("🏛️ EPF Balance", f"₹{epf_balance:,}")
            else:
                st.metric("🏛️ EPF Balance", epf_balance)

        with col4:
            bank_balance = summary.get('bank_balance', 'N/A')
            if isinstance(bank_balance, (int, float)):
                st.metric("🏦 Bank Balance", f"₹{bank_balance:,}")
            else:
                st.metric("🏦 Bank Balance", bank_balance)

        st.markdown('</div>', unsafe_allow_html=True)

        # Financial health indicator
        if isinstance(net_worth, (int, float)) and isinstance(credit_score, (int, float)):
            col1, col2 = st.columns(2)

            with col1:
                # Net worth breakdown
                total_assets = summary.get('total_assets', 0)
                total_liabilities = summary.get('total_liabilities', 0)

                if isinstance(total_assets, (int, float)) and isinstance(total_liabilities, (int, float)):
                    fig = go.Figure(data=[
                        go.Bar(name='Assets', x=['Your Portfolio'], y=[total_assets], marker_color='#11998e'),
                        go.Bar(name='Liabilities', x=['Your Portfolio'], y=[total_liabilities], marker_color='#f5576c')
                    ])
                    fig.update_layout(
                        title="Assets vs Liabilities",
                        barmode='group',
                        height=300,
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Financial health score
                health_score = 0
                if credit_score >= 750:
                    health_score += 40
                elif credit_score >= 700:
                    health_score += 30
                elif credit_score >= 650:
                    health_score += 20

                if total_assets > total_liabilities * 2:
                    health_score += 30
                elif total_assets > total_liabilities:
                    health_score += 20

                if epf_balance > 100000:
                    health_score += 20
                elif epf_balance > 50000:
                    health_score += 10

                if bank_balance > 50000:
                    health_score += 10

                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = health_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Financial Health Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 30], 'color': "#fecfef"},
                            {'range': [30, 60], 'color': "#f093fb"},
                            {'range': [60, 80], 'color': "#667eea"},
                            {'range': [80, 100], 'color': "#11998e"}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

    def render_modern_insights(self):
        """Render AI insights with modern, intuitive design"""
        st.header("🧠 AI-Powered Financial Insights")

        # Controls
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_term = st.text_input("🔍 Search insights...", placeholder="Search by keyword, risk, opportunity...")
        with col2:
            insight_filter = st.selectbox("Filter by type", ["All", "trend_analysis", "risk_assessment", "opportunity", "market_sentiment"])
        with col3:
            # Check quota status for insights generation
            quota_status = quota_manager.check_quota_available(3)  # Estimate 3 requests needed

            if quota_status["available"]:
                if st.button("✨ Generate New Insights", type="primary", key="insights_generate_new"):
                    with st.spinner("🤖 AI is analyzing your financial data..."):
                        try:
                            insight_generator.generate_insights(force=True)
                            st.success("✅ New insights generated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error generating insights: {str(e)}")
                    st.rerun()

                # Show quota status
                st.caption(f"🔄 Quota: {quota_status['daily_used']}/{quota_status['daily_limit']} daily")
            else:
                # Show quota restriction
                st.button("⚠️ Quota Exceeded", disabled=True, type="secondary", key="insights_quota_exceeded")
                st.error(f"❌ **Quota Limit Reached**\n\n"
                        f"Daily: {quota_status['daily_used']}/{quota_status['daily_limit']}\n\n"
                        f"Hourly: {quota_status['hourly_used']}/{quota_status['hourly_limit']}\n\n"
                        f"Please wait before generating more insights.")

        # Interactive AI Chat Section
        st.markdown("---")
        st.subheader("💬 Ask AI About Your Finances")

        user_question = st.text_area(
            "Ask any financial question:",
            placeholder="E.g., 'What's my portfolio allocation?', 'How are my investments performing?', 'What's my risk level?'",
            height=80
        )

        if st.button("🤖 Get AI Answer", key="insights_ai_answer") and user_question:
            with st.spinner("🤖 AI is analyzing your data..."):
                try:
                    # Get financial context
                    self.logger.info(f"Processing AI query: {user_question[:50]}...")
                    db = SessionLocal()
                    recent_data = db.query(MCPData).order_by(MCPData.created_at.desc()).limit(20).all()
                    recent_insights = db.query(AIInsight).order_by(AIInsight.created_at.desc()).limit(5).all()
                    self.logger.debug(f"Found {len(recent_data)} data records, {len(recent_insights)} insights")

                    # Extract actual financial values from database
                    def extract_financial_values(mcp_data):
                        """Extract actual financial values from MCP data"""
                        try:
                            import json
                            raw_data = json.loads(mcp_data.raw_data)
                            if raw_data.get('success') and 'data' in raw_data:
                                content = raw_data['data'].get('content', [])
                                if content and content[0].get('type') == 'text':
                                    # Parse the nested JSON
                                    inner_data = json.loads(content[0]['text'])
                                    return {
                                        'data_type': mcp_data.data_type,
                                        'parsed_content': inner_data,
                                        'timestamp': raw_data.get('timestamp')
                                    }
                        except Exception as e:
                            st.warning(f"Error extracting {mcp_data.data_type}: {e}")
                        return None

                    # Process all financial data
                    extracted_data = {}
                    for data in recent_data:
                        extracted = extract_financial_values(data)
                        if extracted:
                            extracted_data[data.data_type] = extracted['parsed_content']

                    # Prepare context with actual financial values
                    financial_context = {
                        "query": user_question,
                        "data_available": list(extracted_data.keys()),
                        "financial_data": extracted_data,
                        "recent_insights": [
                            {
                                "title": insight.title,
                                "type": insight.insight_type,
                                "content": insight.content[:200] + "..." if len(insight.content) > 200 else insight.content
                            } for insight in recent_insights
                        ]
                    }

                    # Add financial summary for easy AI analysis
                    if extracted_data:
                        summary = {}

                        # Extract net worth summary
                        if 'net_worth' in extracted_data:
                            net_worth = extracted_data['net_worth'].get('netWorthResponse', {})
                            assets = net_worth.get('assetValues', [])
                            liabilities = net_worth.get('liabilityValues', [])

                            total_assets = sum(int(asset['value']['units']) for asset in assets)
                            total_liabilities = sum(int(liability['value']['units']) for liability in liabilities)

                            summary['net_worth'] = {
                                'total_assets': total_assets,
                                'total_liabilities': total_liabilities,
                                'net_worth': total_assets - total_liabilities,
                                'currency': 'INR',
                                'asset_breakdown': {
                                    asset['netWorthAttribute'].replace('ASSET_TYPE_', ''): int(asset['value']['units'])
                                    for asset in assets
                                },
                                'liability_breakdown': {
                                    liability['netWorthAttribute'].replace('LIABILITY_TYPE_', ''): int(liability['value']['units'])
                                    for liability in liabilities
                                }
                            }

                        # Extract credit report summary
                        if 'credit_report' in extracted_data:
                            credit_data = extracted_data['credit_report'].get('creditReportResponse', {})
                            if credit_data:
                                summary['credit_profile'] = {
                                    'score': credit_data.get('score', 'N/A'),
                                    'accounts_summary': credit_data.get('summary', {}),
                                    'recent_inquiries': len(credit_data.get('inquiries', [])),
                                    'active_loans': len(credit_data.get('loans', []))
                                }

                        financial_context['financial_summary'] = summary
                    else:
                        # Add sample data if no real data
                        financial_context["sample_portfolio"] = {
                            "note": "Sample data - connect Fi MCP server for real data",
                            "total_value": 100000,
                            "holdings": [
                                {"symbol": "AAPL", "shares": 50, "value": 8500},
                                {"symbol": "GOOGL", "shares": 20, "value": 5000},
                                {"symbol": "MSFT", "shares": 30, "value": 10000}
                            ]
                        }

                    db.close()

                    # Generate AI response
                    from services.enhanced_ai_agent import enhanced_ai_agent

                    query_lower = user_question.lower()
                    if "portfolio" in query_lower:
                        response = enhanced_ai_agent.generate_portfolio_analysis(financial_context)
                    elif "risk" in query_lower:
                        response = enhanced_ai_agent.generate_risk_assessment(financial_context)
                    else:
                        response = enhanced_ai_agent.generate_market_insight(financial_context)

                    st.success("🤖 AI Response:")
                    st.write(response)

                    with st.expander("📊 View Data Context"):
                        st.json(financial_context)

                except Exception as e:
                    st.error(f"❌ AI analysis error: {e}")
                    st.info("Make sure your Google API key is configured in the .env file")

        st.markdown("---")

        # Get insights
        recent_insights = insight_generator.get_recent_insights(limit=50)

        if not recent_insights:
            st.markdown("""
            <div class="insight-card">
                <h3>🌟 Welcome to AI Financial Insights!</h3>
                <p>No insights available yet. Click "Generate New Insights" to start AI analysis of your financial data.</p>
                <p><strong>What you'll get:</strong></p>
                <ul>
                    <li>📈 Investment opportunities based on your portfolio</li>
                    <li>⚠️ Risk assessments for your current positions</li>
                    <li>💡 Personalized financial advice</li>
                    <li>📊 Market trends affecting your investments</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            return

        # Filter insights
        filtered_insights = recent_insights
        if insight_filter != "All":
            filtered_insights = [i for i in recent_insights if i.insight_type == insight_filter]

        if search_term:
            filtered_insights = [
                i for i in filtered_insights
                if search_term.lower() in i.title.lower() or search_term.lower() in i.content.lower()
            ]

        # Display insights with beautiful cards
        if not filtered_insights:
            st.info("No insights match your search criteria.")
            return

        # Group insights by confidence level
        high_confidence = [i for i in filtered_insights if i.confidence_score >= 0.8]
        medium_confidence = [i for i in filtered_insights if 0.5 <= i.confidence_score < 0.8]
        low_confidence = [i for i in filtered_insights if i.confidence_score < 0.5]

        # Display high confidence insights first
        if high_confidence:
            st.subheader("🌟 High Confidence Insights")
            for insight in high_confidence[:5]:  # Show top 5
                self.render_insight_card(insight, "high")

        if medium_confidence:
            st.subheader("⭐ Medium Confidence Insights")
            for insight in medium_confidence[:3]:  # Show top 3
                self.render_insight_card(insight, "medium")

        if low_confidence:
            with st.expander(f"📝 Other Insights ({len(low_confidence)} more)"):
                for insight in low_confidence:
                    self.render_insight_card(insight, "low")

    def render_insight_card(self, insight: AIInsight, confidence_level: str):
        """Render an individual insight card with modern design"""
        # Choose card style based on confidence
        card_class = f"insight-card insight-{confidence_level}"

        # Get insight type emoji
        type_emoji = {
            "trend_analysis": "📈",
            "risk_assessment": "⚠️",
            "opportunity": "💰",
            "market_sentiment": "📊",
            "financial_health_analysis": "🏥"
        }.get(insight.insight_type, "📝")

        # Format confidence score
        confidence_text = f"{insight.confidence_score:.1%}"
        confidence_color = "#11998e" if insight.confidence_score >= 0.8 else "#f5576c" if insight.confidence_score >= 0.5 else "#fcb69f"

        # Format date
        time_ago = datetime.now() - insight.created_at
        if time_ago.days > 0:
            time_text = f"{time_ago.days} days ago"
        elif time_ago.seconds > 3600:
            time_text = f"{time_ago.seconds // 3600} hours ago"
        else:
            time_text = f"{time_ago.seconds // 60} minutes ago"

        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <h3>{type_emoji} {insight.title}</h3>
                <div style="text-align: right; font-size: 0.9rem;">
                    <div style="background: {confidence_color}; padding: 0.2rem 0.5rem; border-radius: 15px; margin-bottom: 0.3rem;">
                        {confidence_text} confidence
                    </div>
                    <div style="opacity: 0.8;">{time_text}</div>
                </div>
            </div>
            <p style="line-height: 1.6; margin-bottom: 1rem;">{insight.content}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; opacity: 0.9;">
                <span>📂 {insight.insight_type.replace('_', ' ').title()}</span>
                <span>🤖 AI Analysis</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_portfolio_analysis(self):
        """Render detailed portfolio analysis"""
        st.header("📈 Portfolio Analysis")

        # Get net worth data
        db = SessionLocal()
        try:
            latest_nw = db.query(MCPData).filter(
                MCPData.data_type == "net_worth"
            ).order_by(MCPData.timestamp.desc()).first()

            if not latest_nw:
                st.info("No portfolio data available. Please collect data first.")
                return

            nw_data = self.extract_financial_data(latest_nw)

            if 'netWorthResponse' in nw_data:
                net_worth_response = nw_data['netWorthResponse']

                # Asset allocation pie chart
                col1, col2 = st.columns(2)

                with col1:
                    if 'assetValues' in net_worth_response:
                        assets_data = []
                        asset_names = {
                            'ASSET_TYPE_MUTUAL_FUND': 'Mutual Funds',
                            'ASSET_TYPE_EPF': 'EPF',
                            'ASSET_TYPE_INDIAN_SECURITIES': 'Indian Stocks',
                            'ASSET_TYPE_SAVINGS_ACCOUNTS': 'Savings',
                            'ASSET_TYPE_US_SECURITIES': 'US Stocks'
                        }

                        for asset in net_worth_response['assetValues']:
                            asset_type = asset['netWorthAttribute']
                            value = int(asset['value']['units'])
                            readable_name = asset_names.get(asset_type, asset_type)
                            assets_data.append({'Asset': readable_name, 'Value': value})

                        df_assets = pd.DataFrame(assets_data)
                        fig = px.pie(df_assets, values='Value', names='Asset',
                                   title="Asset Allocation")
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)

                with col2:
                    if 'liabilityValues' in net_worth_response:
                        liabilities_data = []
                        liability_names = {
                            'LIABILITY_TYPE_VEHICLE_LOAN': 'Vehicle Loan',
                            'LIABILITY_TYPE_HOME_LOAN': 'Home Loan',
                            'LIABILITY_TYPE_OTHER_LOAN': 'Other Loans'
                        }

                        for liability in net_worth_response['liabilityValues']:
                            liability_type = liability['netWorthAttribute']
                            value = int(liability['value']['units'])
                            readable_name = liability_names.get(liability_type, liability_type)
                            liabilities_data.append({'Liability': readable_name, 'Value': value})

                        df_liabilities = pd.DataFrame(liabilities_data)
                        fig = px.bar(df_liabilities, x='Liability', y='Value',
                                   title="Liabilities Breakdown")
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)

                # Detailed breakdown
                st.subheader("📊 Detailed Portfolio")

                # Assets table
                if 'assetValues' in net_worth_response:
                    assets_df = pd.DataFrame([
                        {
                            'Asset Type': asset_names.get(asset['netWorthAttribute'], asset['netWorthAttribute']),
                            'Value (₹)': f"₹{int(asset['value']['units']):,}",
                            'Percentage': f"{(int(asset['value']['units']) / sum(int(a['value']['units']) for a in net_worth_response['assetValues']) * 100):.1f}%"
                        }
                        for asset in net_worth_response['assetValues']
                    ])
                    st.dataframe(assets_df, use_container_width=True, hide_index=True)

        finally:
            db.close()

    def render_stock_tracker(self):
        """Render stock tracking dashboard with watchlist and AI analysis"""
        st.header("📊 Stock Tracker & AI Analysis")

        # Initialize session state for watchlist
        if 'stock_watchlist' not in st.session_state:
            st.session_state.stock_watchlist = []

        if 'stock_analysis_results' not in st.session_state:
            st.session_state.stock_analysis_results = {}

        # Watchlist management section
        st.subheader("📋 Manage Your Watchlist")

        # Smart stock search with autocomplete
        search_query = st.text_input(
            "🔍 Search for stocks",
            placeholder="Type stock name or symbol (e.g., TCS, Tata, Infosys)",
            help="Search for stocks by name or symbol. Press Enter to search.",
            key="stock_search"
        )

        # Show search suggestions
        if search_query and len(search_query) >= 2:
            with st.spinner("🔍 Searching for stocks..."):
                suggestions = self.get_stock_suggestions(search_query, limit=8)

            if suggestions:
                st.subheader("📋 Search Results")

                # Create columns for suggestions
                cols = st.columns(2)
                for i, suggestion in enumerate(suggestions):
                    with cols[i % 2]:
                        # Create a button for each suggestion
                        if st.button(
                            f"📈 {suggestion['symbol']} - {suggestion['name'][:30]}...",
                            key=f"suggest_{suggestion['symbol']}_{i}",
                            help=f"Add {suggestion['symbol']} to watchlist"
                        ):
                            if suggestion['symbol'] not in st.session_state.stock_watchlist:
                                st.session_state.stock_watchlist.append(suggestion['symbol'])
                                st.success(f"✅ Added {suggestion['symbol']} to watchlist!")
                                st.rerun()
                            else:
                                st.warning(f"⚠️ {suggestion['symbol']} is already in your watchlist!")
            else:
                st.info("No stocks found matching your search. Try a different keyword.")

        # Manual input section
        st.markdown("---")
        st.subheader("📝 Manual Stock Entry")

        col1, col2 = st.columns([3, 1])

        with col1:
            # Input for adding stocks manually
            stock_input = st.text_input(
                "Add stocks manually",
                placeholder="Enter stock symbols separated by commas (e.g., TCS, INFY, RELIANCE)",
                help="Enter stock symbols in uppercase. Press Enter or click Add to validate and add stocks.",
                key="manual_stock_input"
            )

        with col2:
            add_clicked = st.button("➕ Add to Watchlist", type="primary", key="add_manual")

        # Handle stock addition (both Enter key and button click)
        if (stock_input.strip() and (add_clicked or st.session_state.get('manual_stock_input_processed') != stock_input)):
            st.session_state['manual_stock_input_processed'] = stock_input

            # Parse stock symbols
            new_stocks = [stock.strip().upper() for stock in stock_input.split(',') if stock.strip()]
            valid_stocks = []
            invalid_stocks = []

            with st.spinner("🔍 Validating stocks..."):
                for stock in new_stocks:
                    validation = self.validate_stock_symbol(stock)

                    if validation['valid']:
                        valid_stocks.append(validation['symbol'])
                        if validation.get('was_corrected', False):
                            st.info(f"✅ Corrected '{stock}' to '{validation['symbol']}'")
                    else:
                        invalid_stocks.append(stock)
                        st.error(f"❌ Invalid stock: {stock}")

                        # Show suggestions for invalid stocks
                        if 'suggestions' in validation and validation['suggestions']:
                            st.write("💡 Did you mean:")
                            for suggestion in validation['suggestions'][:3]:
                                if st.button(f"📈 {suggestion['symbol']} - {suggestion['name'][:30]}...",
                                           key=f"correct_{stock}_{suggestion['symbol']}"):
                                    if suggestion['symbol'] not in st.session_state.stock_watchlist:
                                        st.session_state.stock_watchlist.append(suggestion['symbol'])
                                        st.success(f"✅ Added {suggestion['symbol']} to watchlist!")
                                        st.rerun()

            # Add valid stocks to watchlist
            for stock in valid_stocks:
                if stock not in st.session_state.stock_watchlist:
                    st.session_state.stock_watchlist.append(stock)

            if valid_stocks:
                st.success(f"✅ Added {len(valid_stocks)} valid stocks to watchlist!")
            if invalid_stocks:
                st.error(f"❌ Could not add {len(invalid_stocks)} invalid stocks")

            st.rerun()

        # Display current watchlist with badges
        if st.session_state.stock_watchlist:
            st.markdown("**Current Watchlist:**")

            # Create badges for each stock
            badge_html = ""
            for i, stock in enumerate(st.session_state.stock_watchlist):
                badge_html += f"""
                <span style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    margin: 0.2rem;
                    display: inline-block;
                    font-weight: bold;
                ">
                    {stock}
                    <a href="?remove_stock={i}" style="color: white; text-decoration: none; margin-left: 0.5rem;">×</a>
                </span>
                """

            st.markdown(badge_html, unsafe_allow_html=True)

            # Handle stock removal
            if st.query_params.get("remove_stock"):
                try:
                    remove_index = int(st.query_params.get("remove_stock"))
                    if 0 <= remove_index < len(st.session_state.stock_watchlist):
                        removed_stock = st.session_state.stock_watchlist.pop(remove_index)
                        st.success(f"✅ Removed {removed_stock} from watchlist")
                        st.rerun()
                except:
                    pass

            # Clear all button
            if st.button("🗑️ Clear All", type="secondary"):
                st.session_state.stock_watchlist = []
                st.session_state.stock_analysis_results = {}
                st.success("✅ Watchlist cleared!")
                st.rerun()

        # AI Analysis Section
        if st.session_state.stock_watchlist:
            st.markdown("---")
            st.subheader("🤖 AI-Powered Stock Analysis")

            # Check quota for analysis
            quota_status = quota_manager.check_quota_available(len(st.session_state.stock_watchlist) * 2)

            if quota_status["available"]:
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button("🧠 Analyze All Stocks", type="primary"):
                        with st.spinner("🤖 AI is analyzing your watchlist..."):
                            try:
                                # Analyze each stock
                                for stock in st.session_state.stock_watchlist:
                                    # Validate and get real data for the stock
                                    validation = self.validate_stock_symbol(stock)

                                    if validation['valid']:
                                        stock_data = validation['data']
                                        analysis_result = self.generate_stock_analysis(validation['symbol'], stock_data)

                                        # Store result
                                        st.session_state.stock_analysis_results[validation['symbol']] = {
                                            'analysis': analysis_result,
                                            'data': stock_data,
                                            'timestamp': datetime.now().isoformat()
                                        }
                                    else:
                                        st.error(f"❌ Cannot analyze {stock}: {validation.get('error', 'Invalid stock')}")
                                        # Show suggestions for invalid stocks
                                        if 'suggestions' in validation and validation['suggestions']:
                                            st.write(f"💡 Suggestions for '{stock}':")
                                            for suggestion in validation['suggestions'][:3]:
                                                st.write(f"   - {suggestion['symbol']}: {suggestion['name']}")

                                st.success(f"✅ AI analysis completed for {len(st.session_state.stock_watchlist)} stocks!")
                                st.rerun()

                            except Exception as e:
                                st.error(f"❌ Error during analysis: {str(e)}")

                with col2:
                    st.caption(f"🔄 Quota: {quota_status['daily_used']}/{quota_status['daily_limit']} daily")
            else:
                st.error(f"❌ **Quota Limit Reached**\n\n"
                        f"Daily: {quota_status['daily_used']}/{quota_status['daily_limit']}\n\n"
                        f"Please wait before running more analysis.")

            # Display analysis results
            if st.session_state.stock_analysis_results:
                st.markdown("---")
                st.subheader("📊 Analysis Results")

                # Create tabs for each stock
                stock_tabs = st.tabs(st.session_state.stock_watchlist)

                for i, stock in enumerate(st.session_state.stock_watchlist):
                    with stock_tabs[i]:
                        if stock in st.session_state.stock_analysis_results:
                            result = st.session_state.stock_analysis_results[stock]
                            data = result['data']

                            # Stock overview
                            col1, col2, col3, col4 = st.columns(4)

                            with col1:
                                st.metric("Current Price", f"₹{data['current_price']:,}")

                            with col2:
                                price_change = data['price_change']
                                st.metric("Price Change", f"₹{price_change:+,}",
                                         delta=f"{data['price_change_percent']:+.2f}%")

                            with col3:
                                st.metric("RSI", f"{data['rsi']:.1f}")

                            with col4:
                                st.metric("Volume", f"{data['volume']:,}")

                            # Data source indicator
                            data_source = data.get('data_source', 'Unknown')
                            last_updated = data.get('last_updated', 'Unknown')

                            if data_source.startswith('Real'):
                                st.success(f"✅ {data_source} - {last_updated}")
                            else:
                                st.warning(f"⚠️ {data_source} - {last_updated}")

                            # Technical indicators
                            col1, col2 = st.columns(2)

                            with col1:
                                # Price chart simulation
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(
                                    x=['9:15', '10:00', '11:00', '12:00', '13:00', '14:00', '15:30'],
                                    y=[data['current_price']-50, data['current_price']-20, data['current_price']-10,
                                       data['current_price'], data['current_price']+15, data['current_price']+25, data['current_price']],
                                    mode='lines+markers',
                                    name=f'{stock} Price',
                                    line=dict(color='#667eea', width=3)
                                ))
                                fig.update_layout(
                                    title=f"{stock} Intraday Price Movement",
                                    xaxis_title="Time",
                                    yaxis_title="Price (₹)",
                                    height=300
                                )
                                st.plotly_chart(fig, use_container_width=True)

                            with col2:
                                # Technical indicators gauge
                                fig = go.Figure(go.Indicator(
                                    mode = "gauge+number",
                                    value = data['rsi'],
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    title = {'text': f"{stock} RSI"},
                                    gauge = {
                                        'axis': {'range': [None, 100]},
                                        'bar': {'color': "#667eea"},
                                        'steps': [
                                            {'range': [0, 30], 'color': "#11998e"},
                                            {'range': [30, 70], 'color': "#667eea"},
                                            {'range': [70, 100], 'color': "#f5576c"}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 4},
                                            'thickness': 0.75,
                                            'value': 70
                                        }
                                    }
                                ))
                                fig.update_layout(height=300)
                                st.plotly_chart(fig, use_container_width=True)

                            # AI Analysis
                            st.subheader("🤖 AI Analysis")

                            # Analysis card
                            st.markdown(f"""
                            <div class="insight-card">
                                <h4>📊 {stock} Analysis</h4>
                                <p style="line-height: 1.6;">{result['analysis']}</p>
                                <div style="font-size: 0.85rem; opacity: 0.8;">
                                    Analyzed: {datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Investment recommendation
                            recommendation = self.get_investment_recommendation(data)
                            st.markdown(f"""
                            <div class="status-{'good' if recommendation['action'] == 'BUY' else 'warning' if recommendation['action'] == 'HOLD' else 'error'}">
                                <h4>💡 Investment Recommendation: {recommendation['action']}</h4>
                                <p><strong>Confidence:</strong> {recommendation['confidence']}%</p>
                                <p><strong>Reasoning:</strong> {recommendation['reasoning']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.info(f"No analysis available for {stock}. Click 'Analyze All Stocks' to get started.")
        else:
            st.info("📋 Add stocks to your watchlist to start tracking and analyzing them!")

    def generate_real_stock_data(self, stock_symbol: str) -> Dict[str, Any]:
        """Generate real stock data using a free stock API"""
        import requests
        import random

        try:
            # Try to get real data from a free API
            # Using Alpha Vantage API (free tier available)
            # You can get a free API key from: https://www.alphavantage.co/support/#api-key

            # For now, we'll use a simple approach with yfinance (if available)
            # or fall back to mock data with a warning

            # Try yfinance first (more reliable for Indian stocks)
            try:
                import yfinance as yf

                # Add .NS suffix for Indian stocks if not present
                ticker_symbol = stock_symbol
                if not stock_symbol.endswith('.NS') and not stock_symbol.endswith('.BO'):
                    ticker_symbol = f"{stock_symbol}.NS"  # NSE

                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info

                # Get current price and basic info
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                if not current_price:
                    # Try getting from history
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                    else:
                        raise Exception("No price data available")

                # Get previous close for price change calculation
                hist = ticker.history(period="2d")
                if len(hist) >= 2:
                    prev_close = hist['Close'].iloc[-2]
                    price_change = current_price - prev_close
                    price_change_percent = (price_change / prev_close) * 100
                else:
                    price_change = 0
                    price_change_percent = 0

                # Get volume
                volume = info.get('volume', hist['Volume'].iloc[-1] if not hist.empty else 0)

                # Calculate RSI (simplified)
                if len(hist) >= 14:
                    gains = hist['Close'].diff().where(hist['Close'].diff() > 0, 0)
                    losses = -hist['Close'].diff().where(hist['Close'].diff() < 0, 0)
                    avg_gain = gains.rolling(14).mean().iloc[-1]
                    avg_loss = losses.rolling(14).mean().iloc[-1]
                    if avg_loss != 0:
                        rs = avg_gain / avg_loss
                        rsi = 100 - (100 / (1 + rs))
                    else:
                        rsi = 50
                else:
                    rsi = 50

                # Determine MACD signal (simplified)
                if len(hist) >= 26:
                    ema12 = hist['Close'].ewm(span=12).mean().iloc[-1]
                    ema26 = hist['Close'].ewm(span=26).mean().iloc[-1]
                    macd_line = ema12 - ema26
                    if macd_line > 0:
                        macd = 'Bullish'
                    elif macd_line < 0:
                        macd = 'Bearish'
                    else:
                        macd = 'Neutral'
                else:
                    macd = 'Neutral'

                # Moving average status
                if len(hist) >= 50:
                    ma50 = hist['Close'].rolling(50).mean().iloc[-1]
                    if current_price > ma50:
                        ma_status = 'Price above 50-day MA'
                    elif current_price < ma50:
                        ma_status = 'Price below 50-day MA'
                    else:
                        ma_status = 'Price near 50-day MA'
                else:
                    ma_status = 'Insufficient data for MA'

                # Support and resistance (simplified)
                if len(hist) >= 20:
                    recent_low = hist['Low'].tail(20).min()
                    recent_high = hist['High'].tail(20).max()
                    support = recent_low
                    resistance = recent_high
                else:
                    support = current_price * 0.95
                    resistance = current_price * 1.05

                return {
                    'current_price': current_price,
                    'price_change': price_change,
                    'price_change_percent': price_change_percent,
                    'daily_range': (hist['Low'].iloc[-1] if not hist.empty else current_price * 0.98,
                                  hist['High'].iloc[-1] if not hist.empty else current_price * 1.02),
                    'volume': volume,
                    'rsi': rsi,
                    'macd': macd,
                    'moving_average': ma_status,
                    'support': support,
                    'resistance': resistance,
                    'data_source': 'Real (yfinance)',
                    'last_updated': 'Live'
                }

            except ImportError:
                # yfinance not available, try Alpha Vantage API
                api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
                if api_key != 'demo':
                    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={api_key}"
                    response = requests.get(url, timeout=10)
                    data = response.json()

                    if 'Global Quote' in data:
                        quote = data['Global Quote']
                        current_price = float(quote.get('05. price', 0))
                        price_change = float(quote.get('09. change', 0))
                        price_change_percent = float(quote.get('10. change percent', '0%').replace('%', ''))
                        volume = int(quote.get('06. volume', 0))

                        return {
                            'current_price': current_price,
                            'price_change': price_change,
                            'price_change_percent': price_change_percent,
                            'daily_range': (current_price * 0.98, current_price * 1.02),
                            'volume': volume,
                            'rsi': 50,  # Would need additional API call for RSI
                            'macd': 'Neutral',
                            'moving_average': 'Data available',
                            'support': current_price * 0.95,
                            'resistance': current_price * 1.05,
                            'data_source': 'Real (Alpha Vantage)',
                            'last_updated': 'Live'
                        }

                # Fall back to mock data with warning
                st.warning(f"⚠️ Real stock data not available for {stock_symbol}. Using mock data. To get real data, install yfinance: `pip install yfinance`")
                return self.generate_mock_stock_data(stock_symbol)

        except Exception as e:
            st.warning(f"⚠️ Error fetching real data for {stock_symbol}: {str(e)}. Using mock data.")
            return self.generate_mock_stock_data(stock_symbol)

    def generate_mock_stock_data(self, stock_symbol: str) -> Dict[str, Any]:
        """Generate realistic mock data for stock analysis (fallback)"""
        import random

        # Base prices for different stocks
        base_prices = {
            'TCS': 3850, 'INFY': 1450, 'RELIANCE': 2200, 'HDFCBANK': 1650,
            'ICICIBANK': 950, 'ITC': 450, 'HINDUNILVR': 2500, 'AXISBANK': 1100,
            'SBIN': 650, 'BHARTIARTL': 1200, 'KOTAKBANK': 1800, 'ASIANPAINT': 3200,
            'MARUTI': 10500, 'ULTRACEMCO': 8500, 'SUNPHARMA': 1200, 'TATAMOTORS': 800,
            'WIPRO': 450, 'POWERGRID': 250, 'NESTLEIND': 2500, 'TECHM': 1200
        }

        base_price = base_prices.get(stock_symbol, random.randint(500, 3000))

        # Generate realistic variations
        price_change = random.randint(-100, 100)
        price_change_percent = (price_change / base_price) * 100
        current_price = base_price + price_change

        daily_range_low = current_price - random.randint(20, 100)
        daily_range_high = current_price + random.randint(20, 100)

        volume = random.randint(100000, 5000000)
        rsi = random.randint(30, 75)

        macd_options = ['Bullish', 'Bearish', 'Neutral']
        macd = random.choice(macd_options)

        ma_status = random.choice(['Price above 50-day MA', 'Price below 50-day MA', 'Price near 50-day MA'])

        support = current_price - random.randint(50, 200)
        resistance = current_price + random.randint(50, 200)

        return {
            'current_price': current_price,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
            'daily_range': (daily_range_low, daily_range_high),
            'volume': volume,
            'rsi': rsi,
            'macd': macd,
            'moving_average': ma_status,
            'support': support,
            'resistance': resistance,
            'data_source': 'Mock Data',
            'last_updated': 'Simulated'
        }

    def get_investment_recommendation(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment recommendation based on technical data"""
        rsi = stock_data['rsi']
        macd = stock_data['macd']
        price_change = stock_data['price_change']

        # Simple rule-based recommendation
        if rsi < 30 and macd == 'Bullish' and price_change > 0:
            return {
                'action': 'BUY',
                'confidence': 85,
                'reasoning': 'Oversold conditions with bullish momentum and positive price action'
            }
        elif rsi > 70 and macd == 'Bearish' and price_change < 0:
            return {
                'action': 'SELL',
                'confidence': 80,
                'reasoning': 'Overbought conditions with bearish momentum and negative price action'
            }
        elif 40 <= rsi <= 60 and abs(price_change) < 20:
            return {
                'action': 'HOLD',
                'confidence': 70,
                'reasoning': 'Neutral RSI with minimal price movement, wait for clearer signals'
            }
        elif rsi < 40 and price_change > 0:
            return {
                'action': 'BUY',
                'confidence': 75,
                'reasoning': 'Low RSI with positive price momentum, potential reversal'
            }
        else:
            return {
                'action': 'HOLD',
                'confidence': 60,
                'reasoning': 'Mixed signals, monitor for clearer trend direction'
            }

    def generate_stock_analysis(self, stock_symbol: str, stock_data: Dict[str, Any]) -> str:
        """Generate a detailed analysis for a given stock using a rule-based approach."""
        analysis_text = f"**Analysis for {stock_symbol}**\n\n"

        # Price Movement
        price_change = stock_data['price_change']
        price_change_percent = stock_data['price_change_percent']
        current_price = stock_data['current_price']

        analysis_text += f"**Price Movement:**\n"
        if price_change > 0:
            analysis_text += f"The stock {stock_symbol} has shown a positive price movement of ₹{price_change:,} ({(price_change_percent):.2f}%) from yesterday's close. This indicates a bullish trend.\n"
        elif price_change < 0:
            analysis_text += f"The stock {stock_symbol} has shown a negative price movement of ₹{abs(price_change):,} ({(price_change_percent):.2f}%) from yesterday's close. This indicates a bearish trend.\n"
        else:
            analysis_text += f"The stock {stock_symbol} has shown minimal price movement. The current price is ₹{current_price:,} ({(price_change_percent):.2f}%) from yesterday's close.\n"

        # RSI (Relative Strength Index)
        rsi = stock_data['rsi']
        analysis_text += f"**RSI (Relative Strength Index):**\n"
        if rsi < 30:
            analysis_text += f"The stock {stock_symbol} is currently oversold (RSI: {rsi}). This often indicates a potential buying opportunity, as the stock is likely to rebound.\n"
        elif rsi > 70:
            analysis_text += f"The stock {stock_symbol} is currently overbought (RSI: {rsi}). This suggests a potential selling opportunity, as the stock might be due for a correction.\n"
        else:
            analysis_text += f"The stock {stock_symbol} is currently neutral (RSI: {rsi}). The current price movement might be driven by other factors.\n"

        # MACD (Moving Average Convergence Divergence)
        macd = stock_data['macd']
        analysis_text += f"**MACD (Moving Average Convergence Divergence):**\n"
        if macd == 'Bullish':
            analysis_text += f"The MACD line is above the signal line, indicating a bullish momentum. This is a positive indicator for the stock {stock_symbol}.\n"
        elif macd == 'Bearish':
            analysis_text += f"The MACD line is below the signal line, indicating a bearish momentum. This is a negative indicator for the stock {stock_symbol}.\n"
        else:
            analysis_text += f"The MACD line is crossing or near the signal line, indicating a neutral momentum for the stock {stock_symbol}.\n"

        # Moving Average
        moving_average = stock_data['moving_average']
        analysis_text += f"**Moving Average:**\n"
        if "above" in moving_average.lower():
            analysis_text += f"The stock {stock_symbol} is currently trading above its 50-day moving average. This is a bullish signal.\n"
        elif "below" in moving_average.lower():
            analysis_text += f"The stock {stock_symbol} is currently trading below its 50-day moving average. This is a bearish signal.\n"
        else:
            analysis_text += f"The stock {stock_symbol} is currently trading near its 50-day moving average. This indicates a balanced position.\n"

        # Support and Resistance
        support = stock_data['support']
        resistance = stock_data['resistance']
        analysis_text += f"**Support and Resistance:**\n"
        analysis_text += f"Current price: ₹{current_price:,} (RSI: {rsi})\n"
        analysis_text += f"Support: ₹{support:,} (Potential buying area)\n"
        analysis_text += f"Resistance: ₹{resistance:,} (Potential selling area)\n"

        # Volume
        volume = stock_data['volume']
        analysis_text += f"**Volume:**\n"
        analysis_text += f"The volume for {stock_symbol} is {volume:,} shares. A higher volume indicates increased interest and potential momentum.\n"

        # Overall Recommendation
        recommendation = self.get_investment_recommendation(stock_data)
        analysis_text += f"\n**Overall Recommendation:**\n"
        analysis_text += f"Action: {recommendation['action']}\n"
        analysis_text += f"Confidence: {recommendation['confidence']}%\n"
        analysis_text += f"Reasoning: {recommendation['reasoning']}\n"

        return analysis_text

    def render_credit_analysis(self):
        """Render credit and debt analysis"""
        st.header("💳 Credit & Debt Analysis")

        # Get credit data
        db = SessionLocal()
        try:
            latest_credit = db.query(MCPData).filter(
                MCPData.data_type == "credit_report"
            ).order_by(MCPData.timestamp.desc()).first()

            if not latest_credit:
                st.info("No credit data available. Please collect data first.")
                return

            credit_data = self.extract_financial_data(latest_credit)

            if 'creditReports' in credit_data and len(credit_data['creditReports']) > 0:
                credit_report = credit_data['creditReports'][0]['creditReportData']

                # Credit score analysis
                if 'score' in credit_report:
                    credit_score = int(credit_report['score']['bureauScore'])

                    col1, col2 = st.columns(2)

                    with col1:
                        # Credit score gauge
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = credit_score,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Credit Score"},
                            gauge = {
                                'axis': {'range': [None, 900]},
                                'bar': {'color': "#667eea"},
                                'steps': [
                                    {'range': [0, 600], 'color': "#fecfef"},
                                    {'range': [600, 700], 'color': "#f093fb"},
                                    {'range': [700, 750], 'color': "#667eea"},
                                    {'range': [750, 900], 'color': "#11998e"}
                                ]
                            }
                        ))
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        # Credit improvement tips
                        if credit_score >= 750:
                            st.markdown("""
                            <div class="status-good">
                                <h4>🌟 Excellent Credit Score!</h4>
                                <p>Your credit score is in the excellent range. Keep up the good work!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        elif credit_score >= 700:
                            st.markdown("""
                            <div class="status-warning">
                                <h4>👍 Good Credit Score</h4>
                                <p>You're doing well! Consider these tips to reach excellent:</p>
                                <ul><li>Pay all bills on time</li><li>Keep credit utilization below 30%</li></ul>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="status-error">
                                <h4>⚠️ Credit Needs Improvement</h4>
                                <p>Focus on these areas:</p>
                                <ul><li>Pay down existing debt</li><li>Never miss payment deadlines</li><li>Consider a secured credit card</li></ul>
                            </div>
                            """, unsafe_allow_html=True)

                # Account summary
                if 'creditAccount' in credit_report and 'creditAccountSummary' in credit_report['creditAccount']:
                    summary = credit_report['creditAccount']['creditAccountSummary']

                    st.subheader("📋 Credit Accounts Summary")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Accounts", summary['account']['creditAccountTotal'])
                    with col2:
                        st.metric("Active Accounts", summary['account']['creditAccountActive'])
                    with col3:
                        st.metric("Closed Accounts", summary['account']['creditAccountClosed'])
                    with col4:
                        st.metric("Default Accounts", summary['account']['creditAccountDefault'])

                    # Outstanding balance
                    if 'totalOutstandingBalance' in summary:
                        balance = summary['totalOutstandingBalance']

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Secured Debt", f"₹{int(balance['outstandingBalanceSecured']):,}")
                        with col2:
                            st.metric("Unsecured Debt", f"₹{int(balance['outstandingBalanceUnSecured']):,}")

        finally:
            db.close()

    def render_mcp_ai_agent(self):
        """Render MCP AI Agent control panel"""
        st.header("🤖 MCP Periodic AI Agent")

        # Get agent status
        agent_status = mcp_periodic_ai_agent.get_agent_status()

        # Agent status overview
        col1, col2, col3 = st.columns(3)

        with col1:
            if agent_status["running"]:
                st.markdown("""
                <div class="status-good">
                    <h4>✅ Agent Active</h4>
                    <p>Periodic collection is running</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-warning">
                    <h4>⏸️ Agent Inactive</h4>
                    <p>Periodic collection is stopped</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            if agent_status["mcp_connection"]:
                st.markdown("""
                <div class="status-good">
                    <h4>🔗 MCP Connected</h4>
                    <p>Fi MCP server is accessible</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-error">
                    <h4>❌ MCP Disconnected</h4>
                    <p>Cannot reach Fi MCP server</p>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            quota_status = quota_manager.check_quota_available(3)
            if quota_status["available"]:
                st.markdown("""
                <div class="status-good">
                    <h4>✅ Quota Available</h4>
                    <p>AI analysis can run</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-error">
                    <h4>⚠️ Quota Exceeded</h4>
                    <p>Wait before running analysis</p>
                </div>
                """, unsafe_allow_html=True)

        # Agent statistics
        st.subheader("📊 Agent Statistics")
        stats = agent_status["stats"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Collections", stats["total_collections"])
        with col2:
            st.metric("Successful Collections", stats["successful_collections"])
        with col3:
            st.metric("Analysis Count", stats["analysis_count"])
        with col4:
            data_types = len(stats["data_types_collected"]) if isinstance(stats["data_types_collected"], set) else 0
            st.metric("Data Types Collected", data_types)

        # Last activity timestamps
        if stats["last_collection_time"]:
            st.info(f"🕒 Last Collection: {stats['last_collection_time']}")
        if stats["last_analysis_time"]:
            st.info(f"🧠 Last Analysis: {stats['last_analysis_time']}")

        # Control panel
        st.subheader("🎛️ Agent Controls")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if not agent_status["running"]:
                if st.button("▶️ Start Periodic Collection", type="primary", key="mcp_start_collection"):
                    with st.spinner("Starting periodic collection..."):
                        try:
                            mcp_periodic_ai_agent.start_periodic_collection()
                            st.success("✅ Periodic collection started!")
                        except Exception as e:
                            st.error(f"❌ Error starting collection: {e}")
                    st.rerun()
            else:
                if st.button("⏹️ Stop Periodic Collection", type="secondary", key="mcp_stop_collection"):
                    with st.spinner("Stopping periodic collection..."):
                        try:
                            mcp_periodic_ai_agent.stop_periodic_collection()
                            st.success("✅ Periodic collection stopped!")
                        except Exception as e:
                            st.error(f"❌ Error stopping collection: {e}")
                    st.rerun()

        with col2:
            if st.button("📥 Collect Data Now", type="primary", key="mcp_collect_data"):
                with st.spinner("Collecting data from Fi MCP..."):
                    try:
                        result = mcp_periodic_ai_agent.collect_mcp_data()
                        if result["success"]:
                            st.success(f"✅ Collected {result['records_stored']} records!")
                            st.json(result)
                        else:
                            st.error(f"❌ Collection failed: {result['error']}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                st.rerun()

        with col3:
            # Check quota for AI analysis
            quota_check = quota_manager.check_quota_available(5)

            if quota_check["available"]:
                if st.button("🧠 Run AI Analysis", type="primary", key="mcp_run_analysis"):
                    with st.spinner("Running comprehensive AI analysis..."):
                        try:
                            result = mcp_periodic_ai_agent.generate_ai_analysis(force=True)
                            if result["success"]:
                                st.success(f"✅ Generated {result['insights_generated']} insights!")

                                # Display insights summary
                                with st.expander("📊 Generated Insights"):
                                    for insight in result["insights"]:
                                        st.markdown(f"**{insight['title']}** ({insight['type']})")
                                        st.write(insight['content'][:200] + "..." if len(insight['content']) > 200 else insight['content'])
                                        st.markdown("---")
                            else:
                                st.error(f"❌ Analysis failed: {result['error']}")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                    st.rerun()
            else:
                st.button("⚠️ AI Quota Exceeded", disabled=True, type="secondary", key="mcp_quota_exceeded")
                st.caption(f"Daily: {quota_check['daily_used']}/{quota_check['daily_limit']}")

        with col4:
            if st.button("🔄 Refresh Status", type="secondary", key="mcp_refresh_status"):
                st.rerun()

        # Configuration section
        with st.expander("⚙️ Agent Configuration"):
            config = agent_status["config"]
            st.json(config)

        # Recent activity logs
        st.subheader("📝 Recent Activity")

        # Show recent MCP data
        db = SessionLocal()
        try:
            recent_data = db.query(MCPData).order_by(MCPData.timestamp.desc()).limit(10).all()

            if recent_data:
                data_list = []
                for record in recent_data:
                    data_list.append({
                        "Timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "Data Type": record.data_type,
                        "Phone": getattr(record, 'phone_number', 'N/A'),
                        "Session": getattr(record, 'session_id', 'N/A')[:20] + "..." if getattr(record, 'session_id', 'N/A') and len(getattr(record, 'session_id', 'N/A')) > 20 else getattr(record, 'session_id', 'N/A')
                    })

                df = pd.DataFrame(data_list)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No recent data collection activity")

        finally:
            db.close()

        # Show recent AI insights
        recent_insights = insight_generator.get_recent_insights(limit=5)
        if recent_insights:
            st.subheader("🧠 Recent AI Insights")
            for insight in recent_insights:
                with st.expander(f"{insight.insight_type.replace('_', ' ').title()}: {insight.title}"):
                    st.write(insight.content)
                    st.caption(f"Confidence: {insight.confidence_score:.1%} • Created: {insight.created_at.strftime('%Y-%m-%d %H:%M')}")

    def render_system_status(self):
        """Render system status"""
        st.header("⚙️ System Status")

        # Connection status
        col1, col2 = st.columns(2)

        with col1:
            if self.mcp_enabled and real_data_collector.test_mcp_connection():
                st.markdown("""
                <div class="status-good">
                    <h4>✅ Fi MCP Server Connected</h4>
                    <p>Real financial data collection is active</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-warning">
                    <h4>📊 Mock Data Mode</h4>
                    <p>Using sample data for demonstration</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            # Quick stats
            db = SessionLocal()
            try:
                total_records = db.query(MCPData).count()
                recent_insights = db.query(AIInsight).count()

                st.metric("Total Records", total_records)
                st.metric("AI Insights", recent_insights)
            finally:
                db.close()

        # Control buttons
        st.subheader("🎛️ Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Collect Data Now", type="primary", key="system_collect_data"):
                with st.spinner("Collecting real financial data..."):
                    real_data_collector.collect_data()
                st.success("Data collection completed!")
                st.rerun()

        with col2:
            # Check quota for insights generation
            quota_check = quota_manager.check_quota_available(3)

            if quota_check["available"]:
                if st.button("🧠 Generate Insights", type="primary", key="system_generate_insights"):
                    with st.spinner("Generating AI insights..."):
                        try:
                            insight_generator.generate_insights(force=True)
                            st.success("✅ Insights generated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    st.rerun()
            else:
                st.button("⚠️ Insights Quota Exceeded", disabled=True, type="secondary", key="system_quota_exceeded")
                st.caption(f"Daily: {quota_check['daily_used']}/{quota_check['daily_limit']}")

        with col3:
            if st.button("📊 Check Quota", type="secondary", key="system_check_quota"):
                stats = quota_manager.get_usage_stats()
                quota_status = stats["quota_status"]

                if quota_status["available"]:
                    st.success(f"✅ Quota OK: {quota_status['daily_used']}/{quota_status['daily_limit']} daily")
                else:
                    st.error(f"❌ Quota Exceeded: {quota_status['daily_used']}/{quota_status['daily_limit']} daily")

    def get_stock_suggestions(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """Get stock suggestions from multiple APIs based on search query"""
        import requests
        from difflib import get_close_matches

        suggestions = []

        # Common Indian stocks for fallback
        indian_stocks = {
            'TCS': 'Tata Consultancy Services Ltd',
            'INFY': 'Infosys Ltd',
            'RELIANCE': 'Reliance Industries Ltd',
            'HDFCBANK': 'HDFC Bank Ltd',
            'ICICIBANK': 'ICICI Bank Ltd',
            'ITC': 'ITC Ltd',
            'HINDUNILVR': 'Hindustan Unilever Ltd',
            'AXISBANK': 'Axis Bank Ltd',
            'SBIN': 'State Bank of India',
            'BHARTIARTL': 'Bharti Airtel Ltd',
            'KOTAKBANK': 'Kotak Mahindra Bank Ltd',
            'ASIANPAINT': 'Asian Paints Ltd',
            'MARUTI': 'Maruti Suzuki India Ltd',
            'ULTRACEMCO': 'UltraTech Cement Ltd',
            'SUNPHARMA': 'Sun Pharmaceutical Industries Ltd',
            'TATAMOTORS': 'Tata Motors Ltd',
            'WIPRO': 'Wipro Ltd',
            'POWERGRID': 'Power Grid Corporation of India Ltd',
            'NESTLEIND': 'Nestle India Ltd',
            'TECHM': 'Tech Mahindra Ltd',
            'HCLTECH': 'HCL Technologies Ltd',
            'BAJFINANCE': 'Bajaj Finance Ltd',
            'TATACONSUM': 'Tata Consumer Products Ltd',
            'BAJAJFINSV': 'Bajaj Finserv Ltd',
            'ADANIENT': 'Adani Enterprises Ltd',
            'JSWSTEEL': 'JSW Steel Ltd',
            'TATASTEEL': 'Tata Steel Ltd',
            'ONGC': 'Oil & Natural Gas Corporation Ltd',
            'COALINDIA': 'Coal India Ltd',
            'NTPC': 'NTPC Ltd',
            'INDUSINDBK': 'IndusInd Bank Ltd',
            'CIPLA': 'Cipla Ltd',
            'DRREDDY': 'Dr Reddy\'s Laboratories Ltd',
            'SHREECEM': 'Shree Cement Ltd',
            'DIVISLAB': 'Divi\'s Laboratories Ltd',
            'EICHERMOT': 'Eicher Motors Ltd',
            'HEROMOTOCO': 'Hero MotoCorp Ltd',
            'BRITANNIA': 'Britannia Industries Ltd',
            'GRASIM': 'Grasim Industries Ltd',
            'ADANIPORTS': 'Adani Ports and Special Economic Zone Ltd',
            'HINDALCO': 'Hindalco Industries Ltd',
            'VEDL': 'Vedanta Ltd',
            'JINDALSTEL': 'Jindal Steel & Power Ltd',
            'TATAPOWER': 'Tata Power Company Ltd',
            'BAJAJ-AUTO': 'Bajaj Auto Ltd',
            'M&M': 'Mahindra & Mahindra Ltd',
            'LT': 'Larsen & Toubro Ltd',
            'HCLTECH': 'HCL Technologies Ltd',
            'SBI': 'State Bank of India',
            'PNB': 'Punjab National Bank',
            'CANBK': 'Canara Bank',
            'UNIONBANK': 'Union Bank of India',
            'BANKBARODA': 'Bank of Baroda',
            'IDBI': 'IDBI Bank Ltd',
            'YESBANK': 'Yes Bank Ltd',
            'FEDERALBNK': 'Federal Bank Ltd',
            'KARURVYSYA': 'Karur Vysya Bank Ltd',
            'SOUTHBANK': 'South Indian Bank Ltd',
            'UCOBANK': 'UCO Bank',
            'INDIANB': 'Indian Bank',
            'CENTRALBK': 'Central Bank of India',
            'BANKINDIA': 'Bank of India',
            'IOB': 'Indian Overseas Bank',
            'ANDHRABANK': 'Andhra Bank',
            'VIJAYABANK': 'Vijaya Bank',
            'DENABANK': 'Dena Bank',
            'ORIENTBANK': 'Orient Bank of Commerce',
            'ALLAHABANK': 'Allahabad Bank',
            'SYNDICATE': 'Syndicate Bank',
            'UNITEDBNK': 'United Bank of India',
            'CORPBANK': 'Corporation Bank',
            'ANDHRABANK': 'Andhra Bank',
            'VIJAYABANK': 'Vijaya Bank',
            'DENABANK': 'Dena Bank',
            'ORIENTBANK': 'Orient Bank of Commerce',
            'ALLAHABANK': 'Allahabad Bank',
            'SYNDICATE': 'Syndicate Bank',
            'UNITEDBNK': 'United Bank of India',
            'CORPBANK': 'Corporation Bank'
        }

        try:
            # Method 1: Try Alpha Vantage API for symbol search
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
            if api_key != 'demo':
                try:
                    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={api_key}"
                    response = requests.get(url, timeout=5)
                    data = response.json()

                    if 'bestMatches' in data:
                        for match in data['bestMatches'][:limit]:
                            symbol = match.get('1. symbol', '')
                            name = match.get('2. name', '')
                            if symbol and name:
                                suggestions.append({
                                    'symbol': symbol,
                                    'name': name,
                                    'exchange': match.get('4. region', ''),
                                    'type': match.get('3. type', '')
                                })
                except Exception as e:
                    self.logger.debug(f"Alpha Vantage API error: {e}")

            # Method 2: Try Yahoo Finance search
            try:
                import yfinance as yf
                # Search for stocks using yfinance
                search_results = yf.Tickers(query)
                if hasattr(search_results, 'tickers'):
                    for ticker in list(search_results.tickers.keys())[:limit]:
                        try:
                            ticker_obj = yf.Ticker(ticker)
                            info = ticker_obj.info
                            name = info.get('longName', info.get('shortName', ticker))
                            suggestions.append({
                                'symbol': ticker,
                                'name': name,
                                'exchange': info.get('exchange', ''),
                                'type': 'Stock'
                            })
                        except:
                            continue
            except Exception as e:
                self.logger.debug(f"Yahoo Finance search error: {e}")

            # Method 3: Use local Indian stocks database with fuzzy matching
            if query.upper() in indian_stocks:
                suggestions.append({
                    'symbol': query.upper(),
                    'name': indian_stocks[query.upper()],
                    'exchange': 'NSE',
                    'type': 'Stock'
                })
            else:
                # Fuzzy matching for Indian stocks
                stock_names = list(indian_stocks.keys())
                matches = get_close_matches(query.upper(), stock_names, n=limit, cutoff=0.6)

                for match in matches:
                    suggestions.append({
                        'symbol': match,
                        'name': indian_stocks[match],
                        'exchange': 'NSE',
                        'type': 'Stock'
                    })

            # Method 4: Try Finnhub API (free tier available)
            finnhub_key = os.getenv('FINNHUB_API_KEY', '')
            if finnhub_key:
                try:
                    url = f"https://finnhub.io/api/v1/search?q={query}&token={finnhub_key}"
                    response = requests.get(url, timeout=5)
                    data = response.json()

                    if 'result' in data:
                        for item in data['result'][:limit]:
                            symbol = item.get('symbol', '')
                            description = item.get('description', '')
                            if symbol and description:
                                suggestions.append({
                                    'symbol': symbol,
                                    'name': description,
                                    'exchange': item.get('primaryExchange', ''),
                                    'type': item.get('type', 'Stock')
                                })
                except Exception as e:
                    self.logger.debug(f"Finnhub API error: {e}")

            # Remove duplicates and limit results
            seen_symbols = set()
            unique_suggestions = []
            for suggestion in suggestions:
                if suggestion['symbol'] not in seen_symbols:
                    seen_symbols.add(suggestion['symbol'])
                    unique_suggestions.append(suggestion)
                    if len(unique_suggestions) >= limit:
                        break

            return unique_suggestions

        except Exception as e:
            self.logger.error(f"Error in stock suggestions: {e}")
            # Fallback to basic Indian stocks
            return [
                {'symbol': 'TCS', 'name': 'Tata Consultancy Services Ltd', 'exchange': 'NSE', 'type': 'Stock'},
                {'symbol': 'INFY', 'name': 'Infosys Ltd', 'exchange': 'NSE', 'type': 'Stock'},
                {'symbol': 'RELIANCE', 'name': 'Reliance Industries Ltd', 'exchange': 'NSE', 'type': 'Stock'},
                {'symbol': 'HDFCBANK', 'name': 'HDFC Bank Ltd', 'exchange': 'NSE', 'type': 'Stock'}
            ]

    def correct_stock_symbol(self, symbol: str) -> str:
        """Try to correct a stock symbol using fuzzy matching"""
        from difflib import get_close_matches

        # Common Indian stocks
        indian_stocks = [
            'TCS', 'INFY', 'RELIANCE', 'HDFCBANK', 'ICICIBANK', 'ITC', 'HINDUNILVR',
            'AXISBANK', 'SBIN', 'BHARTIARTL', 'KOTAKBANK', 'ASIANPAINT', 'MARUTI',
            'ULTRACEMCO', 'SUNPHARMA', 'TATAMOTORS', 'WIPRO', 'POWERGRID', 'NESTLEIND',
            'TECHM', 'HCLTECH', 'BAJFINANCE', 'TATACONSUM', 'BAJAJFINSV', 'ADANIENT',
            'JSWSTEEL', 'TATASTEEL', 'ONGC', 'COALINDIA', 'NTPC', 'INDUSINDBK',
            'CIPLA', 'DRREDDY', 'SHREECEM', 'DIVISLAB', 'EICHERMOT', 'HEROMOTOCO',
            'BRITANNIA', 'GRASIM', 'ADANIPORTS', 'HINDALCO', 'VEDL', 'JINDALSTEL',
            'TATAPOWER', 'BAJAJ-AUTO', 'M&M', 'LT', 'SBI', 'PNB', 'CANBK', 'UNIONBANK',
            'BANKBARODA', 'IDBI', 'YESBANK', 'FEDERALBNK', 'KARURVYSYA', 'SOUTHBANK',
            'UCOBANK', 'INDIANB', 'CENTRALBK', 'BANKINDIA', 'IOB', 'ANDHRABANK',
            'VIJAYABANK', 'DENABANK', 'ORIENTBANK', 'ALLAHABANK', 'SYNDICATE',
            'UNITEDBNK', 'CORPBANK'
        ]

        # Try exact match first
        if symbol.upper() in indian_stocks:
            return symbol.upper()

        # Try fuzzy matching
        matches = get_close_matches(symbol.upper(), indian_stocks, n=1, cutoff=0.7)
        if matches:
            return matches[0]

        # If no match found, return original
        return symbol.upper()

    def validate_stock_symbol(self, symbol: str) -> Dict[str, Any]:
        """Validate if a stock symbol exists and get its real data"""
        try:
            # First try to correct the symbol
            corrected_symbol = self.correct_stock_symbol(symbol)

            # Try to get real data
            real_data = self.generate_real_stock_data(corrected_symbol)

            if real_data.get('data_source', '').startswith('Real'):
                return {
                    'valid': True,
                    'symbol': corrected_symbol,
                    'data': real_data,
                    'was_corrected': corrected_symbol != symbol.upper()
                }
            else:
                # Try with .NS suffix for Indian stocks
                if not corrected_symbol.endswith('.NS'):
                    ns_symbol = f"{corrected_symbol}.NS"
                    ns_data = self.generate_real_stock_data(ns_symbol)
                    if ns_data.get('data_source', '').startswith('Real'):
                        return {
                            'valid': True,
                            'symbol': ns_symbol,
                            'data': ns_data,
                            'was_corrected': True
                        }

                return {
                    'valid': False,
                    'symbol': corrected_symbol,
                    'error': 'Stock not found or no data available',
                    'suggestions': self.get_stock_suggestions(corrected_symbol, limit=5)
                }

        except Exception as e:
            return {
                'valid': False,
                'symbol': symbol,
                'error': str(e),
                'suggestions': self.get_stock_suggestions(symbol, limit=5)
            }

    def render_subscription_tracker(self):
        """Render subscription tracking and management interface"""
        st.header("📱 Subscription Tracker")
        st.markdown("Track your recurring subscriptions and identify potential savings")

        # Initialize session state for subscription data
        if 'subscription_data' not in st.session_state:
            st.session_state.subscription_data = None
        if 'subscription_analysis' not in st.session_state:
            st.session_state.subscription_analysis = None

        # Main controls area
        st.subheader("🔧 Choose Your Data Source")

        # Data source selection
        data_source = st.selectbox(
            "Select how to provide transaction data:",
            ["Select an option...", "Mock Data", "Upload Transactions", "Connect Bank Account"],
            help="Choose how to provide transaction data"
        )

        if data_source == "Upload Transactions":
            uploaded_file = st.file_uploader(
                "Upload transaction CSV/JSON",
                type=['csv', 'json'],
                help="Upload your transaction data file"
            )

            if uploaded_file:
                if st.button("📊 Analyze Subscriptions", type="primary"):
                    with st.spinner("Analyzing your subscriptions..."):
                        try:
                            # Parse uploaded file
                            if uploaded_file.name.endswith('.csv'):
                                import pandas as pd
                                df = pd.read_csv(uploaded_file)
                                transactions = df.to_dict('records')
                            else:
                                transactions = json.load(uploaded_file)

                            # Analyze subscriptions
                            st.session_state.subscription_data = transactions
                            st.session_state.subscription_analysis = self.analyze_subscriptions_mock(transactions)
                            st.success("✅ Subscription analysis complete!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Error analyzing subscriptions: {str(e)}")

        elif data_source == "Mock Data":
            if st.button("📊 Analyze Mock Subscriptions", type="primary"):
                with st.spinner("Analyzing mock subscription data..."):
                    try:
                        mock_transactions = self.generate_mock_transaction_data()
                        st.session_state.subscription_data = mock_transactions
                        st.session_state.subscription_analysis = self.analyze_subscriptions_mock(mock_transactions)
                        st.success("✅ Mock subscription analysis complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error analyzing subscriptions: {str(e)}")

        elif data_source == "Connect Bank Account":
            st.info("🔗 Bank account connection feature coming soon!")
            st.write("This feature will allow you to connect your bank account to automatically analyze your transactions for subscriptions.")

        # Main content area
        if st.session_state.subscription_analysis:
            analysis = st.session_state.subscription_analysis

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Subscriptions",
                    analysis['summary']['total_subscriptions'],
                    help="Number of active subscriptions found"
                )

            with col2:
                st.metric(
                    "Monthly Cost",
                    f"₹{analysis['summary']['total_monthly_cost']:,}",
                    help="Total monthly subscription cost"
                )

            with col3:
                st.metric(
                    "Annual Cost",
                    f"₹{analysis['summary']['total_yearly_cost']:,}",
                    help="Total annual subscription cost"
                )

            with col4:
                potential_savings = sum(rec.get('potential_savings', 0) for rec in analysis['recommendations'])
                st.metric(
                    "Potential Savings",
                    f"₹{potential_savings:,.0f}",
                    help="Potential annual savings from recommendations"
                )

            # Subscription list
            st.subheader("📋 Your Subscriptions")

            if analysis['subscriptions']:
                for i, subscription in enumerate(analysis['subscriptions']):
                    with st.expander(f"🔸 {subscription['name']} - ₹{subscription['amount']}/{subscription['frequency']}"):
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.write(f"**Category:** {subscription['category'].title()}")
                            st.write(f"**Merchant:** {subscription['merchant']}")
                            st.write(f"**Description:** {subscription['description']}")
                            st.write(f"**Annual Cost:** ₹{subscription['annual_cost']:,.2f}")

                        with col2:
                            st.write(f"**Last Charge:** {subscription['last_charge_date'][:10]}")
                            st.write(f"**Next Charge:** {subscription['next_charge_date'][:10]}")

                            # Usage indicator
                            usage_info = analysis['usage_analysis'].get(subscription['name'], {})
                            usage_level = usage_info.get('usage_level', 'unknown')

                            if usage_level == 'high':
                                st.success("🟢 High Usage")
                            elif usage_level == 'medium':
                                st.warning("🟡 Medium Usage")
                            elif usage_level == 'low':
                                st.error("🔴 Low Usage")
                            else:
                                st.info("⚪ Unknown Usage")

                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"❌ Cancel {subscription['name']}", key=f"cancel_{i}"):
                                st.warning(f"Would cancel {subscription['name']} - saves ₹{subscription['annual_cost']:,.2f}/year")

                        with col2:
                            if st.button(f"📊 Usage Details", key=f"usage_{i}"):
                                st.info(f"Usage analysis for {subscription['name']}: {usage_level} usage level")

                        with col3:
                            if st.button(f"💰 Cost Breakdown", key=f"cost_{i}"):
                                st.info(f"Cost breakdown for {subscription['name']}: ₹{subscription['annual_cost']:,.2f}/year")
            else:
                st.info("No subscriptions found in your transaction data.")

            # Recommendations
            if analysis['recommendations']:
                st.subheader("💡 Smart Recommendations")

                for i, rec in enumerate(analysis['recommendations']):
                    priority_color = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }.get(rec['priority'], '⚪')

                    with st.expander(f"{priority_color} {rec['type'].title()}: {rec['reason']}"):
                        st.write(f"**Action:** {rec['type'].title()}")
                        st.write(f"**Reason:** {rec['reason']}")

                        if rec['type'] == 'cancel':
                            st.write(f"**Potential Savings:** ₹{rec['potential_savings']:,.2f}/year")
                            st.write(f"**Subscription:** {rec['subscription']}")

                        elif rec['type'] == 'consolidate':
                            st.write(f"**Potential Savings:** ₹{rec['potential_savings']:,.2f}/year")
                            st.write(f"**Category:** {rec['category'].title()}")
                            st.write(f"**Subscriptions:** {', '.join(rec['subscriptions'])}")

                        elif rec['type'] == 'review_cost':
                            st.write(f"**Current Cost:** ₹{rec['current_cost']:,.2f}/year")
                            st.write(f"**Subscription:** {rec['subscription']}")

                        # Action buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✅ Apply Recommendation", key=f"apply_{i}"):
                                st.success(f"Recommendation applied: {rec['type']}")

                        with col2:
                            if st.button(f"❌ Dismiss", key=f"dismiss_{i}"):
                                st.info("Recommendation dismissed")

            # Cost breakdown chart
            if analysis['cost_analysis']['category_breakdown']:
                st.subheader("📊 Cost Breakdown by Category")

                categories = list(analysis['cost_analysis']['category_breakdown'].keys())
                costs = list(analysis['cost_analysis']['category_breakdown'].values())

                fig = px.pie(
                    names=categories,
                    values=costs,
                    title="Annual Subscription Costs by Category"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Usage analysis
            st.subheader("📈 Usage Analysis")

            usage_data = []
            for sub_name, usage_info in analysis['usage_analysis'].items():
                usage_data.append({
                    'Subscription': sub_name,
                    'Usage Level': usage_info['usage_level'].title(),
                    'Transaction Count': usage_info['transaction_count']
                })

            if usage_data:
                import pandas as pd
                usage_df = pd.DataFrame(usage_data)
                st.dataframe(usage_df, use_container_width=True)

        elif data_source != "Select an option...":
            # Show instructions when no analysis is available
            st.info("👆 Select a data source above to analyze your subscriptions")

            # Show sample data structure
            with st.expander("📋 Sample Transaction Data Format"):
                st.code("""
{
    "date": "2024-01-15",
    "amount": 999.00,
    "merchant": "netflix",
    "description": "Netflix subscription payment",
    "category": "entertainment"
}
                """, language="json")

    def generate_mock_transaction_data(self) -> List[Dict[str, Any]]:
        """Generate mock transaction data for subscription analysis"""
        from datetime import datetime, timedelta
        import random

        # Mock subscription transactions
        subscriptions = [
            {"name": "Netflix", "amount": 499, "frequency": "monthly", "merchant": "netflix"},
            {"name": "Amazon Prime", "amount": 1499, "frequency": "yearly", "merchant": "amazon prime"},
            {"name": "Spotify Premium", "amount": 119, "frequency": "monthly", "merchant": "spotify"},
            {"name": "Adobe Creative Cloud", "amount": 1999, "frequency": "monthly", "merchant": "adobe"},
            {"name": "Cult Fit", "amount": 999, "frequency": "monthly", "merchant": "cult fit"},
            {"name": "Swiggy One", "amount": 299, "frequency": "monthly", "merchant": "swiggy"},
            {"name": "Notion Pro", "amount": 799, "frequency": "monthly", "merchant": "notion"},
            {"name": "Canva Pro", "amount": 399, "frequency": "monthly", "merchant": "canva"},
            {"name": "Zoom Pro", "amount": 1499, "frequency": "monthly", "merchant": "zoom"},
            {"name": "Dropbox Plus", "amount": 999, "frequency": "monthly", "merchant": "dropbox"}
        ]

        transactions = []
        base_date = datetime.now() - timedelta(days=90)

        for sub in subscriptions:
            # Generate multiple transactions for each subscription
            if sub['frequency'] == 'monthly':
                for i in range(3):  # Last 3 months
                    transaction_date = base_date + timedelta(days=i*30)
                    transactions.append({
                        'date': transaction_date,
                        'amount': sub['amount'],
                        'merchant': sub['merchant'],
                        'description': f"{sub['name']} subscription payment",
                        'category': 'subscription'
                    })
            elif sub['frequency'] == 'yearly':
                # Yearly subscription - one transaction
                transactions.append({
                    'date': base_date,
                    'amount': sub['amount'],
                    'merchant': sub['merchant'],
                    'description': f"{sub['name']} yearly subscription",
                    'category': 'subscription'
                })

        # Add some regular transactions (non-subscriptions)
        regular_transactions = [
            {"amount": 2500, "merchant": "grocery store", "description": "Weekly groceries"},
            {"amount": 1500, "merchant": "restaurant", "description": "Dinner"},
            {"amount": 500, "merchant": "gas station", "description": "Fuel"},
            {"amount": 2000, "merchant": "online store", "description": "Shopping"},
        ]

        for i, txn in enumerate(regular_transactions):
            transactions.append({
                'date': base_date + timedelta(days=i*7),
                'amount': txn['amount'],
                'merchant': txn['merchant'],
                'description': txn['description'],
                'category': 'regular'
            })

        return transactions

    def analyze_subscriptions_mock(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock subscription analysis (simplified version)"""
        # This is a simplified version - in production, you'd use the actual agent

        # Identify subscriptions from transactions
        subscriptions = []
        for txn in transactions:
            if txn.get('category') == 'subscription' or any(keyword in txn.get('merchant', '').lower() for keyword in ['netflix', 'amazon', 'spotify', 'adobe', 'cult', 'swiggy', 'notion', 'canva', 'zoom', 'dropbox']):
                # Determine category
                merchant = txn.get('merchant', '').lower()
                if any(streaming in merchant for streaming in ['netflix', 'spotify']):
                    category = 'streaming'
                elif 'amazon' in merchant:
                    category = 'shopping'
                elif any(software in merchant for software in ['adobe', 'notion', 'canva', 'zoom', 'dropbox']):
                    category = 'software'
                elif 'cult' in merchant:
                    category = 'fitness'
                elif 'swiggy' in merchant:
                    category = 'food_delivery'
                else:
                    category = 'other'

                # Calculate frequency (simplified)
                frequency = 'monthly' if txn.get('amount', 0) < 1000 else 'yearly'

                # Calculate annual cost
                annual_cost = txn.get('amount', 0) * (12 if frequency == 'monthly' else 1)

                subscriptions.append({
                    'name': txn.get('merchant', '').title(),
                    'category': category,
                    'amount': txn.get('amount', 0),
                    'frequency': frequency,
                    'merchant': txn.get('merchant', ''),
                    'last_charge_date': txn.get('date', datetime.now()).isoformat(),
                    'next_charge_date': (txn.get('date', datetime.now()) + timedelta(days=30)).isoformat(),
                    'description': txn.get('description', ''),
                    'annual_cost': annual_cost
                })

        # Remove duplicates
        unique_subs = {}
        for sub in subscriptions:
            if sub['merchant'] not in unique_subs:
                unique_subs[sub['merchant']] = sub

        subscriptions = list(unique_subs.values())

        # Generate usage analysis
        usage_analysis = {}
        for sub in subscriptions:
            usage_analysis[sub['name']] = {
                'usage_level': random.choice(['high', 'medium', 'low']),
                'transaction_count': random.randint(1, 5),
                'last_used': sub['last_charge_date']
            }

        # Calculate costs
        total_monthly = sum(sub['annual_cost'] / 12 for sub in subscriptions)
        total_yearly = sum(sub['annual_cost'] for sub in subscriptions)

        category_costs = {}
        for sub in subscriptions:
            cat = sub['category']
            if cat not in category_costs:
                category_costs[cat] = 0
            category_costs[cat] += sub['annual_cost']

        # Generate recommendations
        recommendations = []
        for sub in subscriptions:
            usage_level = usage_analysis[sub['name']]['usage_level']
            if usage_level == 'low':
                recommendations.append({
                    'type': 'cancel',
                    'subscription': sub['name'],
                    'reason': 'Low usage detected',
                    'potential_savings': sub['annual_cost'],
                    'priority': 'high'
                })

        return {
            'subscriptions': subscriptions,
            'usage_analysis': usage_analysis,
            'cost_analysis': {
                'total_monthly': round(total_monthly, 2),
                'total_yearly': round(total_yearly, 2),
                'category_breakdown': {k: round(v, 2) for k, v in category_costs.items()},
                'subscription_count': len(subscriptions)
            },
            'recommendations': recommendations,
            'summary': {
                'total_subscriptions': len(subscriptions),
                'total_monthly_cost': round(total_monthly, 2),
                'total_yearly_cost': round(total_yearly, 2),
                'categories': list(set(sub['category'] for sub in subscriptions)),
                'most_expensive_category': max(category_costs.items(), key=lambda x: x[1])[0] if category_costs else None,
                'analysis_date': datetime.now().isoformat()
            }
        }

def main():
    """Main entry point"""
    dashboard = ModernFinancialDashboard()
    dashboard.main()

if __name__ == "__main__":
    main()