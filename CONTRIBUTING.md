# 贡献指南

感谢您对 SimSynAI 项目的关注！我们欢迎各种形式的贡献。

## 开发环境设置

### 前置要求
- Docker Desktop
- Git

### 本地开发

1. **克隆项目**
```bash
git clone https://github.com/your-username/SimSynAI.git
cd SimSynAI
```

2. **启动开发环境**
```bash
docker compose up -d
```

3. **访问应用**
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/api/v1/docs

## 贡献流程

### 1. 准备工作
- Fork 项目到您的 GitHub 账户
- 创建新的功能分支

### 2. 开发
- 遵循现有的代码风格
- 添加必要的测试
- 确保所有测试通过

### 3. 提交
- 使用清晰的提交信息
- 遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/)

### 4. Pull Request
- 创建 Pull Request
- 描述您的更改
- 关联相关的 Issue

## 代码规范

### 前端 (React + TypeScript)
- 使用 ESLint 和 Prettier
- 组件使用 PascalCase
- 文件名使用 kebab-case

### 后端 (Python + FastAPI)
- 遵循 PEP 8
- 使用类型注解
- 添加文档字符串

## 提交信息格式

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 示例
```
feat(auth): 添加用户注册功能

- 实现用户注册API
- 添加邮箱验证
- 更新前端注册表单

Closes #123
```

## 问题报告

在提交 Issue 前，请：
1. 检查是否已有相似问题
2. 使用 Issue 模板
3. 提供详细的重现步骤
4. 包含错误日志

## 许可证

贡献的代码将采用 MIT 许可证。 