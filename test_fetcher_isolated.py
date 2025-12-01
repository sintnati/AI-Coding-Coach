"""
Test script to isolate fetcher issues.
"""
import asyncio
import sys
import os
import aiohttp

# Add current directory to path
sys.path.append(os.getcwd())

from services.fetcher.codeforces_fetcher import fetch_codeforces

async def test_fetcher():
    print("Testing Codeforces fetcher...")
    handle = "tourist" # Known valid handle
    try:
        print(f"Fetching data for {handle}...")
        data = await fetch_codeforces(handle)
        print(f"Success! Retrieved {len(data)} activities.")
        if data:
            print("Sample activity:", data[0])
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Windows specific event loop policy fix
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(test_fetcher())
