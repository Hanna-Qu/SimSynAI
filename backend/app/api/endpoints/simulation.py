"""仿真任务相关的API端点

提供以下功能：
- 创建和管理仿真任务
- 查询任务状态和结果
- 控制任务执行
- 获取仿真数据
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from typing import List, Optional, Any, Dict
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.schemas.simulation import SimulationTask, SimulationTaskCreate, SimulationTaskUpdate, SimulationDataResponse
from app.services.simulation import SimulationService

router = APIRouter()


@router.post("/task", response_model=SimulationTask)
async def create_simulation_task(
    task_in: SimulationTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的仿真任务
    
    接收任务配置参数并创建新的仿真任务。任务将在创建后进入等待状态，
    需要通过单独的API调用来启动执行。
    
    Args:
        task_in: 任务创建参数，包含模型路径、参数配置等
        db: 数据库会话，由FastAPI依赖注入
        current_user: 当前认证用户，由安全中间件提供
    
    Returns:
        SimulationTask: 创建的任务详情
        
    Raises:
        HTTPException (400): 当任务参数无效时
        HTTPException (401): 当用户未认证时
    """
    simulation_service = SimulationService(db)
    task = await simulation_service.create_task(current_user.id, task_in)
    return task


@router.get("/", response_model=List[SimulationTask])
async def get_user_simulation_tasks(
    skip: int = Query(0, description="分页起始位置"),
    limit: int = Query(100, description="每页数量限制", le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的仿真任务列表
    
    分页获取当前用户创建的所有仿真任务。任务按创建时间倒序排列。
    
    Args:
        skip: 分页起始位置，默认0
        limit: 每页数量，默认100，最大100
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        List[SimulationTask]: 任务列表
    """
    simulation_service = SimulationService(db)
    tasks = await simulation_service.get_user_tasks(current_user.id, skip, limit)
    return tasks


@router.get("/{task_id}", response_model=SimulationTask)
async def get_simulation_task(
    task_id: str = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仿真任务详情
    
    获取指定ID的仿真任务的详细信息，包括：
    - 基本信息(名称、描述等)
    - 配置参数
    - 执行状态
    - 结果概要
    
    Args:
        task_id: 任务ID
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        SimulationTask: 任务详情
        
    Raises:
        HTTPException (404): 任务不存在时
        HTTPException (403): 无权访问该任务时
    """
    simulation_service = SimulationService(db)
    task = await simulation_service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查权限
    if task.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return task


@router.put("/{task_id}", response_model=SimulationTask)
async def update_simulation_task(
    task_id: str,
    task_in: SimulationTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新仿真任务"""
    simulation_service = SimulationService(db)
    task = await simulation_service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查权限
    if task.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 检查任务状态
    if task.status in ["running", "completed"]:
        raise HTTPException(status_code=400, detail="Cannot update running or completed task")
    
    updated_task = await simulation_service.update_task(task_id, task_in)
    if not updated_task:
        raise HTTPException(status_code=400, detail="Failed to update task")
    
    return updated_task


@router.delete("/{task_id}")
async def delete_simulation_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除仿真任务"""
    simulation_service = SimulationService(db)
    task = await simulation_service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查权限
    if task.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await simulation_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete task")
    
    return {"status": "success"}


@router.post("/{task_id}/run")
async def run_simulation_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """运行仿真任务"""
    simulation_service = SimulationService(db)
    task = await simulation_service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查权限
    if task.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 检查任务状态
    if task.status == "running":
        raise HTTPException(status_code=400, detail="Task is already running")
    
    # 在后台运行任务
    background_tasks.add_task(simulation_service.run_task, task_id)
    
    return {"status": "started"}


@router.get("/{task_id}/result", response_model=SimulationDataResponse)
async def get_simulation_result(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仿真结果"""
    simulation_service = SimulationService(db)
    task = await simulation_service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查权限
    if task.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    result = await simulation_service.get_task_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return result


@router.get("/model", response_model=List[Dict[str, Any]])
async def get_available_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取可用的仿真模型列表"""
    simulation_service = SimulationService(db)
    models = await simulation_service.get_available_models()
    return models


@router.get("/model/{model_path}/parameters", response_model=Dict[str, Any])
async def get_model_parameters(
    model_path: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取模型参数信息"""
    simulation_service = SimulationService(db)
    parameters = await simulation_service.get_model_parameters(model_path)
    if not parameters:
        raise HTTPException(status_code=404, detail="Model not found")
    return parameters


@router.get("/results/{task_id}", response_model=SimulationDataResponse)
async def get_simulation_results(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仿真结果数据"""
    simulation_service = SimulationService(db)
    result = await simulation_service.get_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # 检查权限
    task = await simulation_service.get_task(task_id)
    if not task or (task.user_id != current_user.id and not current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return result