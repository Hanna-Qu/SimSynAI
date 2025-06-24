import uvicorn
import logging
import sys
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.db.session import create_db_and_tables

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SimSynAI API",
    description="智能化仿真平台API",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("应用启动中...")
    # 创建数据库表
    create_db_and_tables()
    logger.info("数据库表创建完成")
    
    # 初始化数据库
    from app.db.init_db import init_db
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        logger.info("初始化数据库数据...")
        init_db(db)
        logger.info("数据库初始化完成")
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "欢迎使用SimSynAI API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 