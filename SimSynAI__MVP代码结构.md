# NeuroSimuLab MVP代码结构

## 前端代码结构

```
frontend/
├── public/
│   ├── favicon.ico
│   ├── index.html
│   └── assets/
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── MainLayout.tsx         # 主布局组件
│   │   │   └── SideMenu.tsx           # 侧边菜单
│   │   ├── Chat/
│   │   │   ├── ChatBox.tsx            # 对话框组件
│   │   │   ├── MessageItem.tsx        # 消息项组件
│   │   │   └── ModelSelector.tsx      # 模型选择器
│   │   ├── Simulation/
│   │   │   ├── TaskForm.tsx           # 仿真任务表单
│   │   │   ├── TaskList.tsx           # 任务列表组件
│   │   │   └── TaskDetail.tsx         # 任务详情组件
│   │   └── Visualization/
│   │       ├── ChartComponent.tsx     # 图表组件
│   │       └── Dashboard.tsx          # 仪表盘组件
│   ├── pages/
│   │   ├── Auth/
│   │   │   ├── Login.tsx              # 登录页面
│   │   │   └── Register.tsx           # 注册页面
│   │   ├── Chat/
│   │   │   └── index.tsx              # 对话页面
│   │   ├── Simulation/
│   │   │   ├── index.tsx              # 仿真任务列表页
│   │   │   └── [id].tsx               # 仿真任务详情页
│   │   ├── Visualization/
│   │   │   └── index.tsx              # 数据可视化页面
│   │   ├── Dashboard/
│   │   │   └── index.tsx              # 仪表盘页面
│   │   └── App.tsx                    # 应用入口
│   ├── services/
│   │   ├── api.ts                     # API基础配置
│   │   ├── auth.ts                    # 认证相关API
│   │   ├── chat.ts                    # 对话相关API
│   │   └── simulation.ts              # 仿真相关API
│   ├── utils/
│   │   ├── request.ts                 # 请求工具
│   │   ├── storage.ts                 # 存储工具
│   │   └── format.ts                  # 格式化工具
│   ├── types/
│   │   ├── chat.ts                    # 对话相关类型
│   │   ├── simulation.ts              # 仿真相关类型
│   │   └── user.ts                    # 用户相关类型
│   ├── config/
│   │   └── config.ts                  # 全局配置
│   ├── index.tsx                      # 入口文件
│   └── App.css                        # 全局样式
├── package.json
└── tsconfig.json
```

## 后端代码结构

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py                # 认证相关API
│   │   │   ├── chat.py                # 对话相关API
│   │   │   ├── simulation.py          # 仿真相关API
│   │   │   └── visualization.py       # 可视化相关API
│   │   └── api.py                     # API路由注册
│   ├── core/
│   │   ├── config.py                  # 配置管理
│   │   ├── security.py                # 安全相关
│   │   └── events.py                  # 事件处理
│   ├── db/
│   │   ├── base.py                    # 数据库基础配置
│   │   ├── session.py                 # 会话管理
│   │   └── models/
│   │       ├── user.py                # 用户模型
│   │       ├── chat.py                # 对话模型
│   │       └── simulation.py          # 仿真模型
│   ├── llm/
│   │   ├── base.py                    # LLM基础类
│   │   ├── openai.py                  # OpenAI适配器
│   │   ├── anthropic.py               # Claude适配器
│   │   ├── gemini.py                  # Gemini适配器
│   │   ├── qwen.py                    # Qwen适配器
│   │   ├── deepseek.py                # DeepSeek适配器
│   │   ├── prompts/                   # Prompt模板
│   │   │   ├── simulation_config.py   # 仿真配置提示词
│   │   │   ├── result_analysis.py     # 结果分析提示词
│   │   │   └── error_diagnosis.py     # 错误诊断提示词
│   │   └── agents/
│   │       ├── config_agent.py        # 配置助手Agent
│   │       ├── analysis_agent.py      # 分析助手Agent
│   │       └── diagnosis_agent.py     # 诊断助手Agent
│   ├── simulation/
│   │   ├── engine.py                  # 仿真引擎接口
│   │   ├── skyeye.py                  # SkyEye适配器
│   │   ├── models.py                  # 仿真模型定义
│   │   └── utils.py                   # 仿真工具函数
│   ├── schemas/
│   │   ├── user.py                    # 用户相关Schema
│   │   ├── chat.py                    # 对话相关Schema
│   │   └── simulation.py              # 仿真相关Schema
│   ├── services/
│   │   ├── user.py                    # 用户服务
│   │   ├── chat.py                    # 对话服务
│   │   └── simulation.py              # 仿真服务
│   └── utils/
│       ├── deps.py                    # 依赖注入
│       └── logging.py                 # 日志工具
├── main.py                            # 应用入口
├── alembic/                           # 数据库迁移
│   └── versions/
├── alembic.ini                        # Alembic配置
└── requirements.txt                   # 依赖管理
```

## Docker配置结构

```
docker/
├── docker-compose.yml                 # 服务编排配置
├── frontend.Dockerfile                # 前端Docker配置
├── backend.Dockerfile                 # 后端Docker配置
└── nginx/
    └── nginx.conf                     # Nginx配置
