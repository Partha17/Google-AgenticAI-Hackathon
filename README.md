# 🤖 Agentic AI Financial Insights System

A comprehensive agentic AI system that collects financial data from MCP (Model Context Protocol) servers, generates intelligent insights using Google's Gemini AI through LangChain, and provides an interactive dashboard for analysis.

## 🚀 Features

- **MCP Server Integration**: Connect to Financial MCP servers (currently with mock data)
- **Periodic Data Collection**: Automated data collection from MCP sources
- **AI-Powered Analysis**: LangChain agents with Gemini AI for intelligent insights
- **Real-time Dashboard**: Interactive Streamlit dashboard for data visualization
- **Dual Database System**: Separate storage for raw MCP data and AI insights
- **Configurable Intervals**: Customizable collection and analysis frequencies

## 📋 Prerequisites

- Python 3.8+
- Google AI API Key (for Gemini)
- SQLite (included with Python)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Google-AgenticAI-Hackathon
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Initialize the database**
   ```bash
   python main.py status
   ```

## 🚀 Quick Start

### Start the Complete System
```bash
python main.py start
```

This starts both data collection and AI insight generation.

### Start Individual Components
```bash
# Start only data collection
python main.py start --no-generator

# Start only insight generation
python main.py start --no-collector
```

### Launch the Dashboard
```bash
# Option 1: Through main script
python main.py dashboard

# Option 2: Direct Streamlit
streamlit run dashboard/app.py
```

### Manual Operations
```bash
# Check system status
python main.py status

# Trigger immediate data collection
python main.py collect

# Generate insights now
python main.py generate
```

## 🏗️ Architecture

```
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