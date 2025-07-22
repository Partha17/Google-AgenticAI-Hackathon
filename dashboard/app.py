import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sys
import os
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import SessionLocal, AIInsight, MCPData, create_tables
from services.insight_generator import insight_generator
from services.real_data_collector import real_data_collector
from services.quota_manager import quota_manager

# Page configuration
st.set_page_config(
    page_title="💰 Fi Financial AI Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric > div > div > div > div {
        font-size: 1.2rem;
    }
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
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
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
    }
    .status-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .status-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .status-error {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #333;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ModernFinancialDashboard:
    def __init__(self):
        create_tables()
    
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
        """Get properly parsed financial summary from real MCP data"""
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
                if 'accountDetailsBulkResponse' in nw_data:
                    bank_balance = 0
                    account_map = nw_data['accountDetailsBulkResponse']['accountDetailsMap']
                    for account_id, account_info in account_map.items():
                        if 'depositSummary' in account_info:
                            balance = int(account_info['depositSummary']['currentBalance']['units'])
                            bank_balance += balance
                    summary["bank_balance"] = bank_balance
                
                summary["last_updated"] = latest_nw.timestamp.strftime("%Y-%m-%d %H:%M")
            
            # Get credit score
            latest_credit = db.query(MCPData).filter(
                MCPData.data_type == "credit_report"
            ).order_by(MCPData.timestamp.desc()).first()
            
            if latest_credit:
                credit_data = self.extract_financial_data(latest_credit)
                if 'creditReports' in credit_data and len(credit_data['creditReports']) > 0:
                    credit_report = credit_data['creditReports'][0]
                    if 'creditReportData' in credit_report and 'score' in credit_report['creditReportData']:
                        summary["credit_score"] = int(credit_report['creditReportData']['score']['bureauScore'])
            
            # Get EPF balance
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
        
        except Exception as e:
            st.error(f"Error getting financial summary: {e}")
        finally:
            db.close()
        
        return summary

    def main(self):
        """Main dashboard interface"""
        # Header with modern design
        st.markdown('<div class="financial-summary">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("💰 Fi Financial AI Dashboard")
            st.markdown("**Real-time financial analysis powered by AI agents and Fi MCP data**")
        with col2:
            if st.button("🔄 Refresh Data", type="primary"):
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Financial Overview with real data
        self.render_financial_overview()
        
        # Main content tabs with modern styling
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧠 AI Insights", 
            "📈 Portfolio Analysis", 
            "💳 Credit & Debt",
            "⚙️ System Status"
        ])
        
        with tab1:
            self.render_modern_insights()
        
        with tab2:
            self.render_portfolio_analysis()
        
        with tab3:
            self.render_credit_analysis()
        
        with tab4:
            self.render_system_status()

    def render_financial_overview(self):
        """Render modern financial overview"""
        summary = self.get_parsed_financial_summary()
        
        # Key metrics in cards
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
                if st.button("✨ Generate New Insights", type="primary"):
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
                st.button("⚠️ Quota Exceeded", disabled=True, type="secondary")
                st.error(f"❌ **Quota Limit Reached**\n\n"
                        f"Daily: {quota_status['daily_used']}/{quota_status['daily_limit']}\n\n"
                        f"Hourly: {quota_status['hourly_used']}/{quota_status['hourly_limit']}\n\n"
                        f"Please wait before generating more insights.")
        
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

    def render_system_status(self):
        """Render system status"""
        st.header("⚙️ System Status")
        
        # Connection status
        col1, col2 = st.columns(2)
        
        with col1:
            if real_data_collector.test_mcp_connection():
                st.markdown("""
                <div class="status-good">
                    <h4>✅ Fi MCP Server Connected</h4>
                    <p>Real financial data collection is active</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-error">
                    <h4>❌ Fi MCP Server Disconnected</h4>
                    <p>Cannot collect real financial data</p>
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
            if st.button("📥 Collect Data Now", type="primary"):
                with st.spinner("Collecting real financial data..."):
                    real_data_collector.collect_data()
                st.success("Data collection completed!")
                st.rerun()
        
        with col2:
            # Check quota for insights generation
            quota_check = quota_manager.check_quota_available(3)
            
            if quota_check["available"]:
                if st.button("🧠 Generate Insights", type="primary"):
                    with st.spinner("Generating AI insights..."):
                        try:
                            insight_generator.generate_insights(force=True)
                            st.success("✅ Insights generated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    st.rerun()
            else:
                st.button("⚠️ Insights Quota Exceeded", disabled=True, type="secondary")
                st.caption(f"Daily: {quota_check['daily_used']}/{quota_check['daily_limit']}")
        
        with col3:
            if st.button("📊 Check Quota", type="secondary"):
                from services.quota_manager import quota_manager
                stats = quota_manager.get_usage_stats()
                quota_status = stats["quota_status"]
                
                if quota_status["available"]:
                    st.success(f"✅ Quota OK: {quota_status['daily_used']}/{quota_status['daily_limit']} daily")
                else:
                    st.error(f"❌ Quota Exceeded: {quota_status['daily_used']}/{quota_status['daily_limit']} daily")

def main():
    """Main entry point"""
    dashboard = ModernFinancialDashboard()
    dashboard.main()

if __name__ == "__main__":
    main() 