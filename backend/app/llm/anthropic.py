import anthropic
from typing import Dict, List, Optional, Any
from .base import LLMAdapter

class AnthropicAdapter(LLMAdapter):
    """Anthropic API适配器"""
    
    def __init__(self, api_key: str, model_name: str = "claude-2", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        self.client = anthropic.Anthropic(api_key=api_key)
        
    async def generate(self, 
                      prompt: str, 
                      system_message: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000,
                      messages: Optional[List[Dict[str, str]]] = None) -> str:
        """调用Anthropic API生成文本响应"""
        if messages:
            # 将消息格式转换为Anthropic格式
            anthropic_messages = []
            extracted_system = system_message
            
            for msg in messages:
                role = msg["role"]
                if role == "system":
                    # Claude API处理系统消息的方式不同
                    extracted_system = msg["content"]
                elif role == "user":
                    anthropic_messages.append({
                        "role": "user",
                        "content": msg["content"]
                    })
                elif role == "assistant":
                    anthropic_messages.append({
                        "role": "assistant",
                        "content": msg["content"]
                    })
            
            response = await self.client.messages.create(
                model=self.model_name,
                messages=anthropic_messages,
                system=extracted_system,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            response = await self.client.messages.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                system=system_message,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        return response.content[0].text
    
    async def get_available_models(self) -> List[str]:
        """获取可用的Anthropic模型列表"""
        # Anthropic没有列出模型的API，返回固定列表
        return ["claude-2", "claude-instant-1", "claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "provider": "Anthropic",
            "model": self.model_name,
            "type": "chat",
            "capabilities": ["text generation", "reasoning", "creative writing"]
        } 