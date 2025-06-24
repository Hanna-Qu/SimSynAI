# SimSynAI - AI-Powered Intelligent Simulation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/Hanna-Qu/SimSynAI/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Hanna-Qu/SimSynAI/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/Hanna-Qu/SimSynAI/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

SimSynAI is an intelligent simulation platform that integrates multiple large language models, supporting intelligent dialogue, simulation modeling, data visualization, and other functions.

## ✨ Key Features

- 🧠 **Multi-LLM Integration** - Support for OpenAI, Claude, Gemini, Qwen, DeepSeek, and more
- 🔐 **Secure User System** - JWT authentication, encrypted API key storage
- 💬 **Intelligent Dialogue** - Real-time AI conversations, chat history management
- 🧪 **Simulation Experiments** - Visual modeling, parameter configuration, result analysis
- 📊 **Data Visualization** - Multiple chart types, interactive displays
- 🌐 **Internationalization** - Bilingual interface (Chinese/English)
- 📱 **Responsive Design** - Perfect adaptation for desktop and mobile devices
- 🐳 **Containerized Deployment** - Ready-to-use Docker solution

## 🚀 Quick Start

### Requirements
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for production deployment)
- Git

### Method 1: Docker Containerized Deployment (Recommended for Production)

```bash
# 1. Clone the project
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. Start all services
docker compose up -d

# 3. Wait for services to start (about 1-2 minutes)
docker compose ps

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/api/v1/docs
```

### Method 2: Local Development Environment (Recommended for Development)

Use conda virtual environment for local development to get a better development experience:

#### Quick Start
```bash
# 1. Clone the project
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. Initialize development environment (first run)
# Windows
.\scripts\dev-start.ps1 init

# Linux/macOS
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh init

# 3. Start development services
# Windows
.\scripts\dev-start.ps1 full

# Linux/macOS  
./scripts/dev-start.sh full
```

#### Start Services Separately
```bash
# Start backend service
./scripts/dev-start.sh backend   # or .\scripts\dev-start.ps1 backend

# Start frontend service (new terminal)
./scripts/dev-start.sh frontend  # or .\scripts\dev-start.ps1 frontend
```

#### Manual Environment Configuration
If you prefer manual control, please refer to the [Local Development Environment Setup Guide](docs/development-setup.md)

### Default Accounts
- **Administrator**: `admin` / `admin123`
- **Test User**: `demo` / `demo123`

### Access URLs
- Frontend Application: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs
- Redis: localhost:6379 (Docker mode only)

## Tech Stack

### Frontend
- React 18 + TypeScript
- Ant Design UI Component Library
- React Router v6 Route Management
- Axios HTTP Client
- ECharts Data Visualization
- i18next Internationalization

### Backend
- Python 3.11 + FastAPI
- SQLAlchemy ORM
- SQLite Database
- Multi-LLM Integration (OpenAI, Claude, Gemini, Qwen, DeepSeek)
- Redis Cache

### Deployment
- Docker + Docker Compose
- Nginx Reverse Proxy

## Project Structure

```
SimSynAI/
├── frontend/          # React frontend application
│  ├── src/
│  │  ├── components/    # React components
│  │  ├── locales/       # Internationalization files
│  │  └── styles/        # Style files
│  └── public/            # Static resources
├── backend/           # FastAPI backend
│  ├── app/
│  │  ├── api/           # API routes
│  │  ├── core/          # Core configuration
│  │  ├── db/            # Database models
│  │  ├── llm/           # LLM integration
│  │  ├── services/      # Business logic
│  │  └── simulation/    # Simulation engine
│  └── tests/             # Test files
├── data/              # Data storage
└── docker-compose.yml # Docker configuration
```

## Main Features

### 1. User Authentication
- User registration/login
- JWT token authentication
- User profile management

### 2. Intelligent Dialogue
- Multi-LLM model support
- Real-time message communication
- Conversation history management

### 3. Simulation Modeling
- Visual modeling interface
- Parameter configuration management
- Simulation result analysis

### 4. Data Visualization
- Multiple chart types
- Real-time data updates
- Interactive charts

### 5. Internationalization
- Chinese/English switching
- Localization configuration

## Development Guide

### Environment Variable Configuration

Configure the following environment variables in `docker-compose.yml`:

```yaml
# LLM API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
QWEN_API_KEY=your_qwen_key
DEEPSEEK_API_KEY=your_deepseek_key

# Database
DATABASE_URL=sqlite:///./app.db

# Redis
REDIS_PASSWORD=simsynai

# Security
SECRET_KEY=your_secret_key
```

### Logs and Data

Project data is stored in the following directories:
- `./data/logs/` - Application logs
- `./data/simulation_results/` - Simulation results

### Stop Services

```bash
docker compose down
```

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See LICENSE file for more information.

## Contact

- Project Link: [https://github.com/Hanna-Qu/SimSynAI](https://github.com/Hanna-Qu/SimSynAI)
- Issues: [https://github.com/Hanna-Qu/SimSynAI/issues](https://github.com/Hanna-Qu/SimSynAI/issues)

## Acknowledgments

- [React](https://reactjs.org/) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Docker](https://www.docker.com/) - Containerization platform
- [Ant Design](https://ant.design/) - UI component library
- [ECharts](https://echarts.apache.org/) - Data visualization library

---

**[中文文档](README.md)** | **English Documentation** 