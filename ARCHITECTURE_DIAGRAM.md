# 🏗️ Fi Financial AI Dashboard - Architecture Diagram

## System Overview

```mermaid
graph TB
    %% User Interface Layer
    subgraph "🌐 User Interface Layer"
        UI[Streamlit Dashboard]
        WEB[Web Browser]
        MOBILE[Mobile Browser]
    end

    %% Application Layer
    subgraph "🚀 Application Layer"
        subgraph "📊 Dashboard Components"
            DASH[Streamlit App]
            INSIGHTS[AI Insights Generator]
            PORTFOLIO[Portfolio Analysis]
            STOCKS[Stock Tracker]
            SUBSCRIPTIONS[Subscription Tracker]
            CREDIT[Credit Analysis]
            MCP_AGENT[MCP AI Agent]
            SYSTEM_STATUS[System Status]
        end
        
        subgraph "🤖 AI Agents"
            ADK_ORCH[ADK Orchestrator]
            MARKET_AGENT[Market Analysis Agent]
            RISK_AGENT[Risk Assessment Agent]
            FINANCIAL_AGENT[Financial Data Collector]
            SUBSCRIPTION_AGENT[Subscription Tracking Agent]
            MCP_PERIODIC[MCP Periodic AI Agent]
        end
    end

    %% Services Layer
    subgraph "🔧 Services Layer"
        subgraph "📡 Data Services"
            MCP_CLIENT[Fi MCP Client]
            REAL_DATA[Real Data Collector]
            QUOTA_MGR[Quota Manager]
            LOGGER[Logger Config]
        end
        
        subgraph "🧠 AI Services"
            ENHANCED_AI[Enhanced AI Agent]
            INSIGHT_GEN[Insight Generator]
        end
    end

    %% Data Layer
    subgraph "💾 Data Layer"
        subgraph "🗄️ Database"
            SQLITE[SQLite Database]
            MCP_DATA[(MCP Data)]
            AI_INSIGHTS[(AI Insights)]
            USER_DATA[(User Data)]
        end
        
        subgraph "📁 File Storage"
            LOGS[Log Files]
            CONFIG[Configuration Files]
            STATIC[Static Assets]
        end
    end

    %% External Services
    subgraph "🌍 External Services"
        subgraph "🏦 Financial APIs"
            FI_MCP[Fi MCP Server]
            STOCK_API[Stock Market APIs]
            CREDIT_API[Credit Report APIs]
        end
        
        subgraph "🤖 AI Services"
            GEMINI[Google Gemini AI]
            VERTEX_AI[Google Vertex AI]
            GOOGLE_AI[Google AI Platform]
        end
        
        subgraph "☁️ Google Cloud"
            CLOUD_RUN[Google Cloud Run]
            CLOUD_BUILD[Cloud Build]
            CONTAINER_REG[Container Registry]
            CLOUD_LOGGING[Cloud Logging]
            CLOUD_MONITORING[Cloud Monitoring]
            SECRET_MANAGER[Secret Manager]
            BIGQUERY[BigQuery]
            FIRESTORE[Firestore]
            PUBSUB[Pub/Sub]
            CLOUD_FUNCTIONS[Cloud Functions]
            CLOUD_SCHEDULER[Cloud Scheduler]
        end
    end

    %% Connections - User Interface
    WEB --> UI
    MOBILE --> UI
    UI --> DASH

    %% Connections - Dashboard Components
    DASH --> INSIGHTS
    DASH --> PORTFOLIO
    DASH --> STOCKS
    DASH --> SUBSCRIPTIONS
    DASH --> CREDIT
    DASH --> MCP_AGENT
    DASH --> SYSTEM_STATUS

    %% Connections - AI Agents
    DASH --> ADK_ORCH
    ADK_ORCH --> MARKET_AGENT
    ADK_ORCH --> RISK_AGENT
    ADK_ORCH --> FINANCIAL_AGENT
    ADK_ORCH --> SUBSCRIPTION_AGENT
    ADK_ORCH --> MCP_PERIODIC

    %% Connections - Services
    DASH --> MCP_CLIENT
    DASH --> REAL_DATA
    DASH --> QUOTA_MGR
    DASH --> LOGGER
    DASH --> ENHANCED_AI
    DASH --> INSIGHT_GEN

    %% Connections - Data Layer
    MCP_CLIENT --> SQLITE
    REAL_DATA --> SQLITE
    ENHANCED_AI --> SQLITE
    INSIGHT_GEN --> SQLITE
    LOGGER --> LOGS
    DASH --> CONFIG

    %% Connections - External Services
    MCP_CLIENT --> FI_MCP
    REAL_DATA --> STOCK_API
    REAL_DATA --> CREDIT_API
    ENHANCED_AI --> GEMINI
    ENHANCED_AI --> VERTEX_AI
    ENHANCED_AI --> GOOGLE_AI

    %% Connections - Google Cloud
    DASH --> CLOUD_RUN
    CLOUD_RUN --> CLOUD_BUILD
    CLOUD_BUILD --> CONTAINER_REG
    CLOUD_RUN --> CLOUD_LOGGING
    CLOUD_RUN --> CLOUD_MONITORING
    CLOUD_RUN --> SECRET_MANAGER
    CLOUD_RUN --> BIGQUERY
    CLOUD_RUN --> FIRESTORE
    CLOUD_RUN --> PUBSUB
    CLOUD_RUN --> CLOUD_FUNCTIONS
    CLOUD_RUN --> CLOUD_SCHEDULER

    %% Styling
    classDef userInterface fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef application fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef services fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef data fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef external fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef cloud fill:#e0f2f1,stroke:#004d40,stroke-width:2px

    class UI,WEB,MOBILE userInterface
    class DASH,INSIGHTS,PORTFOLIO,STOCKS,SUBSCRIPTIONS,CREDIT,MCP_AGENT,SYSTEM_STATUS,ADK_ORCH,MARKET_AGENT,RISK_AGENT,FINANCIAL_AGENT,SUBSCRIPTION_AGENT,MCP_PERIODIC application
    class MCP_CLIENT,REAL_DATA,QUOTA_MGR,LOGGER,ENHANCED_AI,INSIGHT_GEN services
    class SQLITE,MCP_DATA,AI_INSIGHTS,USER_DATA,LOGS,CONFIG,STATIC data
    class FI_MCP,STOCK_API,CREDIT_API,GEMINI,VERTEX_AI,GOOGLE_AI external
    class CLOUD_RUN,CLOUD_BUILD,CONTAINER_REG,CLOUD_LOGGING,CLOUD_MONITORING,SECRET_MANAGER,BIGQUERY,FIRESTORE,PUBSUB,CLOUD_FUNCTIONS,CLOUD_SCHEDULER cloud
```

