"""用户管理相关的API端点

提供以下功能：
- 用户注册
- 个人信息管理
- 偏好设置
- 权限控制
- API密钥管理
"""

from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app import schemas
from app.core.security import get_current_user, get_password_hash, verify_password, encrypt_api_key, decrypt_api_key
from app.db.models.user import User
from app.db.session import get_db
from app.services.user import UserService

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> schemas.User:
    """获取当前用户信息
    
    返回当前认证用户的详细信息，包括：
    - 基本信息（用户名、邮箱等）
    - 账户状态
    - 偏好设置
    
    Args:
        current_user: 当前认证用户，由依赖项自动注入
        
    Returns:
        schemas.User: 用户信息模型
        
    Raises:
        HTTPException (401): 未认证时
    """
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.User:
    """更新当前用户信息
    
    允许用户更新以下信息：
    - 密码
    - 个人资料
    - 偏好设置
    
    更新规则：
    1. 只更新提供的字段
    2. 密码会被正确加密
    3. 某些字段可能受限制（如超级用户状态）
    
    Args:
        user_in: 要更新的用户信息
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        schemas.User: 更新后的用户信息
        
    Raises:
        HTTPException (400): 
            - 参数无效
            - 邮箱已存在
        HTTPException (401): 未认证
    """
    user_data = user_in.dict(exclude_unset=True)
    
    if user_data.get("password"):
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    for field, value in user_data.items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/", response_model=schemas.User)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> schemas.User:
    """创建新用户
    
    注册新用户账户。执行以下操作：
    1. 验证用户数据
    2. 检查邮箱和用户名唯一性
    3. 加密密码
    4. 创建用户记录
    
    Args:
        user_in: 用户注册信息
        db: 数据库会话
        
    Returns:
        schemas.User: 创建的用户信息
        
    Raises:
        HTTPException (400): 
            - 邮箱已注册
            - 用户名已存在
            - 参数无效
    """
    # 检查邮箱是否已存在
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
    user = models.User(
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
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific user by id.
    """
    user_service = UserService(db)
    user = user_service.get(user_id=user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.get("/me/api-keys", response_model=schemas.UserAPIKeys)
async def get_user_api_keys(
    current_user: User = Depends(get_current_user),
) -> schemas.UserAPIKeys:
    """获取用户API密钥状态
    
    返回用户是否配置了各种API密钥，不返回实际密钥值
    
    Args:
        current_user: 当前认证用户
        
    Returns:
        schemas.UserAPIKeys: API密钥配置状态
    """
    return schemas.UserAPIKeys(
        openai_api_key=bool(current_user.openai_api_key),
        anthropic_api_key=bool(current_user.anthropic_api_key),
        google_api_key=bool(current_user.google_api_key),
        qwen_api_key=bool(current_user.qwen_api_key),
        deepseek_api_key=bool(current_user.deepseek_api_key),
    )


@router.put("/me/api-keys")
async def update_user_api_keys(
    api_keys: schemas.UserAPIKeysUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """更新用户API密钥
    
    允许用户更新各种LLM服务的API密钥
    
    Args:
        api_keys: 要更新的API密钥
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        Dict[str, Any]: 更新结果
    """
    api_keys_data = api_keys.dict(exclude_unset=True)
    
    # 加密并存储API密钥
    for key, value in api_keys_data.items():
        if value is not None:
            if value == "":  # 空字符串表示删除密钥
                setattr(current_user, key, None)
            else:
                encrypted_key = encrypt_api_key(value)
                setattr(current_user, key, encrypted_key)
    
    db.add(current_user)
    db.commit()
    
    return {
        "status": "success",
        "message": "API密钥更新成功",
        "updated_keys": list(api_keys_data.keys())
    }


@router.post("/me/api-keys/test")
async def test_api_key(
    provider: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """测试API密钥有效性
    
    Args:
        provider: 提供商名称 (openai, anthropic, google, qwen, deepseek)
        current_user: 当前认证用户
        
    Returns:
        Dict[str, Any]: 测试结果
    """
    # 获取对应的加密密钥
    encrypted_key = getattr(current_user, f"{provider}_api_key", None)
    if not encrypted_key:
        return {
            "status": "error",
            "message": f"未配置{provider}的API密钥"
        }
    
    # 解密密钥
    api_key = decrypt_api_key(encrypted_key)
    if not api_key:
        return {
            "status": "error",
            "message": "API密钥解密失败"
        }
    
    # 测试密钥有效性
    try:
        from app.llm.factory import get_llm_adapter
        adapter = get_llm_adapter(provider, api_key=api_key)
        # 简单测试：获取可用模型列表
        models = await adapter.get_available_models()
        return {
            "status": "success",
            "message": f"{provider}的API密钥有效",
            "models_count": len(models) if models else 0
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"API密钥测试失败: {str(e)}"
        }