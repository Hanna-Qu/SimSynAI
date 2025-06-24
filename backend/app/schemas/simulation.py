from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime


class SimulationConfigBase(BaseModel):
    """仿真配置基础模式"""
    parameters: Dict[str, Any]
    model_path: Optional[str] = None
    duration: float
    step_size: float
    output_variables: List[str]


class SimulationTaskBase(BaseModel):
    """仿真任务基础模式"""
    name: str
    description: Optional[str] = None
    model_path: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    duration: float
    step_size: float
    output_variables: List[str] = Field(default_factory=list)
    status: Optional[str] = "pending"
    result_path: Optional[str] = None
    error_message: Optional[str] = None


class SimulationTaskCreate(SimulationTaskBase):
    """仿真任务创建模式"""
    pass


class SimulationTaskUpdate(BaseModel):
    """仿真任务更新模式"""
    name: Optional[str] = None
    description: Optional[str] = None
    model_path: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    duration: Optional[float] = None
    step_size: Optional[float] = None
    output_variables: Optional[List[str]] = None
    status: Optional[str] = None


class SimulationTask(SimulationTaskBase):
    """仿真任务模式（返回给API）"""
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class SimulationResultBase(BaseModel):
    """仿真结果基础模式"""
    task_id: str
    data_path: str
    metadata: Optional[Dict[str, Any]] = None


class SimulationResultCreate(SimulationResultBase):
    """仿真结果创建模式"""
    pass


class SimulationResultInDBBase(SimulationResultBase):
    """数据库中的仿真结果基础模式"""
    id: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


# 直接继承SimulationResultInDBBase，避免重复定义
class SimulationResult(SimulationResultInDBBase):
    """仿真结果模式（返回给API）"""
    pass


class SimulationDataPoint(BaseModel):
    """仿真数据点模式"""
    time: float
    values: Dict[str, float]


class SimulationDataResponse(BaseModel):
    """仿真数据响应模式"""
    status: str
    data: Dict[str, List[float]]
    time_points: List[float]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

    model_config = {"from_attributes": True}