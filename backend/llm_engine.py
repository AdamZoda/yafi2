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
    def __init__(self, model: str = "qwen2.5:3b", host: str = None):
        self.model = model
        # Use environment variable OLLAMA_HOST if set, otherwise default to 11434
        self.host = host or os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
        self.timeout = 180  # Optimized for 3B Model Loading on i7-7600U
        self.max_retries = 1 

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama not available: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.3, **kwargs) -> str:
        """Standard non-streaming generation"""
        if not prompt or len(prompt.strip()) == 0:
            return ""
        
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt[-8000:], 
                "stream": False,
                "temperature": 0.5, # Lower temperature for more professional stability
                "options": {
                    "num_predict": 300, # Shorter responses = Faster Speed
                    "num_ctx": 8192, 
                    "num_thread": 4,
                    "top_k": 40,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                },
                "keep_alive": "5m"
            }
            if kwargs.get("format"):
                payload["format"] = kwargs["format"]
            
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"Ollama error: {e}")
            return ""

    def generate_stream(self, prompt: str, temperature: float = 0.3, **kwargs):
        """Streaming generation"""
        if not prompt or len(prompt.strip()) == 0:
            return
        
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt[-8000:],
                "stream": True,
                "temperature": 0.5,
                "options": {
                    "num_predict": 400,
                    "num_ctx": 8192,
                    "num_thread": 4,
                    "top_k": 40,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                },
                "keep_alive": "5m"
            }
            if kwargs.get("format"):
                payload["format"] = kwargs["format"]
            
            response = requests.post(url, json=payload, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        # WRAP IN JSON FOR FRONTEND COMPATIBILITY
                        yield json.dumps({"token": chunk['response'], "done": False}) + "\n"
                    if chunk.get('done'):
                        yield json.dumps({"token": "", "done": True, "type": "end"}) + "\n"
                        break
        except Exception as e:
            print(f"Ollama streaming error: {e}")
            yield json.dumps({"token": f" [Error: {str(e)}]", "done": True}) + "\n"

class LLMEngine:
    def __init__(self):
        self.provider_name = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model_name = os.getenv("LLM_MODEL", "qwen2.5:3b")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.enabled = os.getenv("USE_LLM", "true").lower() == "true"
        
        print(f"LLM Engine Init:")
        print(f"   Provider: {self.provider_name}")
        print(f"   Model: {self.model_name}")
        print(f"   Host: {self.ollama_host}")
        print(f"   Enabled: {self.enabled}")
        
        if self.provider_name == "ollama":
            self.provider = OllamaProvider(
                model=self.model_name,
                host=self.ollama_host
            )
            
            if not self.provider.is_available():
                print(f"WARNING: Ollama is not available at {self.ollama_host}")
                print(f"   Make sure Ollama is running: ollama serve")
        else:
            self.provider = None
            print(f"Unknown provider: {self.provider_name}")

    def _build_final_prompt(self, user_message, expert_context=None, user_profile=None):
        """Forceful Grounded-First Prompt (YAFI 2.1)"""
        system_intro = (
            "Tu es YAFI, le système expert d'orientation scolaire au MAROC.\n"
            "TON STYLE : Professionnel, précis et synthétique. Tu es un conseiller expert, pas un ami informel.\n"
            "CONSIGNE : Sois direct. Évite les longs paragraphes. Utilise des listes à puces.\n"
            "RÈGLE D'OR : N'UTILISE QUE LES 'DONNÉES EXPERTES' CI-DESSOUS. Si elles sont absentes, réponds simplement que tu n'as pas l'information.\n"
            "IDENTITÉ : YAFI v2.5 créé par Adam Moufrije, Yasser et Fahd.\n"
        )
        
        user_info = ""
        if user_profile:
            bac = user_profile.get('bac')
            ville = user_profile.get('ville')
            if bac or ville:
                user_info = f"[INFO PROFIL : Bac {bac if bac else '?'} | Ville {ville if ville else '?'}]\n"

        facts_block = f"### DONNÉES EXPERTES (SOURCE VÉRITABLE) :\n{expert_context}\n" if expert_context else "### (Aucune donnée experte disponible, utilise le RAG ou tes connaissances générales sur le MAROC uniquement)\n"

        return (
            f"{system_intro}\n"
            f"{user_info}\n"
            f"{facts_block}\n"
            "-----------------\n"
            f"Question de l'élève : {user_message}\n"
            "Ta réponse (Groundée, Humanisée, Marocaine) :"
        )

    def _is_safe(self, text: str) -> bool:
        """Checks if the generated text contains forbidden off-topic content"""
        blacklist = [
            "arabie saoudite", "royaume-uni", "united kingdom", "saudi arabia", 
            "tourisme", "visiter la ville", "faire du soleil", "plages de",
            "monuments", "touristique", "recette", "tajine", "couscous", "cuisine", 
            "ingrédients", "cuisson", "match", "football", "météo", "température"
        ]
        text_low = text.lower()
        for word in blacklist:
            if word in text_low:
                if word == "visiter" and any(x in text_low for x in ["école", "ecole", "campus", "établissement"]):
                    continue
                return False
        return True

    def ask(self, prompt: str, temperature: float = 0.3, expert_context: str = None, user_profile: dict = None, **kwargs) -> str:
        if not self.enabled or not self.provider:
            return ""
        
        final_prompt = self._build_final_prompt(prompt, expert_context, user_profile)
        response = self.provider.generate(final_prompt, temperature=temperature, **kwargs)
        
        if not self._is_safe(response):
            return "Je m'excuse, je me suis un peu égaré. Je suis votre expert en orientation au Maroc. Comment puis-je vous aider pour vos études ou votre carrière ?"
        
        return response

    def ask_stream(self, prompt: str, temperature: float = 0.3, expert_context: str = None, user_profile: dict = None, **kwargs):
        if not self.enabled or not self.provider:
            yield "LLM engine is disabled or no provider"
            return
        
        final_prompt = self._build_final_prompt(prompt, expert_context, user_profile)
        full_text = ""
        for chunk in self.provider.generate_stream(final_prompt, temperature=temperature, **kwargs):
            full_text += chunk
            yield chunk
            
        if not self._is_safe(full_text):
            print(f"WARNING: Potential off-topic detected in stream: {full_text[:50]}...")
    
    def health_check(self) -> dict:
        return {
            "provider": self.provider_name,
            "model": self.model_name,
            "enabled": self.enabled,
            "available": self.provider.is_available() if self.provider else False
        }

llm_engine = LLMEngine()
