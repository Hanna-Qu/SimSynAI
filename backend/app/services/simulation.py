import os
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models.simulation import SimulationTask, SimulationResult
from app.schemas.simulation import (
    SimulationTaskCreate, 
    SimulationTaskUpdate,
    SimulationTask as SimulationTaskSchema,
    SimulationDataResponse
)
from app.simulation.engine import SimulationConfig
from app.simulation.skyeye import SkyEyeAdapter
from app.core.logging import logger


class SimulationService:
    """仿真服务类
    
    处理神经元网络仿真的核心业务逻辑，包括：
    - 仿真任务的创建、运行和管理
    - 仿真结果的存储和检索
    - 仿真参数的验证和优化
    - 多用户任务调度
    """
    
    def __init__(self, db: Session, simulation_engine: Optional[SkyEyeAdapter] = None):
        """初始化仿真服务
        
        Args:
            db: SQLAlchemy数据库会话
            simulation_engine: 仿真引擎实例，默认创建新的SkyEye实例
        """
        self.db = db
        self.simulation_engine = simulation_engine or SkyEyeAdapter()
        self.results_dir = os.environ.get("SIMULATION_RESULTS_DIR", "./results")
        
        # 确保结果目录存在
        os.makedirs(self.results_dir, exist_ok=True)
    
    async def create_task(self, user_id: str, task_in: SimulationTaskCreate) -> SimulationTaskSchema:
        """创建新的仿真任务
        
        创建任务记录并进行初始化配置，包括：
        - 生成唯一任务ID
        - 创建数据库记录
        - 准备结果存储路径
        - 验证模型和参数
        
        Args:
            user_id: 创建任务的用户ID
            task_in: 任务创建请求数据
            
        Returns:
            SimulationTaskSchema: 创建的任务信息
            
        Raises:
            ValueError: 当任务参数无效时
            IOError: 当模型文件不可访问时
        """
        task_id = str(uuid.uuid4())
        
        # 创建任务记录
        task = SimulationTask(
            id=task_id,
            user_id=user_id,
            name=task_in.name,
            description=task_in.description,
            model_path=task_in.model_path,
            parameters=task_in.parameters,
            duration=task_in.duration,
            step_size=task_in.step_size,
            output_variables=task_in.output_variables,
            status="pending"
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return SimulationTaskSchema.from_orm(task)
    
    async def get_task(self, task_id: str) -> Optional[SimulationTaskSchema]:
        """获取任务详情"""
        task = self.db.query(SimulationTask).filter(SimulationTask.id == task_id).first()
        if not task:
            return None
        
        return SimulationTaskSchema.from_orm(task)
    
    async def get_tasks(self, user_id: str, skip: int = 0, limit: int = 100) -> List[SimulationTaskSchema]:
        """获取用户的任务列表"""
        tasks = self.db.query(SimulationTask).filter(
            SimulationTask.user_id == user_id
        ).order_by(SimulationTask.created_at.desc()).offset(skip).limit(limit).all()
        
        return [SimulationTaskSchema.from_orm(task) for task in tasks]
    
    async def update_task(self, task_id: str, task_in: SimulationTaskUpdate) -> Optional[SimulationTaskSchema]:
        """更新任务"""
        task = self.db.query(SimulationTask).filter(SimulationTask.id == task_id).first()
        if not task:
            return None
        
        # 检查任务状态
        if task.status in ["running", "completed"]:
            return None
        
        # 更新任务
        update_data = task_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return SimulationTaskSchema.from_orm(task)
    
    async def execute_task(self, task_id: str) -> Optional[SimulationTaskSchema]:
        """执行仿真任务"""
        task = self.db.query(SimulationTask).filter(SimulationTask.id == task_id).first()
        if not task:
            return None
        
        # 更新任务状态为运行中
        task.status = "running"
        self.db.add(task)
        self.db.commit()
        
        try:
            # 创建仿真配置
            config = SimulationConfig(
                parameters=task.parameters,
                model_path=task.model_path,
                duration=task.duration,
                step_size=task.step_size,
                output_variables=task.output_variables
            )
            
            # 运行仿真
            result = await self.simulation_engine.run_simulation(config, task_id)
            
            # 保存结果数据到文件
            result_path = os.path.join(self.results_dir, f"{task_id}.json")
            with open(result_path, "w") as f:
                json.dump({
                    "task_id": result.task_id,
                    "status": result.status,
                    "data": result.data,
                    "time_points": result.time_points,
                    "metadata": result.metadata,
                    "error_message": result.error_message
                }, f)
            
            # 更新任务状态
            task.status = result.status
            task.result_path = result_path
            task.error_message = result.error_message
            task.completed_at = datetime.now()
            
            # 创建结果记录
            db_result = SimulationResult(
                id=str(uuid.uuid4()),
                task_id=task_id,
                data_path=result_path,
                metadata=result.metadata
            )
            
            self.db.add(task)
            self.db.add(db_result)
            self.db.commit()
            self.db.refresh(task)
            
            return SimulationTaskSchema.from_orm(task)
            
        except Exception as e:
            logger.exception(f"仿真任务运行异常: {str(e)}")
            
            # 更新任务状态为失败
            task.status = "failed"
            task.error_message = str(e)
            task.completed_at = datetime.now()
            
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            return SimulationTaskSchema.from_orm(task)
    
    async def get_task_result(self, task_id: str) -> Optional[SimulationDataResponse]:
        """获取任务结果数据"""
        task = self.db.query(SimulationTask).filter(SimulationTask.id == task_id).first()
        if not task:
            return None
        
        if not task.result_path or not os.path.exists(task.result_path):
            return SimulationDataResponse(
                task_id=task_id,
                status=task.status,
                data=[],
                metadata={},
                error_message="结果数据不可用"
            )
        
        try:
            # 读取结果数据
            with open(task.result_path, "r") as f:
                result_data = json.load(f)
            
            # 转换为响应格式
            data_points = []
            time_points = result_data.get("time_points", [])
            data = result_data.get("data", {})
            
            for i, t in enumerate(time_points):
                point_values = {}
                for var, values in data.items():
                    if i < len(values):
                        point_values[var] = values[i]
                
                data_points.append({
                    "time": t,
                    "values": point_values
                })
            
            return SimulationDataResponse(
                task_id=task_id,
                status=task.status,
                data=data_points,
                metadata=result_data.get("metadata", {}),
                error_message=result_data.get("error_message")
            )
            
        except Exception as e:
            return SimulationDataResponse(
                task_id=task_id,
                status=task.status,
                data=[],
                metadata={},
                error_message=f"读取结果数据失败: {str(e)}"
            )
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用的仿真模型"""
        try:
            return await self.simulation_engine.get_available_models()
        except Exception as e:
            logger.exception(f"获取可用模型异常: {str(e)}")
            return []
    
    async def get_model_parameters(self, model_path: str) -> Dict[str, Any]:
        """获取模型参数"""
        return await self.simulation_engine.get_model_parameters(model_path)