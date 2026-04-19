pip install google-genaiimport os
import json
from typing import Optional, Dict, Any

class CacheManager:
    def __init__(self, base_path: str = "./data/api_cache/"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)

    def _get_file_path(self, key: str) -> str:
        return os.path.join(self.base_path, f"{key}.json")

    def exists(self, key: str) -> bool:
        return os.path.exists(self._get_file_path(key))

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        path = self._get_file_path(key)
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def set(self, key: str, value: Dict[str, Any]) -> None:
        path = self._get_file_path(key)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(value, f, indent=2)
