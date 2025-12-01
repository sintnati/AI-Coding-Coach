"""
Quick diagnostic test for the AI agent platform
"""
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("=" * 60)
print("AI AGENT PLATFORM DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Basic imports
print("\n[TEST 1] Testing basic imports...")
try:
    from services.fetcher.codeforces_fetcher import fetch_all
    print("✓ Fetcher module imported successfully")
except Exception as e:
    print(f"✗ Fetcher import failed: {e}")

try:
    from services.preprocessor.preprocess import normalize_activities
    print("✓ Preprocessor module imported successfully")
except Exception as e:
    print(f"✗ Preprocessor import failed: {e}")

try:
    from libs.memory.faiss_store import FaissStore
    print("✓ FaissStore imported successfully")
except Exception as e:
    print(f"✗ FaissStore import failed: {e}")

# Test 2: Agent imports
print("\n[TEST 2] Testing agent imports...")
try:
    from services.agents.analyzer_agent import AnalyzerAgent
    print("✓ AnalyzerAgent imported successfully")
except Exception as e:
    print(f"✗ AnalyzerAgent import failed: {e}")

try:
    from services.agents.weakness_detector_agent import WeaknessDetectorAgent
    print("✓ WeaknessDetectorAgent imported successfully")
except Exception as e:
    print(f"✗ WeaknessDetectorAgent import failed: {e}")

try:
    from services.agents.task_generator_agent import TaskGeneratorAgent
    print("✓ TaskGeneratorAgent imported successfully")
except Exception as e:
    print(f"✗ TaskGeneratorAgent import failed: {e}")

try:
    from services.agents.orchestrator_agent import OrchestratorAgent
    print("✓ OrchestratorAgent imported successfully")
except Exception as e:
    print(f"✗ OrchestratorAgent import failed: {e}")

# Test 3: LLM Client
print("\n[TEST 3] Testing LLM client...")
try:
    from services.analyser.llm_client import generate_text
    print("✓ LLM client imported successfully")
except Exception as e:
    print(f"✗ LLM client import failed: {e}")

# Test 4: Sessions and Observability
print("\n[TEST 4] Testing libs modules...")
try:
    from libs.sessions import PersistentSessionService
    print("✓ PersistentSessionService imported successfully")
except Exception as e:
    print(f"✗ PersistentSessionService import failed: {e}")

try:
    from libs.observability import get_health_status, RequestTimer
    print("✓ Observability modules imported successfully")
except Exception as e:
    print(f"✗ Observability import failed: {e}")

# Test 5: Gateway app
print("\n[TEST 5] Testing gateway app...")
try:
    from services.gateway.app import app
    print("✓ Gateway app imported successfully")
except Exception as e:
    print(f"✗ Gateway app import failed: {e}")

# Test 6: Environment variables
print("\n[TEST 6] Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    print(f"✓ GEMINI_API_KEY is set (length: {len(gemini_api_key)})")
else:
    print("✗ GEMINI_API_KEY is not set!")

print("\n" + "=" * 60)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 60)
