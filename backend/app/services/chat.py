from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models.chat import ChatMessage, ChatSession
from app.db.models.user import User
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.llm.base import LLMAdapter


class ChatService:
    """聊天服务类
    
    处理用户与AI助手的对话交互，功能包括：
    - 消息处理与AI响应生成
    - 对话历史管理
    - 多模型支持
    - 上下文理解与任务关联
    """
    
    def __init__(self, db: Session, llm_adapter: Optional[LLMAdapter] = None):
        """初始化聊天服务
        
        Args:
            db: SQLAlchemy数据库会话
            llm_adapter: 语言模型适配器实例，用于生成响应
        """
        self.db = db
        self.llm_adapter = llm_adapter
    
    async def process_message(
        self,
        user_id: str,
        content: str,
        model: str,
        task_id: Optional[str] = None
    ) -> ChatMessageResponse:
        """处理用户消息并获取AI响应
        
        工作流程：
        1. 保存用户消息到数据库
        2. 获取相关的历史对话作为上下文
        3. 使用语言模型生成回复
        4. 保存AI响应
        5. 处理特殊指令(如果有)
        
        Args:
            user_id: 发送消息的用户ID
            content: 消息内容
            model: 使用的语言模型名称
            task_id: 关联的仿真任务ID(可选)
            
        Returns:
            ChatMessageResponse: AI的响应消息
            
        Raises:
            ValueError: 当消息格式无效或模型不可用时
        """
        # 创建用户消息记录
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            user_id=user_id,
            task_id=task_id,
            role="user",
            content=content,
            model=model
        )
        self.db.add(user_message)
        self.db.commit()
        self.db.refresh(user_message)
        
        # 获取历史消息作为上下文
        history = self.get_message_history_sync(user_id, task_id, limit=10)
        messages = []
        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": content
        })
        
        # 调用LLM获取响应
        if not self.llm_adapter:
            # 如果没有提供适配器，返回错误消息
            response_content = "错误：未配置LLM适配器"
        else:
            try:
                # 从消息中提取系统消息
                system_message = None
                filtered_messages = []
                for msg in messages:
                    if msg["role"] == "system":
                        system_message = msg["content"]
                    else:
                        filtered_messages.append(msg)
                
                response_content = await self.llm_adapter.generate(
                    prompt=content,
                    system_message=system_message,
                    messages=filtered_messages,
                    temperature=0.7,
                    max_tokens=2000
                )
            except Exception as e:
                response_content = f"错误：调用LLM时出错 - {str(e)}"
        
        # 创建AI响应消息记录
        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            user_id=user_id,
            task_id=task_id,
            role="assistant",
            content=response_content,
            model=model
        )
        self.db.add(assistant_message)
        self.db.commit()
        self.db.refresh(assistant_message)
        
        # 返回响应
        return ChatMessageResponse(
            id=assistant_message.id,
            user_id=user_id,
            role="assistant",
            content=response_content,
            model=model,
            task_id=task_id,
            timestamp=assistant_message.timestamp
        )
    
    def get_message_history_sync(
        self,
        user_id: str,
        task_id: Optional[str] = None,
        limit: int = 50
    ) -> List[ChatMessage]:
        """同步获取消息历史"""
        query = self.db.query(ChatMessage).filter(ChatMessage.user_id == user_id)
        if task_id:
            query = query.filter(ChatMessage.task_id == task_id)
        return query.order_by(ChatMessage.timestamp.asc()).limit(limit).all()
    
    async def get_message_history(
        self,
        user_id: str,
        task_id: Optional[str] = None,
        limit: int = 50
    ) -> List[ChatMessageResponse]:
        """获取消息历史"""
        messages = self.get_message_history_sync(user_id, task_id, limit)
        return [
            ChatMessageResponse(
                id=msg.id,
                user_id=msg.user_id,
                role=msg.role,
                content=msg.content,
                model=msg.model,
                task_id=msg.task_id,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]
    
    async def get_messages(
        self,
        user_id: str,
        task_id: Optional[str] = None,
        limit: int = 50
    ) -> List[ChatMessageResponse]:
        """获取用户消息（get_message_history的别名）"""
        return await self.get_message_history(user_id, task_id, limit)
    
    def save_message_history(
        self,
        user_id: str,
        message_content: str,
        response_content: str,
        task_id: Optional[str] = None
    ) -> None:
        """保存消息历史（用于后台任务）"""
        # 这个方法是为了在后台任务中使用，已经在process_message中实现了保存功能
        pass
    
    async def set_preferred_model(
        self,
        user_id: str,
        model_name: str
    ) -> bool:
        """设置用户首选模型"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.preferred_model = model_name
        self.db.add(user)
        self.db.commit()
        return True
    
    def create_chat_session(
        self,
        user_id: str,
        title: str = "新对话"
    ) -> ChatSession:
        """创建聊天会话"""
        session = ChatSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_chat_sessions(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[ChatSession]:
        """获取用户的聊天会话列表"""
        return self.db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.updated_at.desc()).limit(limit).all()
