# SimSynAI - 基于大语言模型的智能化仿真平台

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/Hanna-Qu/SimSynAI/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Hanna-Qu/SimSynAI/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/Hanna-Qu/SimSynAI/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

SimSynAI 是一个集成了多种大语言模型的智能化仿真平台，支持智能对话、仿真建模、数据可视化等功能。

## ✨ 主要特性

- 🧠 **多LLM模型集成** - 支持OpenAI、Claude、Gemini、千问、DeepSeek等
- 🔐 **安全的用户系统** - JWT认证、API密钥加密存储
- 💬 **智能对话** - 实时AI对话、历史记录管理
- 🧪 **仿真实验** - 可视化建模、参数配置、结果分析
- 📊 **数据可视化** - 多种图表类型、交互式展示
- 🌐 **国际化支持** - 中英文双语界面
- 📱 **响应式设计** - 完美适配桌面和移动设备
- 🐳 **容器化部署** - 开箱即用的Docker解决方案

## 🚀 快速开始

### 环境要求
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (生产部署)
- Git

### 方式1：Docker容器化运行（推荐用于生产）

```bash
# 1. 克隆项目
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. 启动所有服务
docker compose up -d

# 3. 等待服务启动完成 (约1-2分钟)
docker compose ps

# 4. 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/api/v1/docs
```

### 方式2：本地开发环境（推荐用于开发）

使用conda虚拟环境进行本地开发，获得更好的开发体验：

#### 快速启动
```bash
# 1. 克隆项目
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. 初始化开发环境（首次运行）
# Windows
.\scripts\dev-start.ps1 init

# Linux/macOS
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh init

# 3. 启动开发服务
# Windows
.\scripts\dev-start.ps1 full

# Linux/macOS  
./scripts/dev-start.sh full
```

#### 分别启动服务
```bash
# 启动后端服务
./scripts/dev-start.sh backend   # 或 .\scripts\dev-start.ps1 backend

# 启动前端服务（新终端）
./scripts/dev-start.sh frontend  # 或 .\scripts\dev-start.ps1 frontend
```

#### 手动环境配置
如果您喜欢手动控制，请参考[本地开发环境设置指南](docs/development-setup.md)

### 默认账户
- **管理员**: `admin` / `admin123`
- **测试用户**: `demo` / `demo123`

### 访问地址
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/api/v1/docs
- Redis: localhost:6379 (仅Docker方式)

## 技术栈

### 前端
- React 18 + TypeScript
- Ant Design UI组件库
- React Router v6 路由管理
- Axios HTTP客户端
- ECharts 数据可视化
- i18next 国际化

### 后端
- Python 3.11 + FastAPI
- SQLAlchemy ORM
- SQLite 数据库
- 多LLM集成 (OpenAI, Claude, Gemini, Qwen, DeepSeek)
- Redis 缓存

### 部署
- Docker + Docker Compose
- Nginx 反向代理

## 项目结构

```
SimSynAI/
├── frontend/          # React前端应用
│  ├── src/
│  │  ├── components/    # React组件
│  │  ├── locales/       # 国际化文件
│  │  └── styles/        # 样式文件
│  └── public/            # 静态资源
├── backend/           # FastAPI后端
│  ├── app/
│  │  ├── api/           # API路由
│  │  ├── core/          # 核心配置
│  │  ├── db/            # 数据库模型
│  │  ├── llm/           # LLM集成
│  │  ├── services/      # 业务逻辑
│  │  └── simulation/    # 仿真引擎
│  └── tests/             # 测试文件
├── data/              # 数据存储
└── docker-compose.yml # Docker配置
```

## 主要功能

### 1. 用户认证
- 用户注册/登录
- JWT令牌认证
- 用户资料管理

### 2. 智能对话
- 多LLM模型支持
- 实时消息通信
- 对话历史管理

### 3. 仿真建模
- 可视化建模界面
- 参数配置管理
- 仿真结果分析

### 4. 数据可视化
- 多种图表类型
- 实时数据更新
- 交互式图表

### 5. 国际化
- 中英文切换
- 本地化配置

## 开发说明

### 环境变量配置

在`docker-compose.yml` 中配置以下环境变量：

```yaml
# LLM API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
QWEN_API_KEY=your_qwen_key
DEEPSEEK_API_KEY=your_deepseek_key

# 数据库
DATABASE_URL=sqlite:///./app.db

# Redis
REDIS_PASSWORD=simsynai

# 安全
SECRET_KEY=your_secret_key
```

### 日志和数据

项目数据存储在以下目录：
- `./data/logs/` - 应用日志
- `./data/simulation_results/` - 仿真结果

### 停止服务

```bash
docker compose down
```

## 贡献指南

1. Fork 项目
2. 创建分支(`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

根据 MIT 许可证进行分发和使用，详情请参阅 LICENSE 文件。

## 联系方式

- 项目链接: [https://github.com/Hanna-Qu/SimSynAI](https://github.com/Hanna-Qu/SimSynAI)
- 问题反馈: [https://github.com/Hanna-Qu/SimSynAI/issues](https://github.com/Hanna-Qu/SimSynAI/issues)

## 致谢

- [React](https://reactjs.org/) - 前端框架
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [Docker](https://www.docker.com/) - 容器化平台
- [Ant Design](https://ant.design/) - UI组件库
- [ECharts](https://echarts.apache.org/) - 数据可视化库

---

**[English Documentation](README.md)** | **中文文档**
