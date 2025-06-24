import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.simulation.engine import SimulationResult


@pytest.fixture
def mock_simulation_result():
    """模拟仿真结果"""
    with patch("app.services.simulation.SimulationService.get_task_result") as mock:
        result = SimulationResult(
            task_id="test-task-id",
            status="completed",
            data={"position": [0.1, 0.2, 0.3], "velocity": [1.0, 1.1, 1.2]},
            time_points=[0.0, 0.1, 0.2],
            metadata={"model": "test/model.skyeye"}
        )
        mock.return_value = result
        yield result


def test_get_visualization_data(client: TestClient, token_headers, mock_simulation_result):
    """测试获取可视化数据"""
    # 需要先创建一个任务
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
    
    # 获取可视化数据
    response = client.get(
        f"{settings.API_V1_STR}/visualization/data/{task_id}",
        headers=token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "test-task-id"  # 这里使用模拟返回的ID
    assert data["status"] == "completed"
    assert "data" in data
    assert "metadata" in data


def test_get_visualization_templates(client: TestClient, token_headers):
    """测试获取可视化模板"""
    response = client.get(
        f"{settings.API_V1_STR}/visualization/templates",
        headers=token_headers
    )
    
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) >= 1
    
    # 验证模板内容
    line_chart = next((t for t in templates if t["id"] == "line_chart"), None)
    assert line_chart is not None
    assert line_chart["name"] == "折线图"
    assert line_chart["chart_type"] == "line"
    assert "default_options" in line_chart
    
    multi_line_chart = next((t for t in templates if t["id"] == "multi_line_chart"), None)
    assert multi_line_chart is not None
    assert multi_line_chart["name"] == "多变量折线图"
    
    scatter_chart = next((t for t in templates if t["id"] == "scatter_chart"), None)
    assert scatter_chart is not None
    assert scatter_chart["name"] == "散点图"
    assert scatter_chart["chart_type"] == "scatter" 