import json
import hashlib
from pathlib import Path

class AICache:
    def __init__(self):
        self.cache_file = Path.home() / ".autofix_cache.json"
        self.cache = self._load()

    def _load(self):
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save(self):
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f)
        except Exception:
            pass

    def get(self, content: str):
        key = hashlib.md5(content.encode()).hexdigest()
        return self.cache.get(key)

    def set(self, content: str, analysis: dict):
        key = hashlib.md5(content.encode()).hexdigest()
        self.cache[key] = analysis
        self._save()