## Deployment Architecture

```mermaid
graph TB
    %% Development Environment
    subgraph "💻 Development Environment"
        DEV[Local Development]
        GIT[Git Repository]
        BRANCHES[Feature Branches]
        MERGE[Branch Merging]
    end

    %% CI/CD Pipeline
    subgraph "🔄 CI/CD Pipeline"
        BUILD[Cloud Build]
        TEST[Automated Testing]
        VERSION[Version Tagging]
        DEPLOY[Deploy to Cloud Run]
    end

    %% Production Environment
    subgraph "🚀 Production Environment"
        subgraph "☁️ Google Cloud Run"
            SERVICE[Fi Financial Dashboard Service]
            REVISIONS[Multiple Revisions]
            TRAFFIC[Traffic Management]
            SCALING[Auto Scaling]
        end
        
        subgraph "📊 Monitoring & Logging"
            LOGS[Cloud Logging]
            METRICS[Cloud Monitoring]
            ALERTS[Alerting]
            DASHBOARDS[Monitoring Dashboards]
        end
    end

    %% Data Flow
    subgraph "📡 Data Flow"
        MCP_SERVER[Fi MCP Server]
        AI_SERVICES[AI Services]
        DATABASE[SQLite Database]
    end

    %% Rollback System
    subgraph "🔄 Rollback System"
        ROLLBACK[Rollback Scripts]
        VERSION_HISTORY[Version History]
        REVISION_MANAGEMENT[Revision Management]
    end

    %% Connections
    DEV --> GIT
    GIT --> BRANCHES
    BRANCHES --> MERGE
    MERGE --> BUILD
    BUILD --> TEST
    TEST --> VERSION
    VERSION --> DEPLOY
    DEPLOY --> SERVICE
    SERVICE --> REVISIONS
    REVISIONS --> TRAFFIC
    TRAFFIC --> SCALING
    
    SERVICE --> LOGS
    SERVICE --> METRICS
    METRICS --> ALERTS
    ALERTS --> DASHBOARDS
    
    SERVICE --> MCP_SERVER
    SERVICE --> AI_SERVICES
    SERVICE --> DATABASE
    
    REVISIONS --> ROLLBACK
    ROLLBACK --> VERSION_HISTORY
    VERSION_HISTORY --> REVISION_MANAGEMENT

    %% Styling
    classDef dev fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef cicd fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef production fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef rollback fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px

    class DEV,GIT,BRANCHES,MERGE dev
    class BUILD,TEST,VERSION,DEPLOY cicd
    class SERVICE,REVISIONS,TRAFFIC,SCALING,LOGS,METRICS,ALERTS,DASHBOARDS production
    class MCP_SERVER,AI_SERVICES,DATABASE data
    class ROLLBACK,VERSION_HISTORY,REVISION_MANAGEMENT rollback
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Dashboard as 📊 Dashboard
    participant MCPClient as 📡 MCP Client
    participant FIServer as 🏦 Fi MCP Server
    participant AIAgent as 🤖 AI Agent
    participant Database as 💾 Database
    participant CloudRun as ☁️ Cloud Run
    participant Monitoring as 📈 Monitoring

    User->>Dashboard: Access Dashboard
    Dashboard->>MCPClient: Request Financial Data
    MCPClient->>FIServer: Fetch Data
    FIServer-->>MCPClient: Return Financial Data
    MCPClient->>Database: Store Data
    MCPClient-->>Dashboard: Return Data
    
    Dashboard->>AIAgent: Request AI Analysis
    AIAgent->>Database: Read Financial Data
    AIAgent->>AIAgent: Generate Insights
    AIAgent->>Database: Store Insights
    AIAgent-->>Dashboard: Return Analysis
    
    Dashboard->>CloudRun: Deploy Updates
    CloudRun->>Monitoring: Report Metrics
    Monitoring-->>CloudRun: Health Status
    
    Dashboard-->>User: Display Results
```

