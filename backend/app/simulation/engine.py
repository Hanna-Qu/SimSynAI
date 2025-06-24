from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class SimulationConfig(BaseModel):
    """仿真配置模型"""
    parameters: Dict[str, Any]
    model_path: Optional[str] = None
    duration: float
    step_size: float
    output_variables: List[str]


class SimulationResult(BaseModel):
    """仿真结果模型"""
    task_id: str
    status: str
    data: Dict[str, List[float]]
    time_points: List[float]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None


class SimulationEngine(ABC):
    """仿真引擎抽象基类
    
    定义了神经元仿真引擎的标准接口。
    具体的仿真引擎实现(如SkyEye)需要继承此类并实现所有抽象方法。
    """
    
    @abstractmethod
    async def initialize(self) -> bool:
        """初始化引擎
        
        执行引擎启动前的必要初始化工作，如:
        - 检查依赖项
        - 加载配置
        - 准备工作目录
        - 初始化资源
        
        Returns:
            bool: 初始化是否成功
        """
        pass
    
    @abstractmethod
    async def validate_config(self, config: SimulationConfig) -> Dict[str, Any]:
        """验证配置有效性
        
        检查仿真参数配置是否合法有效，包括:
        - 必需参数是否完整
        - 参数值是否在合理范围内
        - 模型文件是否存在且格式正确
        - 输出变量是否可用
        
        Args:
            config: 仿真配置对象
            
        Returns:
            Dict[str, Any]: 验证结果，包含是否通过和具体问题说明
            
        Raises:
            ValueError: 当配置存在严重问题时抛出
        """
        pass
    
    @abstractmethod
    async def run_simulation(self, config: SimulationConfig, task_id: str) -> SimulationResult:
        """运行仿真任务
        
        根据给定配置执行神经元网络仿真计算，包括:
        - 准备仿真环境
        - 加载模型
        - 设置参数
        - 执行计算
        - 收集结果
        
        Args:
            config: 仿真配置对象
            task_id: 任务ID，用于标识和追踪任务
            
        Returns:
            SimulationResult: 仿真结果对象，包含输出数据和元信息
            
        Raises:
            SimulationError: 仿真过程中出现错误时抛出
        """
        pass
    
    @abstractmethod
    async def get_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态
        
        查询指定任务的运行状态，返回包括:
        - 运行阶段(pending/running/completed/failed)
        - 进度百分比
        - 运行时间
        - 资源使用情况
        - 错误信息(如果有)
        
        Args:
            task_id: 任务ID
            
        Returns:
            Dict[str, Any]: 任务状态信息
        """
        pass
    
    @abstractmethod
    async def stop_simulation(self, task_id: str) -> bool:
        """停止仿真任务
        
        安全地终止正在运行的仿真任务，包括:
        - 停止计算
        - 清理资源
        - 保存中间结果
        
        Args:
            task_id: 要停止的任务ID
            
        Returns:
            bool: 是否成功停止任务
        """
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用的仿真模型"""
        pass
    
    @abstractmethod
    async def get_model_parameters(self, model_path: str) -> Dict[str, Any]:
        """获取模型参数"""
        pass