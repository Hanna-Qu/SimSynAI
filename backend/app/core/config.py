import os
import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    PROJECT_NAME: str = "SimSynAI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # 默认超级管理员
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@simsynai.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"  # 建议在生产环境中更改
    
    # 默认测试用户
    DEFAULT_USER: str = "demo"
    DEFAULT_USER_EMAIL: str = "demo@simsynai.com"
    DEFAULT_USER_PASSWORD: str = "demo123"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    QWEN_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    
    # SkyEye配置
    SKYEYE_PATH: str = "/usr/local/bin/skyeye"
    SKYEYE_MODELS_DIR: str = "./models"
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", "sqlite:///./app.db"
    )
    SQLALCHEMY_ECHO: bool = False
    
    # 仿真引擎配置
    SIMULATION_RESULTS_DIR: str = os.getenv("SIMULATION_RESULTS_DIR", "./simulation_results")
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
      # Redis配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    # 默认LLM模型
    DEFAULT_LLM_MODEL: str = "gpt-3.5-turbo"
    
    class Config:
        """配置类设置
        
        case_sensitive: 区分大小写
        env_file: 环境变量文件路径
        """
        case_sensitive = True
        env_file = ".env"


settings = Settings() 