## Component Architecture

```mermaid
graph LR
    %% Core Components
    subgraph "🎯 Core Components"
        MAIN[main_adk.py]
        START[start_system.py]
        CONFIG[config.py]
        LAUNCH[launch_dashboard.py]
    end

    %% Dashboard Components
    subgraph "📊 Dashboard"
        APP[dashboard/app.py]
        STREAMLIT[Streamlit Framework]
        UI_COMPONENTS[UI Components]
    end

    %% Agent System
    subgraph "🤖 Agent System"
        ADK_AGENTS[adk_agents/]
        ORCHESTRATOR[adk_orchestrator.py]
        AGENT_CONFIG[agent_config.py]
        AI_BASE[ai_analysis_base.py]
    end

    %% Services
    subgraph "🔧 Services"
        SERVICES[services/]
        ENHANCED_AI[enhanced_ai_agent.py]
        MCP_CLIENT[fi_mcp_client.py]
        INSIGHT_GEN[insight_generator.py]
        QUOTA_MGR[quota_manager.py]
        REAL_DATA[real_data_collector.py]
    end

    %% Models
    subgraph "🗄️ Models"
        MODELS[models/]
        DATABASE[database.py]
    end

    %% External Services
    subgraph "🌍 External"
        FI_MCP_SERVER[fi-mcp-server/]
        FI_MCP_DEPLOY[fi-mcp-deploy/]
    end

    %% Deployment
    subgraph "🚀 Deployment"
        DEPLOY_SCRIPTS[Deployment Scripts]
        CLOUDBUILD[cloudbuild.yaml]
        DOCKERFILE[Dockerfile]
    end

    %% Connections
    MAIN --> START
    START --> CONFIG
    CONFIG --> LAUNCH
    LAUNCH --> APP
    
    APP --> STREAMLIT
    STREAMLIT --> UI_COMPONENTS
    
    MAIN --> ADK_AGENTS
    ADK_AGENTS --> ORCHESTRATOR
    ORCHESTRATOR --> AGENT_CONFIG
    AGENT_CONFIG --> AI_BASE
    
    APP --> SERVICES
    SERVICES --> ENHANCED_AI
    SERVICES --> MCP_CLIENT
    SERVICES --> INSIGHT_GEN
    SERVICES --> QUOTA_MGR
    SERVICES --> REAL_DATA
    
    SERVICES --> MODELS
    MODELS --> DATABASE
    
    MCP_CLIENT --> FI_MCP_SERVER
    FI_MCP_SERVER --> FI_MCP_DEPLOY
    
    APP --> DEPLOY_SCRIPTS
    DEPLOY_SCRIPTS --> CLOUDBUILD
    CLOUDBUILD --> DOCKERFILE

    %% Styling
    classDef core fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef dashboard fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef agents fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef services fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef models fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef external fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    classDef deployment fill:#f1f8e9,stroke:#33691e,stroke-width:2px

    class MAIN,START,CONFIG,LAUNCH core
    class APP,STREAMLIT,UI_COMPONENTS dashboard
    class ADK_AGENTS,ORCHESTRATOR,AGENT_CONFIG,AI_BASE agents
    class SERVICES,ENHANCED_AI,MCP_CLIENT,INSIGHT_GEN,QUOTA_MGR,REAL_DATA services
    class MODELS,DATABASE models
    class FI_MCP_SERVER,FI_MCP_DEPLOY external
    class DEPLOY_SCRIPTS,CLOUDBUILD,DOCKERFILE deployment
```

