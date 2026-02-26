import json
import time
from typing import Any, Dict, List

from tracing.trace import Trace


class LocalFileTrace(Trace):
    
    def __init__(self, filepath: str = "trace.json"):
        self.filepath = filepath
        self.records: List[Dict[str, Any]] = []

    def record(self, event_type: str, details: Dict[str, Any]):
        record = {
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        }
        self.records.append(record)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
