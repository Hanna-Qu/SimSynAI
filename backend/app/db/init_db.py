"""
数据库初始化脚本

负责创建初始数据，包括：
- 默认超级管理员
- 默认测试用户
- 基础配置数据
"""

import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.user import User
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """初始化数据库
    
    创建默认用户和基础配置数据
    
    Args:
        db: 数据库会话
    """
    # 检查是否已有超级管理员
    superuser = db.query(User).filter(User.is_superuser == True).first()
    if not superuser:
        # 创建默认超级管理员
        superuser = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            username=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            full_name="管理员",
            is_active=True,
            is_superuser=True,
        )
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        logger.info(f"创建默认超级管理员: {superuser.username}")
    
    # 检查是否已有测试用户
    test_user = db.query(User).filter(User.username == settings.DEFAULT_USER).first()
    if not test_user:
        # 创建默认测试用户
        test_user = User(
            email=settings.DEFAULT_USER_EMAIL,
            username=settings.DEFAULT_USER,
            hashed_password=get_password_hash(settings.DEFAULT_USER_PASSWORD),
            full_name="测试用户",
            is_active=True,
            is_superuser=False,
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        logger.info(f"创建默认测试用户: {test_user.username}") 