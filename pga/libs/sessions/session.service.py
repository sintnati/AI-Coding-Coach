from typing import Dict
import time, uuid


class InMemorySessionService:
def __init__(self):
self.sessions: Dict[str, dict] = {}


def create(self, user_id: str) -> dict:
sid = str(uuid.uuid4())
self.sessions[sid] = {"user_id": user_id, "created_at": time.time(), "context": []}
return {"session_id": sid}


def get(self, session_id: str):
return self.sessions.get(session_id)


def update_context(self, session_id: str, item):
s = self.sessions.get(session_id)
if s is None:
return False
s["context"].append(item)
return True