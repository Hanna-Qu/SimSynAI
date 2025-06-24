import httpx
from typing import Dict, List, Optional, Any
from .base import LLMAdapter

class DeepSeekAdapter(LLMAdapter):
    """DeepSeek API适配器"""
    
    def __init__(self, api_key: str, model_name: str = "deepseek-chat", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        self.base_url = kwargs.get("base_url", "https://api.deepseek.com/v1/chat/completions")
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
        """调用DeepSeek API生成文本响应"""
        if messages is None:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API错误: {response.status_code}, {response.text}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def get_available_models(self) -> List[str]:
        """获取可用的DeepSeek模型列表"""
        # DeepSeek没有列出模型的API，返回固定列表
        return ["deepseek-chat", "deepseek-coder", "deepseek-lite"]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "provider": "DeepSeek",
            "model": self.model_name,
            "type": "chat",
            "capabilities": ["text generation", "code generation", "reasoning"]
        } 