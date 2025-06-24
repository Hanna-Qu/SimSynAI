from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建SQLAlchemy引擎
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    echo=settings.SQLALCHEMY_ECHO
)

# 创建SessionLocal类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取数据库会话依赖
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建数据库表
def create_db_and_tables():
    """创建数据库表"""
    from app.db.base import Base
    Base.metadata.create_all(bind=engine) 