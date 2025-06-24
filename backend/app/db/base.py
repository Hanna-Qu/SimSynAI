"""
导入所有模型，以便Alembic可以检测到它们
"""

from app.db.base_class import Base
from app.db.models.user import User
from app.db.models.chat import ChatMessage, ChatSession
from app.db.models.simulation import SimulationTask, SimulationResult 