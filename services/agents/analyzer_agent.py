"""
Specialized agent for analyzing coding patterns and skill levels.
"""
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class AnalyzerAgent:
    """Analyzes user's coding patterns, strengths, and skill progression."""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.agent_name = "AnalyzerAgent"

    async def analyze(self, activities: List[Dict], growth_metrics: Dict) -> Dict[str, Any]:
        """
        Analyze coding patterns and skill levels.

        Args:
            activities: List of coding activities
            growth_metrics: Growth metrics from preprocessor

        Returns:
            Analysis results including skill map and patterns
        """
        logger.info(f"{self.agent_name}: Starting pattern analysis")

        # Prepare analysis prompt
        prompt = f"""Analyze this coding activity data and identify patterns:

Total Activities: {len(activities)}
Platforms: {growth_metrics.get('total_platforms', 0)}
Days Active: {growth_metrics.get('days_active', 0)}
Current Streak: {growth_metrics.get('streak', {}).get('current', 0)}

Platform Stats:
{self._format_platform_stats(growth_metrics.get('platform_stats', {}))}

Based on this data, provide:
1. Skill level assessment (Beginner/Intermediate/Advanced)
2. Primary programming languages
3. Coding patterns (consistency, difficulty progression)
4. Platform preferences

Return as JSON with keys: skill_level, languages, patterns, platform_preference"""

        try:
            response = await self.llm_client(prompt, "gemini-2.0-flash")
            logger.info(f"{self.agent_name}: Analysis complete")

            # Try to parse JSON response
            import json
            from services.analyser.llm_client import extract_json_from_text

            try:
                cleaned_response = extract_json_from_text(response)
                parsed_analysis = json.loads(cleaned_response)
                logger.info(f"{self.agent_name}: Successfully parsed JSON response")
            except json.JSONDecodeError:
                # If not valid JSON, create a structured response
                logger.warning(f"{self.agent_name}: Response is not valid JSON, using fallback structure")
                parsed_analysis = {
                    "skill_level": "Intermediate",
                    "languages": ["Python", "C++"],
                    "patterns": ["Regular practice"],
                    "platform_preference": "Multiple platforms",
                    "raw_response": response
                }

            return {
                "status": "success",
                "analysis": parsed_analysis,
                "growth_metrics": growth_metrics
            }
        except Exception as e:
            logger.error(f"{self.agent_name}: Analysis failed - {e}")
            # Return fallback response
            return {
                "status": "error",
                "error": str(e),
                "analysis": {
                    "skill_level": "Intermediate",
                    "languages": [],
                    "patterns": [f"Analysis based on {len(activities)} activities"],
                    "platform_preference": "Unknown"
                },
                "growth_metrics": growth_metrics
            }

    def _format_platform_stats(self, stats: Dict) -> str:
        """Format platform stats for prompt."""
        lines = []
        for platform, data in stats.items():
            lines.append(f"  {platform}: {data.get('solved', 0)}/{data.get('total', 0)} solved")
        return "\n".join(lines) if lines else "No data"
