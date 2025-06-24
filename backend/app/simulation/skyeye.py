import os
import json
import asyncio
import tempfile
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime
import pandas as pd
from pathlib import Path
import uuid

from .engine import SimulationEngine, SimulationConfig, SimulationResult
from app.core.config import settings
from app.core.logging import logger


class SkyEyeAdapter(SimulationEngine):
    """SkyEye仿真引擎适配器"""
    
    def __init__(self, skyeye_path: Optional[str] = None):
        """
        初始化SkyEye仿真引擎适配器
        
        Args:
            skyeye_path: SkyEye可执行文件路径，如果为None则使用配置中的路径
        """
        self.skyeye_path = skyeye_path or settings.SKYEYE_PATH
        self.results_dir = Path(settings.SIMULATION_RESULTS_DIR)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
    async def initialize(self) -> bool:
        """初始化引擎"""
        return True

    async def validate_config(self, config: SimulationConfig) -> bool:
        """验证配置是否有效"""
        return True

    async def get_model_parameters(self, model_path: str) -> Dict[str, Any]:
        """获取模型参数"""
        return {}

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用模型列表"""
        return []

    async def get_status(self, task_id: str) -> str:
        """获取任务状态"""
        return "pending"

    async def stop_simulation(self, task_id: str) -> bool:
        """停止仿真"""
        return True
        
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
        # 创建结果目录
        result_dir = self.results_dir / task_id
        result_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建配置文件
        config_path = result_dir / "config.json"
        config = {
            "model_path": model_path,
            "parameters": parameters,
            "duration": duration,
            "step_size": step_size,
            "output_variables": output_variables
        }
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        # 准备命令行参数
        cmd = [
            str(self.skyeye_path),
            "--model", model_path,
            "--duration", str(duration),
            "--step", str(step_size),
            "--output", str(result_dir / "results.csv")
        ]
        
        # 添加参数
        for key, value in parameters.items():
            cmd.extend(["--param", f"{key}={value}"])
        
        # 添加输出变量
        for var in output_variables:
            cmd.extend(["--output-var", var])
        
        try:
            # 运行仿真
            logger.info(f"运行仿真任务 {task_id}")
            logger.debug(f"命令: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # 记录输出
            with open(result_dir / "stdout.log", "wb") as f:
                f.write(stdout)
            
            with open(result_dir / "stderr.log", "wb") as f:
                f.write(stderr)
            
            # 检查是否成功
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8')
                logger.error(f"仿真失败: {error_msg}")
                return {
                    "status": "failed",
                    "error_message": error_msg
                }
            
            # 读取结果
            results_path = result_dir / "results.csv"
            if not results_path.exists():
                return {
                    "status": "failed",
                    "error_message": "仿真完成但未生成结果文件"
                }
            
            # 解析结果
            df = pd.read_csv(results_path)
            time_points = df["time"].tolist()
            
            data = {}
            for var in output_variables:
                if var in df.columns:
                    data[var] = df[var].tolist()
            
            return {
                "status": "completed",
                "data": data,
                "time_points": time_points,
                "metadata": {
                    "model": model_path,
                    "duration": duration,
                    "step_size": step_size,
                    "parameters": parameters
                }
            }
            
        except Exception as e:
            logger.exception(f"仿真执行异常: {str(e)}")
            return {
                "status": "failed",
                "error_message": str(e)
            }
    
    async def get_model_info(self, model_path: str) -> Dict[str, Any]:
        """
        获取模型信息
        
        Args:
            model_path: 模型文件路径
            
        Returns:
            Dict[str, Any]: 模型信息
        """
        try:
            cmd = [
                str(self.skyeye_path),
                "--info",
                model_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                return {
                    "status": "error",
                    "message": stderr.decode('utf-8')
                }
            
            # 解析输出
            info_text = stdout.decode('utf-8')
            
            # 这里假设SkyEye输出JSON格式的模型信息
            # 如果不是，需要根据实际输出格式进行解析
            try:
                info = json.loads(info_text)
                return {
                    "status": "success",
                    "info": info
                }
            except json.JSONDecodeError:
                # 如果不是JSON格式，返回原始文本
                return {
                    "status": "success",
                    "info": {
                        "description": info_text,
                        "raw_output": info_text
                    }
                }
                
        except Exception as e:
            logger.exception(f"获取模型信息异常: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def list_models(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出可用模型
        
        Args:
            directory: 模型目录，如果为None则使用默认目录
            
        Returns:
            List[Dict[str, Any]]: 模型列表
        """
        try:
            model_dir = Path(directory) if directory else Path(self.skyeye_path).parent / "models"
            
            if not model_dir.exists():
                return []
            
            models = []
            for file in model_dir.glob("*.mdl"):
                models.append({
                    "name": file.stem,
                    "path": str(file),
                    "size": file.stat().st_size,
                    "modified": file.stat().st_mtime
                })
            
            return models
        except Exception as e:
            logger.exception(f"列出模型异常: {str(e)}")
            return [] 