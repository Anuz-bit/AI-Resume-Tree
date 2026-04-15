import json
import yaml
from typing import Dict, Any

from shared.llm_client import LLMClient
from shared.schema_validator import SchemaValidator, ValidationError

class TreeBuilderError(Exception):
    pass

class ResumeTreeBuilder:
    def __init__(self):
        self.llm = LLMClient()
        self.validator = SchemaValidator()
        self.prompt_path = "./prompts/build_tree.yaml"
        
    def _load_prompt(self, resume_json: Dict[str, Any]) -> tuple[str, str]:
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
            
        system = prompt_data.get('system', '')
        user_template = prompt_data.get('user_template', '')
        
        user_prompt = user_template.replace('{resume_json}', json.dumps(resume_json, indent=2))
        return system, user_prompt

    def build_tree(self, resume_json: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt, user_prompt = self._load_prompt(resume_json)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Assuming temperature 0.2 for tree generation
                tree_json = self.llm.call_json(user_prompt, system_prompt, 0.2)
                
                self.validator.validate(tree_json, "tree_node.json")
                return tree_json
            except (ValidationError, Exception) as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise TreeBuilderError(f"Failed to build tree after {max_retries} attempts. Last error: {str(last_error)}")
