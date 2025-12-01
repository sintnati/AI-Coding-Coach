import json
import uuid
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class Message:
agent_id: str
task_id: str
payload: Dict[str, Any]
trace_id: str = None
meta: Dict[str, Any] = None


def __post_init__(self):
if not self.trace_id:
self.trace_id = str(uuid.uuid4())


def to_json(self):
return json.dumps(asdict(self))