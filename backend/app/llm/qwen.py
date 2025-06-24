import httpx
from typing import Dict, List, Optional, Any
from .base import LLMAdapter

class QwenAdapter(LLMAdapter):
    """阿里云Qwen API适配器"""
    
    def __init__(self, api_key: str, model_name: str = "qwen-plus", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        self.base_url = kwargs.get("base_url", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    async def generate(self, 
                      prompt: str, 
                      system_message: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000,
                      messages: Optional[List[Dict[str, str]]] = None) -> str:
        """调用Qwen API生成文本响应"""
        if messages is None:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model_name,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Qwen API错误: {response.status_code}, {response.text}")
            
            result = response.json()
            return result["output"]["text"]
    
    async def get_available_models(self) -> List[str]:
        """获取可用的Qwen模型列表"""
        # Qwen没有列出模型的API，返回固定列表
        return ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "provider": "Alibaba Cloud",
            "model": self.model_name,
            "type": "chat",
            "capabilities": ["text generation", "code generation", "reasoning"]
        } 