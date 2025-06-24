# GitHub发布指南

本指南将帮助您将SimSynAI项目发布到GitHub，并设置版本管理。

## 步骤1：准备环境

### 1.1 安装Git
如果您的系统没有安装Git，请先安装：

**Windows:**
- 下载并安装 [Git for Windows](https://git-scm.com/download/win)
- 或使用包管理器：`winget install Git.Git`

**macOS:**
```bash
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

### 1.2 配置Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 步骤2：创建GitHub仓库

### 2.1 在GitHub上创建新仓库
1. 登录到 [GitHub](https://github.com)
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `SimSynAI`
   - **Description**: `基于大语言模型的智能化仿真平台`
   - **Visibility**: Public (如果您希望开源) 或 Private
   - **不要**勾选 "Add a README file"、"Add .gitignore"、"Choose a license"
4. 点击 "Create repository"

### 2.2 记录仓库URL
创建后，GitHub会显示仓库URL，形如：
```
https://github.com/your-username/SimSynAI.git
```

## 步骤3：初始化本地Git仓库

在项目根目录（SimSynAI文件夹）中执行：

```bash
# 1. 初始化Git仓库
git init

# 2. 添加所有文件到暂存区
git add .

# 3. 创建初始提交
git commit -m "feat: 初始项目提交

- 🎉 SimSynAI v1.0.0 初始版本
- 🤖 多LLM模型集成 (OpenAI, Claude, Gemini, Qwen, DeepSeek)
- 🔐 用户认证系统 (注册/登录/JWT)
- 💬 智能对话功能
- 🔬 仿真实验管理
- 📊 数据可视化
- 🌐 国际化支持 (中英文)
- 📱 响应式设计
- 🐳 Docker容器化部署"

# 4. 添加远程仓库 (替换为您的实际仓库URL)
git remote add origin https://github.com/your-username/SimSynAI.git

# 5. 创建并切换到main分支
git branch -M main

# 6. 推送到GitHub
git push -u origin main
```

## 步骤4：创建分支策略

### 4.1 创建develop分支
```bash
# 创建并切换到develop分支
git checkout -b develop

# 推送develop分支到远程
git push -u origin develop
```

### 4.2 设置分支保护规则
在GitHub仓库页面：
1. 进入 "Settings" > "Branches"
2. 点击 "Add rule" 添加保护规则
3. 为 `main` 分支设置：
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require up-to-date branches before merging
   - ✅ Include administrators

## 步骤5：设置GitHub Actions

### 5.1 启用Actions
1. 在GitHub仓库页面，点击 "Actions" 选项卡
2. 如果提示启用Actions，点击 "I understand my workflows, go ahead and enable them"

### 5.2 配置Secrets
在仓库设置中添加必要的密钥：
1. 进入 "Settings" > "Secrets and variables" > "Actions"
2. 添加以下Repository secrets（如果需要）：
   - `DOCKER_USERNAME`: Docker Hub用户名
   - `DOCKER_PASSWORD`: Docker Hub密码
   - `OPENAI_API_KEY`: OpenAI API密钥
   - 其他API密钥...

## 步骤6：创建第一个Release

### 6.1 使用脚本发布版本
```bash
# 使用发布脚本创建新版本
python scripts/release.py patch "初始版本发布"
```

### 6.2 手动创建Release
如果不使用脚本，可以手动创建：

```bash
# 1. 创建版本标签
git tag -a v1.0.0 -m "发布版本 1.0.0"

# 2. 推送标签到远程
git push origin v1.0.0
```

然后在GitHub上：
1. 进入仓库的 "Releases" 页面
2. 点击 "Create a new release"
3. 选择刚创建的标签 `v1.0.0`
4. 填写Release信息：
   - **Release title**: `v1.0.0 - 初始版本`
   - **Description**: 从CHANGELOG.md复制内容
5. 点击 "Publish release"

## 步骤7：配置项目设置

### 7.1 更新README徽章
将README.md中的徽章URL替换为实际的仓库URL：
```markdown
[![CI/CD](https://github.com/your-username/SimSynAI/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/your-username/SimSynAI/actions)
[![Version](https://img.shields.io/github/v/release/your-username/SimSynAI)](https://github.com/your-username/SimSynAI/releases)
```

### 7.2 设置仓库描述和主题
在GitHub仓库主页：
1. 点击右上角的齿轮图标 "Settings"
2. 在 "General" 设置中：
   - 添加仓库描述
   - 设置网站URL（如果有）
   - 添加主题标签：`ai`, `llm`, `simulation`, `react`, `fastapi`, `docker`

## 步骤8：版本管理工作流

### 8.1 日常开发流程
```bash
# 1. 从main分支创建功能分支
git checkout main
git pull origin main
git checkout -b feature/new-feature

# 2. 进行开发并提交
git add .
git commit -m "feat(scope): 添加新功能"

# 3. 推送分支并创建PR
git push origin feature/new-feature
```

### 8.2 发布新版本
```bash
# 1. 切换到main分支
git checkout main
git pull origin main

# 2. 使用发布脚本
python scripts/release.py minor "添加新功能"

# 3. 脚本会自动：
# - 更新版本号
# - 更新CHANGELOG.md
# - 创建Git标签
# - 推送到远程仓库
```

## 常见问题

### Q1: 推送时提示认证失败
A1: 使用Personal Access Token代替密码：
1. 在GitHub设置中创建Personal Access Token
2. 使用token作为密码进行推送

### Q2: CI/CD失败
A2: 检查GitHub Actions日志：
1. 进入仓库的Actions页面
2. 点击失败的工作流查看详细日志

### Q3: Docker镜像推送失败
A3: 确保设置了正确的Docker Hub凭据或GitHub Package Registry权限

## 下一步

项目发布到GitHub后，您可以：
1. 邀请团队成员协作
2. 设置CI/CD自动部署
3. 配置Issues和Project管理
4. 集成第三方服务（如Codecov、Snyk等）
5. 创建Wiki文档

恭喜！您已成功将SimSynAI项目发布到GitHub并设置了完善的版本管理系统。 