"""LLM适配器工厂模块

提供统一的接口来创建和管理不同LLM提供商的适配器实例。
支持的提供商：
- OpenAI (GPT系列)
- Anthropic (Claude系列)
- Google (Gemini)
- Alibaba (通义千问)
- DeepSeek

每个适配器都实现了统一的接口，使得应用可以无缝切换不同的LLM提供商。
"""

from typing import Optional, Dict, Any, Mapping
from enum import Enum

from app.core.config import settings
from app.llm.base import LLMAdapter
from app.llm.openai import OpenAIAdapter
from app.llm.anthropic import AnthropicAdapter
from app.llm.gemini import GeminiAdapter
from app.llm.qwen import QwenAdapter
from app.llm.deepseek import DeepSeekAdapter
from app.core.logging import logger


class LLMProvider(str, Enum):
    """LLM提供商枚举"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    QWEN = "qwen"
    DEEPSEEK = "deepseek"


# 提供商到模型的映射
DEFAULT_MODELS: Mapping[str, str] = {
    LLMProvider.OPENAI: "gpt-3.5-turbo",
    LLMProvider.ANTHROPIC: "claude-2",
    LLMProvider.GEMINI: "gemini-pro",
    LLMProvider.QWEN: "qwen-plus",
    LLMProvider.DEEPSEEK: "deepseek-chat",
}


def get_llm_adapter(
    provider: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    **kwargs: Any
) -> LLMAdapter:
    """获取LLM适配器实例
    
    基于提供商名称创建对应的适配器实例。支持自定义API密钥和模型名称，
    如果未提供则使用配置文件中的默认值。
    
    参数验证流程：
    1. 检查提供商是否支持
    2. 验证API密钥
    3. 确认模型名称
    4. 验证其他参数
    
    Args:
        provider: 提供商名称，参见LLMProvider枚举
        api_key: API密钥，None时使用配置中的密钥
        model_name: 模型名称，None时使用默认模型
        **kwargs: 其他配置参数，如温度、最大tokens等
        
    Returns:
        LLMAdapter: 初始化好的适配器实例
        
    Raises:
        ValueError: 当提供商不受支持或API密钥无效时
    """
    try:
        provider = LLMProvider(provider.lower())
    except ValueError:
        raise ValueError(f"不支持的LLM提供商: {provider}，支持的提供商: {', '.join(p.value for p in LLMProvider)}")
    
    # 获取API密钥
    if api_key is None:
        api_key = getattr(settings, f"{provider.upper()}_API_KEY", None)
        if not api_key:
            raise ValueError(f"未提供{provider}的API密钥，请在配置文件中设置{provider.upper()}_API_KEY或通过参数传入")
    
    # 获取模型名称
    if model_name is None:
        model_name = DEFAULT_MODELS.get(provider)
        logger.debug(f"使用{provider}的默认模型: {model_name}")
    
    # 创建适配器实例
    try:
        if provider == LLMProvider.OPENAI:
            return OpenAIAdapter(api_key, model_name, **kwargs)
        elif provider == LLMProvider.ANTHROPIC:
            return AnthropicAdapter(api_key, model_name, **kwargs)
        elif provider == LLMProvider.GEMINI:
            return GeminiAdapter(api_key, model_name, **kwargs)
        elif provider == LLMProvider.QWEN:
            return QwenAdapter(api_key, model_name, **kwargs)
        elif provider == LLMProvider.DEEPSEEK:
            return DeepSeekAdapter(api_key, model_name, **kwargs)
    except Exception as e:
        raise RuntimeError(f"创建{provider}适配器时发生错误: {str(e)}")
    
    raise ValueError(f"不支持的LLM提供商: {provider}")


def get_provider_from_model(model_name: str) -> str:
    """
    从模型名称推断提供商
    
    Args:
        model_name: 模型名称
        
    Returns:
        str: 提供商名称
    """
    model_name = model_name.lower()
    
    if any(x in model_name for x in ["gpt", "davinci", "text-embedding"]):
        return "openai"
    elif "claude" in model_name:
        return "anthropic"
    elif "gemini" in model_name:
        return "gemini"
    elif "qwen" in model_name:
        return "qwen"
    elif "deepseek" in model_name:
        return "deepseek"
    else:
        # 默认使用OpenAI
        return "openai"