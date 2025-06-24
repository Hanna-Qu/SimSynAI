"""AI对话相关的API端点

提供以下功能：
- 与AI助手进行对话
- 管理对话会话
- 查看历史记录
- WebSocket实时对话
- 多模型支持
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query, status
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.schemas.chat import ChatMessageResponse, ChatMessageCreate, ChatSession, ChatSessionCreate
from app.services.chat import ChatService
from app.llm.factory import get_llm_adapter, get_provider_from_model
from app.core.logging import logger

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    message: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatMessageResponse:
    """发送消息并获取AI响应
    
    处理用户发送的消息，调用相应的语言模型生成回复。
    支持多种模型，可以处理上下文相关的对话。
    
    流程：
    1. 验证消息格式
    2. 获取合适的模型适配器
    3. 加载对话历史
    4. 生成AI响应
    5. 保存对话记录
    
    Args:
        message: 用户消息内容和配置
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        ChatMessageResponse: AI的响应消息
        
    Raises:
        HTTPException (400): 
            - 消息格式无效
            - 模型不可用
        HTTPException (500): AI生成响应失败
    """
    try:
        # 获取提供商和用户API密钥
        provider = get_provider_from_model(message.model)
        
        # 获取用户的API密钥
        from app.core.security import decrypt_api_key
        api_key_field = f"{provider}_api_key"
        encrypted_key = getattr(current_user, api_key_field, None)
        
        if not encrypted_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"未配置{provider}的API密钥，请前往个人设置页面配置"
            )
        
        # 解密API密钥
        api_key = decrypt_api_key(encrypted_key)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{provider}的API密钥无效，请重新配置"
            )
        
        # 获取适配器
        llm_adapter = get_llm_adapter(provider, api_key=api_key, model_name=message.model)
        
        logger.debug(f"Using {provider} model: {message.model}")
        
        # 创建聊天服务
        chat_service = ChatService(db, llm_adapter)
        
        # 发送消息并获取响应
        response = await chat_service.process_message(
            user_id=current_user.id,
            content=message.content,
            model=message.model,
            task_id=message.task_id
        )
        
        return response
        
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="处理消息时出错，请稍后重试"
        )


@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    limit: int = Query(50, description="返回的最大消息数量", ge=1, le=100),
    before: Optional[str] = Query(None, description="获取此消息ID之前的历史记录"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ChatMessageResponse]:
    """获取聊天历史记录
    
    分页获取用户的历史对话记录。记录按时间倒序排列。
    
    支持以下功能：
    - 分页加载
    - 按时间范围筛选
    - 按对话主题筛选
    
    Args:
        limit: 返回的最大消息数量
        before: 分页标记，获取此消息之前的记录
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        List[ChatMessageResponse]: 历史消息列表
        
    Raises:
        HTTPException (400): 参数无效
    """
    chat_service = ChatService(db)
    return await chat_service.get_messages(current_user.id)


@router.post("/model", response_model=Dict[str, str])
async def change_model(
    model_data: Dict[str, str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """更改当前使用的模型
    
    允许用户切换不同的语言模型，如GPT-3.5、GPT-4、Claude等。
    
    Args:
        model_data: 包含模型名称的数据
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        Dict[str, str]: 包含成功消息和当前模型名称
        
    Raises:
        HTTPException (400): 模型名称无效
        HTTPException (500): 更新首选模型失败
    """
    model_name = model_data.get("model")
    if not model_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供模型名称"
        )
    
    chat_service = ChatService(db)
    success = await chat_service.set_preferred_model(current_user.id, model_name)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新首选模型失败"
        )
    
    return {
        "message": "模型已更改",
        "current_model": model_name
    }


@router.post("/sessions", response_model=ChatSession)
async def create_chat_session(
    session_data: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatSession:
    """创建新的聊天会话
    
    创建一个新的聊天会话，用于组织对话。
    
    Args:
        session_data: 会话创建数据
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        ChatSession: 创建的会话信息
        
    Raises:
        HTTPException (500): 创建会话失败
    """
    chat_service = ChatService(db)
    session = chat_service.create_chat_session(
        user_id=current_user.id,
        title=session_data.title
    )
    
    return session


@router.get("/sessions", response_model=List[ChatSession])
async def get_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ChatSession]:
    """获取用户的聊天会话列表
    
    返回用户创建的所有聊天会话。
    
    Args:
        db: 数据库会话
        current_user: 当前认证用户
        
    Returns:
        List[ChatSession]: 会话列表
    """
    chat_service = ChatService(db)
    sessions = chat_service.get_chat_sessions(current_user.id)
    return sessions