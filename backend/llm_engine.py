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
<<<<<<< HEAD
        self.timeout = 25  # Fast timeout - 1.2B model should respond quickly
=======
        self.timeout = 45  # Increased for stability on 2-core / 4GB RAM hardware
>>>>>>> 3257fc1 (final)
        self.max_retries = 1  # Only 1 attempt to avoid long waits

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
<<<<<<< HEAD
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
=======
            print(f"Ollama not available: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.3, **kwargs) -> str:
        """Standard non-streaming generation"""
        if not prompt or len(prompt.strip()) == 0:
            return ""
        
        # Combine all chunks if we use the stream version under the hood, 
        # but for efficiency we'll keep a direct non-stream call too
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt[-8000:],
                "stream": False,
                "temperature": temperature,
                "options": {
                    "num_predict": 512,    # Increased from 150
                    "num_ctx": 4096,       # Increased from 1536
                    "num_thread": 4,
                    "top_k": 40,           # More diversity
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                },
                "keep_alive": -1            # Keep in RAM Indefinitely
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
        """
        Generate response from Ollama as a stream of chunks
        Yields:
            String chunks of the response
        """
        if not prompt or len(prompt.strip()) == 0:
            return
        
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt[-8000:],
                "stream": True,
                "temperature": temperature,
                "options": {
                    "num_predict": 1024,   # Increased for longer responses
                    "num_ctx": 8192,       # Massive context expansion
                    "num_thread": 4,
                    "top_k": 40,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                },
                "keep_alive": -1
            }
            if kwargs.get("format"):
                payload["format"] = kwargs["format"]
            
            response = requests.post(url, json=payload, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        yield chunk['response']
                    if chunk.get('done'):
                        break
        except Exception as e:
            print(f"Ollama streaming error: {e}")
            yield f" [Error: {str(e)}]"
>>>>>>> 3257fc1 (final)

class LLMEngine:
    def __init__(self):
        self.provider_name = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model_name = os.getenv("LLM_MODEL", "llama3.2:1b")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.enabled = os.getenv("USE_LLM", "true").lower() == "true"
        
<<<<<<< HEAD
        print(f"📌 LLM Engine Init:")
=======
        print(f"LLM Engine Init:")
>>>>>>> 3257fc1 (final)
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
<<<<<<< HEAD
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
=======
                print(f"WARNING: Ollama is not available at {self.ollama_host}")
                print(f"   Make sure Ollama is running: ollama serve")
        else:
            self.provider = None
            print(f"Unknown provider: {self.provider_name}")

    def _build_final_prompt(self, user_message, expert_context=None, user_profile=None):
        """Locked Academic Persona Prompt"""
        # Identity and Domain Locking
        system_intro = (
            "Tu es YAFI, l'assistant expert en ORIENTATION SCOLAIRE ET UNIVERSITAIRE au MAROC.\n"
            "Tu as été créé par Adam Moufrije, Yasser et Fahd.\n"
            "RÈGLES ABSOLUES (ARCHITECTURE YAFI 2.1) :\n"
            "1. RÉPONSES BASÉES SUR LES DONNÉES : Utilise SEULEMENT les DONNÉES EXPERTES fournies. Si une info est absente, dis 'Je n'ai pas cette donnée précise'.\n"
            "2. ANTI-HALLUCINATION : Ne mentionne jamais de pays étrangers (Arabie, France, USA) comme s'ils faisaient partie de l'orientation marocaine. Si on te demande pour un autre pays, dis poliment que ton expertise se limite strictement au Maroc.\n"
            "3. MAROC STRICT : Ton expertise est limitée au système d'enseignement au MAROC.\n"
            "4. TON : Professionnel, bienveillant, concis (3-4 phrases max).\n"
            "5. DISAMBIGUATION : UIK = Agadir | UIR = Rabat | EMI = Public (Rabat) | EMSI = Privé (Multi-villes).\n"
            "6. HORS-SUJET : Bloque immédiatement toute question sur la cuisine, le sport ou la météo. Reste académique.\n"
            "7. IDENTITÉ : Présente-toi comme YAFI. Ne redis jamais 'Bonjour' inutilement.\n"
        )
        
        # Memory awareness
        user_info = ""
        if user_profile:
            bac = user_profile.get('bac')
            ville = user_profile.get('ville')
            if bac or ville:
                user_info = f"[INFO PROFIL : L'utilisateur est en {bac if bac else '?'} à {ville if ville else '?'}.]\n"

        # Facts
        facts_block = f"### DONNÉES EXPERTES :\n{expert_context}\n" if expert_context else ""

        return (
            f"{system_intro}\n\n"
            f"{user_info}\n"
            f"{facts_block}\n"
            f"Message de l'utilisateur : {user_message}\n\n"
            "Réponse de YAFI (Orientation Maroc uniquement) :"
        )

    def _is_safe(self, text: str) -> bool:
        """Checks if the generated text contains forbidden off-topic content"""
        blacklist = [
            "arabie saoudite", "royaume-uni", "united kingdom", "saudi arabia", 
            "tourisme", "visiter la ville", "faire du soleil", "plages de",
            "monuments", "touristique",
            # Cuisine / Food (Faille Q5 Stress Test)
            "recette", "tajine", "couscous", "cuisine", "ingrédients", "cuisson",
            "grammes de", "cuillère", "four", "mijoter",
            # Sport / Loisirs
            "match", "football", "météo", "température",
            # Politique
            "élection", "parti politique", "vote"
        ]
        text_low = text.lower()
        for word in blacklist:
            if word in text_low:
                # Exception: "visiter" is allowed if followed by "école", "établissement", "campus"
                if word == "visiter" and any(x in text_low for x in ["école", "ecole", "campus", "établissement"]):
                    continue
                return False
        return True

    def ask(self, prompt: str, temperature: float = 0.3, expert_context: str = None, user_profile: dict = None, **kwargs) -> str:
        """Standard ask with safety guard"""
        if not self.enabled or not self.provider:
            return ""
        
        final_prompt = self._build_final_prompt(prompt, expert_context, user_profile)
        response = self.provider.generate(final_prompt, temperature=temperature, **kwargs)
        
        if not self._is_safe(response):
            return "Je m'excuse, je me suis un peu égaré. Je suis votre expert en orientation au Maroc. Comment puis-je vous aider pour vos études ou votre carrière ?"
        
        return response

    def ask_stream(self, prompt: str, temperature: float = 0.3, expert_context: str = None, user_profile: dict = None, **kwargs):
        """Streaming ask with safety guard (buffers chunks to validate)"""
        if not self.enabled or not self.provider:
            yield "LLM engine is disabled or no provider"
            return
        
        final_prompt = self._build_final_prompt(prompt, expert_context, user_profile)
        full_text = ""
        for chunk in self.provider.generate_stream(final_prompt, temperature=temperature, **kwargs):
            full_text += chunk
            yield chunk
            
        # Post-stream validation (informative for logging/future)
        if not self._is_safe(full_text):
            print(f"WARNING: Potential off-topic detected in stream: {full_text[:50]}...")
>>>>>>> 3257fc1 (final)
    
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
