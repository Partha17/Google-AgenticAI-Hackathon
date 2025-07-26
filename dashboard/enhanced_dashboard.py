"""
Enhanced Financial Dashboard with Complete Google Cloud Integration
Comprehensive dashboard showcasing all Google Cloud services and multi-agent capabilities
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import asyncio
import logging

# Import all Google Cloud services
from services.google_cloud_manager import google_cloud_manager
from services.google_vertex_ai_enhanced import vertex_ai_enhanced
from services.google_auth_manager import google_auth_manager
from services.google_scheduler_manager import google_scheduler_manager
from services.google_cloud_functions_manager import google_cloud_functions_manager
from dashboard.google_charts_integration import google_charts

# Import ADK components
from adk_agents.adk_orchestrator import adk_orchestrator
from dashboard.adk_integration import adk_integration

# Configure Streamlit
st.set_page_config(
    page_title="🚀 Enhanced Financial Multi-Agent System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced design
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: none;
    }
    
    .enhanced-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #6B73FF 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .service-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .service-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-healthy { background-color: #4CAF50; }
    .status-warning { background-color: #FF9800; }
    .status-error { background-color: #f44336; }
    
    .chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 1.5rem;
        min-height: 500px;
        border: 1px solid #dee2e6;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main enhanced dashboard application"""
    
    # Enhanced Header
    st.markdown("""
    <div class="enhanced-header">
        <h1>🚀 Enhanced Financial Multi-Agent System</h1>
        <p>Powered by Google Cloud Platform • Multi-Agent ADK Architecture • Advanced AI Analytics</p>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 1rem;">
            <span>🔥 Firestore</span>
            <span>⚡ Cloud Functions</span>
            <span>🧠 Vertex AI</span>
            <span>📊 BigQuery</span>
            <span>🔐 Auth</span>
            <span>⏰ Scheduler</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication
    auth_result = google_auth_manager.create_login_widget()
    
    if not auth_result.get("authenticated"):
        st.info("🔐 Please authenticate to access the enhanced dashboard features")
        return
    
    # Sidebar with Google Cloud Status
    display_google_cloud_status()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Overview", 
        "🤖 Multi-Agent Control", 
        "☁️ Cloud Services", 
        "📊 Advanced Analytics",
        "💬 AI Assistant", 
        "⚙️ System Management"
    ])
    
    with tab1:
        show_enhanced_overview()
    
    with tab2:
        show_multi_agent_control()
    
    with tab3:
        show_cloud_services_dashboard()
    
    with tab4:
        show_advanced_analytics()
    
    with tab5:
        show_ai_assistant()
    
    with tab6:
        show_system_management()

def display_google_cloud_status():
    """Display Google Cloud services status in sidebar"""
    st.sidebar.markdown("## ☁️ Google Cloud Status")
    
    # Get comprehensive status
    try:
        cloud_status = asyncio.run(google_cloud_manager.get_comprehensive_status())
        
        st.sidebar.markdown("### Core Services")
        
        services = cloud_status.get("services", {})
        for service_name, service_info in services.items():
            status = service_info.get("status", "unknown")
            
            if status == "healthy":
                icon = "🟢"
            elif status == "degraded":
                icon = "🟡"
            else:
                icon = "🔴"
            
            display_name = service_name.replace("_", " ").title()
            st.sidebar.markdown(f"{icon} **{display_name}**")
        
        # Overall health
        overall_health = cloud_status.get("overall_health", "unknown")
        if overall_health == "healthy":
            st.sidebar.success("✅ All systems operational")
        elif overall_health == "degraded":
            st.sidebar.warning("⚠️ Some services degraded")
        else:
            st.sidebar.error("❌ System issues detected")
    
    except Exception as e:
        st.sidebar.error(f"❌ Status check failed: {str(e)}")
    
    # Quick actions
    st.sidebar.markdown("### 🚀 Quick Actions")
    
    if st.sidebar.button("🔄 Refresh All Services"):
        st.rerun()
    
    if st.sidebar.button("🔧 Initialize System"):
        with st.spinner("Initializing all services..."):
            try:
                # Initialize all services
                initialization_results = asyncio.run(initialize_all_services())
                if initialization_results.get("success"):
                    st.sidebar.success("✅ System initialized")
                else:
                    st.sidebar.error("❌ Initialization failed")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")

def show_enhanced_overview():
    """Show enhanced system overview"""
    
    st.subheader("🏗️ Enhanced Multi-Agent Architecture")
    
    # System metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 Agents</h3>
            <h2>4</h2>
            <p>Active AI Agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>☁️ Services</h3>
            <h2>8</h2>
            <p>Google Cloud Services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Functions</h3>
            <h2>5</h2>
            <p>Serverless Functions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Workflows</h3>
            <h2>6</h2>
            <p>Automated Workflows</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Architecture diagram
    st.subheader("🔄 System Architecture")
    
    architecture_col1, architecture_col2 = st.columns([2, 1])
    
    with architecture_col1:
        st.markdown("""
        <div class="service-card">
            <h4>📱 User Interface Layer</h4>
            <p><strong>Enhanced Streamlit Dashboard</strong> • Google Authentication • Real-time Updates</p>
        </div>
        
        <div class="service-card">
            <h4>🤖 Multi-Agent Layer</h4>
            <p><strong>ADK Orchestrator</strong> • Financial Data Collector • Risk Assessment • Market Analysis</p>
        </div>
        
        <div class="service-card">
            <h4>☁️ Google Cloud Services Layer</h4>
            <p><strong>Firestore</strong> • <strong>Cloud Functions</strong> • <strong>Vertex AI</strong> • <strong>BigQuery</strong> • <strong>Monitoring</strong></p>
        </div>
        
        <div class="service-card">
            <h4>🔗 Data Sources</h4>
            <p><strong>Fi MCP Server</strong> • Market Data APIs • External Financial Services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with architecture_col2:
        st.markdown("### 🎯 Key Features")
        st.markdown("""
        - **🔐 Secure Authentication** via Google OAuth
        - **⚡ Serverless Computing** with Cloud Functions
        - **🧠 Advanced AI** powered by Vertex AI
        - **📊 Real-time Analytics** with BigQuery
        - **🔄 Automated Workflows** via Cloud Scheduler
        - **📈 Interactive Visualizations** with Google Charts
        - **🔍 Comprehensive Monitoring** and Logging
        - **🌐 Multi-language Support** and Voice AI
        """)

def show_multi_agent_control():
    """Show multi-agent control dashboard"""
    
    st.subheader("🤖 Multi-Agent Control Center")
    
    # Agent status
    agent_col1, agent_col2 = st.columns([2, 1])
    
    with agent_col1:
        st.markdown("### 📊 Agent Status Dashboard")
        
        # Get agent status
        try:
            agent_status = asyncio.run(adk_orchestrator.initialize_system())
            
            if agent_status.get("system_status") == "ready":
                st.success("✅ All agents operational")
                
                agent_statuses = agent_status.get("agent_status", {})
                for agent_name, status in agent_statuses.items():
                    agent_display_name = agent_name.replace("_", " ").title()
                    if status.get("status") == "ready":
                        st.markdown(f"🟢 **{agent_display_name}**: Ready")
                    else:
                        st.markdown(f"🔴 **{agent_display_name}**: Error")
            else:
                st.warning("⚠️ Some agents not ready")
        
        except Exception as e:
            st.error(f"❌ Error getting agent status: {str(e)}")
    
    with agent_col2:
        st.markdown("### 🎮 Agent Controls")
        
        if st.button("🚀 Run Comprehensive Analysis"):
            with st.spinner("Running comprehensive analysis..."):
                try:
                    result = asyncio.run(adk_orchestrator.execute_comprehensive_analysis())
                    if result.get("workflow_status") == "completed":
                        st.success("✅ Analysis completed successfully")
                        
                        # Show results summary
                        execution_time = result.get("execution_time_seconds", 0)
                        st.info(f"⏱️ Execution time: {execution_time:.1f} seconds")
                        
                        # Show agent outputs
                        agent_outputs = result.get("agent_outputs", {})
                        for agent, output in agent_outputs.items():
                            if isinstance(output, dict) and not output.get("error"):
                                st.success(f"✅ {agent.replace('_', ' ').title()}: Success")
                    else:
                        st.error("❌ Analysis failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        if st.button("📊 Risk Assessment"):
            with st.spinner("Running risk assessment..."):
                try:
                    result = asyncio.run(adk_orchestrator.execute_targeted_analysis("risk_assessment"))
                    if result.get("status") == "completed":
                        st.success("✅ Risk assessment completed")
                    else:
                        st.error("❌ Risk assessment failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        if st.button("📈 Market Analysis"):
            with st.spinner("Running market analysis..."):
                try:
                    result = asyncio.run(adk_orchestrator.execute_targeted_analysis("market_analysis"))
                    if result.get("status") == "completed":
                        st.success("✅ Market analysis completed")
                    else:
                        st.error("❌ Market analysis failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_cloud_services_dashboard():
    """Show Google Cloud services dashboard"""
    
    st.subheader("☁️ Google Cloud Services Dashboard")
    
    # Service tabs
    service_tab1, service_tab2, service_tab3, service_tab4 = st.tabs([
        "🔥 Storage & Data", 
        "⚡ Compute & Functions", 
        "🧠 AI & Analytics", 
        "🔐 Security & Monitoring"
    ])
    
    with service_tab1:
        show_storage_data_services()
    
    with service_tab2:
        show_compute_functions_services()
    
    with service_tab3:
        show_ai_analytics_services()
    
    with service_tab4:
        show_security_monitoring_services()

def show_storage_data_services():
    """Show storage and data services"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Firestore")
        
        if st.button("Test Firestore Connection"):
            with st.spinner("Testing Firestore..."):
                try:
                    result = asyncio.run(google_cloud_manager.store_financial_data(
                        "test_user", 
                        {"test": True, "timestamp": datetime.utcnow().isoformat()}
                    ))
                    if result:
                        st.success("✅ Firestore connection successful")
                    else:
                        st.error("❌ Firestore connection failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown("### 📦 Cloud Storage")
        
        if st.button("Test Cloud Storage"):
            with st.spinner("Testing Cloud Storage..."):
                try:
                    result = asyncio.run(google_cloud_manager.upload_file(
                        "test.txt", 
                        "test-file.txt", 
                        "Test content"
                    ))
                    if result:
                        st.success("✅ Cloud Storage connection successful")
                    else:
                        st.error("❌ Cloud Storage connection failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 📊 BigQuery")
        
        if st.button("Test BigQuery Connection"):
            with st.spinner("Testing BigQuery..."):
                try:
                    test_metrics = {
                        "agent_id": "test_agent",
                        "metric_name": "test_metric", 
                        "metric_value": 1.0,
                        "test": True
                    }
                    result = asyncio.run(google_cloud_manager.store_agent_metrics(test_metrics))
                    if result:
                        st.success("✅ BigQuery connection successful")
                    else:
                        st.error("❌ BigQuery connection failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown("### 📡 Pub/Sub")
        
        if st.button("Test Pub/Sub"):
            with st.spinner("Testing Pub/Sub..."):
                try:
                    result = asyncio.run(google_cloud_manager.publish_agent_event(
                        "test_agent", 
                        "test_event", 
                        {"test": True}
                    ))
                    st.success("✅ Pub/Sub message published")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_compute_functions_services():
    """Show compute and functions services"""
    
    st.markdown("### ⚡ Cloud Functions Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # List deployed functions
        if st.button("📋 List Deployed Functions"):
            with st.spinner("Loading functions..."):
                try:
                    functions_status = asyncio.run(google_cloud_functions_manager.get_functions_status())
                    if functions_status.get("success"):
                        functions = functions_status.get("functions", [])
                        if functions:
                            df = pd.DataFrame(functions)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info("No functions deployed")
                    else:
                        st.error(f"❌ Error: {functions_status.get('error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 🚀 Quick Deploy")
        
        if st.button("Deploy Financial Functions"):
            with st.spinner("Deploying functions..."):
                try:
                    result = asyncio.run(google_cloud_functions_manager.deploy_all_financial_functions())
                    if result.get("success"):
                        deployed = result.get("deployed_functions", 0)
                        total = result.get("total_functions", 0)
                        st.success(f"✅ Deployed {deployed}/{total} functions")
                    else:
                        st.error(f"❌ Deployment failed: {result.get('error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_ai_analytics_services():
    """Show AI and analytics services"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧠 Vertex AI Enhanced")
        
        # Test sentiment analysis
        if st.button("Test Market Sentiment Analysis"):
            with st.spinner("Analyzing sentiment..."):
                try:
                    test_data = [
                        "The market is showing strong bullish signals",
                        "Economic indicators are positive",
                        "Tech stocks are performing well"
                    ]
                    result = asyncio.run(vertex_ai_enhanced.analyze_market_sentiment(test_data))
                    if result.get("success"):
                        st.success("✅ Sentiment analysis completed")
                        sentiment = result.get("sentiment_analysis", {})
                        st.json(sentiment)
                    else:
                        st.error(f"❌ Error: {result.get('error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Test portfolio optimization
        if st.button("Test AI Portfolio Optimization"):
            with st.spinner("Optimizing portfolio..."):
                try:
                    test_portfolio = {
                        "stocks": 60,
                        "bonds": 30,
                        "cash": 10
                    }
                    test_objectives = {
                        "risk_tolerance": "moderate",
                        "time_horizon": "long_term"
                    }
                    result = asyncio.run(vertex_ai_enhanced.optimize_portfolio_ai(test_portfolio, test_objectives))
                    if result.get("success"):
                        st.success("✅ Portfolio optimization completed")
                    else:
                        st.error(f"❌ Error: {result.get('error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Google Charts")
        
        # Demo charts
        if st.button("Show Portfolio Treemap"):
            demo_portfolio_data = {
                "holdings": [
                    {"name": "Apple", "sector": "Technology", "value": 50000, "change_percent": 2.5},
                    {"name": "Microsoft", "sector": "Technology", "value": 40000, "change_percent": 1.8},
                    {"name": "Amazon", "sector": "Consumer", "value": 30000, "change_percent": -0.5},
                    {"name": "Tesla", "sector": "Automotive", "value": 25000, "change_percent": 3.2}
                ]
            }
            
            treemap_html = google_charts.create_portfolio_treemap(demo_portfolio_data)
            google_charts.render_in_streamlit(treemap_html, height=400)
        
        if st.button("Show Risk Gauge"):
            risk_gauge_html = google_charts.create_risk_gauge_chart(65.0, "Medium-High")
            google_charts.render_in_streamlit(risk_gauge_html, height=350)

def show_security_monitoring_services():
    """Show security and monitoring services"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔐 Authentication Status")
        
        auth_status = google_auth_manager.get_auth_status()
        
        if auth_status.get("oauth_configured"):
            st.success("✅ OAuth configured")
        else:
            st.warning("⚠️ OAuth not configured")
        
        if auth_status.get("firebase_available"):
            st.success("✅ Firebase Auth available")
        else:
            st.info("ℹ️ Firebase Auth not configured")
        
        active_sessions = auth_status.get("active_sessions", 0)
        st.metric("Active Sessions", active_sessions)
        
        authenticated_users = auth_status.get("authenticated_users", 0)
        st.metric("Authenticated Users", authenticated_users)
    
    with col2:
        st.markdown("### 📊 Cloud Monitoring")
        
        if st.button("Record Test Metric"):
            with st.spinner("Recording metric..."):
                try:
                    result = asyncio.run(google_cloud_manager.record_custom_metric(
                        "dashboard_test", 
                        75.0, 
                        {"source": "dashboard", "test": "true"}
                    ))
                    if result:
                        st.success("✅ Metric recorded successfully")
                    else:
                        st.error("❌ Failed to record metric")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        if st.button("Get System Metrics"):
            with st.spinner("Retrieving metrics..."):
                try:
                    metrics = asyncio.run(google_cloud_manager.get_system_metrics(hours_back=1))
                    if metrics:
                        st.success("✅ Metrics retrieved")
                        st.json(metrics)
                    else:
                        st.info("No metrics found")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_advanced_analytics():
    """Show advanced analytics dashboard"""
    
    st.subheader("📊 Advanced Analytics Suite")
    
    # Sample financial data for demo
    demo_financial_data = {
        "portfolio": {
            "holdings": [
                {"name": "AAPL", "sector": "Technology", "value": 50000, "change_percent": 2.5},
                {"name": "MSFT", "sector": "Technology", "value": 40000, "change_percent": 1.8},
                {"name": "AMZN", "sector": "Consumer", "value": 30000, "change_percent": -0.5},
                {"name": "TSLA", "sector": "Automotive", "value": 25000, "change_percent": 3.2}
            ]
        },
        "risk_assessment": {
            "risk_score": 65.0,
            "risk_level": "Medium-High"
        },
        "sector_allocation": {
            "Technology": 45.0,
            "Healthcare": 20.0,
            "Finance": 15.0,
            "Consumer": 12.0,
            "Energy": 8.0
        },
        "metrics": [
            {"name": "Portfolio Value", "current_value": 85, "target_value": 90, "status": "normal"},
            {"name": "Diversification", "current_value": 78, "target_value": 80, "status": "warning"},
            {"name": "Risk Level", "current_value": 65, "target_value": 60, "status": "warning"},
            {"name": "Performance", "current_value": 92, "target_value": 85, "status": "good"}
        ]
    }
    
    # Generate all charts
    charts = google_charts.create_advanced_analytics_suite(demo_financial_data)
    
    # Display charts in tabs
    chart_tab1, chart_tab2, chart_tab3 = st.tabs([
        "📈 Portfolio & Performance", 
        "🎯 Risk & Allocation", 
        "📊 Real-time Metrics"
    ])
    
    with chart_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            if "portfolio_treemap" in charts:
                st.markdown("#### Portfolio Allocation Treemap")
                google_charts.render_in_streamlit(charts["portfolio_treemap"], height=400)
        
        with col2:
            if "sector_pie" in charts:
                st.markdown("#### Sector Allocation")
                google_charts.render_in_streamlit(charts["sector_pie"], height=400)
    
    with chart_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            if "risk_gauge" in charts:
                st.markdown("#### Risk Assessment Gauge")
                google_charts.render_in_streamlit(charts["risk_gauge"], height=350)
        
        with col2:
            st.markdown("#### Advanced Risk Metrics")
            st.metric("Value at Risk (95%)", "$12,500", delta="-$500")
            st.metric("Sharpe Ratio", "1.42", delta="0.08")
            st.metric("Beta", "1.15", delta="-0.03")
            st.metric("Max Drawdown", "8.5%", delta="1.2%")
    
    with chart_tab3:
        if "metrics_dashboard" in charts:
            st.markdown("#### Real-time Financial Metrics")
            google_charts.render_in_streamlit(charts["metrics_dashboard"], height=500)

def show_ai_assistant():
    """Show AI assistant interface"""
    
    st.subheader("💬 Enhanced AI Financial Assistant")
    
    # Chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
    
    # Chat input
    user_input = st.text_input("Ask your financial question:", key="chat_input")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Send") and user_input:
            process_chat_message(user_input)
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col3:
        st.markdown("**Quick Questions:**")
        if st.button("Analyze my portfolio"):
            process_chat_message("Please analyze my portfolio comprehensively")
        if st.button("What's my risk level?"):
            process_chat_message("What is my current risk level and how can I optimize it?")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI capabilities showcase
    st.markdown("### 🧠 AI Capabilities")
    
    capability_col1, capability_col2 = st.columns(2)
    
    with capability_col1:
        st.markdown("""
        **🔍 Analysis Capabilities:**
        - Portfolio performance analysis
        - Risk assessment and stress testing
        - Market sentiment analysis
        - Investment opportunity identification
        - Diversification optimization
        """)
    
    with capability_col2:
        st.markdown("""
        **🌐 Advanced Features:**
        - Multi-language support
        - Voice-to-text queries
        - Text-to-speech responses
        - Custom financial forecasting
        - Real-time market monitoring
        """)

def show_system_management():
    """Show system management interface"""
    
    st.subheader("⚙️ System Management & Configuration")
    
    mgmt_tab1, mgmt_tab2, mgmt_tab3 = st.tabs([
        "📅 Scheduler Management", 
        "🔧 Service Configuration", 
        "📈 Performance Monitoring"
    ])
    
    with mgmt_tab1:
        show_scheduler_management()
    
    with mgmt_tab2:
        show_service_configuration()
    
    with mgmt_tab3:
        show_performance_monitoring()

def show_scheduler_management():
    """Show scheduler management interface"""
    
    st.markdown("### ⏰ Cloud Scheduler Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📋 List Scheduled Jobs"):
            with st.spinner("Loading scheduled jobs..."):
                try:
                    jobs_result = asyncio.run(google_scheduler_manager.list_all_jobs())
                    if jobs_result.get("success"):
                        jobs = jobs_result.get("jobs", [])
                        if jobs:
                            df = pd.DataFrame(jobs)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info("No scheduled jobs found")
                    else:
                        st.error(f"❌ Error: {jobs_result.get('error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 🚀 Quick Setup")
        
        if st.button("Setup Financial Workflows"):
            with st.spinner("Setting up workflows..."):
                try:
                    result = asyncio.run(google_scheduler_manager.setup_financial_workflows())
                    if result.get("success"):
                        created = result.get("workflows_created", 0)
                        total = result.get("total_workflows", 0)
                        st.success(f"✅ Created {created}/{total} workflows")
                    else:
                        st.error(f"❌ Setup failed: {result.get('error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def show_service_configuration():
    """Show service configuration interface"""
    
    st.markdown("### 🔧 Service Configuration")
    
    # Configuration status
    config_data = {
        "Google Cloud Project": st.session_state.get("project_id", "Not configured"),
        "Cloud Region": st.session_state.get("location", "us-central1"),
        "Firestore Database": "Configured" if google_cloud_manager.initialized_services.get("firestore") else "Not configured",
        "BigQuery Dataset": "Configured" if google_cloud_manager.initialized_services.get("bigquery") else "Not configured",
        "Pub/Sub Topics": "Configured" if google_cloud_manager.initialized_services.get("pubsub") else "Not configured",
    }
    
    for config_item, status in config_data.items():
        if "Configured" in status:
            st.success(f"✅ {config_item}: {status}")
        else:
            st.warning(f"⚠️ {config_item}: {status}")

def show_performance_monitoring():
    """Show performance monitoring interface"""
    
    st.markdown("### 📈 Performance Monitoring")
    
    # Generate sample performance data
    performance_data = {
        "System Metrics": {
            "CPU Usage": 45.2,
            "Memory Usage": 62.8,
            "Network I/O": 23.1,
            "Storage Usage": 38.9
        },
        "Agent Performance": {
            "Data Collector": 95.5,
            "Risk Assessor": 92.3,
            "Market Analyzer": 88.7,
            "Orchestrator": 97.1
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### System Metrics")
        for metric, value in performance_data["System Metrics"].items():
            st.metric(metric, f"{value}%", delta=f"{value-50:.1f}%")
    
    with col2:
        st.markdown("#### Agent Performance")
        for agent, score in performance_data["Agent Performance"].items():
            st.metric(agent, f"{score}%", delta=f"{score-90:.1f}%")

# Helper functions

def process_chat_message(user_input: str):
    """Process chat message with AI assistant"""
    try:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response (placeholder)
        if "portfolio" in user_input.lower():
            response = "🤖 Based on your portfolio analysis, I can see you have a well-diversified investment mix. Your current risk level is moderate, with strong performance in technology sectors. I recommend considering some rebalancing to reduce concentration risk."
        elif "risk" in user_input.lower():
            response = "🤖 Your current risk level is Medium-High (65/100). This is slightly above your target of 60. I suggest reducing exposure to volatile assets and increasing allocation to bonds or defensive stocks."
        elif "market" in user_input.lower():
            response = "🤖 Current market sentiment is bullish with strong momentum in tech and healthcare sectors. However, be aware of potential volatility in the coming weeks due to economic indicators."
        else:
            response = "🤖 I can help you with portfolio analysis, risk assessment, market insights, and investment recommendations. What specific aspect of your finances would you like to explore?"
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Trigger rerun to update chat
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error processing message: {str(e)}")

async def initialize_all_services():
    """Initialize all Google Cloud services"""
    try:
        # Initialize ADK system
        adk_result = await adk_orchestrator.initialize_system()
        
        # Get cloud services status
        cloud_status = await google_cloud_manager.get_comprehensive_status()
        
        return {
            "success": True,
            "adk_status": adk_result,
            "cloud_status": cloud_status
        }
        
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    main() 