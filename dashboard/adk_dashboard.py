"""
ADK Multi-Agent Financial Dashboard
Clean dashboard specifically for the ADK multi-agent system
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import asyncio
import logging

# Configure Streamlit
st.set_page_config(
    page_title="🤖 ADK Financial Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import ADK components
try:
    from dashboard.adk_integration import (
        adk_integration, 
        display_adk_status, 
        create_adk_chat_interface,
        create_adk_analysis_dashboard
    )
    ADK_AVAILABLE = True
except ImportError as e:
    st.error(f"ADK components not available: {e}")
    ADK_AVAILABLE = False

# Custom CSS for modern ADK design
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: none;
    }
    
    .adk-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        min-height: 400px;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main ADK dashboard application"""
    
    # Header
    st.markdown("""
    <div class="adk-header">
        <h1>🤖 ADK Financial Multi-Agent System</h1>
        <p>Sophisticated financial intelligence through coordinated AI agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display ADK system status in sidebar
    display_adk_status()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Overview", 
        "🤖 Multi-Agent Analysis", 
        "💬 Chat Assistant", 
        "📊 System Monitoring"
    ])
    
    with tab1:
        show_overview()
    
    with tab2:
        if ADK_AVAILABLE:
            create_adk_analysis_dashboard()
        else:
            st.error("ADK system is not available. Please check the installation.")
    
    with tab3:
        if ADK_AVAILABLE:
            create_adk_chat_interface()
        else:
            st.error("ADK chat system is not available. Please check the installation.")
    
    with tab4:
        show_system_monitoring()

def show_overview():
    """Show ADK system overview"""
    
    st.subheader("🏗️ Multi-Agent Architecture")
    
    # Agent overview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h3>🔍 Financial Data Collector Agent</h3>
            <p><strong>Specialization:</strong> Real-time data collection and validation</p>
            <ul>
                <li>Fi MCP server integration</li>
                <li>Data quality assessment</li>
                <li>Multi-source aggregation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="agent-card">
            <h3>📈 Market Analysis Agent</h3>
            <p><strong>Specialization:</strong> Market intelligence and opportunity identification</p>
            <ul>
                <li>Technical analysis</li>
                <li>Market regime detection</li>
                <li>Investment opportunities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h3>⚖️ Risk Assessment Agent</h3>
            <p><strong>Specialization:</strong> Portfolio risk analysis and stress testing</p>
            <ul>
                <li>Advanced risk metrics</li>
                <li>Stress testing scenarios</li>
                <li>Mitigation strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="agent-card">
            <h3>🎯 ADK Orchestrator Agent</h3>
            <p><strong>Specialization:</strong> Multi-agent coordination and synthesis</p>
            <ul>
                <li>Workflow orchestration</li>
                <li>Cross-agent insights</li>
                <li>System health monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Benefits section
    st.subheader("✨ Multi-Agent Benefits")
    
    benefit_col1, benefit_col2, benefit_col3 = st.columns(3)
    
    with benefit_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 Enhanced Performance</h4>
            <p>Parallel processing with specialized agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with benefit_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 Superior Intelligence</h4>
            <p>Cross-agent collaboration and synthesis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with benefit_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>⚖️ Advanced Analysis</h4>
            <p>Multi-dimensional financial insights</p>
        </div>
        """, unsafe_allow_html=True)

def show_system_monitoring():
    """Show system monitoring and health metrics"""
    
    st.subheader("📊 System Monitoring")
    
    if not ADK_AVAILABLE:
        st.error("ADK system monitoring is not available.")
        return
    
    # System status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔍 System Health Check")
        
        if st.button("🔄 Refresh System Status"):
            with st.spinner("Checking system health..."):
                try:
                    status = asyncio.run(adk_integration.get_system_status())
                    
                    if "error" not in status:
                        overall_status = status.get("overall_status", "unknown")
                        
                        # Status indicator
                        status_color = {
                            "healthy": "🟢",
                            "partial": "🟡", 
                            "degraded": "🟠",
                            "error": "🔴"
                        }.get(overall_status, "⚪")
                        
                        st.markdown(f"**Overall Status:** {status_color} {overall_status.title()}")
                        
                        # Agent health details
                        agent_health = status.get("agent_health", {})
                        
                        st.markdown("**Agent Health:**")
                        for agent, health in agent_health.items():
                            agent_name = agent.replace("_", " ").title()
                            health_status = health.get("status", "unknown")
                            
                            health_emoji = {
                                "healthy": "✅",
                                "partial": "⚠️",
                                "degraded": "🟠", 
                                "error": "❌"
                            }.get(health_status, "❓")
                            
                            st.write(f"{health_emoji} **{agent_name}:** {health_status.title()}")
                        
                        # Performance metrics
                        performance_metrics = status.get("performance_metrics", {})
                        if performance_metrics:
                            st.markdown("**Performance Metrics:**")
                            for metric, value in performance_metrics.items():
                                if isinstance(value, dict) and not value.get("error"):
                                    st.write(f"• **{metric.replace('_', ' ').title()}:** {value}")
                        
                        # Active alerts
                        alerts = status.get("alerts", [])
                        if alerts:
                            st.markdown("**🚨 Active Alerts:**")
                            for alert in alerts:
                                st.warning(f"⚠️ {alert}")
                        else:
                            st.success("✅ No active alerts")
                    
                    else:
                        st.error(f"System check failed: {status.get('error')}")
                
                except Exception as e:
                    st.error(f"Error checking system status: {str(e)}")
    
    with col2:
        st.markdown("### 📈 Quick Actions")
        
        if st.button("🔄 Initialize System"):
            with st.spinner("Initializing ADK system..."):
                try:
                    success = asyncio.run(adk_integration.initialize_adk_system())
                    if success:
                        st.success("✅ System initialized successfully!")
                    else:
                        st.error("❌ System initialization failed")
                except Exception as e:
                    st.error(f"Initialization error: {str(e)}")
        
        if st.button("🧪 Run System Test"):
            with st.spinner("Running system test..."):
                st.info("System test functionality coming soon...")

    # Documentation section
    st.subheader("📚 Documentation")
    
    doc_col1, doc_col2 = st.columns(2)
    
    with doc_col1:
        st.markdown("""
        **🚀 Quick Start:**
        1. Ensure Fi MCP server is running on port 8080
        2. Configure Google Cloud credentials
        3. Initialize the ADK system
        4. Start using multi-agent analysis
        """)
    
    with doc_col2:
        st.markdown("""
        **🔗 Resources:**
        - [Google Cloud ADK Tutorial](https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation)
        - [Multi-Agent Guide](https://github.com/iamthuya/google-cloud-workshops/blob/main/ai-agents/agent-development-kit/orchestrating_multi_agent_systems.ipynb)
        - [Project README](README.md)
        """)

if __name__ == "__main__":
    main() 