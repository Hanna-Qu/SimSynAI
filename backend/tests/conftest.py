"""测试配置模块

提供测试环境的配置和固件(fixtures)，包括：
- 数据库设置
- 测试客户端
- 模拟用户认证
- API密钥配置
- 测试数据准备
"""

import os
import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# 设置测试环境变量
test_env_vars: Dict[str, str] = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "OPENAI_API_KEY": "sk-test",
    "ANTHROPIC_API_KEY": "test",
    "GOOGLE_API_KEY": "test",
    "QWEN_API_KEY": "test",
    "DEEPSEEK_API_KEY": "test",
    "TESTING": "true"
}

for key, value in test_env_vars.items():
    os.environ[key] = value

from app.db.base import Base
from app.core.config import settings
from app.main import app
from app.db.session import get_db
from app.core.security import get_password_hash
from app.db.models.user import User


# 配置测试数据库
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """提供测试数据库会话
    
    为每个测试函数提供一个独立的数据库会话，包括：
    1. 创建所有表
    2. 提供数据库会话
    3. 测试后清理数据
    
    Yields:
        Session: SQLAlchemy会话对象
    """
    # 重置数据库状态
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 创建测试会话
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        db.rollback()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    # 覆盖依赖项
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # 清理依赖项覆盖
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def test_user(db):
    # 创建测试用户
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@pytest.fixture(scope="function")
def test_superuser(db):
    # 创建测试超级用户
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("password"),
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@pytest.fixture(scope="function")
def token_headers(client, test_user):
    # 获取测试用户的访问令牌
    login_data = {
        "username": test_user.email,
        "password": "password",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = response.json()
    
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture(scope="function")
def superuser_token_headers(client, test_superuser):
    # 获取超级用户的访问令牌
    login_data = {
        "username": test_superuser.email,
        "password": "password",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = response.json()
    
    return {"Authorization": f"Bearer {tokens['access_token']}"}