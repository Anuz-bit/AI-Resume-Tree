import os
import hashlib
import yaml
import pdfplumber
import docx
from typing import Dict, Any

from shared.llm_client import LLMClient
from shared.schema_validator import SchemaValidator, ValidationError

class ParseError(Exception):
    pass

class ResumeParser:
    def __init__(self):
        self.llm = LLMClient()
        self.validator = SchemaValidator()
        self.prompt_path = "./prompts/extract_resume.yaml"
        
    def _extract_text(self, file_path: str) -> (str, str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")
            
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        
        ext = file_path.lower().split('.')[-1]
        text = ""
        
        if ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        elif ext in ['doc', 'docx']:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext == 'txt':
            text = file_bytes.decode('utf-8', errors='ignore')
        else:
            raise ParseError(f"Unsupported file extension: {ext}")
            
        return text.strip(), file_hash

    def _load_prompt(self, raw_text: str) -> (str, str):
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
            
        system_prompt = prompt_data.get('system', '')
        user_template = prompt_data.get('user_template', '')
        
        user_prompt = user_template.replace('{raw_text}', raw_text)
        return system_prompt, user_prompt

    def parse(self, file_path: str) -> Dict[str, Any]:
        text, file_hash = self._extract_text(file_path)
        if not text:
            raise ParseError("No text could be extracted from the file.")
            
        system_prompt, user_prompt = self._load_prompt(text)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Temperature 0.1 for M1 extraction
                result_json = self.llm.call_json(user_prompt, system_prompt, 0.1)
                
                # Make sure file_hash is present as per schema
                result_json['file_hash'] = file_hash
                
                self.validator.validate(result_json, "resume_json.json")
                return result_json
            except (ValidationError, Exception) as e:
                last_error = e
                # Re-throw if it's the last attempt
                if attempt == max_retries - 1:
                    raise ParseError(f"Failed to parse resume after {max_retries} attempts. Last error: {str(last_error)}")
