"""
Specialized agent for detecting weak areas and improvement opportunities.
"""
import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)


class WeaknessDetectorAgent:
    """Identifies weak topics and areas needing improvement."""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.agent_name = "WeaknessDetectorAgent"

    async def detect_weaknesses(self, activities: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """
        Detect weak areas and topics needing improvement.

        Args:
            activities: List of coding activities
            analysis: Results from AnalyzerAgent

        Returns:
            Weak topics and improvement areas
        """
        logger.info(f"{self.agent_name}: Detecting weak areas")

        # Extract topics from activities
        topics = self._extract_topics(activities)

        prompt = f"""Based on this coding activity, identify weak areas:

Topics attempted: {', '.join(topics[:20])}
Skill Level: {analysis.get('analysis', {}).get('skill_level', 'Unknown')}

Analyze:
1. Topics with low success rate
2. Avoided or missing fundamental topics
3. Areas with inconsistent performance
4. Gaps in knowledge

Return JSON with: weak_topics (list), missing_fundamentals (list), improvement_priority (list)"""

        try:
            response = await self.llm_client(prompt, "gemini-2.0-flash")
            logger.info(f"{self.agent_name}: Weakness detection complete")

            # Try to parse JSON response
            try:
                from services.analyser.llm_client import extract_json_from_text
                cleaned_response = extract_json_from_text(response)
                parsed = json.loads(cleaned_response)
                logger.info(f"{self.agent_name}: Successfully parsed JSON response")
                return {"status": "success", "weaknesses": parsed}
            except json.JSONDecodeError:
                # If not valid JSON, try to extract useful info or use fallback
                logger.warning(f"{self.agent_name}: Response is not valid JSON, using fallback")
                return {
                    "status": "success",
                    "weaknesses": {
                        "weak_topics": topics[:3] if topics else ["algorithms", "data-structures"],
                        "missing_fundamentals": ["practice consistency"],
                        "improvement_priority": ["Focus on weak topics"],
                        "raw_response": response
                    }
                }

        except Exception as e:
            logger.error(f"{self.agent_name}: Detection failed - {e}")
            # Return fallback weaknesses
            return {
                "status": "error",
                "error": str(e),
                "weaknesses": {
                    "weak_topics": topics[:3] if topics else ["algorithms", "data-structures"],
                    "missing_fundamentals": ["practice consistency"],
                    "improvement_priority": ["Focus on weak topics"]
                }
            }

    def _extract_topics(self, activities: List[Dict]) -> List[str]:
        """Extract unique topics from activities."""
        topics = set()
        for activity in activities:
            if isinstance(activity, dict) and 'tags' in activity:
                topics.update(activity.get('tags', []))
        return list(topics)
