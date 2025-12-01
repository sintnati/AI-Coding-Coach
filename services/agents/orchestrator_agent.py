"""
Orchestrator agent that coordinates multiple specialized agents.
"""
import logging
import asyncio
from typing import Dict, List, Any
from services.agents.analyzer_agent import AnalyzerAgent
from services.agents.weakness_detector_agent import WeaknessDetectorAgent
from services.agents.task_generator_agent import TaskGeneratorAgent

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """Coordinates multiple specialized agents for comprehensive analysis."""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.agent_name = "OrchestratorAgent"

        # Initialize specialized agents
        self.analyzer = AnalyzerAgent(llm_client)
        self.weakness_detector = WeaknessDetectorAgent(llm_client)
        self.task_generator = TaskGeneratorAgent(llm_client)

        logger.info(f"{self.agent_name}: Initialized with 3 specialized agents")

    async def run_analysis(self, user_id: str, processed_data: Dict) -> Dict[str, Any]:
        """
        Run comprehensive multi-agent analysis.

        Args:
            user_id: User identifier
            processed_data: Processed activity data with growth metrics

        Returns:
            Comprehensive analysis results from all agents
        """
        logger.info(f"{self.agent_name}: Starting multi-agent analysis for user {user_id}")

        activities = processed_data.get('activities', [])
        growth_metrics = processed_data.get('growth_metrics', {})

        try:
            # Phase 1: Pattern Analysis (sequential - needed for next steps)
            logger.info(f"{self.agent_name}: Phase 1 - Pattern Analysis")
            analysis_result = await self.analyzer.analyze(activities, growth_metrics)

            # Phase 2: Weakness detection
            logger.info(f"{self.agent_name}: Phase 2 - Weakness Detection")
            weakness_result = await self.weakness_detector.detect_weaknesses(activities, analysis_result)

            # Phase 3: Task Generation (depends on weaknesses)
            logger.info(f"{self.agent_name}: Phase 3 - Task Generation")
            tasks_result = await self.task_generator.generate_tasks(weakness_result, analysis_result)

            # Combine results
            final_result = {
                "user_id": user_id,
                "analysis": analysis_result,
                "weaknesses": weakness_result,
                "tasks": tasks_result.get('tasks', []),
                "growth_metrics": growth_metrics,
                "agent_execution": {
                    "orchestrator": self.agent_name,
                    "agents_used": ["AnalyzerAgent", "WeaknessDetectorAgent", "TaskGeneratorAgent"],
                    "execution_mode": "sequential"
                }
            }

            logger.info(f"{self.agent_name}: Multi-agent analysis complete")
            return final_result

        except Exception as e:
            logger.error(f"{self.agent_name}: Analysis failed - {e}", exc_info=True)
            return {
                "user_id": user_id,
                "error": str(e),
                "status": "failed",
                "growth_metrics": growth_metrics
            }

    async def run_parallel_analysis(self, user_id: str, processed_data: Dict) -> Dict[str, Any]:
        """
        Run analysis with parallel agent execution where possible.

        Args:
            user_id: User identifier
            processed_data: Processed activity data

        Returns:
            Analysis results from parallel execution
        """
        logger.info(f"{self.agent_name}: Starting PARALLEL multi-agent analysis")

        activities = processed_data.get('activities', [])
        growth_metrics = processed_data.get('growth_metrics', {})

        try:
            # Phase 1: Pattern Analysis (must be first)
            analysis_result = await self.analyzer.analyze(activities, growth_metrics)

            # Phase 2: Run weakness detection (could be parallel in future with other tasks)
            logger.info(f"{self.agent_name}: Running parallel agents")
            weakness_result = await self.weakness_detector.detect_weaknesses(activities, analysis_result)

            # Phase 3: Generate final tasks
            tasks_result = await self.task_generator.generate_tasks(weakness_result, analysis_result)

            final_result = {
                "user_id": user_id,
                "analysis": analysis_result,
                "weaknesses": weakness_result,
                "tasks": tasks_result.get('tasks', []),
                "growth_metrics": growth_metrics,
                "agent_execution": {
                    "orchestrator": self.agent_name,
                    "agents_used": ["AnalyzerAgent", "WeaknessDetectorAgent", "TaskGeneratorAgent"],
                    "execution_mode": "parallel"
                }
            }

            logger.info(f"{self.agent_name}: Parallel analysis complete")
            return final_result

        except Exception as e:
            logger.error(f"{self.agent_name}: Parallel analysis failed - {e}", exc_info=True)
            return {
                "user_id": user_id,
                "error": str(e),
                "status": "failed",
                "growth_metrics": growth_metrics
            }
