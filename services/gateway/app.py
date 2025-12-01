from fastapi import FastAPI, HTTPException, Response
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import logging
from services.fetcher.codeforces_fetcher import fetch_all
from services.preprocessor.preprocess import normalize_activities
from services.coach.coach import CoachAgent
from libs.memory.faiss_store import FaissStore
from libs.sessions import PersistentSessionService
from libs.observability import get_health_status, RequestTimer
import uvicorn
import os
import sys

# Fix for Windows event loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(title="AI Coding Coach", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Config
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Initialize services
mem = FaissStore(dim=512)

# Import LLM client for agents
from services.analyser.llm_client import generate_text

# Initialize multi-agent orchestrator
from services.agents.orchestrator_agent import OrchestratorAgent
orchestrator = OrchestratorAgent(generate_text)

session_service = PersistentSessionService()

logger.info(f"Initialized AI Coding Coach with Multi-Agent System")
logger.info(f"Agents: AnalyzerAgent, WeaknessDetectorAgent, TaskGeneratorAgent")
logger.info(f"Persistent storage enabled")




class LinkRequest(BaseModel):
    user_id: str
    handles: dict
    session_id: str = None  # Optional session ID for continuity


@app.get("/")
async def root():
    """Serve the web UI"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return get_health_status()


@app.get("/metrics")
async def metrics():
    """Metrics endpoint."""
    from libs.observability import metrics_collector
    return metrics_collector.get_metrics()


@app.post("/analyze")
async def analyze(req: LinkRequest, response: fastapi.Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    with RequestTimer("/analyze"):
        try:
            logger.info(f"Analysis request from user: {req.user_id}")

            # Validate input
            if not req.handles:
                raise HTTPException(status_code=400, detail="At least one platform handle required")

            # Get or create session
            if req.session_id:
                session = session_service.get(req.session_id)
                if not session:
                    logger.warning(f"Session {req.session_id} not found, creating new")
                    session = session_service.create(req.user_id)
            else:
                session = session_service.create(req.user_id)

            logger.info(f"Using session: {session['session_id']}")

            # Fetch data from all platforms
            logger.info(f"Received handles from user {req.user_id}: {req.handles}")
            logger.info(f"Fetching data from platforms: {list(req.handles.keys())}")

            # Validate that we have at least one non-empty handle
            valid_handles = {k: v for k, v in req.handles.items() if v and str(v).strip()}
            if not valid_handles:
                logger.error(f"No valid handles provided. Received: {req.handles}")
                raise HTTPException(
                    status_code=400,
                    detail="No valid platform handles provided. Please enter at least one username/handle."
                )

            logger.info(f"Valid handles to fetch: {valid_handles}")
            raw_lists = await fetch_all(valid_handles)
            # Extract activities and stats
            activities = []
            stats = {}
            if isinstance(raw_lists, dict) and "activities" in raw_lists:
                activities = raw_lists.get("activities", [])
                stats = raw_lists.get("stats", {})
            elif isinstance(raw_lists, list):
                activities = raw_lists

            logger.info(f"Fetched {len(activities)} total activities from {len(set(item.get('platform', 'unknown') for item in activities))} platforms")
            logger.info(f"Fetched stats from {len(stats)} platforms: {list(stats.keys())}")

            # Check if we got any data (activities OR stats)
            if not activities and not stats:
                logger.warning(f"No data fetched for user {req.user_id} from any platform")
                raise HTTPException(
                    status_code=404,
                    detail="Could not fetch data from any platform. Please verify your usernames are correct and publicly accessible."
                )

            # Log summary of fetched data
            platform_counts = {}
            for item in activities:
                p = item.get('platform', 'unknown')
                platform_counts[p] = platform_counts.get(p, 0) + 1
            logger.info(f"Fetched data summary for {req.user_id}: {platform_counts}")

            # Process and normalize
            logger.info(f"Processing {len(activities)} activities and stats from {len(stats)} platforms")
            processed = normalize_activities(raw_lists)

            # Validate processed data - we need either activities or stats
            if not processed or (not processed.get('activities') and not processed.get('platform_stats')):
                logger.warning(f"No valid data found after processing for user {req.user_id}")
                raise HTTPException(
                    status_code=404,
                    detail="No coding data found. Please ensure you have public submissions or profile data on the provided platforms."
                )

            # Run multi-agent AI analysis
            logger.info("Running multi-agent AI analysis")
            result = await orchestrator.run_parallel_analysis(req.user_id, processed)

            # Check if analysis failed
            if result.get("status") == "failed":
                error_msg = result.get("error", "Unknown error during analysis")
                logger.error(f"AI analysis failed for user {req.user_id}: {error_msg}")
                raise HTTPException(
                    status_code=500,
                    detail=f"AI analysis failed: {error_msg}"
                )

            # Update session context
            session_service.update_context(session["session_id"], {
                "timestamp": processed.get("growth_metrics", {}).get("days_active"),
                "platforms": processed.get("platforms", []),
                "total_activities": processed.get("total_count", 0)
            })

            # Add session ID and timestamp to response
            result["session_id"] = session["session_id"]
            import time
            result["fetched_at"] = time.time()

            logger.info(f"Analysis complete for user {req.user_id}")
            return result

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Analysis failed for user {req.user_id}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

