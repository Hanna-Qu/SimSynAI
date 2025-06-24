"""OpenAI API适配器模块

实现与OpenAI API的交互，支持：
- GPT系列模型调用
- 上下文管理
- 流式响应
- 错误处理与重试
"""

import openai
from openai import OpenAI, OpenAIError
from typing import Dict, List, Optional, Any, Sequence
from tenacity import retry, stop_after_attempt, wait_exponential

from .base import LLMAdapter
from app.core.logging import logger


class OpenAIAdapter(LLMAdapter):
    """OpenAI API适配器
    
    提供与OpenAI API的标准化接口，支持：
    - 文本生成
    - 代码生成
    - 对话管理
    - 模型选择
    
    使用 tenacity 库实现自动重试机制，处理临时性API错误。
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-3.5-turbo",
        organization: Optional[str] = None,
        **kwargs: Any
    ):
        """初始化OpenAI适配器
        
        Args:
            api_key: OpenAI API密钥
            model_name: 模型名称，默认使用gpt-3.5-turbo
            organization: 组织ID(可选)
            **kwargs: 其他配置参数
        
        Raises:
            ValueError: API密钥无效
            ConnectionError: 无法连接到OpenAI服务
        """
        super().__init__(api_key, model_name, **kwargs)
        
        try:
            self.client = OpenAI(
                api_key=api_key,
                organization=organization,
                **kwargs
            )
            logger.debug(f"OpenAI客户端初始化成功，使用模型：{model_name}")
        except Exception as e:
            logger.error(f"OpenAI客户端初始化失败: {str(e)}")
            raise ConnectionError(f"无法连接到OpenAI服务: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def generate(
        self, 
        prompt: str, 
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        messages: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """调用OpenAI API生成文本响应
        
        支持两种调用方式：
        1. 直接提供prompt和system_message
        2. 提供完整的消息历史数组
        
        Args:
            prompt: 提示文本
            system_message: 系统指令
            temperature: 采样温度，控制输出随机性
            max_tokens: 生成的最大token数
            messages: 完整的消息历史记录
            
        Returns:
            str: 生成的文本响应
            
        Raises:
            OpenAIError: API调用失败
            ValueError: 参数无效
        """
        try:
            if messages is None:
                messages = []
                if system_message:
                    messages.append({
                        "role": "system",
                        "content": system_message
                    })
                messages.append({
                    "role": "user",
                    "content": prompt
                })
            elif system_message and not any(msg.get("role") == "system" for msg in messages):
                messages.insert(0, {
                    "role": "system",
                    "content": system_message
                })
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except OpenAIError as e:
            logger.error(f"OpenAI API调用失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"生成文本时发生未知错误: {str(e)}")
            raise ValueError(f"生成文本失败: {str(e)}")
    
    async def get_available_models(self) -> List[str]:
        """获取可用的OpenAI模型列表
        
        Returns:
            List[str]: 可用模型ID列表
            
        Raises:
            OpenAIError: API调用失败
        """
        try:
            models = await self.client.models.list()
            return [model.id for model in models.data]
        except OpenAIError as e:
            logger.error(f"获取模型列表失败: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取当前模型信息
        
        Returns:
            Dict[str, Any]: 包含模型详细信息的字典
        """
        return {
            "provider": "OpenAI",
            "model": self.model_name,
            "type": "chat",
            "capabilities": [
                "text generation",
                "code generation",
                "reasoning",
                "context understanding"
            ],
            "max_context_length": 4096 if "gpt-3.5" in self.model_name else 8192,
            "supports_streaming": True
        }