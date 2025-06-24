# SimSynAI 快速入门指南

## 📋 概述

SimSynAI 是一个基于大语言模型的智能化仿真平台，支持多种部署方式和开发环境。

## 🚀 三种启动方式

### 1. 生产环境 - Docker容器化部署

**适用场景**: 生产部署、团队协作、快速体验

```bash
# 一键启动所有服务
docker compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:8000/docs
```

**优点**: 
- ✅ 环境隔离，无依赖冲突
- ✅ 一致的运行环境
- ✅ 简单的部署流程

**缺点**: 
- ❌ 启动较慢
- ❌ 调试不便
- ❌ 资源占用较大

### 2. 开发环境 - Conda虚拟环境

**适用场景**: 日常开发、代码调试、功能测试

```bash
# 快速启动（推荐）
.\scripts\dev-start.ps1 init    # 首次初始化
.\scripts\dev-start.ps1 full    # 启动服务

# 分别启动
.\scripts\dev-start.ps1 backend   # 启动后端
.\scripts\dev-start.ps1 frontend  # 启动前端
```

**优点**: 
- ✅ 启动快速
- ✅ 便于调试
- ✅ 热重载支持
- ✅ 直接编辑代码

**缺点**: 
- ❌ 需要安装依赖
- ❌ 环境配置复杂

### 3. 混合模式 - 最佳开发体验

**适用场景**: 前后端分离开发、性能优化

```bash
# 依赖服务用Docker
docker run -d --name redis -p 6379:6379 redis:7.0-alpine

# 应用服务用本地环境
conda activate simsynai
cd backend && uvicorn app.main:app --reload &
cd frontend && pnpm start &
```

**优点**: 
- ✅ 结合两种方式的优点
- ✅ 灵活的服务管理
- ✅ 最佳开发体验

## 🔧 首次设置

### 1. 环境准备

**Docker方式**:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Conda方式**:
- [Anaconda](https://www.anaconda.com/products/distribution) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Node.js](https://nodejs.org/) (LTS版本)
- [pnpm](https://pnpm.io/): `npm install -g pnpm`

### 2. 项目获取

```bash
# 克隆项目
git clone https://github.com/your-username/SimSynAI.git
cd SimSynAI
```

### 3. 根据需要选择启动方式

| 场景 | 推荐方式 | 命令 |
|------|---------|------|
| 快速体验 | Docker | `docker compose up -d` |
| 日常开发 | Conda | `.\scripts\dev-start.ps1 full` |
| 前端开发 | 混合 | Docker后端 + 本地前端 |
| 后端开发 | 混合 | 本地后端 + Docker前端 |

## 🎯 默认账户

| 用户名 | 密码 | 角色 | 用途 |
|--------|------|------|------|
| admin | admin123 | 管理员 | 系统管理、用户管理 |
| demo | demo123 | 普通用户 | 功能测试、演示 |

## 📍 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端应用 | http://localhost:3000 | React应用界面 |
| 后端API | http://localhost:8000 | FastAPI服务 |
| API文档 | http://localhost:8000/docs | Swagger文档 |
| Redis | localhost:6379 | 缓存服务(Docker) |

## 🛠️ 开发工具

### VS Code配置

项目包含VS Code配置文件，自动设置Python解释器和格式化工具。

推荐插件：
- Python
- Black Formatter
- Prettier
- Docker
- GitLens

### Git钩子

项目配置了pre-commit钩子，自动进行代码检查：

```bash
# 安装钩子
conda activate simsynai
pip install pre-commit
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

## 🚀 发布到GitHub

### 使用自动化脚本

```bash
# 快速设置GitHub仓库
.\scripts\setup-github.ps1 -GitHubUsername "你的用户名"

# 创建新版本
.\scripts\release.py patch
.\scripts\quick-publish.ps1
```

### 手动步骤

1. 在GitHub创建新仓库
2. 连接远程仓库：
   ```bash
   git remote add origin https://github.com/你的用户名/SimSynAI.git
   git branch -M main
   git push -u origin main
   ```

## 🔐 环境变量配置

### 生产环境 (.env)

```bash
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
QWEN_API_KEY=your_qwen_key
DEEPSEEK_API_KEY=your_deepseek_key

# 安全配置
SECRET_KEY=your_very_secure_secret_key
DEBUG=false

# 数据库
DATABASE_URL=sqlite:///./app.db
```

### 开发环境 (backend/.env)

```bash
# 开发模式配置
DEBUG=true
DATABASE_URL=sqlite:///./dev_app.db
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## 📚 进阶配置

### 自定义LLM配置

编辑 `backend/app/core/config.py` 添加新的LLM配置。

### 数据库迁移

```bash
conda activate simsynai
cd backend
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

### 前端自定义

前端基于 React + TypeScript + Ant Design：
- 组件在 `frontend/src/components/`
- 样式在 `frontend/src/styles/`
- 国际化在 `frontend/src/locales/`

## 🆘 常见问题

### 1. 端口冲突
```bash
# 检查端口占用
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# 更改端口
uvicorn app.main:app --port 8001  # 后端
REACT_APP_PORT=3001 pnpm start   # 前端
```

### 2. 数据库问题
```bash
# 重置数据库
rm backend/app.db  # 或 backend/dev_app.db
.\scripts\dev-start.ps1 init
```

### 3. 依赖问题
```bash
# 重新安装依赖
conda env remove -n simsynai
conda env create -f environment.yml

# 前端依赖
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### 4. Docker问题
```bash
# 完全重建
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

## 🎉 享受开发！

现在您已经掌握了SimSynAI的所有启动方式，选择最适合您的方式开始探索这个智能化仿真平台吧！

如有问题，请查看：
- [详细开发指南](development-setup.md)
- [GitHub发布指南](github-setup.md)
- [项目文档](../README.md) 