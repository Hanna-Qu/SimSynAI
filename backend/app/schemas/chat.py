from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ChatMessageBase(BaseModel):
    """聊天消息基础模式"""
    role: str  # user 或 assistant
    content: str
    model: str
    task_id: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    """聊天消息创建模式"""
    pass


class ChatMessageUpdate(ChatMessageBase):
    """聊天消息更新模式"""
    pass


class ChatMessageInDBBase(ChatMessageBase):
    id: str
    user_id: str
    timestamp: datetime
    
    model_config = {"from_attributes": True}


class ChatMessageResponse(ChatMessageBase):
    """聊天消息响应模式"""
    id: str
    user_id: str
    timestamp: datetime
    
    model_config = {"from_attributes": True}


class ChatHistory(BaseModel):
    messages: List[ChatMessageResponse]


class ChatSessionBase(BaseModel):
    """聊天会话基础模式"""
    title: str = "新对话"


class ChatSessionCreate(ChatSessionBase):
    """聊天会话创建模式"""
    pass


class ChatSessionUpdate(ChatSessionBase):
    """聊天会话更新模式"""
    pass


class ChatSessionInDBBase(ChatSessionBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


# 直接继承ChatSessionInDBBase，避免重复定义相同的字段和Config
class ChatSession(ChatSessionInDBBase):
    """聊天会话模式（返回给API）"""
    pass