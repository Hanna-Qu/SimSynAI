"""仿真API测试模块

测试仿真相关的功能，包括：
- 任务创建和管理
- 参数验证
- 结果获取
- 错误处理
- 数据持久化

使用Mock对象模拟仿真引擎，避免实际执行耗时的仿真计算。
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from typing import Dict, Any, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.simulation.engine import SimulationEngine, SimulationConfig, SimulationResult
from app.schemas.simulation import SimulationTaskCreate


@pytest.fixture
def mock_simulation_engine():
    """模拟仿真引擎固件
    
    提供以下模拟功能：
    1. 仿真任务执行
    2. 模型管理
    3. 参数验证
    4. 结果生成
    
    Returns:
        MagicMock: 模拟的仿真引擎实例
    """
    with patch("app.services.simulation.SkyEyeAdapter") as mock:
        engine = MagicMock(spec=SimulationEngine)
        
        # 模拟运行仿真
        async def mock_run_simulation(config: SimulationConfig, task_id: str) -> SimulationResult:
            """模拟仿真执行过程
            
            生成模拟的时间序列数据，包括：
            - 位置数据
            - 速度数据
            - 时间点
            - 元数据
            """
            return SimulationResult(
                task_id=task_id,
                status="completed",
                data={
                    "position": [0.1, 0.2, 0.3], 
                    "velocity": [1.0, 1.1, 1.2]
                },
                time_points=[0.0, 0.1, 0.2],
                metadata={"model": config.model_path}
            )
        
        engine.run_simulation.side_effect = mock_run_simulation
        
        # 模拟获取可用模型
        async def mock_get_available_models() -> List[Dict[str, str]]:
            """模拟模型列表获取
            
            返回预定义的测试模型信息。
            """
            return [
                {
                    "name": "test_model",
                    "path": "test/model.skyeye",
                    "description": "测试模型"
                }
            ]
        
        engine.get_available_models.side_effect = mock_get_available_models
        
        # 模拟获取模型参数
        async def mock_get_model_parameters(model_path: str) -> Dict[str, Any]:
            """模拟模型参数获取
            
            返回预定义的参数模式，包括：
            - 参数类型和默认值
            - 可用的输出变量
            """
            return {
                "parameters": {
                    "param1": {
                        "type": "float",
                        "default": 1.0,
                        "description": "测试参数"
                    }
                },
                "outputs": ["position", "velocity"]
            }
        
        engine.get_model_parameters.side_effect = mock_get_model_parameters
        
        mock.return_value = engine
        yield engine


def test_create_simulation_task(client: TestClient, token_headers):
    """测试创建仿真任务"""
    task_data = {
        "name": "测试任务",
        "description": "这是一个测试任务",
        "parameters": {
            "initial_state": {"position": 0, "velocity": 0},
            "control_params": {"gain": 1.0}
        },
        "model_path": "test/model.skyeye",
        "duration": 10.0,
        "step_size": 0.1,
        "output_variables": ["position", "velocity"]
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/simulation/task",
        headers=token_headers,
        json=task_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "测试任务"
    assert data["status"] == "pending"
    assert "id" in data


def test_get_simulation_task(client: TestClient, token_headers, mock_simulation_engine):
    """测试获取仿真任务"""
    # 先创建一个任务
    task_data = {
        "name": "测试任务",
        "description": "这是一个测试任务",
        "parameters": {
            "initial_state": {"position": 0, "velocity": 0},
            "control_params": {"gain": 1.0}
        },
        "model_path": "test/model.skyeye",
        "duration": 10.0,
        "step_size": 0.1,
        "output_variables": ["position", "velocity"]
    }
    
    create_response = client.post(
        f"{settings.API_V1_STR}/simulation/task",
        headers=token_headers,
        json=task_data
    )
    
    task_id = create_response.json()["id"]
    
    # 获取任务详情
    response = client.get(
        f"{settings.API_V1_STR}/simulation/task/{task_id}",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "测试任务"


def test_get_simulation_tasks(client: TestClient, token_headers):
    """测试获取仿真任务列表"""
    # 先创建一个任务
    task_data = {
        "name": "测试任务",
        "description": "这是一个测试任务",
        "parameters": {
            "initial_state": {"position": 0, "velocity": 0},
            "control_params": {"gain": 1.0}
        },
        "model_path": "test/model.skyeye",
        "duration": 10.0,
        "step_size": 0.1,
        "output_variables": ["position", "velocity"]
    }
    
    client.post(
        f"{settings.API_V1_STR}/simulation/task",
        headers=token_headers,
        json=task_data
    )
    
    # 获取任务列表
    response = client.get(
        f"{settings.API_V1_STR}/simulation/tasks",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    # 验证任务内容
    task = next((t for t in data if t["name"] == "测试任务"), None)
    assert task is not None
    assert task["description"] == "这是一个测试任务"


def test_execute_simulation_task(client: TestClient, token_headers, mock_simulation_engine):
    """测试执行仿真任务"""
    # 先创建一个任务
    task_data = {
        "name": "测试任务",
        "description": "这是一个测试任务",
        "parameters": {
            "initial_state": {"position": 0, "velocity": 0},
            "control_params": {"gain": 1.0}
        },
        "model_path": "test/model.skyeye",
        "duration": 10.0,
        "step_size": 0.1,
        "output_variables": ["position", "velocity"]
    }
    
    create_response = client.post(
        f"{settings.API_V1_STR}/simulation/task",
        headers=token_headers,
        json=task_data
    )
    
    task_id = create_response.json()["id"]
    
    # 执行任务
    response = client.post(
        f"{settings.API_V1_STR}/simulation/task/{task_id}/execute",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == "running"


def test_get_available_models(client: TestClient, token_headers, mock_simulation_engine):
    """测试获取可用模型"""
    response = client.get(
        f"{settings.API_V1_STR}/simulation/models",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    model = data[0]
    assert model["name"] == "test_model"
    assert model["path"] == "test/model.skyeye"


def test_get_model_parameters(client: TestClient, token_headers, mock_simulation_engine):
    """测试获取模型参数"""
    model_path = "test/model.skyeye"
    
    response = client.get(
        f"{settings.API_V1_STR}/simulation/model/{model_path}/parameters",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "parameters" in data
    assert "param1" in data["parameters"]
    assert data["parameters"]["param1"]["default"] == 1.0