from typing import Optional
from pydantic import BaseModel, EmailStr


class TokenPayload(BaseModel):
    """JWT令牌负载"""
    sub: Optional[str] = None


class UserBase(BaseModel):
    """用户基础模式"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    preferred_model: Optional[str] = "gpt-3.5-turbo"


class UserCreate(UserBase):
    """用户创建模式"""
    email: EmailStr
    username: str
    password: str


class UserUpdate(UserBase):
    """用户更新模式"""
    password: Optional[str] = None


class UserAPIKeysUpdate(BaseModel):
    """用户API密钥更新模式"""
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    qwen_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None


class UserAPIKeys(BaseModel):
    """用户API密钥信息（返回时隐藏实际密钥）"""
    openai_api_key: Optional[bool] = False
    anthropic_api_key: Optional[bool] = False
    google_api_key: Optional[bool] = False
    qwen_api_key: Optional[bool] = False
    deepseek_api_key: Optional[bool] = False


class UserInDBBase(UserBase):
    """数据库中的用户模式"""
    id: str
    
    model_config = {"from_attributes": True}


class User(UserInDBBase):
    """用户模式（返回给API）"""
    pass


class UserInDB(UserInDBBase):
    """数据库中的用户模式（包含密码）"""
    hashed_password: str


class Token(BaseModel):
    """访问令牌"""
    access_token: str
    token_type: str