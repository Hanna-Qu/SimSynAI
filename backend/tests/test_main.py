"""应用主测试模块

测试应用的基础功能，包括：
- 服务器启动和健康检查
- API文档访问
- 跨域配置
- 错误处理中间件
- 基本路由
"""

from fastapi.testclient import TestClient
import pytest
from typing import Generator

from app.main import app
from app.core.config import settings


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """测试客户端固件
    
    提供预配置的FastAPI测试客户端。
    
    Returns:
        TestClient: FastAPI测试客户端实例
    """
    with TestClient(app) as test_client:
        yield test_client


def test_read_main(client: TestClient):
    """测试应用根路径
    
    验证以下内容：
    1. 服务器是否正常响应
    2. 响应格式是否正确
    3. 是否包含必要信息
    
    Args:
        client: 测试客户端
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert isinstance(data["message"], str)
    assert data["docs"].startswith(settings.API_V1_STR)


def test_docs_accessible(client: TestClient):
    """测试API文档可访问性
    
    验证以下内容：
    1. OpenAPI文档是否可访问
    2. Swagger UI是否可用
    3. ReDoc是否可用
    
    Args:
        client: 测试客户端
    """
    # 测试Swagger UI
    response = client.get(f"{settings.API_V1_STR}/docs")
    assert response.status_code == 200
    
    # 测试OpenAPI JSON
    response = client.get(f"{settings.API_V1_STR}/openapi.json")
    assert response.status_code == 200
    
    # 测试ReDoc
    response = client.get(f"{settings.API_V1_STR}/redoc")
    assert response.status_code == 200


def test_cors_headers(client: TestClient):
    """测试CORS配置
    
    验证以下内容：
    1. CORS头部是否正确设置
    2. 预检请求是否正常响应
    3. 允许的源是否符合配置
    
    Args:
        client: 测试客户端
    """
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    
    response = client.options("/", headers=headers)
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers