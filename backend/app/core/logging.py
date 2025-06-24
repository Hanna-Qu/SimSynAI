import sys
import logging
from pathlib import Path
from loguru import logger
from pydantic import BaseModel

from app.core.config import settings


class LogConfig(BaseModel):
    """日志配置"""
    LOG_LEVEL: str = settings.LOG_LEVEL
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_FILE_PATH: Path = Path("logs/app.log")


# 配置日志
def setup_logging():
    """设置日志配置"""
    config = LogConfig()
    
    # 确保日志目录存在
    config.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # 移除默认处理器
    logger.remove()
    
    # 添加控制台处理器
    logger.add(
        sys.stderr,
        format=config.LOG_FORMAT,
        level=config.LOG_LEVEL,
        colorize=True,
    )
    
    # 添加文件处理器
    logger.add(
        config.LOG_FILE_PATH,
        format=config.LOG_FORMAT,
        level=config.LOG_LEVEL,
        rotation="10 MB",
        compression="zip",
        retention="1 month",
    )
    
    # 拦截标准库日志
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # 获取对应的Loguru级别
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            
            # 查找调用者
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            
            # 使用Loguru记录日志
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
    
    # 配置标准库日志拦截
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    
    # 替换uvicorn和FastAPI的日志处理器
    for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]
    
    return logger 