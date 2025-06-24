"""
SimSynAI后端主应用模块

提供以下功能：
- FastAPI应用初始化和配置
- CORS中间件设置
- API路由注册
- 数据库初始化
- 生命周期事件处理
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

from app.api.api import api_router
from app.core.config import settings
from app.db.session import create_db_and_tables
from app.core.logging import setup_logging

# 设置日志
logger = setup_logging()

# 应用启动时间
start_time = datetime.now()

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="神经元网络仿真实验平台API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 配置CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def on_startup():
    """应用启动事件处理器
    
    执行以下初始化操作：
    1. 创建数据库表
    2. 初始化默认用户
    3. 初始化必要的目录
    4. 准备缓存
    5. 启动后台任务
    """
    logger.info("应用启动")
    create_db_and_tables()
    logger.info("数据库表初始化完成")
    
    # 初始化默认用户
    from app.db.session import SessionLocal
    from app.db.init_db import init_db
    
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("默认用户初始化完成")
    except Exception as e:
        logger.error(f"初始化默认用户失败: {e}")
    finally:
        db.close()

@app.on_event("shutdown")
async def on_shutdown():
    """应用关闭事件处理器
    
    执行以下清理操作：
    1. 关闭数据库连接
    2. 停止后台任务
    3. 清理临时文件
    """
    logger.info("应用关闭，执行清理操作")

@app.get("/")
async def root():
    """API根路径处理器
    
    Returns:
        dict: 包含欢迎信息和版本信息的响应
    """
    logger.debug("访问根路径")
    return {
        "message": "Welcome to SimSynAI API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs"
    }

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    """健康检查端点
    
    提供系统健康状态信息，用于监控和Docker健康检查
    
    Returns:
        dict: 包含健康状态信息的响应
    """
    logger.debug("健康检查请求")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": str(datetime.now() - start_time),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)