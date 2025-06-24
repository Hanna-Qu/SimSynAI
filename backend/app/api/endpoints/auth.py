"""认证相关的API端点

提供以下功能：
- 用户登录和令牌颁发
- 令牌刷新
- 密码重置
- 会话管理
"""

from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app import schemas
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.services.user import UserService
from app.core.security import create_access_token, verify_password
from app.db.models.user import User
from app.schemas.user import Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    """用户登录接口
    
    实现了OAuth2密码模式的令牌颁发。支持使用邮箱或用户名登录。
    登录成功后返回JWT访问令牌。
    
    验证流程：
    1. 检查用户是否存在
    2. 验证密码
    3. 检查账户状态
    4. 生成访问令牌
    
    Args:
        response: FastAPI响应对象，用于设置cookie
        db: 数据库会话
        form_data: OAuth2表单数据，包含username和password
        
    Returns:
        Dict[str, str]: 包含访问令牌和令牌类型的字典
        
    Raises:
        HTTPException (401):
            - 用户不存在
            - 密码错误
            - 令牌无效
        HTTPException (400): 账户未激活
    """
    # 检查用户是否存在
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否激活
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账户未激活，请联系管理员",
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=Token)
async def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """注册新用户并返回访问令牌"""    # 检查邮箱是否已存在
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # 检查用户名是否已存在
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    
    # 创建新用户
    from app.core.security import get_password_hash
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
        full_name=user_in.full_name,
        preferred_model=user_in.preferred_model
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }