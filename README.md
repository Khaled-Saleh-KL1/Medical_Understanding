# Medical Understanding AI Assistant 🏥🤖🧠

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain)](https://langchain-ai.github.io/langgraph/)

## Overview

The **Medical Understanding AI Assistant** is a comprehensive, multilingual AI-powered healthcare consultation system that combines cutting-edge artificial intelligence with specialized medical knowledge. Built using Google's Gemini AI and LangGraph framework, this system provides intelligent medical consultations, AI research assistance, and general knowledge support in both Arabic and English.

This sophisticated system features a multi-agent architecture with specialized expert agents, conversation memory persistence via PostgreSQL, real-time web search capabilities, and emergency situation detection. It offers three distinct interfaces: a command-line interface, a REST API, and a modern web GUI built with Streamlit.

## 🌟 Key Features

### Core Capabilities
- **🩺 Advanced Medical Consultation**: Professional-grade medical advice with specialist knowledge
- **🔬 AI Research Expertise**: Cutting-edge artificial intelligence and machine learning guidance
- **🌍 Multilingual Support**: Native support for Arabic and English with cultural sensitivity
- **📡 Real-time Information**: Live web search integration for current medical research and data
- **🚨 Emergency Detection**: Automatic identification and escalation protocols for urgent medical situations
- **💾 Persistent Memory**: PostgreSQL-based conversation history and context retention
- **🧠 Multi-Agent Architecture**: Specialized expert agents for different domains

### User Interfaces
- **💻 Command Line Interface**: Direct terminal-based interaction for developers
- **🌐 REST API**: FastAPI-based endpoints for integration with external systems
- **📱 Web GUI**: Modern Streamlit interface with chat functionality and session management

### Technical Excellence
- **⚡ Stream Processing**: Real-time response streaming with LangGraph
- **🛡️ Robust Error Handling**: Comprehensive error management and graceful fallbacks
- **📊 Graph Visualization**: Visual representation of agent workflows and decision trees
- **🔐 Security**: Environment-based API key management and secure data handling
- **🐳 Containerization**: Docker support for easy deployment and scaling

## 🏗️ Project Architecture

```
Medical_Understanding/
├── api/                    # FastAPI REST API
│   ├── main.py            # API entry point
│   ├── helpers/           # Detection & health checks
│   ├── models/            # Request/response schemas
│   ├── routes/            # API endpoints
│   └── log/               # API logs
│
├── gui/                   # Streamlit Web Interface
│   ├── streamlit_app.py   # Main web app
│   ├── requirements.txt   # GUI dependencies
│   └── log/               # GUI logs
│
├── src/                   # Core AI System
│   ├── Run_Chatbot.py     # CLI interface
│   ├── StateGraph.py      # LangGraph workflow
│   │
│   ├── AgentExpert/       # Specialized AI Agents
│   │   ├── doctor.py      # Medical specialist
│   │   ├── arabic_doctor.py
│   │   ├── ai_researcher.py
│   │   ├── arabic_ai_researcher.py
│   │   └── general_expert.py
│   │
│   ├── tools/             # Agent Tools
│   │   ├── ConsultDoctor.py
│   │   ├── ConsultArabicDoctor.py
│   │   ├── WebSearch.py
│   │   ├── MultilingualSupport.py
│   │   └── HumanAssistant.py
│   │
│   ├── nodes/             # LangGraph Components
│   │   ├── LLM.py         # Language model config
│   │   ├── ToolNode.py    # Tool execution
│   │   └── visualize_graph.py
│   │
│   ├── models/            # Database & Models
│   │   ├── connect_database.py
│   │   ├── inspect_conversations.py
│   │   └── quick_check.py
│   │
│   └── assets/            # Generated files
│       └── visualize/     # Graph visualizations
│
├── Docker/                # Containerization
│   ├── docker-compose.yml
│   └── dockerfile
│
├── requirements.txt       # Python dependencies
├── LICENSE               # MIT license
└── README.md             # This file
```

## 🤖 Multi-Agent Expert System

The system employs a sophisticated multi-agent architecture where specialized AI experts handle different domains:

### Medical Experts
- **🩺 English Medical Doctor**: Comprehensive medical knowledge with Western medical practices
- **🩺 Arabic Medical Doctor**: Arabic medical expertise with cultural considerations and Islamic medical ethics

### Research Experts  
- **🔬 AI Research Specialist**: Cutting-edge AI/ML research, latest developments, technical implementation
- **🔬 Arabic AI Research Specialist**: AI research expertise in Arabic with localized technical terminology

### Support Experts
- **🧠 General Knowledge Expert**: Broad academic knowledge across multiple disciplines
- **🌐 Multilingual Support Agent**: Language detection, cultural adaptation, and translation services
- **🔍 Web Search Agent**: Real-time information retrieval from trusted sources
- **👨‍💼 Human Assistant**: Escalation to human support for complex situations

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database (optional, falls back to memory storage)
- Google Gemini API key
- Tavily Search API key (optional, for web search)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Khaled-Saleh-KL1/Medical_Understanding.git
cd Medical_Understanding

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# Required: Google Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: PostgreSQL Database for Conversation Memory
DATABASE_URL=postgresql://username:password@localhost:5432/my_agent_db

# Optional: Tavily Search API for Real-time Web Search
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Database Setup (Optional)

If using PostgreSQL for conversation persistence:

```sql
-- Create database
CREATE DATABASE my_db_agent;

-- The application will automatically create the required tables
```

### 4. Launch Options

#### Option A: Command Line Interface
```bash
cd src
python Run_Chatbot.py
```

#### Option B: Web GUI (Recommended)
```bash
cd gui
streamlit run streamlit_app.py
```

#### Option C: REST API
```bash
cd api
fastapi dev main.py
```

#### Option D: Docker Deployment
```bash
cd Docker
Run the docker compose file
then go to localhost:8501 on web
```

## 💻 Usage Examples

### Command Line Interface

```bash
$ python src/Run_Chatbot.py

🤖 LangGraph Chatbot
Session ID: abc123de-f456-7890-abcd-ef1234567890
This conversation will be stored in PostgreSQL for memory persistence.
Type 'quit', 'exit', or 'q' to end the conversation.
Type 'new' to start a new conversation thread.

================================ Human Message =================================
User: I have chest pain and difficulty breathing
================================== Ai Message ==================================
🚨 EMERGENCY SITUATION DETECTED 🚨

Based on your symptoms (chest pain and difficulty breathing), this could indicate a serious medical emergency such as:
- Heart attack
- Pulmonary embolism  
- Severe allergic reaction

**IMMEDIATE ACTION REQUIRED:**
1. Call 911 (or your local emergency number) immediately
2. If you have aspirin and no allergies, chew one 325mg tablet
3. Sit upright and try to stay calm
4. Do not drive yourself to the hospital

This is not a time for self-diagnosis. Please seek emergency medical care immediately.
```

### Web GUI Interface

The Streamlit interface provides:
- **Chat Interface**: Modern chat UI with message history
- **Session Management**: Create new conversations or continue existing ones
- **Emergency Detection**: Visual alerts for emergency situations  
- **Language Selection**: Automatic language detection or manual selection
- **Connection Modes**: Direct integration or API connection
- **Export Options**: Download conversation history

### REST API Usage

```bash
# Start a chat conversation
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of diabetes?",
    "session_id": "user123",
    "language": "en"
  }'

# Response
{
  "status": "success",
  "message": "Diabetes symptoms include frequent urination, excessive thirst, unexplained weight loss, fatigue, blurred vision, and slow-healing wounds. If you experience these symptoms, consult a healthcare provider for proper testing and diagnosis.",
  "session_id": "user123",
  "timestamp": "2025-08-25T10:30:00",
  "expert_used": "medical_doctor",
  "language_detected": "english",
  "is_emergency": false,
  "response_time_ms": 1250
}

# Check system health
curl -X GET "http://localhost:8000/health"
```

## 🌐 Multilingual Capabilities

### Arabic Language Support

The system provides comprehensive Arabic language support:

```bash
User: أشعر بألم في الصدر وصعوبة في التنفس
AI Response: 
🚨 حالة طوارئ محتملة 🚨

بناءً على الأعراض التي وصفتها (ألم في الصدر وصعوبة في التنفس), قد تشير هذه الأعراض إلى حالة طبية طارئة مثل:
- النوبة القلبية  
- الانسداد الرئوي
- رد فعل تحسسي شديد

**إجراء فوري مطلوب:**
١. اتصل بالطوارئ (٩٩٧ أو الرقم المحلي للطوارئ) فوراً
٢. إذا كان لديك أسبرين ولا تعاني من حساسية، امضغ قرص ٣٢٥ ملغ
٣. اجلس بوضعية منتصبة وحاول أن تبقى هادئاً
٤. لا تقد السيارة بنفسك إلى المستشفى

هذا ليس وقت التشخيص الذاتي. يرجى طلب الرعاية الطبية الطارئة فوراً.
```

### Cultural Sensitivity Features

- **Islamic Medical Ethics**: Consideration of Islamic principles in medical advice
- **Cultural Context**: Culturally appropriate responses for Arabic-speaking users
- **Regional Awareness**: Adaptation to different Arabic dialects and regional practices
- **Religious Considerations**: Respectful handling of religious beliefs in medical contexts

### Custom Agent Configuration

You can extend the system with custom expert agents:

```python
# src/AgentExpert/custom_expert.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import datetime

class CustomExpertAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.5
        )
        self.system_prompt = self._get_custom_prompt()
    
    def _get_custom_prompt(self):
        return """
        You are a specialized expert in [YOUR_DOMAIN].
        Provide accurate, helpful responses in your area of expertise.
        """
    
    def get_response(self, user_input: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_input)
        ]
        response = self.llm.invoke(messages)
        return response.content
```

## 📊 Monitoring and Analytics

### Health Monitoring

The system includes comprehensive health monitoring:

```bash
# Check overall system health
GET /health

# Response
{
  "status": "healthy",
  "timestamp": "2025-08-25T10:30:00Z",
  "services": {
    "database": "connected",
    "gemini_api": "available", 
    "web_search": "available",
    "memory": "optimal"
  },
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

### Conversation Analytics

Monitor conversation patterns and expert usage:

```python
# src/models/inspect_conversations.py provides tools for:
# - Conversation length analysis
# - Expert utilization metrics  
# - Language distribution statistics
# - Emergency detection frequency
# - Response time analytics
```

### Logging

Comprehensive logging across all components:

```bash
# View logs
tail -f src/log/errors.log        # Core system logs
tail -f api/log/errors.log        # API-specific logs  
tail -f gui/log/errors.log        # GUI-specific logs
tail -f src/nodes/log/errors.log  # Node execution logs
```

## 🚨 Emergency Detection System

The system includes sophisticated emergency detection capabilities:

### Automatic Detection

Emergency keywords and patterns are automatically detected:
- Medical emergencies: "chest pain", "difficulty breathing", "severe bleeding"
- Mental health crises: "suicide", "self-harm", "overdose"  
- Urgent situations: "emergency", "urgent", "critical"

### Emergency Response Protocol

When an emergency is detected:

1. **Immediate Alert**: Visual and textual emergency warnings
2. **Priority Response**: Emergency protocols take precedence over normal conversation flow
3. **Clear Instructions**: Step-by-step guidance for immediate action
4. **Resource Information**: Emergency contact numbers and procedures
5. **Human Escalation**: Automatic escalation to human assistance when configured

### Cultural Emergency Support

- **Arabic Emergency Numbers**: Country-specific emergency contacts for Arabic users
- **Religious Considerations**: Appropriate spiritual support suggestions when relevant
- **Cultural Sensitivity**: Emergency advice adapted to cultural contexts

### Medical Disclaimer
The system includes comprehensive medical disclaimers and emphasizes that AI assistance does not replace professional medical care.

## 📚 API Documentation

### REST API Endpoints

#### Chat Endpoints
```bash
POST /chat/                    # Send a message to the AI assistant
GET  /chat/history/{session}   # Get conversation history
DELETE /chat/session/{session} # Clear session history
```

#### Health Endpoints
```bash
GET /health                    # Overall system health
GET /health/database          # Database connectivity
GET /health/services          # External service status
```

#### Admin Endpoints (if enabled)
```bash
GET /admin/stats              # Usage statistics
GET /admin/sessions           # Active sessions
POST /admin/maintenance       # Maintenance mode toggle
```

## 🎯 Use Cases

### Healthcare Professionals
- **Quick Consultations**: Rapid medical information lookup
- **Patient Education**: Generate explanations for medical conditions
- **Research Support**: Latest medical research and guidelines
- **Multilingual Support**: Communicate with Arabic-speaking patients

### Medical Students
- **Study Assistance**: Comprehensive medical knowledge database
- **Case Studies**: Interactive medical scenario analysis
- **Exam Preparation**: Practice questions and explanations
- **Research Guidance**: AI/ML applications in healthcare

### General Public
- **Health Education**: Reliable medical information and guidance
- **Symptom Assessment**: Preliminary symptom evaluation
- **Emergency Guidance**: Critical situation management
- **Preventive Care**: Health maintenance and wellness advice

### Researchers and Developers
- **AI Research**: Latest developments in artificial intelligence
- **Implementation Guidance**: Technical implementation support
- **Academic Support**: Research methodology and best practices
- **Technology Integration**: AI integration strategies

### Contact Information
- **Project Lead**: [Khaled Saleh](https://github.com/Khaled-Saleh-KL1)
- **Email**: khaledsalehkl1@gmail.com

## 🙏 Acknowledgments

### Technologies
- **Google Gemini AI**: Powerful language model capabilities
- **LangGraph**: Sophisticated agent workflow framework  
- **FastAPI**: High-performance API framework
- **Streamlit**: Intuitive web interface framework
- **PostgreSQL**: Reliable conversation persistence
- **Tavily Search**: Real-time web search integration

### Inspiration
This project was inspired by the need for accessible, multilingual medical information and the potential for AI to democratize healthcare knowledge while maintaining the highest standards of medical ethics and cultural sensitivity.

---

**Disclaimer**: This AI assistant is designed to provide educational information and preliminary guidance only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions you may have regarding medical conditions or treatments. In case of emergency, contact your local emergency services immediately.