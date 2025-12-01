"""
Debug script to test fetching data from platforms
"""
import asyncio
import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

async def test_fetch():
    from services.fetcher.codeforces_fetcher import fetch_all

    print("=" * 60)
    print("TESTING DATA FETCHING")
    print("=" * 60)
    print()

    # Test with a known valid handle
    print("[TEST] Testing with Codeforces handle 'tourist'...")
    handles = {
        "codeforces": "tourist"
    }

    print(f"Input handles: {handles}")
    result = await fetch_all(handles)

    print(f"\nResult: {len(result)} items fetched")
    if result:
        print(f"Sample item: {json.dumps(result[0], indent=2)}")
        print(f"\nPlatforms found: {set(item.get('platform') for item in result)}")
    else:
        print("ERROR: No data fetched!")

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_fetch())

