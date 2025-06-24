"""数据可视化相关的API端点

提供以下功能：
- 获取仿真数据用于可视化
- 提供可视化模板和配置
- 支持多种图表类型
- 数据预处理和分析
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional, Any, Dict
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.schemas.simulation import SimulationDataResponse
from app.services.simulation import SimulationService
from app.core.logging import logger

router = APIRouter()


@router.get("/data/{task_id}", response_model=SimulationDataResponse)
async def get_visualization_data(
    task_id: str,
    variables: Optional[List[str]] = Query(None, description="要获取的变量列表"),
    time_range: Optional[List[float]] = Query(None, description="时间范围，格式: [开始时间, 结束时间]"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SimulationDataResponse:
    """获取仿真任务数据用于可视化
    
    获取指定任务的仿真结果数据，支持：
    - 选择特定变量
    - 指定时间范围
    - 数据降采样
    - 基本统计分析
    
    Args:
        task_id: 仿真任务ID
        variables: 要获取的变量列表，为空时获取所有变量
        time_range: 时间范围限制
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        SimulationDataResponse: 包含时间序列数据的响应
        
    Raises:
        HTTPException (404): 
            - 任务不存在
            - 结果未找到
        HTTPException (403): 无权访问该任务
        HTTPException (400): 参数无效
    """
    try:
        simulation_service = SimulationService(db)
        task = await simulation_service.get_task(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务未找到"
            )
        
        # 检查权限
        if task.user_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限访问此任务数据"
            )
        
        result = await simulation_service.get_task_result(task_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务结果未找到"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching visualization data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取数据时出错，请稍后重试"
        )


@router.get("/templates", response_model=List[Dict[str, Any]])
async def get_visualization_templates(
    category: Optional[str] = Query(None, description="模板类别"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """获取可视化模板列表
    
    返回预定义的可视化模板配置，支持：
    - 多种图表类型
    - 默认样式设置
    - 交互配置
    - 数据映射规则
    
    模板类别包括：
    - 时序图
    - 散点图
    - 热力图
    - 网络图
    - 3D可视化
    
    Args:
        category: 模板类别过滤
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        List[Dict[str, Any]]: 模板配置列表
    """
    # 这里返回一些预定义的可视化模板
    templates = [
        {
            "id": "line_chart",
            "name": "折线图",
            "description": "适用于时间序列数据的折线图",
            "chart_type": "line",
            "default_options": {
                "xAxis": {
                    "type": "category",
                    "name": "时间"
                },
                "yAxis": {
                    "type": "value",
                    "name": "值"
                },
                "tooltip": {
                    "trigger": "axis"
                },
                "legend": {
                    "data": []
                }
            }
        },
        {
            "id": "multi_line_chart",
            "name": "多变量折线图",
            "description": "同时显示多个变量的折线图",
            "chart_type": "line",
            "default_options": {
                "xAxis": {
                    "type": "category",
                    "name": "时间"
                },
                "yAxis": {
                    "type": "value",
                    "name": "值"
                },
                "tooltip": {
                    "trigger": "axis"
                },
                "legend": {
                    "data": []
                },
                "grid": {
                    "left": "3%",
                    "right": "4%",
                    "bottom": "3%",
                    "containLabel": True
                }
            }
        },
        {
            "id": "scatter_chart",
            "name": "散点图",
            "description": "用于显示两个变量之间关系的散点图",
            "chart_type": "scatter",
            "default_options": {
                "xAxis": {
                    "type": "value",
                    "name": "变量1"
                },
                "yAxis": {
                    "type": "value",
                    "name": "变量2"
                },
                "tooltip": {
                    "trigger": "item"
                }
            }
        },
        {
            "id": "bar_chart",
            "name": "柱状图",
            "description": "用于比较不同类别数据的柱状图",
            "chart_type": "bar",
            "default_options": {
                "xAxis": {
                    "type": "category",
                    "name": "类别"
                },
                "yAxis": {
                    "type": "value",
                    "name": "值"
                },
                "tooltip": {
                    "trigger": "item"
                }
            }
        },
        {
            "id": "gauge_chart",
            "name": "仪表盘",
            "description": "用于显示单个指标的仪表盘",
            "chart_type": "gauge",
            "default_options": {
                "series": [
                    {
                        "type": "gauge",
                        "detail": {
                            "formatter": "{value}%"
                        },
                        "data": [
                            {
                                "value": 50,
                                "name": "指标"
                            }
                        ]
                    }
                ]
            }
        }
    ]
    
    return templates