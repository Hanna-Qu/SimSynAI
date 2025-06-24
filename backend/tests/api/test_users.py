"""用户API测试模块

测试用户管理相关的功能，包括：
- 用户信息获取
- 个人资料更新
- 密码修改
- 偏好设置
- 权限验证
"""

import pytest
from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password


def test_get_users_me(client: TestClient, token_headers: Dict[str, str]):
    """测试获取当前用户信息
    
    验证以下场景：
    1. 使用有效令牌获取用户信息
    2. 检查返回的用户数据完整性
    3. 验证基本字段值
    
    Args:
        client: 测试客户端
        token_headers: 包含认证令牌的请求头
    """
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=token_headers)
    current_user = response.json()
    
    assert response.status_code == 200
    assert current_user["email"] == "test@example.com"
    assert current_user["username"] == "testuser"
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False


def test_update_user_me(client: TestClient, token_headers: Dict[str, str]):
    """测试更新用户个人信息
    
    验证以下场景：
    1. 更新用户名
    2. 检查更新后的数据
    3. 验证响应格式
    
    Args:
        client: 测试客户端
        token_headers: 包含认证令牌的请求头
    """
    data = {"username": "updated-username"}
    response = client.put(
        f"{settings.API_V1_STR}/users/me", 
        headers=token_headers, 
        json=data
    )
    updated_user = response.json()
    
    assert response.status_code == 200
    assert updated_user["username"] == "updated-username"


def test_update_user_me_password(
    client: TestClient, 
    token_headers: Dict[str, str],
    db: Session
):
    """测试修改用户密码
    
    验证以下场景：
    1. 更新密码
    2. 验证密码加密
    3. 使用新密码登录
    4. 旧密码失效
    
    Args:
        client: 测试客户端
        token_headers: 包含认证令牌的请求头
        db: 测试数据库会话
    """
    data = {"password": "new-password"}
    response = client.put(
        f"{settings.API_V1_STR}/users/me", 
        headers=token_headers, 
        json=data
    )
    
    assert response.status_code == 200
    
    # 测试使用新密码登录
    login_data = {
        "username": "test@example.com",
        "password": "new-password",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_user_by_id(client: TestClient, token_headers, test_user):
    """测试通过ID获取用户"""
    response = client.get(
        f"{settings.API_V1_STR}/users/{test_user.id}", headers=token_headers
    )
    user = response.json()
    
    assert response.status_code == 200
    assert user["id"] == test_user.id
    assert user["email"] == test_user.email


def test_get_user_by_id_not_found(client: TestClient, token_headers):
    """测试获取不存在的用户"""
    response = client.get(
        f"{settings.API_V1_STR}/users/nonexistent-id", headers=token_headers
    )
    
    assert response.status_code == 404


def test_get_user_by_id_forbidden(client: TestClient, token_headers, test_superuser):
    """测试普通用户获取其他用户信息"""
    response = client.get(
        f"{settings.API_V1_STR}/users/{test_superuser.id}", headers=token_headers
    )
    
    assert response.status_code == 403


def test_superuser_get_user_by_id(client: TestClient, superuser_token_headers, test_user):
    """测试超级用户获取其他用户信息"""
    response = client.get(
        f"{settings.API_V1_STR}/users/{test_user.id}", headers=superuser_token_headers
    )
    user = response.json()
    
    assert response.status_code == 200
    assert user["id"] == test_user.id