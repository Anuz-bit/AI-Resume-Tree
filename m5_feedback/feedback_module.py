import json
import uuid
import yaml
from typing import Dict, Any

from shared.llm_client import LLMClient

class FeedbackError(Exception):
    pass

class FeedbackModule:
    def __init__(self):
        self.llm = LLMClient()
        self.prompt_path = "./prompts/feedback.yaml"
        
    def _load_prompt(self, eval_result: Dict[str, Any]) -> tuple[str, str]:
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
            
        system = prompt_data.get('system', '')
        user_template = prompt_data.get('user_template', '')
        
        user_prompt = user_template.replace(
            '{eval_result}', json.dumps(eval_result, indent=2)
        )
        return system, user_prompt

    def generate_feedback(self, eval_result: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt, user_prompt = self._load_prompt(eval_result)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Temperature 0.4 for M5 feedback
                feedback_json = self.llm.call_json(user_prompt, system_prompt, 0.4)
                
                # Assign feedback ID and reference eval ID
                feedback_json['feedback_id'] = str(uuid.uuid4())
                feedback_json['eval_id'] = eval_result.get('eval_id', '')
                
                # No formal schema to validate as per constraints (only 4 schemas defined)
                # Just return the JSON object
                return feedback_json
            except Exception as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise FeedbackError(f"Failed to generate feedback after {max_retries} attempts. Last error: {str(last_error)}")
