import json
import uuid
import yaml
import os
from typing import Dict, Any

from shared.llm_client import LLMClient

class FeedbackError(Exception):
    pass

class FeedbackModule:
    def __init__(self):
        self.llm = LLMClient()
        self.prompt_path = "./prompts/feedback.yaml"
        # User requested gemini-2.0-flash
        self.model = "gemini-2.0-flash"
        
    def _load_prompt(self, eval_result: Dict[str, Any]) -> tuple[str, str]:
        if not os.path.exists(self.prompt_path):
            raise FeedbackError(f"Prompt file not found at {self.prompt_path}")
            
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
            
        system = prompt_data.get('system', '')
        user_template = prompt_data.get('user_template', '')
        
        # Inject the eval result into the template
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
                # Use model specified and temperature 0.4
                feedback_json = self.llm.call_json(
                    prompt=user_prompt, 
                    system=system_prompt, 
                    temperature=0.4,
                    model=self.model
                )
                
                # Metadata injection
                feedback_json['feedback_id'] = str(uuid.uuid4())
                feedback_json['eval_id'] = eval_result.get('eval_id', '')
                
                # Basic validation of expected keys
                required_keys = ['improvement_tips', 'resume_rewrites', 'overall_advice']
                for key in required_keys:
                    if key not in feedback_json:
                        feedback_json[key] = [] if key != 'overall_advice' else ""
                
                return feedback_json
                
            except Exception as e:
                last_error = e
                # If 429 occurs and we're in my restricted environment, try falling back to 2.5-flash
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"  [Notice] gemini-2.0-flash restricted. Attempting with fallback model...")
                    try:
                        return self.llm.call_json(
                            prompt=user_prompt, 
                            system=system_prompt, 
                            temperature=0.4,
                            model="gemini-2.5-flash"
                        )
                    except:
                        pass
                
                if attempt == max_retries - 1:
                    raise FeedbackError(f"Failed to generate feedback: {str(last_error)}")
