# 🚀 Quick Start Guide - Local Mode

## Overview
Your Enhanced Financial Multi-Agent System is now ready to run locally with intelligent AI analysis that uses actual financial data!

## ✅ What's Fixed
- **AI Analysis**: Now fetches real financial data from your database
- **Sample Data**: Provides demo portfolio data when no real data is available
- **Context-Aware Responses**: AI chooses appropriate analysis method based on your question
- **Both Dashboards**: Original and Enhanced dashboards both have interactive AI features

## 🎯 Quick Launch Options

### Option 1: Complete System Startup (NEW - Recommended)
```bash
# Start everything: Fi MCP Server + ADK Agents + Dashboard
./start.sh

# Or with Python directly
python start_system.py
```

### Option 2: Dashboard Only Launcher
```bash
# Interactive dashboard launcher
python launch_dashboard.py --interactive

# Direct dashboard launch
python launch_dashboard.py --dashboard original
python launch_dashboard.py --dashboard enhanced
```

### Option 3: Advanced System Options
```bash
# Complete system with enhanced dashboard
./start.sh --dashboard enhanced

# Complete system with process monitoring
./start.sh --monitor

# Cleanup existing processes only
./start.sh --cleanup-only
```

## 💬 AI Analysis Features

### What You Can Ask:
- **Portfolio Questions**: "Give me my portfolio", "What's my asset allocation?"
- **Risk Analysis**: "What's my risk level?", "Assess my investment risk"
- **Performance**: "How are my investments performing?"
- **Spending**: "Analyze my spending patterns"
- **General**: Any financial question

### How It Works:
1. **Real Data**: AI fetches your actual financial data from the database
2. **Fi MCP Integration**: Connects to Fi MCP server for live financial data
3. **Sample Data**: Shows demo portfolio when no real data exists
4. **Context Display**: View exactly what data the AI used for analysis

## 📊 Dashboard Features

### Original Dashboard (Stable)
- **URL**: http://localhost:8501
- **Features**: 
  - Financial overview with real data
  - Interactive AI chat
  - Automatic insights generation
  - Quota management

### Enhanced Dashboard (Google Cloud)
- **URL**: http://localhost:8502 (when run separately)
- **Features**:
  - All original features
  - Google Cloud integration (optional)
  - Enhanced visualizations
  - Local mode fallback

## 🔌 Fi MCP Server

### Check if Running:
```bash
curl http://localhost:8080
```

### Start Manually:
```bash
cd fi-mcp-server
FI_MCP_PORT=8080 go run main.go
```

## 🛠 Troubleshooting

### AI Analysis Not Working:
1. Check your `.env` file has `GOOGLE_API_KEY`
2. Ensure database is accessible
3. Look for error messages in the expandable "Data Context" section

### No Financial Data:
- The AI will use sample portfolio data for demonstration
- Start the Fi MCP server to collect real financial data
- Sample data includes AAPL, GOOGL, MSFT holdings

### Enhanced Dashboard Issues:
- Runs in "Local Mode" when Google Cloud services aren't configured
- All basic features still work
- Shows warnings for unavailable enhanced features

## 🎯 Next Steps

1. **Test AI Analysis**: Ask "Give me my portfolio" to see the improved AI response
2. **Connect Real Data**: Set up Fi MCP server for actual financial data
3. **Explore Features**: Try different types of questions (risk, portfolio, spending)
4. **Configure Google Cloud**: For full enhanced features (optional)

## 📋 System Status Check

The dashboards will show:
- ✅ Database connectivity
- ✅ Fi MCP server status  
- ✅ AI analysis capability
- ✅ Google Cloud services (Enhanced dashboard only)

Your system is now ready with intelligent AI analysis that actually uses your financial data! 🎉 