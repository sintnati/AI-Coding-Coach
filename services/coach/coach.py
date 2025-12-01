from libs.memory.faiss_store import FaissStore
from services.analyser.analyze import analyze_user_activity


class CoachAgent:
    def __init__(self, mem_store: FaissStore, model_name: str = "gemini-2.0-flash"):
        self.mem = mem_store
        self.model_name = model_name


    def run_cycle(self, user_id, recent_activities):
        analysis = analyze_user_activity(recent_activities, self.model_name)
        # convert analysis to tasks; this is simplified
        actions = analysis.get("actions") if isinstance(analysis, dict) else None
        if not actions:
            actions = [{"title": "Practice Graph BFS (easy)", "due_days": 2}]
        # persist summaries into memory (placeholder embeddings)
        # In real app call embedding model and add vectors to FAISS
        return {"tasks": actions, "analysis": analysis}