## Security Architecture

```mermaid
graph TB
    %% Security Layers
    subgraph "🔒 Security Layers"
        subgraph "🌐 Network Security"
            HTTPS[HTTPS/TLS]
            CORS[CORS Configuration]
            FIREWALL[Cloud Firewall]
        end
        
        subgraph "🔐 Authentication"
            GOOGLE_AUTH[Google OAuth]
            API_KEYS[API Key Management]
            SECRET_MANAGER[Secret Manager]
        end
        
        subgraph "🛡️ Data Security"
            ENCRYPTION[Data Encryption]
            ACCESS_CONTROL[Access Control]
            AUDIT_LOGS[Audit Logging]
        end
    end

    %% Application Security
    subgraph "🚀 Application Security"
        INPUT_VALIDATION[Input Validation]
        SQL_INJECTION[SQL Injection Prevention]
        XSS_PROTECTION[XSS Protection]
        RATE_LIMITING[Rate Limiting]
    end

    %% Cloud Security
    subgraph "☁️ Cloud Security"
        IAM[IAM Roles]
        SERVICE_ACCOUNTS[Service Accounts]
        NETWORK_POLICIES[Network Policies]
        SECURITY_SCANNING[Security Scanning]
    end

    %% Connections
    HTTPS --> CORS
    CORS --> FIREWALL
    GOOGLE_AUTH --> API_KEYS
    API_KEYS --> SECRET_MANAGER
    ENCRYPTION --> ACCESS_CONTROL
    ACCESS_CONTROL --> AUDIT_LOGS
    
    INPUT_VALIDATION --> SQL_INJECTION
    SQL_INJECTION --> XSS_PROTECTION
    XSS_PROTECTION --> RATE_LIMITING
    
    IAM --> SERVICE_ACCOUNTS
    SERVICE_ACCOUNTS --> NETWORK_POLICIES
    NETWORK_POLICIES --> SECURITY_SCANNING

    %% Styling
    classDef network fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef auth fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef data fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef app fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef cloud fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class HTTPS,CORS,FIREWALL network
    class GOOGLE_AUTH,API_KEYS,SECRET_MANAGER auth
    class ENCRYPTION,ACCESS_CONTROL,AUDIT_LOGS data
    class INPUT_VALIDATION,SQL_INJECTION,XSS_PROTECTION,RATE_LIMITING app
    class IAM,SERVICE_ACCOUNTS,NETWORK_POLICIES,SECURITY_SCANNING cloud
```

