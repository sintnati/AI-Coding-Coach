import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("Importing fetcher...", flush=True)
try:
    from services.fetcher.codeforces_fetcher import fetch_all
    print("Fetcher imported.", flush=True)
except Exception as e:
    print(f"Fetcher failed: {e}", flush=True)

print("Importing preprocessor...", flush=True)
try:
    from services.preprocessor.preprocess import normalize_activities
    print("Preprocessor imported.", flush=True)
except Exception as e:
    print(f"Preprocessor failed: {e}", flush=True)

print("Importing coach...", flush=True)
try:
    from services.coach.coach import CoachAgent
    print("Coach imported.", flush=True)
except Exception as e:
    print(f"Coach failed: {e}", flush=True)

print("Importing faiss_store...", flush=True)
try:
    from libs.memory.faiss_store import FaissStore
    print("FaissStore imported.", flush=True)
except Exception as e:
    print(f"FaissStore failed: {e}", flush=True)

print("Imports done.", flush=True)
