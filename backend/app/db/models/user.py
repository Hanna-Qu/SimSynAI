from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base
from app.core.security import get_password_hash


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    preferred_model = Column(String, default="gpt-3.5-turbo")
    
    # API密钥字段 - 加密存储
    openai_api_key = Column(Text, nullable=True)
    anthropic_api_key = Column(Text, nullable=True)
    google_api_key = Column(Text, nullable=True)
    qwen_api_key = Column(Text, nullable=True)
    deepseek_api_key = Column(Text, nullable=True)
    
    # 关系
    chat_messages = relationship("ChatMessage", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    simulation_tasks = relationship("SimulationTask", back_populates="user")
    
    def set_password(self, password: str) -> None:
        """设置密码"""
        self.hashed_password = get_password_hash(password)
        
    def check_password(self, password: str) -> bool:
        """检查密码"""
        from app.core.security import verify_password
        return verify_password(password, self.hashed_password) 