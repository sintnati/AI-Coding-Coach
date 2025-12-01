"""
Test script to verify agent flow with mocked LLM.
"""
import asyncio
import sys
import os
from unittest.mock import MagicMock, AsyncMock

# Add current directory to path
sys.path.append(os.getcwd())

from services.agents.orchestrator_agent import OrchestratorAgent

# Mock LLM client
async def mock_llm_client(prompt, model, **kwargs):
    if "Analyze this coding activity" in prompt:
        return '{"skill_level": "Intermediate", "languages": ["Python"], "patterns": ["Consistent"], "platform_preference": "Codeforces"}'
    elif "identify weak areas" in prompt:
        return '{"weak_topics": ["graphs"], "missing_fundamentals": [], "improvement_priority": ["graphs"]}'
    elif "Generate" in prompt and "tasks" in prompt:
        return '[{"title": "Graph BFS", "difficulty": "Medium", "topic": "graphs", "due_days": 3, "reason": "Practice"}]'
    return "{}"

async def test_flow():
    print("Initializing orchestrator...")
    orchestrator = OrchestratorAgent(mock_llm_client)

    user_id = "test_user"
    processed_data = {
        "activities": [{"platform": "codeforces", "tags": ["graphs"], "verdict": "OK"}],
        "growth_metrics": {
            "total_platforms": 1,
            "days_active": 10,
            "platform_stats": {"codeforces": {"total": 10, "solved": 5}}
        }
    }

    print("Running analysis...")
    result = await orchestrator.run_analysis(user_id, processed_data)

    print("\nResult keys:", result.keys())
    if "error" in result:
        print("FAILED with error:", result["error"])
    else:
        print("SUCCESS!")
        print("Tasks generated:", len(result.get("tasks", [])))

if __name__ == "__main__":
    asyncio.run(test_flow())
