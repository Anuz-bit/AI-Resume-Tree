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
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise LLMError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash"
        self._cache = {}
        self._initialized = True

    def _cache_key(self, prompt, system, temperature):
        raw = f"{prompt}{system}{temperature}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def call(self, prompt, system="", temperature=0.2):
        key = self._cache_key(prompt, system, temperature)
        if key in self._cache:
            return self._cache[key]

        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=4096
                    )
                )
                result = response.text
                self._cache[key] = result
                return result
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise LLMError(f"LLM API call failed after {max_retries} retries: {str(e)}")

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