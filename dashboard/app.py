import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import SessionLocal, AIInsight, MCPData, create_tables
from services.insight_generator import insight_generator
from services.real_data_collector import real_data_collector

# Page configuration
st.set_page_config(
    page_title="Fi MCP Financial Insights Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FinancialDashboard:
    def __init__(self):
        create_tables()  # Ensure tables exist
    
    def main(self):
        """Main dashboard interface"""
        st.title("💰 Fi MCP Financial Insights Dashboard")
        st.markdown("Real-time financial analysis powered by AI agents and Fi MCP data")
        
        # Sidebar
        self.render_sidebar()
        
        # Main content with data-specific tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📈 Overview", 
            "💰 Net Worth", 
            "🏦 Bank Transactions", 
            "🏛️ EPF Details", 
            "📊 Credit Report",
            "🧠 AI Insights", 
            "⚙️ System Status"
        ])
        
        with tab1:
            self.render_overview()
        
        with tab2:
            self.render_net_worth_panel()
        
        with tab3:
            self.render_bank_transactions_panel()
        
        with tab4:
            self.render_epf_panel()
        
        with tab5:
            self.render_credit_report_panel()
        
        with tab6:
            self.render_insights()
        
        with tab7:
            self.render_system_status()
    
    def render_sidebar(self):
        """Render sidebar controls"""
        st.sidebar.header("🎛️ Controls")
        
        # Fi MCP Connection Status
        st.sidebar.subheader("🔗 Fi MCP Status")
        if real_data_collector.test_mcp_connection():
            st.sidebar.success("✅ Fi MCP Connected")
        else:
            st.sidebar.error("❌ Fi MCP Disconnected")
            st.sidebar.info("Start Fi MCP server: `cd fi-mcp-server && FI_MCP_PORT=8080 go run . &`")
        
        # System controls
        st.sidebar.subheader("System Control")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🚀 Collect Data"):
                with st.spinner("Collecting real financial data..."):
                    real_data_collector.collect_data()
                st.success("Data collection completed!")
        
        with col2:
            if st.button("🧠 Generate Insights"):
                with st.spinner("Generating AI insights..."):
                    insight_generator.generate_insights()
                st.success("AI analysis completed!")
        
        # Filters
        st.sidebar.subheader("📊 Filters")
        
        insight_types = ["All", "trend_analysis", "risk_assessment", "opportunity", "market_sentiment"]
        selected_type = st.sidebar.selectbox("Insight Type", insight_types)
        
        days_back = st.sidebar.slider("Days to show", 1, 30, 7)
        
        # Financial summary
        st.sidebar.subheader("💰 Quick Summary")
        summary = real_data_collector.get_latest_financial_summary()
        
        for key, value in summary.items():
            if value != "N/A":
                formatted_key = key.replace("_", " ").title()
                if isinstance(value, (int, float)) and ("balance" in key or "worth" in key or "assets" in key):
                    st.sidebar.metric(formatted_key, f"₹{value:,}")
                else:
                    st.sidebar.metric(formatted_key, str(value))
        
        return selected_type, days_back
    
    def render_overview(self):
        """Render financial overview section"""
        st.header("📈 Financial Overview")
        
        # Get financial summary
        summary = real_data_collector.get_latest_financial_summary()
        stats = real_data_collector.get_collection_stats()
        
        # Key financial metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            net_worth = summary.get('net_worth', 'N/A')
            if isinstance(net_worth, (int, float)):
                st.metric("Net Worth", f"₹{net_worth:,}")
            else:
                st.metric("Net Worth", net_worth)
        
        with col2:
            credit_score = summary.get('credit_score', 'N/A')
            if isinstance(credit_score, (int, float)) and credit_score > 0:
                color = "normal"
                if credit_score >= 750:
                    color = "inverse"
                elif credit_score < 600:
                    color = "off"
                st.metric("Credit Score", credit_score)
            else:
                st.metric("Credit Score", "N/A")
        
        with col3:
            epf_balance = summary.get('epf_balance', 'N/A')
            if isinstance(epf_balance, (int, float)):
                st.metric("EPF Balance", f"₹{epf_balance:,}")
            else:
                st.metric("EPF Balance", epf_balance)
        
        with col4:
            st.metric("Data Success Rate", f"{stats.get('success_rate', 0):.1f}%")
        
        # Financial data breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Data Collection Status")
            data_types = list(stats.get('data_types_collected', []))
            
            if data_types:
                # Create a status overview
                status_data = []
                db = SessionLocal()
                try:
                    for data_type in ["net_worth", "bank_transactions", "epf_details", "credit_report"]:
                        count = db.query(MCPData).filter(MCPData.data_type == data_type).count()
                        status = "✅ Available" if count > 0 else "⏳ Pending"
                        status_data.append({"Data Type": data_type.replace("_", " ").title(), "Status": status, "Records": count})
                finally:
                    db.close()
                
                df_status = pd.DataFrame(status_data)
                st.dataframe(df_status, use_container_width=True, hide_index=True)
            else:
                st.info("No financial data collected yet. Click 'Collect Data' to start.")
        
        with col2:
            st.subheader("🎯 Recent AI Insights")
            recent_insights = insight_generator.get_recent_insights(limit=3)
            
            if recent_insights:
                for insight in recent_insights:
                    with st.container():
                        st.markdown(f"**{insight.title}**")
                        st.markdown(f"*{insight.insight_type}* • Confidence: {insight.confidence_score:.2f}")
                        st.markdown(f"_{insight.content[:100]}..._")
                        st.markdown("---")
            else:
                st.info("No insights generated yet. Click 'Generate Insights' to start AI analysis.")
    
    def render_net_worth_panel(self):
        """Render Net Worth analysis panel"""
        st.header("💰 Net Worth Analysis")
        
        # Get net worth data
        db = SessionLocal()
        try:
            net_worth_records = db.query(MCPData).filter(
                MCPData.data_type == "net_worth"
            ).order_by(MCPData.timestamp.desc()).all()
            
            if not net_worth_records:
                st.info("No net worth data available. Collect data from Fi MCP to see analysis.")
                return
            
            # Parse latest net worth data
            latest_record = net_worth_records[0]
            net_worth_data = latest_record.get_data()
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_nw = net_worth_data.get('total_net_worth', 'N/A')
                if isinstance(total_nw, (int, float)):
                    st.metric("Total Net Worth", f"₹{total_nw:,}")
                else:
                    st.metric("Total Net Worth", total_nw)
            
            with col2:
                total_assets = net_worth_data.get('total_assets', 'N/A')
                if isinstance(total_assets, (int, float)):
                    st.metric("Total Assets", f"₹{total_assets:,}")
                else:
                    st.metric("Total Assets", total_assets)
            
            with col3:
                total_liabilities = net_worth_data.get('total_liabilities', 'N/A')
                if isinstance(total_liabilities, (int, float)):
                    st.metric("Total Liabilities", f"₹{total_liabilities:,}")
                else:
                    st.metric("Total Liabilities", total_liabilities)
            
            # Asset breakdown
            assets = net_worth_data.get('assets', {})
            liabilities = net_worth_data.get('liabilities', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                if assets:
                    st.subheader("📈 Assets Breakdown")
                    
                    # Convert asset types to readable names
                    asset_names = {
                        'ASSET_TYPE_MUTUAL_FUND': 'Mutual Funds',
                        'ASSET_TYPE_EPF': 'EPF',
                        'ASSET_TYPE_BANK_ACCOUNT': 'Bank Accounts',
                        'ASSET_TYPE_STOCKS': 'Stocks',
                        'ASSET_TYPE_GOLD': 'Gold',
                        'ASSET_TYPE_REAL_ESTATE': 'Real Estate'
                    }
                    
                    readable_assets = {}
                    for key, value in assets.items():
                        readable_key = asset_names.get(key, key.replace('ASSET_TYPE_', '').replace('_', ' ').title())
                        readable_assets[readable_key] = value
                    
                    if readable_assets:
                        df_assets = pd.DataFrame(list(readable_assets.items()), columns=['Asset Type', 'Value'])
                        fig_assets = px.pie(df_assets, values='Value', names='Asset Type', 
                                          title="Asset Distribution")
                        st.plotly_chart(fig_assets, use_container_width=True)
                
            with col2:
                if liabilities:
                    st.subheader("📉 Liabilities Breakdown")
                    
                    # Convert liability types to readable names
                    liability_names = {
                        'LIABILITY_TYPE_VEHICLE_LOAN': 'Vehicle Loan',
                        'LIABILITY_TYPE_HOME_LOAN': 'Home Loan',
                        'LIABILITY_TYPE_PERSONAL_LOAN': 'Personal Loan',
                        'LIABILITY_TYPE_CREDIT_CARD': 'Credit Card',
                        'LIABILITY_TYPE_OTHER': 'Other'
                    }
                    
                    readable_liabilities = {}
                    for key, value in liabilities.items():
                        readable_key = liability_names.get(key, key.replace('LIABILITY_TYPE_', '').replace('_', ' ').title())
                        readable_liabilities[readable_key] = value
                    
                    if readable_liabilities:
                        df_liabilities = pd.DataFrame(list(readable_liabilities.items()), columns=['Liability Type', 'Value'])
                        fig_liabilities = px.bar(df_liabilities, x='Liability Type', y='Value',
                                               title="Liabilities by Type")
                        st.plotly_chart(fig_liabilities, use_container_width=True)
            
            # Raw data
            st.subheader("📋 Raw Net Worth Data")
            with st.expander("View detailed data"):
                st.json(net_worth_data)
            
        finally:
            db.close()
    
    def render_bank_transactions_panel(self):
        """Render Bank Transactions analysis panel"""
        st.header("🏦 Bank Transactions Analysis")
        
        # Get bank transaction data
        db = SessionLocal()
        try:
            bank_records = db.query(MCPData).filter(
                MCPData.data_type == "bank_transactions"
            ).order_by(MCPData.timestamp.desc()).all()
            
            if not bank_records:
                st.info("No bank transaction data available. Collect data from Fi MCP to see analysis.")
                return
            
            # Parse latest bank data
            latest_record = bank_records[0]
            bank_data = latest_record.get_data()
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                transaction_count = bank_data.get('transaction_count', 0)
                st.metric("Transaction Count", transaction_count)
            
            with col2:
                total_amount = bank_data.get('total_amount', 0)
                if isinstance(total_amount, (int, float)):
                    st.metric("Total Transaction Volume", f"₹{total_amount:,}")
                else:
                    st.metric("Total Transaction Volume", total_amount)
            
            with col3:
                last_updated = bank_data.get('timestamp', 'N/A')
                if last_updated != 'N/A':
                    formatted_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                    st.metric("Last Updated", formatted_time)
                else:
                    st.metric("Last Updated", last_updated)
            
            # Transaction analysis
            st.subheader("📊 Transaction Insights")
            
            if transaction_count > 0:
                st.info(f"Found {transaction_count} transactions in the latest data collection.")
                
                # Check if there's detailed transaction data in the raw response
                raw_data = bank_data.get('data', {})
                if 'transactions' in raw_data:
                    transactions = raw_data['transactions']
                    st.subheader("📋 Recent Transactions")
                    
                    # Display transaction details
                    if transactions:
                        for i, txn in enumerate(transactions[:10]):  # Show first 10 transactions
                            with st.expander(f"Transaction {i+1}"):
                                st.json(txn)
                    else:
                        st.info("No detailed transaction data available in current format.")
            else:
                st.info("No transactions found in the current data. This might be due to data format or collection issues.")
            
            # Raw data
            st.subheader("📋 Raw Bank Transaction Data")
            with st.expander("View detailed data"):
                st.json(bank_data)
            
        finally:
            db.close()
    
    def render_epf_panel(self):
        """Render EPF Details analysis panel"""
        st.header("🏛️ EPF (Employee Provident Fund) Analysis")
        
        # Get EPF data
        db = SessionLocal()
        try:
            epf_records = db.query(MCPData).filter(
                MCPData.data_type == "epf_details"
            ).order_by(MCPData.timestamp.desc()).all()
            
            if not epf_records:
                st.info("No EPF data available. Collect data from Fi MCP to see analysis.")
                return
            
            # Parse latest EPF data
            latest_record = epf_records[0]
            epf_data = latest_record.get_data()
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                epf_balance = epf_data.get('epf_balance', 0)
                if isinstance(epf_balance, (int, float)):
                    st.metric("EPF Balance", f"₹{epf_balance:,}")
                else:
                    st.metric("EPF Balance", epf_balance)
            
            with col2:
                last_updated = epf_data.get('timestamp', 'N/A')
                if last_updated != 'N/A':
                    formatted_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                    st.metric("Last Updated", formatted_time)
                else:
                    st.metric("Last Updated", last_updated)
            
            with col3:
                success_status = "✅ Success" if epf_data.get('success') else "❌ Failed"
                st.metric("Data Status", success_status)
            
            # EPF Analysis
            st.subheader("📊 EPF Insights")
            
            if isinstance(epf_balance, (int, float)) and epf_balance > 0:
                st.success(f"Your EPF account shows a balance of ₹{epf_balance:,}")
                
                # EPF projections (simple example)
                if epf_balance > 100000:
                    projected_annual = epf_balance * 0.08  # Assuming 8% annual return
                    st.info(f"Projected annual interest (8%): ₹{projected_annual:,.0f}")
                
            elif epf_balance == 0:
                st.warning("EPF balance shows ₹0. This might indicate:")
                st.markdown("- No EPF account linked")
                st.markdown("- Account not yet activated")
                st.markdown("- Data collection issue")
            else:
                st.info("EPF balance data not available in current format.")
            
            # Raw data
            st.subheader("📋 Raw EPF Data")
            with st.expander("View detailed data"):
                st.json(epf_data)
            
        finally:
            db.close()
    
    def render_credit_report_panel(self):
        """Render Credit Report analysis panel"""
        st.header("📊 Credit Report Analysis")
        
        # Get credit report data
        db = SessionLocal()
        try:
            credit_records = db.query(MCPData).filter(
                MCPData.data_type == "credit_report"
            ).order_by(MCPData.timestamp.desc()).all()
            
            if not credit_records:
                st.info("No credit report data available. Collect data from Fi MCP to see analysis.")
                return
            
            # Parse latest credit data
            latest_record = credit_records[0]
            credit_data = latest_record.get_data()
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                credit_score = credit_data.get('credit_score', 0)
                if isinstance(credit_score, (int, float)) and credit_score > 0:
                    # Color coding for credit score
                    if credit_score >= 750:
                        st.success(f"Credit Score: {credit_score}")
                        st.markdown("**Excellent** 🌟")
                    elif credit_score >= 700:
                        st.info(f"Credit Score: {credit_score}")
                        st.markdown("**Good** 👍")
                    elif credit_score >= 650:
                        st.warning(f"Credit Score: {credit_score}")
                        st.markdown("**Fair** ⚠️")
                    else:
                        st.error(f"Credit Score: {credit_score}")
                        st.markdown("**Poor** ❌")
                else:
                    st.metric("Credit Score", "N/A")
            
            with col2:
                last_updated = credit_data.get('timestamp', 'N/A')
                if last_updated != 'N/A':
                    formatted_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                    st.metric("Last Updated", formatted_time)
                else:
                    st.metric("Last Updated", last_updated)
            
            with col3:
                success_status = "✅ Success" if credit_data.get('success') else "❌ Failed"
                st.metric("Data Status", success_status)
            
            # Credit Score Analysis
            st.subheader("📈 Credit Score Insights")
            
            if isinstance(credit_score, (int, float)) and credit_score > 0:
                # Credit score gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = credit_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Credit Score"},
                    delta = {'reference': 750},
                    gauge = {
                        'axis': {'range': [None, 900]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 550], 'color': "lightgray"},
                            {'range': [550, 650], 'color': "yellow"},
                            {'range': [650, 750], 'color': "orange"},
                            {'range': [750, 900], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 800
                        }
                    }
                ))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Credit improvement tips
                st.subheader("💡 Credit Improvement Tips")
                if credit_score < 750:
                    st.markdown("**To improve your credit score:**")
                    st.markdown("- Pay all bills on time")
                    st.markdown("- Keep credit utilization below 30%")
                    st.markdown("- Don't close old credit accounts")
                    st.markdown("- Monitor your credit report regularly")
                    st.markdown("- Avoid multiple credit inquiries")
                else:
                    st.success("Excellent credit score! Keep maintaining good credit habits.")
            
            elif credit_score == 0:
                st.warning("Credit score shows 0. This might indicate:")
                st.markdown("- No credit history available")
                st.markdown("- Credit report not accessible")
                st.markdown("- Data collection issue")
            
            # Raw data
            st.subheader("📋 Raw Credit Report Data")
            with st.expander("View detailed data"):
                st.json(credit_data)
            
        finally:
            db.close()
    
    def render_insights(self):
        """Render AI insights section"""
        st.header("🧠 AI Generated Financial Insights")
        
        # Get recent insights
        recent_insights = insight_generator.get_recent_insights(limit=20)
        
        if not recent_insights:
            st.info("No insights generated yet. Click 'Generate Insights' to start AI analysis of your financial data.")
            return
        
        # Filter controls
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Recent Financial Insights")
        with col2:
            if st.button("🔄 Refresh Insights"):
                st.rerun()
        
        # Display insights with financial focus
        for insight in recent_insights:
            with st.expander(f"📝 {insight.title} ({insight.insight_type})", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(insight.content)
                    
                    # Show financial relevance
                    if any(keyword in insight.content.lower() for keyword in ['financial', 'investment', 'portfolio', 'risk']):
                        st.info("💡 This insight is relevant to your financial portfolio")
                
                with col2:
                    confidence_color = "green" if insight.confidence_score > 0.7 else "orange" if insight.confidence_score > 0.4 else "red"
                    st.markdown(f"**Confidence:** :{confidence_color}[{insight.confidence_score:.2f}]")
                    st.markdown(f"**Created:** {insight.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                with col3:
                    metadata = insight.get_metadata()
                    if metadata.get('key_factors'):
                        st.markdown("**Key Factors:**")
                        for factor in metadata['key_factors']:
                            st.markdown(f"• {factor}")
                    
                    if metadata.get('recommended_actions'):
                        st.markdown("**Recommendations:**")
                        for action in metadata['recommended_actions']:
                            st.markdown(f"• {action}")
    
    def render_system_status(self):
        """Render system status section"""
        st.header("⚙️ System Status")
        
        # Fi MCP Connection
        st.subheader("🔗 Fi MCP Server Status")
        col1, col2 = st.columns(2)
        
        with col1:
            if real_data_collector.test_mcp_connection():
                st.success("✅ Fi MCP Server Connected")
                st.info("Real financial data collection is active")
            else:
                st.error("❌ Fi MCP Server Disconnected")
                st.warning("Cannot collect real financial data")
        
        with col2:
            st.info("**Fi MCP Server Setup:**")
            st.code("cd fi-mcp-server")
            st.code("FI_MCP_PORT=8080 go run . &")
        
        # System information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Database Status")
            
            db = SessionLocal()
            try:
                mcp_count = db.query(MCPData).count()
                unprocessed_count = db.query(MCPData).filter(MCPData.processed == False).count()
                insights_count = db.query(AIInsight).count()
                
                st.metric("Total Records", mcp_count)
                st.metric("Unprocessed Records", unprocessed_count)
                st.metric("Generated Insights", insights_count)
                
                # Financial data breakdown
                st.markdown("**Financial Data Types:**")
                for data_type in ["net_worth", "bank_transactions", "epf_details", "credit_report"]:
                    count = db.query(MCPData).filter(MCPData.data_type == data_type).count()
                    status = "✅" if count > 0 else "⏳"
                    st.markdown(f"{status} {data_type.replace('_', ' ').title()}: {count} records")
                
            except Exception as e:
                st.error(f"Database connection error: {e}")
            finally:
                db.close()
        
        with col2:
            st.subheader("🔧 Configuration")
            
            from config import settings
            
            st.info(f"**Collection Interval:** {settings.collection_interval_minutes} minutes")
            st.info(f"**Insights Interval:** {settings.insights_generation_interval_minutes} minutes")
            st.info(f"**Database:** {settings.database_url}")
            st.info(f"**Log Level:** {settings.log_level}")
            
            # Collection statistics
            stats = real_data_collector.get_collection_stats()
            st.markdown("**Collection Stats:**")
            st.markdown(f"- Success Rate: {stats.get('success_rate', 0):.1f}%")
            st.markdown(f"- Total Collections: {stats.get('total_collections', 0)}")
            st.markdown(f"- Data Types: {len(stats.get('data_types_collected', []))}")
        
        # Control buttons
        st.subheader("🎛️ System Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Generate Insights Now"):
                with st.spinner("Generating AI insights..."):
                    insight_generator.generate_insights()
                st.success("Insight generation completed!")
        
        with col2:
            if st.button("📥 Collect Data Now"):
                with st.spinner("Collecting real financial data..."):
                    real_data_collector.collect_data()
                st.success("Data collection completed!")
        
        with col3:
            if st.button("🧪 Test Fi MCP Connection"):
                with st.spinner("Testing connection..."):
                    if real_data_collector.test_mcp_connection():
                        st.success("✅ Connection successful!")
                    else:
                        st.error("❌ Connection failed!")
        
        with col4:
            if st.button("📊 Export Financial Data"):
                # Export financial insights to CSV
                insights = insight_generator.get_recent_insights(limit=1000)
                if insights:
                    data = []
                    for insight in insights:
                        data.append({
                            'title': insight.title,
                            'type': insight.insight_type,
                            'content': insight.content,
                            'confidence': insight.confidence_score,
                            'created_at': insight.created_at
                        })
                    
                    df = pd.DataFrame(data)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="📄 Download Financial Insights",
                        data=csv,
                        file_name=f"financial_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

def main():
    """Main entry point"""
    dashboard = FinancialDashboard()
    dashboard.main()

if __name__ == "__main__":
    main() 