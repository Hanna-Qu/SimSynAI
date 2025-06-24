import google.generativeai as genai
from typing import Dict, List, Optional, Any
from .base import LLMAdapter

class GeminiAdapter(LLMAdapter):
    """Google Gemini API适配器"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
    async def generate(self, 
                      prompt: str, 
                      system_message: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000,
                      messages: Optional[List[Dict[str, str]]] = None) -> str:
        """调用Gemini API生成文本响应"""
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "top_p": 0.95,
            "top_k": 0,
        }
        
        extracted_system = system_message
        
        if messages:
            # 转换消息格式为Gemini格式
            gemini_messages = []
            for msg in messages:
                role = msg["role"]
                if role == "user":
                    gemini_messages.append({
                        "role": "user",
                        "parts": [msg["content"]]
                    })
                elif role == "assistant":
                    gemini_messages.append({
                        "role": "model",
                        "parts": [msg["content"]]
                    })
                elif role == "system":
                    # 将系统消息保存起来
                    extracted_system = msg["content"]
            
            if extracted_system:
                # 在第一条消息前添加系统指令
                if len(gemini_messages) > 0 and gemini_messages[0]["role"] == "user":
                    gemini_messages[0]["parts"][0] = f"{extracted_system}\n\n{gemini_messages[0]['parts'][0]}"
                else:
                    gemini_messages.insert(0, {
                        "role": "user",
                        "parts": [extracted_system]
                    })
            
            chat = self.model.start_chat(history=gemini_messages)
            response = await chat.send_message_async(
                prompt if not gemini_messages else "",
                generation_config=generation_config
            )
        else:
            full_prompt = prompt
            if extracted_system:
                full_prompt = f"{extracted_system}\n\n{prompt}"
                
            response = await self.model.generate_content_async(
                full_prompt,
                generation_config=generation_config
            )
        
        return response.text
    
    async def get_available_models(self) -> List[str]:
        """获取可用的Gemini模型列表"""
        models = genai.list_models()
        return [model.name for model in models if "gemini" in model.name]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "provider": "Google",
            "model": self.model_name,
            "type": "chat",
            "capabilities": ["text generation", "multimodal", "reasoning"]
        } 