```

## 核心代码示例

### 1. 后端 - LLM模型适配器基类 (backend/app/llm/base.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class LLMAdapter(ABC):
    """大语言模型适配器基类"""
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        self.api_key = api_key
        self.model_name = model_name
        self.extra_config = kwargs
        
    @abstractmethod
    async def generate(self, 
                      prompt: str, 
                      system_message: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000,
                      messages: Optional[List[Dict[str, str]]] = None) -> str:
        """生成文本响应"""
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        pass
```

### 2. 后端 - OpenAI适配器实现 (backend/app/llm/openai.py)

```python
import openai
from typing import Dict, List, Optional, Any
from .base import LLMAdapter

class OpenAIAdapter(LLMAdapter):
    """OpenAI API适配器"""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        
    async def generate(self, 
                      prompt: str, 
                      system_message: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000,
                      messages: Optional[List[Dict[str, str]]] = None) -> str:
        """调用OpenAI API生成文本响应"""
        if messages is None:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    async def get_available_models(self) -> List[str]:
        """获取可用的OpenAI模型列表"""
        models = await self.client.models.list()
        return [model.id for model in models.data]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "provider": "OpenAI",
            "model": self.model_name,
            "type": "chat",
            "capabilities": ["text generation", "code generation", "reasoning"]
        }
```

### 3. 后端 - 仿真引擎接口 (backend/app/simulation/engine.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

class SimulationConfig(BaseModel):
    """仿真配置模型"""
    parameters: Dict[str, Any]
    model_path: Optional[str] = None
    duration: float
    step_size: float
    output_variables: List[str]

class SimulationResult(BaseModel):
    """仿真结果模型"""
    task_id: str
    status: str
    data: Dict[str, List[float]]
    time_points: List[float]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

class SimulationEngine(ABC):
    """仿真引擎抽象基类"""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """初始化引擎"""
        pass
    
    @abstractmethod
    async def validate_config(self, config: SimulationConfig) -> Dict[str, Any]:
        """验证配置有效性"""
        pass
    
    @abstractmethod
    async def run_simulation(self, config: SimulationConfig) -> SimulationResult:
        """运行仿真任务"""
        pass
    
    @abstractmethod
    async def get_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        pass
    
    @abstractmethod
    async def stop_simulation(self, task_id: str) -> bool:
        """停止仿真任务"""
        pass
```

### 4. 前端 - 对话组件 (frontend/src/components/Chat/ChatBox.tsx)

```typescript
import React, { useState, useEffect, useRef } from 'react';
import { Input, Button, Select, Spin, message } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import MessageItem from './MessageItem';
import ModelSelector from './ModelSelector';
import { sendMessage, getHistory } from '../../services/chat';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatBoxProps {
  taskId?: string; // 可选的关联任务ID
}

