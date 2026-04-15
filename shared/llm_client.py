import os
import json
import hashlib
import time
import google.generativeai as genai

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
            raise LLMError("GEMINI_API_KEY environment variable not set")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
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

    def _parse_retry_delay(self, error_msg):
        import re
        match = re.search(r"retryDelay['\"]:\s*['\"](\d+)s['\"]", str(error_msg))
        if match:
            return int(match.group(1))
        return None

    def call(self, prompt, system="", temperature=0.2):
        key = self._cache_key(prompt, system, temperature)
        if key in self._cache:
            return self._cache[key]

        # Use system instructions natively if available in GenerativeModel, but merging is safer
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        max_retries = 5
        base_delays = [15, 30, 60, 60, 120]

        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        response_mime_type="application/json"
                    )
                )
                result = response.text
                self._cache[key] = result
                self._save_cache()
                return result
            except Exception as e:
                err_str = str(e)
                if ("429" in err_str or "quota" in err_str.lower() or "503" in err_str) and attempt < max_retries - 1:
                    api_delay = self._parse_retry_delay(err_str)
                    wait_time = (api_delay + 5) if api_delay else base_delays[attempt]
                    print(f"  [Rate limited] Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    raise LLMError(f"LLM API call failed: {err_str}")

    def call_json(self, prompt, system="", temperature=0.2):
        json_system = (system or "") + "\nReturn ONLY valid JSON. No markdown, no backticks, no explanation."
        response_text = self.call(prompt, json_system, temperature)

        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise LLMError(f"Failed to parse JSON response: {e}\nResponse was: {cleaned[:200]}")