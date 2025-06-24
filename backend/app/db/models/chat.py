from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base_class import Base


class ChatMessage(Base):
    """聊天消息模型"""
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    task_id = Column(String, ForeignKey("simulation_tasks.id"), nullable=True)
    role = Column(String, nullable=False)  # 'user' 或 'assistant'
    content = Column(Text, nullable=False)
    model = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="chat_messages")
    task = relationship("SimulationTask", back_populates="chat_messages")


class ChatSession(Base):
    """聊天会话模型"""
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, default="新对话")
    
    # 关系
    user = relationship("User", back_populates="chat_sessions")