"""
Test script to verify imports work without hanging.
"""
import sys
import os
import time

# Add current directory to path
sys.path.append(os.getcwd())

print("Starting import test...")
start_time = time.time()

try:
    print("Importing app...", end=" ", flush=True)
    from services.gateway.app import app
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

try:
    print("Importing orchestrator...", end=" ", flush=True)
    from services.agents.orchestrator_agent import OrchestratorAgent
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

try:
    print("Importing analyzer...", end=" ", flush=True)
    from services.agents.analyzer_agent import AnalyzerAgent
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

end_time = time.time()
print(f"Import test completed in {end_time - start_time:.2f} seconds")
