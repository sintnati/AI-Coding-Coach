"""
Specialized agent for generating personalized practice tasks.
"""
import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)


class TaskGeneratorAgent:
    """Generates personalized practice tasks and recommendations."""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.agent_name = "TaskGeneratorAgent"

    async def generate_tasks(self, weaknesses: Dict, analysis: Dict, count: int = 5) -> Dict[str, Any]:
        """
        Generate personalized practice tasks.

        Args:
            weaknesses: Weak areas from WeaknessDetectorAgent
            analysis: Analysis from AnalyzerAgent
            count: Number of tasks to generate

        Returns:
            List of personalized tasks
        """
        logger.info(f"{self.agent_name}: Generating {count} tasks")

        weak_topics = weaknesses.get('weaknesses', {}).get('weak_topics', [])
        skill_level = analysis.get('analysis', {}).get('skill_level', 'Intermediate')

        prompt = f"""Generate {count} personalized coding practice tasks:

Skill Level: {skill_level}
Weak Topics: {', '.join(weak_topics[:5]) if weak_topics else 'General practice'}

For each task, provide:
1. Title (specific problem type)
2. Difficulty (Easy/Medium/Hard)
3. Topic/Tag
4. Estimated time (in days)
5. Why this task (brief explanation)

Return as JSON array with keys: title, difficulty, topic, due_days, reason"""

        try:
            response = await self.llm_client(prompt, "gemini-1.5-pro")
            logger.info(f"{self.agent_name}: Task generation complete")

            # Try to parse JSON
            try:
                from services.analyser.llm_client import extract_json_from_text
                cleaned_response = extract_json_from_text(response)
                tasks = json.loads(cleaned_response)
                if isinstance(tasks, list):
                    return {"status": "success", "tasks": tasks}
                else:
                    # Fallback tasks
                    return {"status": "success", "tasks": self._generate_fallback_tasks(weak_topics)}
            except:
                return {"status": "success", "tasks": self._generate_fallback_tasks(weak_topics)}

        except Exception as e:
            logger.error(f"{self.agent_name}: Generation failed - {e}")
            return {"status": "error", "error": str(e), "tasks": self._generate_fallback_tasks(weak_topics)}

    def _generate_fallback_tasks(self, topics: List[str]) -> List[Dict]:
        """Generate fallback tasks if LLM fails."""
        fallback = [
            {"title": "Practice Graph BFS Problems", "difficulty": "Medium", "topic": "graphs", "due_days": 3, "reason": "Strengthen graph traversal"},
            {"title": "Dynamic Programming Basics", "difficulty": "Easy", "topic": "dp", "due_days": 5, "reason": "Build DP foundation"},
            {"title": "Binary Search Variations", "difficulty": "Medium", "topic": "binary-search", "due_days": 2, "reason": "Master search techniques"},
        ]

        if topics:
            fallback[0]["topic"] = topics[0]
            fallback[0]["title"] = f"Practice {topics[0].title()} Problems"

        return fallback
