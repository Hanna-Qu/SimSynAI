from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from fastapi import Depends

from app.core.config import settings


class LLMAdapter(ABC):
    """
    大语言模型适配器基类
    
    这个抽象基类定义了与不同LLM提供商交互的标准接口。
    所有具体的适配器实现都应该继承这个类并实现其抽象方法。
    """
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        """
        初始化LLM适配器
        
        Args:
            api_key: API密钥
            model_name: 模型名称
            **kwargs: 其他参数
        """
        self.api_key = api_key
        self.model_name = model_name
        self.kwargs = kwargs
    
    @abstractmethod
    async def generate(self, 
                      prompt: str, 
                      system_message: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000,
                      messages: Optional[List[Dict[str, str]]] = None) -> str:
        """
        生成文本响应
        
        Args:
            prompt: 提示文本
            system_message: 系统消息
            temperature: 温度参数，控制随机性
            max_tokens: 生成的最大token数
            messages: 消息历史，格式为[{"role": "user", "content": "..."}, ...]
            
        Returns:
            str: 生成的文本响应
        """
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """
        获取可用的模型列表
        
        Returns:
            List[str]: 可用的模型名称列表
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            Dict[str, Any]: 模型信息，包括提供商、模型名称、类型等
        """
        pass


# 适配器工厂
class LLMAdapterFactory:
    """LLM适配器工厂类
    
    负责创建和管理不同LLM提供商的适配器实例。
    支持的提供商包括:
    - OpenAI (GPT)
    - Anthropic (Claude)
    - Google (Gemini)
    - Alibaba (Qwen)
    - DeepSeek
    """
    
    @staticmethod
    def get_adapter(provider: str, api_key: Optional[str] = None, model_name: Optional[str] = None, **kwargs) -> LLMAdapter:
        """获取适配器实例"""
        if provider == "openai":
            from app.llm.openai import OpenAIAdapter
            return OpenAIAdapter(
                api_key=api_key or settings.OPENAI_API_KEY,
                model_name=model_name or "gpt-3.5-turbo",
                **kwargs
            )
        elif provider == "anthropic":
            from app.llm.anthropic import AnthropicAdapter
            return AnthropicAdapter(
                api_key=api_key or settings.ANTHROPIC_API_KEY,
                model_name=model_name or "claude-2",
                **kwargs
            )
        elif provider == "gemini":
            from app.llm.gemini import GeminiAdapter
            return GeminiAdapter(
                api_key=api_key or settings.GOOGLE_API_KEY,
                model_name=model_name or "gemini-pro",
                **kwargs
            )
        elif provider == "qwen":
            from app.llm.qwen import QwenAdapter
            return QwenAdapter(
                api_key=api_key or settings.QWEN_API_KEY,
                model_name=model_name or "qwen-plus",
                **kwargs
            )
        elif provider == "deepseek":
            from app.llm.deepseek import DeepSeekAdapter
            return DeepSeekAdapter(
                api_key=api_key or settings.DEEPSEEK_API_KEY,
                model_name=model_name or "deepseek-chat",
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


# 依赖注入获取默认适配器
def get_llm_adapter(provider: str = "openai", model_name: Optional[str] = None) -> LLMAdapter:
    """获取LLM适配器依赖"""
    return LLMAdapterFactory.get_adapter(provider, model_name=model_name) 