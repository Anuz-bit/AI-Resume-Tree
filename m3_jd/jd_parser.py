import os
import hashlib
import yaml
from typing import Dict, Any

from shared.llm_client import LLMClient
from shared.schema_validator import SchemaValidator, ValidationError

class JDParseError(Exception):
    pass

class JDParser:
    def __init__(self):
        self.llm = LLMClient()
        self.validator = SchemaValidator()
        self.prompt_path = "./prompts/parse_jd.yaml"
        
    def _read_jd_text(self, file_path: str) -> (str, str):
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"JD file not found: {abs_path}")
            
        try:
            with open(abs_path, "r", encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(abs_path, "r", encoding='latin-1') as f:
                text = f.read()
                
        # Handle CRLF vs LF
        text = text.replace('\r\n', '\n')
            
        jd_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return text.strip(), jd_hash

    def _load_prompt(self, jd_text: str) -> (str, str):
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
            
        system = prompt_data.get('system', '')
        user_template = prompt_data.get('user_template', '')
        
        user_prompt = user_template.replace('{jd_text}', jd_text)
        return system, user_prompt

    def parse(self, file_path: str) -> Dict[str, Any]:
        text, jd_hash = self._read_jd_text(file_path)
        if not text:
            raise JDParseError("No text found in JD file.")
            
        system_prompt, user_prompt = self._load_prompt(text)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Temperature 0.1 for consistent extraction
                jd_json = self.llm.call_json(user_prompt, system_prompt, 0.1)
                jd_json['jd_hash'] = jd_hash
                
                self.validator.validate(jd_json, "jd_tree.json")
                return jd_json
            except (ValidationError, Exception) as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise JDParseError(f"Failed to parse JD after {max_retries} attempts. Last error: {str(last_error)}")
