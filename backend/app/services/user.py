from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """用户服务类
    
    处理所有用户相关的业务逻辑，包括:
    - 用户CRUD操作
    - 密码管理
    - 用户查询
    """
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话对象
        """
        self.db = db

    def get(self, user_id: str) -> Optional[User]:
        """根据ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[User]: 找到的用户对象，不存在则返回None
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户
        
        Args:
            email: 用户邮箱
            
        Returns:
            Optional[User]: 找到的用户对象，不存在则返回None
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户
        
        Args:
            username: 用户名
            
        Returns:
            Optional[User]: 找到的用户对象，不存在则返回None
        """
        return self.db.query(User).filter(User.username == username).first()

    def create(self, obj_in: UserCreate) -> User:
        """创建新用户
        
        Args:
            obj_in: 用户创建模式对象，包含所需信息
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            IntegrityError: 当用户名或邮箱已存在时
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
            full_name=obj_in.full_name,
            preferred_model=obj_in.preferred_model
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: User, obj_in: UserUpdate) -> User:
        """更新用户信息
        
        支持部分字段更新，特殊处理密码字段。
        
        Args:
            db_obj: 待更新的用户对象
            obj_in: 更新数据对象，包含要更新的字段
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            IntegrityError: 当更新的唯一字段(如邮箱)已存在时
        """
        update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser