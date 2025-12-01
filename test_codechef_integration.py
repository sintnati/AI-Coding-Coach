"""
Simple integration test for CodeChef with the full application flow.
Tests both the fetcher and the app validation logic.
"""
import asyncio
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add to path
sys.path.insert(0, os.getcwd())

# Load env
from dotenv import load_dotenv
load_dotenv()

async def test_full_flow():
    """Test the complete flow from fetch to validation."""
    from services.fetcher.codeforces_fetcher import fetch_all

    handles = {
        "codechef": "kashyap1311"  # Replace with your username
    }

    print("\n" + "="*60)
    print("Testing Full CodeChef Integration")
    print("="*60)

    # Step 1: Fetch data
    print("\n[1] Fetching data...")
    result = await fetch_all(handles)

    print(f"   Type: {type(result)}")
    print(f"   Keys: {result.keys() if isinstance(result, dict) else 'N/A'}")

    if isinstance(result, dict):
        activities = result.get("activities", [])
        stats = result.get("stats", {})

        print(f"   Activities: {len(activities)}")
        print(f"   Stats platforms: {list(stats.keys())}")
        print(f"   Stats data: {stats}")

        # Step 2: Validate (mimic app.py logic)
        print("\n[2] Validating data (app.py logic)...")
        if not activities and not stats:
            print("   ✗ FAIL: No data")
            return False
        else:
            print("   ✓ PASS: Data present")

        # Step 3: Process
        print("\n[3] Processing data...")
        from services.preprocessor.preprocess import normalize_activities
        processed = normalize_activities(result)

        print(f"   Processed keys: {processed.keys()}")
        print(f"   Total count: {processed.get('total_count', 0)}")
        print(f"   Platforms: {processed.get('platforms', [])}")
        print(f"   Growth metrics: {list(processed.get('growth_metrics', {}).keys())}")

        # Check platform_stats for CodeChef
        platform_stats = processed.get('growth_metrics', {}).get('platform_stats', {})
        if 'codechef' in platform_stats:
            print(f"\n   ✓ CodeChef stats in processed data:")
            print(f"      {platform_stats['codechef']}")
        else:
            print(f"\n   ⚠ CodeChef not in platform_stats")

        # Step 4: Final validation (mimic app.py)
        print("\n[4] Final validation...")
        if not processed or (not processed.get('activities') and not processed.get('platform_stats')):
            print("   ✗ FAIL: No valid processed data")
            return False
        else:
            print("   ✓ PASS: Valid processed data")

        print("\n" + "="*60)
        print("✓✓ SUCCESS: CodeChef integration working!")
        print("="*60)
        return True
    else:
        print("   ✗ FAIL: Unexpected result type")
        return False

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        success = asyncio.run(test_full_flow())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.exception("Test failed")
        sys.exit(1)