## Performance Architecture

```mermaid
graph TB
    %% Performance Components
    subgraph "⚡ Performance Optimization"
        subgraph "🚀 Caching"
            MEMORY_CACHE[Memory Cache]
            DISK_CACHE[Disk Cache]
            CDN[CDN Caching]
        end
        
        subgraph "📊 Database Optimization"
            INDEXING[Database Indexing]
            QUERY_OPTIMIZATION[Query Optimization]
            CONNECTION_POOLING[Connection Pooling]
        end
        
        subgraph "🔄 Load Balancing"
            AUTO_SCALING[Auto Scaling]
            TRAFFIC_DISTRIBUTION[Traffic Distribution]
            HEALTH_CHECKS[Health Checks]
        end
    end

    %% Monitoring
    subgraph "📈 Performance Monitoring"
        METRICS[Performance Metrics]
        ALERTS[Performance Alerts]
        DASHBOARDS[Performance Dashboards]
        LOGGING[Performance Logging]
    end

    %% Optimization
    subgraph "🔧 Optimization Strategies"
        LAZY_LOADING[Lazy Loading]
        COMPRESSION[Data Compression]
        MINIFICATION[Code Minification]
        IMAGE_OPTIMIZATION[Image Optimization]
    end

    %% Connections
    MEMORY_CACHE --> DISK_CACHE
    DISK_CACHE --> CDN
    INDEXING --> QUERY_OPTIMIZATION
    QUERY_OPTIMIZATION --> CONNECTION_POOLING
    AUTO_SCALING --> TRAFFIC_DISTRIBUTION
    TRAFFIC_DISTRIBUTION --> HEALTH_CHECKS
    
    METRICS --> ALERTS
    ALERTS --> DASHBOARDS
    DASHBOARDS --> LOGGING
    
    LAZY_LOADING --> COMPRESSION
    COMPRESSION --> MINIFICATION
    MINIFICATION --> IMAGE_OPTIMIZATION

    %% Styling
    classDef caching fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef database fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef loadbalancing fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef monitoring fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef optimization fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class MEMORY_CACHE,DISK_CACHE,CDN caching
    class INDEXING,QUERY_OPTIMIZATION,CONNECTION_POOLING database
    class AUTO_SCALING,TRAFFIC_DISTRIBUTION,HEALTH_CHECKS loadbalancing
    class METRICS,ALERTS,DASHBOARDS,LOGGING monitoring
    class LAZY_LOADING,COMPRESSION,MINIFICATION,IMAGE_OPTIMIZATION optimization
```

## Technology Stack

