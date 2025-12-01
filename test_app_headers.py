import asyncio
import sys
import os
from fastapi.testclient import TestClient
from services.gateway.app import app

# Add current directory to path
sys.path.append(os.getcwd())

def test_headers():
    print("=" * 60)
    print("TESTING APP HEADERS")
    print("=" * 60)
    print()

    client = TestClient(app)

    # We need to mock the fetch_all and orchestrator to avoid real calls
    # But for now, let's just see if we can hit the endpoint and get headers
    # even if it fails later, or we can hit a lighter endpoint if we added headers globally?
    # We added headers only to /analyze.

    # Let's try to mock the internal calls or just expect a 400/404 but check headers
    # If we send invalid data, we might get 400, but headers might not be set if exception is raised before
    # checking the code, the header is set at the beginning of the function.
    # But if exception is raised, FastAPI might override response?
    # Let's try with a valid-ish request that fails fast.

    try:
        response = client.post("/analyze", json={"user_id": "test", "handles": {}})
        # This will raise 400 because handles are empty

        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")

        # Note: If exception is raised, the response object passed to function might not be used
        # unless we handle exception and return response.
        # In FastAPI, if we raise HTTPException, the dependency response might not be sent.
        # Let's see.

        if "cache-control" in response.headers:
             print(f"✓ Cache-Control: {response.headers['cache-control']}")
        else:
             print("✗ Cache-Control header missing (might be due to exception)")

    except Exception as e:
        print(f"✗ Error: {e}")
    print()

if __name__ == "__main__":
    test_headers()
