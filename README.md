# 🤖 Agentic AI Financial Insights System

A comprehensive financial analysis system that integrates with **Fi MCP (Model Context Protocol)** to collect real financial data and generate AI-powered insights using Google Gemini AI with advanced prompt engineering.

## 🌟 Key Features

### 💰 Real Financial Data Integration
- **Fi MCP Server Integration**: Connects to real financial data sources
- **Net Worth Analysis**: Complete asset and liability breakdown
- **Bank Transactions**: Transaction history and spending patterns
- **EPF Details**: Employee Provident Fund balance and insights
- **Credit Reports**: Credit score monitoring and improvement tips

### 🧠 Enhanced AI Analysis
- **Advanced AI Agent**: Institutional-grade financial analysis using enhanced prompt engineering
- **Google Gemini 2.0**: Latest AI model for sophisticated financial insights
- **Chain-of-Thought Reasoning**: Transparent, logical financial analysis
- **Risk Assessment**: Comprehensive portfolio risk evaluation
- **Opportunity Identification**: Investment and financial opportunities

### 📊 Data-Specific Dashboard
- **Net Worth Panel**: Asset/liability visualization and breakdown
- **Bank Transactions Panel**: Transaction analysis and spending insights
- **EPF Panel**: Provident fund tracking and projections
- **Credit Report Panel**: Credit score monitoring with improvement tips
- **AI Insights Panel**: Generated financial recommendations and analysis

## 🏗️ System Architecture

```
Fi MCP Server (Go) → Real Data Collector (Python) → Enhanced AI Agent (LangChain + Gemini) → Insights Dashboard (Streamlit)
                                     ↓
                            SQLite Database (Financial Data + AI Insights)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Go 1.23+** (for Fi MCP server)
- **Google Gemini API Key**

### 1. Setup Fi MCP Server

```bash
# Clone and setup Fi MCP server
mkdir fi-mcp-server && cd fi-mcp-server
git clone https://github.com/epiFi/fi-mcp-dev.git .
go mod tidy

# Start Fi MCP server
FI_MCP_PORT=8080 go run . &
cd ..
```

### 2. Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Setup environment variables
cp .env.example .env

# Edit .env file:
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./agentic_ai.db
MCP_SERVER_URL=http://localhost:8080
LOG_LEVEL=INFO
COLLECTION_INTERVAL_MINUTES=5
INSIGHTS_GENERATION_INTERVAL_MINUTES=15
```

### 4. Run the System

```bash
# Test Fi MCP connection
python3 main.py test

# Start data collection and AI analysis
python3 main.py start

# Launch dashboard
python3 main.py dashboard
```

## 📋 Available Commands

```bash
# System operations
python3 main.py start          # Start data collection and AI analysis
python3 main.py status         # Check system status
python3 main.py collect        # Collect data immediately
python3 main.py generate       # Generate insights immediately
python3 main.py test           # Test Fi MCP server connection
python3 main.py dashboard      # Launch Streamlit dashboard

# Options
--no-collector                 # Start without data collector
--no-generator                 # Start without insight generator
```

## 💾 Database Schema

### MCP Data Table
- **Real Financial Data**: Net worth, transactions, EPF, credit reports
- **Timestamps**: Data collection timeline
- **Processing Status**: Track AI analysis progress

### AI Insights Table
- **Enhanced Insights**: Institutional-grade financial analysis
- **Confidence Scores**: AI certainty in recommendations
- **Metadata**: Key factors, recommendations, reasoning chains

## 🎯 Dashboard Features

### 📈 Overview Panel
- Financial summary metrics (Net Worth, Credit Score, EPF Balance)
- Data collection status
- Recent AI insights preview

### 💰 Net Worth Panel
- Total net worth calculation
- Asset distribution pie charts
- Liability breakdown
- Investment portfolio visualization

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Server    │───▶│  Data Collector  │───▶│   Database      │
│   (Fi MCP)      │    │  Service         │    │   (MCP Data)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Dashboard     │◀───│   AI Agent       │◀───│   Unprocessed   │
│   (Streamlit)   │    │   (LangChain +   │    │   Data          │
└─────────────────┘    │    Gemini)       │    └─────────────────┘
        ▲              └──────────────────┘
        │                       │
        │                       ▼
        │              ┌─────────────────┐
        └──────────────│   Database      │
                       │   (AI Insights) │
                       └─────────────────┘
```

## 📁 Project Structure

```
├── main.py                    # Main entry point
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── models/
│   └── database.py           # SQLAlchemy models
├── services/
│   ├── mcp_mock.py          # Mock MCP data generator
│   ├── data_collector.py    # Data collection service
│   ├── ai_agent.py          # LangChain AI agent
│   └── insight_generator.py # Insight generation orchestrator
└── dashboard/
    └── app.py               # Streamlit dashboard
```

## 🔧 Configuration

Key configuration options in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini AI API key | Required |
| `DATABASE_URL` | SQLite database path | `sqlite:///./agentic_ai.db` |
| `COLLECTION_INTERVAL_MINUTES` | Data collection frequency | `5` |
| `INSIGHTS_GENERATION_INTERVAL_MINUTES` | AI analysis frequency | `15` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🧠 AI Insights Types

The system generates four types of AI insights:

1. **Trend Analysis** - Market trends and patterns
2. **Risk Assessment** - Risk factors and mitigation strategies  
3. **Opportunity Identification** - Investment opportunities
4. **Market Sentiment** - Overall market sentiment analysis

## 📊 Dashboard Features

### Overview Tab
- System metrics and KPIs
- Insights distribution by type
- Confidence score analytics

### AI Insights Tab
- Recent insights with confidence scores
- Key factors and recommendations
- Expandable insight details

### Data Analysis Tab
- Raw data visualization
- Collection timeline
- Stock price trends (when available)

### System Status Tab
- Database statistics
- System configuration
- Manual control buttons
- Data export functionality

## 🔌 MCP Server Integration

Currently using mock data. To connect to a real Fi MCP server:

1. Update `MCP_SERVER_URL` in `.env`
2. Modify `services/data_collector.py` to use actual MCP client
3. Replace mock data calls with real MCP API calls

## 🛡️ Error Handling

- Graceful database error handling
- AI generation fallbacks
- Service restart capabilities
- Comprehensive logging

## 📈 Monitoring

Check logs in `agentic_ai.log` or use:

```bash
tail -f agentic_ai.log
```

## 🔄 Development

### Adding New Data Types
1. Extend `MockMCPService` in `services/mcp_mock.py`
2. Update AI prompts in `services/ai_agent.py`
3. Add visualization in `dashboard/app.py`

### Customizing AI Analysis
- Modify prompts in `AIInsightAgent` class
- Adjust batch sizes and intervals
- Add new insight types

## 🐛 Troubleshooting

### Common Issues

1. **Missing Google API Key**
   ```
   Error: Google API key is required
   ```
   Solution: Set `GOOGLE_API_KEY` in `.env`

2. **Database Connection Issues**
   ```
   Error: no such table
   ```
   Solution: Run `python main.py status` to initialize

3. **Port Already in Use (Dashboard)**
   ```
   Error: Port 8501 is already in use
   ```
   Solution: Kill existing Streamlit processes or use different port

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language understanding
- LangChain for AI agent framework
- Streamlit for rapid dashboard development
- SQLAlchemy for robust database ORM 