```mermaid
graph TB
    %% Frontend
    subgraph "🎨 Frontend"
        STREAMLIT[Streamlit]
        PLOTLY[Plotly]
        PANDAS[Pandas]
        NUMPY[NumPy]
    end

    %% Backend
    subgraph "⚙️ Backend"
        PYTHON[Python 3.11]
        FASTAPI[FastAPI]
        UVICORN[Uvicorn]
        SQLALCHEMY[SQLAlchemy]
    end

    %% AI/ML
    subgraph "🤖 AI/ML"
        LANGCHAIN[LangChain]
        GEMINI[Google Gemini]
        VERTEX_AI[Vertex AI]
        GOOGLE_GENAI[Google Generative AI]
    end

    %% Cloud Services
    subgraph "☁️ Google Cloud"
        CLOUD_RUN[Cloud Run]
        CLOUD_BUILD[Cloud Build]
        CONTAINER_REG[Container Registry]
        CLOUD_LOGGING[Cloud Logging]
        CLOUD_MONITORING[Cloud Monitoring]
        SECRET_MANAGER[Secret Manager]
        BIGQUERY[BigQuery]
        FIRESTORE[Firestore]
        PUBSUB[Pub/Sub]
        CLOUD_FUNCTIONS[Cloud Functions]
        CLOUD_SCHEDULER[Cloud Scheduler]
    end

    %% External APIs
    subgraph "🌍 External APIs"
        FI_MCP[Fi MCP Server]
        STOCK_APIS[Stock Market APIs]
        CREDIT_APIS[Credit Report APIs]
        ALPHA_VANTAGE[Alpha Vantage]
        FINNHUB[Finnhub]
    end

    %% Database
    subgraph "🗄️ Database"
        SQLITE[SQLite]
        GOOGLE_SHEETS[Google Sheets]
        CSV[CSV Files]
    end

    %% DevOps
    subgraph "🛠️ DevOps"
        DOCKER[Docker]
        GIT[Git]
        BASH[Bash Scripts]
        YAML[YAML Configs]
    end

    %% Connections
    STREAMLIT --> PLOTLY
    PLOTLY --> PANDAS
    PANDAS --> NUMPY
    
    PYTHON --> FASTAPI
    FASTAPI --> UVICORN
    UVICORN --> SQLALCHEMY
    
    LANGCHAIN --> GEMINI
    GEMINI --> VERTEX_AI
    VERTEX_AI --> GOOGLE_GENAI
    
    CLOUD_RUN --> CLOUD_BUILD
    CLOUD_BUILD --> CONTAINER_REG
    CLOUD_RUN --> CLOUD_LOGGING
    CLOUD_RUN --> CLOUD_MONITORING
    CLOUD_RUN --> SECRET_MANAGER
    CLOUD_RUN --> BIGQUERY
    CLOUD_RUN --> FIRESTORE
    CLOUD_RUN --> PUBSUB
    CLOUD_RUN --> CLOUD_FUNCTIONS
    CLOUD_RUN --> CLOUD_SCHEDULER
    
    FI_MCP --> STOCK_APIS
    STOCK_APIS --> CREDIT_APIS
    CREDIT_APIS --> ALPHA_VANTAGE
    ALPHA_VANTAGE --> FINNHUB
    
    SQLITE --> GOOGLE_SHEETS
    GOOGLE_SHEETS --> CSV
    
    DOCKER --> GIT
    GIT --> BASH
    BASH --> YAML

    %% Styling
    classDef frontend fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef ai fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef cloud fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef external fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef database fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    classDef devops fill:#f1f8e9,stroke:#33691e,stroke-width:2px

    class STREAMLIT,PLOTLY,PANDAS,NUMPY frontend
    class PYTHON,FASTAPI,UVICORN,SQLALCHEMY backend
    class LANGCHAIN,GEMINI,VERTEX_AI,GOOGLE_GENAI ai
    class CLOUD_RUN,CLOUD_BUILD,CONTAINER_REG,CLOUD_LOGGING,CLOUD_MONITORING,SECRET_MANAGER,BIGQUERY,FIRESTORE,PUBSUB,CLOUD_FUNCTIONS,CLOUD_SCHEDULER cloud
    class FI_MCP,STOCK_APIS,CREDIT_APIS,ALPHA_VANTAGE,FINNHUB external
    class SQLITE,GOOGLE_SHEETS,CSV database
    class DOCKER,GIT,BASH,YAML devops
```

## Key Features

- **🎯 Multi-Agent System**: Orchestrated AI agents for different financial analysis tasks
- **📊 Real-time Dashboard**: Streamlit-based interactive financial dashboard
- **🤖 AI-Powered Insights**: Google Gemini and Vertex AI integration
- **🔄 Versioned Deployment**: Full rollback capability with Cloud Run revisions
- **📡 MCP Integration**: Fi MCP server for real financial data
- **☁️ Cloud-Native**: Built on Google Cloud Platform with auto-scaling
- **🔒 Secure**: OAuth authentication, API key management, and data encryption
- **📈 Monitored**: Comprehensive logging and monitoring
- **🚀 CI/CD**: Automated deployment pipeline with testing
- **💾 Data Persistence**: SQLite database with backup capabilities 