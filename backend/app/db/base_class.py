from typing import Any
from datetime import datetime
import uuid

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, String, DateTime


@as_declarative()
class Base:
    """
    SQLAlchemy 基础模型类
    所有模型都继承自此类，提供通用字段和方法
    """
    id: Any
    __name__: str
    
    # 自动生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # 通用字段
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 