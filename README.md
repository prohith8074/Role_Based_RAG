# 🚀 Role-Based RAG Assistant

**Enterprise-Grade Retrieval-Augmented Generation System with Advanced Conversation Memory**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/langgraph-0.0.55-green.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A sophisticated AI assistant system that provides personalized responses based on organizational roles, leveraging multiple vector databases and advanced conversation memory management.**

## 🎯 Overview

The Role-Based RAG Assistant is a production-ready system designed for enterprise environments, particularly FinTech companies. It implements intelligent role-based access control, ensuring users receive contextually appropriate responses based on their organizational position while maintaining conversation continuity across sessions.

### 🔑 Key Features

- **🔐 Role-Based Access Control**: 6 distinct user roles with tailored data access
- **🧠 Multi-Vector Database Architecture**: Milvus, Qdrant, and Pinecone integration
- **⚡ Advanced AI Model Routing**: Role-specific AI models for optimized responses
- **💬 Persistent Conversation Memory**: Context-aware multi-turn conversations
- **📊 Quality Evaluation**: Automated response assessment with Opik and Groq
- **🔄 LangGraph Workflow**: Sophisticated state management and routing

## 🏗️ System Architecture

### AI Model Assignments by Role

| Role | Vector Database | AI Model | Evaluation System |
|------|----------------|----------|-------------------|
| **Finance & C-Level** | Pinecone | GPT-4o | Direct Processing |
| **Employee & Engineering** | Milvus | Gemini 2.5 Flash | Opik + Groq/Llama3-70b-8192 |
| **HR & Marketing** | Qdrant | Cohere Command-R | Opik + Groq/Llama3-70b-8192 |

### Architecture Diagram

![langgraph_workflow_diagram](https://github.com/user-attachments/assets/20fc8e1b-1f5f-4a8d-98dc-58d62b087e16)



## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Required API keys (see [Environment Setup](#environment-setup))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/role-based-rag-assistant.git
   cd role-based-rag-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Initialize database**
   ```bash
   python -c "from database import init_database; init_database()"
   ```

5. **Run the application**
   ```bash
   streamlit run main.py --server.port 5000
   ```

## 🔧 Environment Setup

### Required API Keys

Create a `.env` file with the following configurations:

```env
# AI Models
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Vector Databases
## Milvus (Employee & Engineering)
MILVUS_CLIENT_EMPLOYEE_URI=your_milvus_employee_uri
MILVUS_CLIENT_EMPLOYEE_TOKEN=your_milvus_employee_token
MILVUS_COHERE_API=your_milvus_cohere_api_key

## Qdrant (HR & Marketing)
QDRANT_CLIENT_HR_URL=your_qdrant_hr_url
QDRANT_CLIENT_HR_API_KEY=your_qdrant_hr_api_key
QDRANT_CLIENT_MARKETING_URL=your_qdrant_marketing_url
QDRANT_CLIENT_MARKETING_API_KEY=your_qdrant_marketing_api_key

## Pinecone (Finance & C-Level)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# Evaluation & Monitoring
OPIK_API_KEY=your_opik_api_key_here
```

### API Key Sources

- **OpenAI**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Gemini**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Cohere**: [Cohere Dashboard](https://dashboard.cohere.ai/api-keys)
- **Groq**: [Groq Console](https://console.groq.com/keys)
- **Milvus**: [Zilliz Cloud](https://cloud.zilliz.com/)
- **Qdrant**: [Qdrant Cloud](https://cloud.qdrant.io/)
- **Pinecone**: [Pinecone Console](https://app.pinecone.io/)
- **Opik**: [Opik Platform](https://www.comet.com/site/products/opik/)

## 👥 Demo Users

The system comes with pre-configured demo users for testing:

| Role | Email | Password | Access Level |
|------|-------|----------|--------------|
| Employee | alice@company.com | password123 | Basic company information |
| Engineering | bob@company.com | password123 | Technical documentation |
| HR | charlie@company.com | password123 | HR policies & procedures |
| Finance | diana@company.com | password123 | Financial reports & analytics |
| Marketing | eve@company.com | password123 | Marketing materials & campaigns |
| C-Level | frank@company.com | password123 | Executive insights & all data |


## 🛠️ Core Components

### 1. LangGraph Workflow Engine
- **State Management**: TypedDict-based conversation tracking
- **Role Routing**: Intelligent assistant selection based on user roles
- **Memory Integration**: Persistent context across sessions
- **Error Handling**: Graceful fallback mechanisms

### 2. RAG Assistants
Each role has a dedicated assistant with:
- **Specialized Vector Search**: Role-appropriate database querying
- **Custom AI Models**: Optimized for specific use cases
- **Context Processing**: Domain-specific response generation
- **Quality Evaluation**: Automated response assessment

### 3. Conversation Memory System
- **Context Preservation**: Maintains conversation history
- **Smart Compression**: Summarizes long conversations
- **Session Management**: User-specific memory isolation
- **Buffer Management**: Efficient memory usage

### 4. Authentication & Security
- **Role-Based Access**: Secure user authentication
- **Data Isolation**: Department-level access controls
- **Session Management**: Secure state handling
- **Password Encryption**: Bcrypt-based security

*FinSolve Technologies - Empowering Financial Innovation through AI*
