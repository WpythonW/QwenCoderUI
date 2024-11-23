# llms_api_client.py
from typing import List, Dict, Any, Optional
import aiohttp
from dataclasses import dataclass

@dataclass
class ModelResponse:
    """Unified response structure for all models"""
    generated_text: str
    raw_response: Any
    status: bool
    error: Optional[str] = None

class CodeGenerationAPI:
    """Unified API for code generation models"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
        # Model endpoints
        self.STARCODER_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder2-15b"
        self.QWEN_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"

    async def query_model_async(self, session: aiohttp.ClientSession, prompt: str, model: str, **kwargs) -> ModelResponse:
        """Generic async query method for both models"""
        try:
            url = self.STARCODER_URL if model == "starcoder" else f"https://api-inference.huggingface.co/models/{self.QWEN_MODEL}"
            
            # Different payload format for each model
            if model == "starcoder":
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": kwargs.get("max_tokens", 500),
                        "temperature": kwargs.get("temperature", 0.7),
                        "top_p": kwargs.get("top_p", 0.95),
                        "do_sample": kwargs.get("do_sample", True)
                    }
                }
            else:  # qwen
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": kwargs.get("max_tokens", 500),
                        "temperature": kwargs.get("temperature", 0.7),
                        "top_p": kwargs.get("top_p", 0.95)
                    }
                }
            
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    # Handle different response formats
                    if model == "starcoder":
                        text = result[0]["generated_text"]
                    else:
                        text = result[0]["generated_text"] if isinstance(result[0], dict) else result[0]
                    return ModelResponse(
                        generated_text=text,
                        raw_response=result,
                        status=True
                    )
                else:
                    error_text = await response.text()
                    return ModelResponse(
                        generated_text="",
                        raw_response=error_text,
                        status=False,
                        error=f"API Error ({response.status}): {error_text}"
                    )
                    
        except Exception as e:
            return ModelResponse(
                generated_text="",
                raw_response=str(e),
                status=False,
                error=f"Error querying {model}: {str(e)}"
            )

    async def generate_code_async(self, session: aiohttp.ClientSession, prompt: str, model: str = "qwen", **kwargs) -> ModelResponse:
        """Async unified method to generate code using specified model"""
        if model.lower() not in ["qwen", "starcoder"]:
            return ModelResponse(
                generated_text="",
                raw_response=None,
                status=False,
                error=f"Unknown model: {model}"
            )
        
        return await self.query_model_async(session, prompt, model.lower(), **kwargs)