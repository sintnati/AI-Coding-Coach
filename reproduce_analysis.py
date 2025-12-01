import asyncio
import sys
import os
import json
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

from services.agents.analyzer_agent import AnalyzerAgent

async def test_analysis_parsing():
    print("Testing AnalyzerAgent JSON parsing...")

    # Mock LLM client that returns Markdown-wrapped JSON
    async def mock_llm_client(prompt, model):
        return """```json
{
    "skill_level": "Advanced",
    "languages": ["Python", "Rust"],
    "patterns": ["Consistent daily practice"],
    "platform_preference": "Codeforces"
}
```"""

    agent = AnalyzerAgent(mock_llm_client)

    activities = [{"platform": "codeforces", "verdict": "OK"}]
    growth_metrics = {"total_platforms": 1}

    result = await agent.analyze(activities, growth_metrics)

    print(f"Status: {result['status']}")
    print(f"Analysis: {result['analysis']}")

    if result['analysis'].get('skill_level') == "Intermediate" and "raw_response" in result['analysis']:
        print("ISSUE REPRODUCED: Fallback triggered due to Markdown code blocks.")
    elif result['analysis'].get('skill_level') == "Advanced":
        print("ISSUE NOT REPRODUCED: JSON parsed successfully.")
    else:
        print("Unexpected result.")

if __name__ == "__main__":
    asyncio.run(test_analysis_parsing())
