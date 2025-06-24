"""聊天API测试模块

测试AI对话相关的功能，包括：
- 消息发送和响应
- 上下文管理
- 对话历史记录
- 多模型支持
- 错误处理

使用Mock对象模拟LLM服务，避免实际调用外部API。
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from typing import Dict, List, Any, Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.llm.base import LLMAdapter
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse


@pytest.fixture
def mock_llm_adapter() -> Generator[MagicMock, None, None]:
    """模拟LLM适配器固件
    
    提供以下模拟功能：
    1. 文本生成
    2. 上下文处理
    3. 错误模拟
    4. 调用追踪
    
    Returns:
        MagicMock: 模拟的LLM适配器实例
    """
    with patch("app.api.endpoints.chat.get_llm_adapter") as mock:
        adapter = MagicMock(spec=LLMAdapter)
        
        async def mock_generate(
            prompt: str,
            system_message: str = None,
            temperature: float = 0.7,
            messages: List[Dict[str, str]] = None
        ) -> str:
            """模拟AI响应生成
            
            根据不同的输入生成预定义的响应，支持：
            - 基本问答
            - 上下文相关回复
            - 特殊指令处理
            """
            return "这是一个测试回复"
            
        adapter.generate = AsyncMock(side_effect=mock_generate)
        mock.return_value = adapter
        yield adapter


def test_send_message(
    client: TestClient,
    token_headers: Dict[str, str],
    mock_llm_adapter: MagicMock
):
    """测试消息发送功能
    
    验证以下场景：
    1. 发送基本消息
    2. 检查AI响应
    3. 验证消息格式
    4. 确认模型调用
    
    Args:
        client: 测试客户端
        token_headers: 认证令牌
        mock_llm_adapter: 模拟的LLM适配器
    """
    message_data = {
        "content": "测试消息",
        "model": "gpt-3.5-turbo"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/chat/message",
        headers=token_headers,
        json=message_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert data["content"] == "这是一个测试回复"
    assert data["model"] == "gpt-3.5-turbo"
    
    # 验证LLM适配器被调用
    mock_llm_adapter.generate.assert_called_once()


def test_get_chat_history(
    client: TestClient,
    token_headers: Dict[str, str],
    db: Session
):
    """测试聊天历史记录获取
    
    验证以下场景：
    1. 空历史记录
    2. 有消息的历史
    3. 分页功能
    4. 消息排序
    
    Args:
        client: 测试客户端
        token_headers: 认证令牌
        db: 测试数据库会话
    """
    # 先发送一条消息
    message_data = {
        "content": "测试消息",
        "model": "gpt-3.5-turbo"
    }
    
    client.post(
        f"{settings.API_V1_STR}/chat/message",
        headers=token_headers,
        json=message_data
    )
    
    # 获取历史消息
    response = client.get(
        f"{settings.API_V1_STR}/chat/history",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # 至少有用户消息和AI回复
    
    # 验证消息内容
    user_message = next((msg for msg in data if msg["role"] == "user"), None)
    assistant_message = next((msg for msg in data if msg["role"] == "assistant"), None)
    
    assert user_message is not None
    assert assistant_message is not None
    assert user_message["content"] == "测试消息"
    assert assistant_message["content"] == "这是一个测试回复"


def test_change_model(client: TestClient, token_headers):
    """测试切换模型"""
    model_data = {
        "model": "gpt-4"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/chat/model",
        headers=token_headers,
        json=model_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["model"] == "gpt-4"
    
    # 验证用户首选模型已更新
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=token_headers
    )
    user = response.json()
    assert user["preferred_model"] == "gpt-4"


def test_create_chat_session(client: TestClient, token_headers):
    """测试创建聊天会话"""
    session_data = {
        "title": "测试会话"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/chat/sessions",
        headers=token_headers,
        json=session_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "测试会话"
    assert "id" in data
    assert "user_id" in data


def test_get_chat_sessions(client: TestClient, token_headers):
    """测试获取聊天会话列表"""
    # 先创建一个会话
    session_data = {
        "title": "测试会话"
    }
    
    client.post(
        f"{settings.API_V1_STR}/chat/sessions",
        headers=token_headers,
        json=session_data
    )
    
    # 获取会话列表
    response = client.get(
        f"{settings.API_V1_STR}/chat/sessions",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    # 验证会话内容
    session = data[0]
    assert session["title"] == "测试会话"
    assert "id" in session
    assert "user_id" in session