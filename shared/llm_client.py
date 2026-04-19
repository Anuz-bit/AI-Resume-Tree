import os
import json
import hashlib
import time
from google import genai
from google.genai import types

class LLMError(Exception):
    pass


class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
            
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise LLMError("GEMINI_API_KEY environment variable not set. Please add it to a .env file.")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"
        
        self.cache_file = "./data/api_cache/llm_cache.json"
        self._cache = self._load_cache()
        self._initialized = True

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_cache(self):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self._cache, f)
        except Exception:
            pass

    def _cache_key(self, prompt, system, temperature):
        raw = f"{prompt}{system}{temperature}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def call(self, prompt, system="", temperature=0.2, model=None):
        key = self._cache_key(prompt, system, temperature)
        if key in self._cache:
            return self._cache[key]

        target_model = model or self.model_id
        max_retries = 5
        base_delays = [5, 10, 20, 40, 60]

        for attempt in range(max_retries):
            try:
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system if system else None,
                    response_mime_type="application/json"
                )
                
                response = self.client.models.generate_content(
                    model=target_model,
                    contents=prompt,
                    config=config
                )
                
                result = response.text
                if not result:
                     raise LLMError("Empty response from LLM")
                     
                self._cache[key] = result
                self._save_cache()
                return result
            except Exception as e:
                err_str = str(e)
                if ("429" in err_str or "quota" in err_str.lower() or "503" in err_str) and attempt < max_retries - 1:
                    wait_time = base_delays[attempt]
                    print(f"  [Rate limited/Error] Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    raise LLMError(f"LLM API call failed after {attempt+1} attempts: {err_str}")

    def call_json(self, prompt, system="", temperature=0.2, model=None):
        # The new SDK handles application/json response_mime_type well, 
        # but we keep the system instruction nudge for safety.
        json_system = (system or "") + "\nReturn ONLY valid JSON."
        response_text = self.call(prompt, json_system, temperature, model=model)

        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[-1].split("```")[0]
            else:
                cleaned = cleaned.split("```")[-2]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            # Fallback: try to find anything between { and }
            try:
                start = cleaned.find('{')
                end = cleaned.rfind('}') + 1
                if start != -1 and end != 0:
                    return json.loads(cleaned[start:end])
            except:
                pass
            raise LLMError(f"Failed to parse JSON response: {e}\nResponse was: {cleaned[:200]}")