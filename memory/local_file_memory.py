import json
import os
from typing import Dict, List

from memory.memory import Memory


class LocalFileMemory(Memory):
    
    def __init__(self, filepath: str = "session.json"):
        self.filepath = filepath
        self.messages: List[Dict[str, str]] = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.messages = json.load(f)
            except Exception:
                self.messages = []

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.save()

    def get_context(self) -> List[Dict[str, str]]:
        return self.messages