const ChatBox: React.FC<ChatBoxProps> = ({ taskId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('gpt-4');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // 加载历史消息
  useEffect(() => {
    const loadHistory = async () => {
      if (taskId) {
        try {
          const history = await getHistory(taskId);
          setMessages(history);
        } catch (error) {
          message.error('加载历史消息失败');
        }
      }
    };
    
    loadHistory();
  }, [taskId]);

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 发送消息
  const handleSend = async () => {
    if (!inputValue.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    
    try {
      const response = await sendMessage({
        content: inputValue,
        model: selectedModel,
        taskId: taskId,
      });
      
      const assistantMessage: Message = {
        id: response.id,
        role: 'assistant',
        content: response.content,
        timestamp: response.timestamp,
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      message.error('发送消息失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-box">
      <div className="model-selector-container">
        <ModelSelector value={selectedModel} onChange={setSelectedModel} />
      </div>
      
      <div className="messages-container">
        {messages.map(msg => (
          <MessageItem key={msg.id} message={msg} />
        ))}
        {loading && (
          <div className="loading-message">
            <Spin size="small" /> AI正在思考...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-container">
        <Input.TextArea
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          placeholder="输入您的问题或指令..."
          autoSize={{ minRows: 1, maxRows: 4 }}
          onPressEnter={e => {
            if (!e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <Button 
          type="primary" 
          icon={<SendOutlined />} 
          onClick={handleSend}
          loading={loading}
        />
      </div>
    </div>
  );
};

export default ChatBox;
```

### 5. 后端 - 对话API端点 (backend/app/api/endpoints/chat.py)

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatHistory
from app.services.chat import ChatService
from app.llm.base import get_llm_adapter

router = APIRouter()

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    message: ChatMessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    llm_adapter = Depends(get_llm_adapter)
):
    """发送对话消息"""
    try:
        chat_service = ChatService(db, llm_adapter)
        response = await chat_service.process_message(
            user_id=current_user.id,
            content=message.content,
            model=message.model,
            task_id=message.task_id
        )
        
        # 异步保存对话历史
        background_tasks.add_task(
            chat_service.save_message_history,
            user_id=current_user.id,
            message_content=message.content,
            response_content=response.content,
            task_id=message.task_id
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    task_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取对话历史"""
    try:
        chat_service = ChatService(db)
        history = await chat_service.get_message_history(
            user_id=current_user.id,
            task_id=task_id,
            limit=limit
        )
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/model", response_model=dict)
async def change_model(
    model_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """切换对话模型"""
    try:
        chat_service = ChatService(db)
        result = await chat_service.set_preferred_model(
            user_id=current_user.id,
            model_name=model_data.get("model")
        )
        return {"success": result, "model": model_data.get("model")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 6. Docker Compose配置 (docker/docker-compose.yml)

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ..
      dockerfile: docker/frontend.Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - neurosimlab-network

  backend:
    build:
      context: ..
      dockerfile: docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
      - SECRET_KEY=${SECRET_KEY:-supersecretkey}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - QWEN_API_KEY=${QWEN_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ../backend:/app
      - simulation-data:/app/data
    depends_on:
      - redis
    networks:
      - neurosimlab-network

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - neurosimlab-network

networks:
  neurosimlab-network:
    driver: bridge

volumes:
  redis-data:
  simulation-data:
```

## 启动脚本示例 (start.sh)

```bash
#!/bin/bash

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 显示欢迎信息
echo "======================================"
echo "  NeuroSimuLab 启动脚本"
echo "======================================"

# 设置环境变量
echo "正在配置环境变量..."
if [ ! -f .env ]; then
    echo "创建.env文件..."
    cat > .env << EOL
# API密钥配置
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
QWEN_API_KEY=your_qwen_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# 安全配置
SECRET_KEY=supersecretkey

# 系统配置
DEBUG=true
EOL
    echo "已创建默认.env文件，请编辑该文件配置您的API密钥"
    exit 1
else
    echo ".env文件已存在"
fi

# 启动服务
echo "正在启动NeuroSimuLab服务..."
docker-compose -f docker/docker-compose.yml up -d

# 检查服务是否成功启动
if [ $? -eq 0 ]; then
    echo "======================================"
    echo "  NeuroSimuLab 已成功启动"
    echo "  前端访问地址: http://localhost:3000"
    echo "  API文档地址: http://localhost:8000/docs"
    echo "======================================"
else
    echo "服务启动失败，请检查日志"
    exit 1
fi
``` 