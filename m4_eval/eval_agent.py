import json
import uuid
import yaml
from typing import Dict, Any

from shared.llm_client import LLMClient
from shared.schema_validator import SchemaValidator, ValidationError

class EvalError(Exception):
    pass

class EvaluationAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.validator = SchemaValidator()
        self.prompt_path = "./prompts/evaluate.yaml"
        
    def _load_prompt(self, resume_tree: Dict[str, Any], jd_tree: Dict[str, Any]) -> tuple[str, str]:
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
            
        system = prompt_data.get('system', '')
        user_template = prompt_data.get('user_template', '')
        
        user_prompt = user_template.replace(
            '{resume_tree}', json.dumps(resume_tree, indent=2)
        ).replace(
            '{jd_tree}', json.dumps(jd_tree, indent=2)
        )
        return system, user_prompt

    def evaluate(self, resume_tree: Dict[str, Any], jd_tree: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt, user_prompt = self._load_prompt(resume_tree, jd_tree)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Temperature 0.2
                eval_json = self.llm.call_json(user_prompt, system_prompt, 0.2)
                eval_json['eval_id'] = str(uuid.uuid4())
                
                self.validator.validate(eval_json, "eval_result.json")
                return eval_json
            except (ValidationError, Exception) as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise EvalError(f"Failed to evaluate candidate after {max_retries} attempts. Last error: {str(last_error)}")
