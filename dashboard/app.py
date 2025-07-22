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
from services.data_collector import data_collector

# Page configuration
st.set_page_config(
    page_title="Agentic AI Financial Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class Dashboard:
    def __init__(self):
        create_tables()  # Ensure tables exist
    
    def main(self):
        """Main dashboard interface"""
        st.title("🤖 Agentic AI Financial Insights Dashboard")
        st.markdown("Real-time financial analysis powered by AI agents")
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🧠 AI Insights", "📊 Data Analysis", "⚙️ System Status"])
        
        with tab1:
            self.render_overview()
        
        with tab2:
            self.render_insights()
        
        with tab3:
            self.render_data_analysis()
        
        with tab4:
            self.render_system_status()
    
    def render_sidebar(self):
        """Render sidebar controls"""
        st.sidebar.header("🎛️ Controls")
        
        # System controls
        st.sidebar.subheader("System Control")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🚀 Start Data Collection"):
                data_collector.start_collection()
                st.success("Data collection started!")
        
        with col2:
            if st.button("🧠 Start AI Analysis"):
                insight_generator.start_generation()
                st.success("AI analysis started!")
        
        # Filters
        st.sidebar.subheader("📊 Filters")
        
        insight_types = ["All", "trend_analysis", "risk_assessment", "opportunity", "market_sentiment"]
        selected_type = st.sidebar.selectbox("Insight Type", insight_types)
        
        days_back = st.sidebar.slider("Days to show", 1, 30, 7)
        
        return selected_type, days_back
    
    def render_overview(self):
        """Render overview section"""
        st.header("📈 System Overview")
        
        # Get statistics
        stats = insight_generator.get_insights_stats()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Insights", stats['total_insights'])
        
        with col2:
            avg_confidence = 0
            if stats['by_type']:
                avg_confidence = sum(s['avg_confidence'] for s in stats['by_type']) / len(stats['by_type'])
            st.metric("Avg Confidence", f"{avg_confidence:.2f}")
        
        with col3:
            st.metric("Data Types", len(stats['by_type']))
        
        with col4:
            # Get data collection count
            db = SessionLocal()
            try:
                data_count = db.query(MCPData).count()
                st.metric("Data Points", data_count)
            finally:
                db.close()
        
        # Insights by type chart
        if stats['by_type']:
            st.subheader("📊 Insights by Type")
            
            df_types = pd.DataFrame(stats['by_type'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(df_types, values='count', names='type', 
                               title="Distribution of Insight Types")
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar = px.bar(df_types, x='type', y='avg_confidence',
                               title="Average Confidence by Type")
                st.plotly_chart(fig_bar, use_container_width=True)
    
    def render_insights(self):
        """Render AI insights section"""
        st.header("🧠 AI Generated Insights")
        
        # Get recent insights
        recent_insights = insight_generator.get_recent_insights(limit=20)
        
        if not recent_insights:
            st.info("No insights generated yet. Start the system to begin analysis.")
            return
        
        # Filter controls
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Recent Insights")
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        # Display insights
        for insight in recent_insights:
            with st.expander(f"📝 {insight.title} ({insight.insight_type})", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(insight.content)
                
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
    
    def render_data_analysis(self):
        """Render data analysis section"""
        st.header("📊 Data Analysis")
        
        # Get MCP data
        db = SessionLocal()
        try:
            # Recent data trends
            recent_data = db.query(MCPData).order_by(MCPData.timestamp.desc()).limit(100).all()
            
            if not recent_data:
                st.info("No data collected yet. Start data collection to see analysis.")
                return
            
            # Convert to DataFrame
            data_list = []
            for record in recent_data:
                data = record.get_data()
                data['id'] = record.id
                data['timestamp'] = record.timestamp
                data['data_type'] = record.data_type
                data_list.append(data)
            
            df = pd.DataFrame(data_list)
            
            # Data overview
            st.subheader("Data Overview")
            col1, col2 = st.columns(2)
            
            with col1:
                # Data types distribution
                type_counts = df['data_type'].value_counts()
                fig_types = px.bar(x=type_counts.index, y=type_counts.values,
                                 title="Data Collection by Type")
                st.plotly_chart(fig_types, use_container_width=True)
            
            with col2:
                # Data collection timeline
                df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
                hourly_counts = df.groupby('hour').size()
                fig_timeline = px.line(x=hourly_counts.index, y=hourly_counts.values,
                                     title="Data Collection Timeline (by Hour)")
                st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Stock data analysis (if available)
            stock_data = df[df['data_type'] == 'stock_data']
            if not stock_data.empty and 'price' in stock_data.columns:
                st.subheader("Stock Price Analysis")
                
                # Stock prices by symbol
                if 'symbol' in stock_data.columns:
                    symbols = stock_data['symbol'].unique()[:5]  # Top 5 symbols
                    
                    for symbol in symbols:
                        symbol_data = stock_data[stock_data['symbol'] == symbol].sort_values('timestamp')
                        if len(symbol_data) > 1:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=symbol_data['timestamp'],
                                y=symbol_data['price'],
                                mode='lines+markers',
                                name=symbol,
                                line=dict(width=2)
                            ))
                            fig.update_layout(title=f"{symbol} Price Trend", 
                                            xaxis_title="Time", 
                                            yaxis_title="Price ($)")
                            st.plotly_chart(fig, use_container_width=True)
            
            # Raw data table
            st.subheader("Recent Data Points")
            st.dataframe(df.head(20), use_container_width=True)
            
        finally:
            db.close()
    
    def render_system_status(self):
        """Render system status section"""
        st.header("⚙️ System Status")
        
        # System information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Database Status")
            
            db = SessionLocal()
            try:
                mcp_count = db.query(MCPData).count()
                unprocessed_count = db.query(MCPData).filter(MCPData.processed == False).count()
                insights_count = db.query(AIInsight).count()
                
                st.metric("MCP Records", mcp_count)
                st.metric("Unprocessed Records", unprocessed_count)
                st.metric("Generated Insights", insights_count)
                
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
        
        # Control buttons
        st.subheader("🎛️ System Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Generate Insights Now"):
                insight_generator.generate_insights()
                st.success("Insight generation triggered!")
        
        with col2:
            if st.button("📥 Collect Data Now"):
                data_collector.collect_data()
                st.success("Data collection triggered!")
        
        with col3:
            if st.button("🗑️ Clear Processed Data"):
                if st.session_state.get('confirm_clear'):
                    # Clear processed data
                    db = SessionLocal()
                    try:
                        db.query(MCPData).filter(MCPData.processed == True).delete()
                        db.commit()
                        st.success("Processed data cleared!")
                    finally:
                        db.close()
                    st.session_state['confirm_clear'] = False
                else:
                    st.session_state['confirm_clear'] = True
                    st.warning("Click again to confirm clearing processed data")
        
        with col4:
            if st.button("📊 Export Data"):
                # Export insights to CSV
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
                        label="📄 Download Insights CSV",
                        data=csv,
                        file_name=f"ai_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

def main():
    """Main entry point"""
    dashboard = Dashboard()
    dashboard.main()

if __name__ == "__main__":
    main() 