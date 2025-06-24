from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Any

from app.db.session import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.core.config import settings
from app.llm.factory import get_llm_adapter

router = APIRouter()


@router.get("/available", response_model=List[Dict[str, Any]])
async def get_available_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取可用的LLM模型列表"""
    # 检查API密钥是否配置
    available_models = []
    
    # OpenAI模型
    if settings.OPENAI_API_KEY:
        try:
            openai_adapter = get_llm_adapter("openai", settings.OPENAI_API_KEY)
            models = await openai_adapter.get_available_models()
            # 过滤出常用的GPT模型
            gpt_models = [m for m in models if any(x in m for x in ["gpt-3.5", "gpt-4"])]
            for model in gpt_models[:5]:  # 限制返回数量
                available_models.append({
                    "id": model,
                    "name": model,
                    "provider": "OpenAI",
                    "type": "chat"
                })
        except Exception as e:
            # 如果获取失败，添加默认模型
            available_models.append({
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "provider": "OpenAI",
                "type": "chat"
            })
            available_models.append({
                "id": "gpt-4",
                "name": "GPT-4",
                "provider": "OpenAI",
                "type": "chat"
            })
    
    # Anthropic模型
    if settings.ANTHROPIC_API_KEY:
        available_models.extend([
            {
                "id": "claude-3-opus",
                "name": "Claude 3 Opus",
                "provider": "Anthropic",
                "type": "chat"
            },
            {
                "id": "claude-3-sonnet",
                "name": "Claude 3 Sonnet",
                "provider": "Anthropic",
                "type": "chat"
            },
            {
                "id": "claude-3-haiku",
                "name": "Claude 3 Haiku",
                "provider": "Anthropic",
                "type": "chat"
            }
        ])
    
    # Google模型
    if settings.GOOGLE_API_KEY:
        available_models.extend([
            {
                "id": "gemini-pro",
                "name": "Gemini Pro",
                "provider": "Google",
                "type": "chat"
            },
            {
                "id": "gemini-ultra",
                "name": "Gemini Ultra",
                "provider": "Google",
                "type": "chat"
            }
        ])
    
    # Qwen模型
    if settings.QWEN_API_KEY:
        available_models.extend([
            {
                "id": "qwen-turbo",
                "name": "Qwen Turbo",
                "provider": "Alibaba Cloud",
                "type": "chat"
            },
            {
                "id": "qwen-plus",
                "name": "Qwen Plus",
                "provider": "Alibaba Cloud",
                "type": "chat"
            },
            {
                "id": "qwen-max",
                "name": "Qwen Max",
                "provider": "Alibaba Cloud",
                "type": "chat"
            }
        ])
    
    # DeepSeek模型
    if settings.DEEPSEEK_API_KEY:
        available_models.extend([
            {
                "id": "deepseek-chat",
                "name": "DeepSeek Chat",
                "provider": "DeepSeek",
                "type": "chat"
            },
            {
                "id": "deepseek-coder",
                "name": "DeepSeek Coder",
                "provider": "DeepSeek",
                "type": "chat"
            }
        ])
    
    return available_models


@router.post("/set-preferred", response_model=Dict[str, Any])
async def set_preferred_model(
    model_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """设置用户首选模型"""
    # 更新用户首选模型
    current_user.preferred_model = model_id
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": "success",
        "message": f"Preferred model set to {model_id}",
        "preferred_model": model_id
    } 