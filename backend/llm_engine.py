import os
import requests
import json
import time
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3.2:1b", host: str = None):
        self.model = model
        # Use environment variable OLLAMA_HOST if set, otherwise default to 11434
        self.host = host or os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
        self.timeout = 25  # Fast timeout - 1.2B model should respond quickly
        self.max_retries = 1  # Only 1 attempt to avoid long waits

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️  Ollama not available: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.3, **kwargs) -> str:
        """
        Generate response from Ollama
        
        Args:
            prompt: The prompt to send
            temperature: Creativity level (0.0-1.0, lower = more focused)
            
        Returns:
            Generated text or empty string on error
        """
        if not prompt or len(prompt.strip()) == 0:
            return ""
        
        for attempt in range(self.max_retries):
            try:
                url = f"{self.host}/api/generate"
                payload = {
                    "model": self.model,
                    "prompt": prompt[-3000:],  # Truncate prompt to last 3000 chars max
                    "stream": False,
                    "temperature": temperature,
                    "options": {
                        "num_predict": 150,   # Concise but useful responses
                        "num_ctx": 1536,      # Balanced context window
                        "top_k": 15,          # Focused sampling
                        "top_p": 0.75,        # Balanced generation
                        "repeat_penalty": 1.1
                    }
                }
                # Remove empty format key
                fmt = kwargs.get("format", "")
                if fmt:
                    payload["format"] = fmt
                
                response = requests.post(
                    url,
                    json=payload,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                result = response.json().get("response", "").strip()
                
                if result:
                    return result
                    
            except requests.Timeout:
                print(f"⚠️  Ollama timeout (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    
            except requests.ConnectionError as e:
                print(f"❌ Ollama connection error: {e}")
                return ""
                
            except Exception as e:
                print(f"❌ Ollama error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(0.5)
        
        return ""

class LLMEngine:
    def __init__(self):
        self.provider_name = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model_name = os.getenv("LLM_MODEL", "llama3.2:1b")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.enabled = os.getenv("USE_LLM", "true").lower() == "true"
        
        print(f"📌 LLM Engine Init:")
        print(f"   Provider: {self.provider_name}")
        print(f"   Model: {self.model_name}")
        print(f"   Host: {self.ollama_host}")
        print(f"   Enabled: {self.enabled}")
        
        if self.provider_name == "ollama":
            self.provider = OllamaProvider(
                model=self.model_name,
                host=self.ollama_host
            )
            
            # Check availability
            if not self.provider.is_available():
                print(f"⚠️ WARNING: Ollama is not available at {self.ollama_host}")
                print(f"   Make sure Ollama is running: ollama serve")
        else:
            self.provider = None
            print(f"❌ Unknown provider: {self.provider_name}")

    def ask(self, prompt: str, temperature: float = 0.3, **kwargs) -> str:
        """
        Ask the LLM engine a question
        
        Args:
            prompt: The prompt/question
            temperature: Creativity level (0.0-1.0)
            
        Returns:
            Generated response or empty string on failure
        """
        if not self.enabled:
            print("⚠️ LLM engine is disabled")
            return ""
        
        if not self.provider:
            print("❌ No LLM provider configured")
            return ""
        
        return self.provider.generate(prompt, temperature=temperature, **kwargs)
    
    def health_check(self) -> dict:
        """Check the health status of the LLM engine"""
        return {
            "provider": self.provider_name,
            "model": self.model_name,
            "enabled": self.enabled,
            "available": self.provider.is_available() if self.provider else False
        }

# Singleton instance
llm_engine = LLMEngine()
