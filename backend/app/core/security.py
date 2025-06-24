from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import base64

from app.core.config import settings
from app.db.session import get_db
from app.schemas.user import TokenPayload

# 密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2密码Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# API密钥加密器
def get_encryption_key() -> bytes:
    """获取加密密钥"""
    # 使用SECRET_KEY生成固定的加密密钥
    key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode().ljust(32, b'0')[:32])
    return key

cipher_suite = Fernet(get_encryption_key())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)


def encrypt_api_key(api_key: str) -> str:
    """加密API密钥"""
    if not api_key:
        return ""
    return cipher_suite.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """解密API密钥"""
    if not encrypted_key:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_key.encode()).decode()
    except Exception:
        return ""


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenPayload]:
    """验证令牌"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
    except JWTError:
        return None
    return token_data


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Any:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    from app.db.models.user import User
    user = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user 