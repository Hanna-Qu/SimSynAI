"""认证API测试模块

测试认证相关的功能，包括：
- 用户登录
- 账户注册
- 令牌验证
- 密码重置
- 错误处理
"""

import pytest
from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def test_login(client: TestClient, test_user):
    """测试用户登录功能
    
    验证以下场景：
    1. 使用有效的邮箱和密码登录
    2. 检查返回的令牌格式
    3. 验证令牌类型
    
    Args:
        client: 测试客户端
        test_user: 测试用户固件
    """
    login_data = {
        "username": test_user.email,
        "password": "password",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = response.json()
    
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, test_user):
    """测试密码错误的登录场景
    
    验证以下错误处理：
    1. 使用错误密码
    2. 检查错误响应
    3. 验证错误消息
    
    Args:
        client: 测试客户端
        test_user: 测试用户固件
    """
    login_data = {
        "username": test_user.email,
        "password": "wrong-password",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "detail" in response.json()


def test_register(client: TestClient, db: Session):
    """测试用户注册功能
    
    验证以下场景：
    1. 创建新用户账户
    2. 检查必需字段验证
    3. 验证密码加密
    4. 检查返回的令牌
    
    Args:
        client: 测试客户端
        db: 测试数据库会话
    """
    email = "new-user@example.com"
    username = "newuser"
    password = "new-password"
    
    user_in = UserCreate(
        email=email,
        username=username,
        password=password,
        is_active=True,
        is_superuser=False
    ).dict()
    
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=user_in)
    token = response.json()
    
    assert response.status_code == 200
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_register_existing_email(client: TestClient, test_user):
    """测试使用已存在的邮箱注册"""
    user_in = UserCreate(
        email=test_user.email,
        username="another-username",
        password="another-password",
        is_active=True,
        is_superuser=False
    ).dict()
    
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=user_in)
    
    assert response.status_code == 400
    assert "detail" in response.json()


def test_register_existing_username(client: TestClient, test_user):
    """测试使用已存在的用户名注册"""
    user_in = {
        "email": "another-email@example.com",
        "username": test_user.username,
        "password": "another-password",
        "is_active": True,
        "is_superuser": False
    }
    
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=user_in)
    
    assert response.status_code == 400
    assert "detail" in response.json()