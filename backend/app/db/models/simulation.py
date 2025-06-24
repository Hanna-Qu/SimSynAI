from sqlalchemy import Column, String, Float, JSON, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.db.base_class import Base


class SimulationTask(Base):
    """仿真任务模型"""
    __tablename__ = "simulation_tasks"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending, running, completed, failed
    parameters = Column(JSON, nullable=False)
    model_path = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    step_size = Column(Float, nullable=False)
    output_variables = Column(JSON, nullable=False)
    result_path = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    user = relationship("User", back_populates="simulation_tasks")
    result = relationship("SimulationResult", back_populates="task", uselist=False)
    chat_messages = relationship("ChatMessage", back_populates="task")


class SimulationResult(Base):
    """仿真结果模型"""
    __tablename__ = "simulation_results"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("simulation_tasks.id"), nullable=False)
    data_path = Column(String)  # 数据文件路径
    result_metadata = Column(JSON, nullable=True)  # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False)
    data = Column(JSON, nullable=True)
    time_points = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # 关系
    task = relationship("SimulationTask", back_populates="result")

    def __repr__(self):
        return f"<SimulationResult(id={self.id}, task_id={self.task_id}, status={self.status})>" 