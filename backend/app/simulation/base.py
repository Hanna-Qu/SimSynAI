from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class SimulationEngine(ABC):
    """仿真引擎基类"""
    
    @abstractmethod
    async def run_simulation(
        self,
        model_path: str,
        parameters: Dict[str, Any],
        duration: float,
        step_size: float,
        output_variables: List[str],
        task_id: str
    ) -> Dict[str, Any]:
        """
        运行仿真
        
        Args:
            model_path: 模型文件路径
            parameters: 仿真参数
            duration: 仿真时长
            step_size: 仿真步长
            output_variables: 输出变量列表
            task_id: 任务ID
            
        Returns:
            Dict[str, Any]: 仿真结果
        """
        pass
    
    @abstractmethod
    async def get_model_info(self, model_path: str) -> Dict[str, Any]:
        """
        获取模型信息
        
        Args:
            model_path: 模型文件路径
            
        Returns:
            Dict[str, Any]: 模型信息
        """
        pass
    
    @abstractmethod
    async def list_models(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出可用模型
        
        Args:
            directory: 模型目录，如果为None则使用默认目录
            
        Returns:
            List[Dict[str, Any]]: 模型列表
        """
        pass 