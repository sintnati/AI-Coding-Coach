"""
Quick diagnostic - non-interactive version.
Just run this to see what's happening with your data fetching.
"""
import asyncio
import sys
import os
import json

sys.path.append(os.getcwd())

from services.fetcher.codeforces_fetcher import fetch_all

async def quick_test():
    print("\n" + "="*60)
    print("QUICK DATA FETCHING TEST")
    print("="*60)

    # Check .env
    print("\n1. Checking environment...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print(f"   ✅ GEMINI_API_KEY is set")
    else:
        print(f"   ❌ GEMINI_API_KEY is NOT set")
        print(f"   → Create .env file with your API key")

    # Test with example handles
    print("\n2. Testing with example handles...")
    test_handles = {
        "leetcode": "leetcode",
        "codeforces": "tourist"
    }

    print(f"   Testing: {test_handles}")

    try:
        result = await fetch_all(test_handles)

        print("\n3. Results:")
        print(f"   Type: {type(result)}")

        if isinstance(result, dict):
            activities = result.get("activities", [])
            stats = result.get("stats", {})

            print(f"   Activities: {len(activities)}")
            print(f"   Stats: {list(stats.keys())}")

            if stats:
                print("\n4. Fetched Statistics:")
                for platform, data in stats.items():
                    print(f"\n   {platform.upper()}:")
                    print(f"   {json.dumps(data, indent=6)}")
            else:
                print("\n   ❌ NO STATS FETCHED")
                print("\n   This means:")
                print("   - APIs failed")
                print("   - Gemini scraping didn't work (no .env file)")
                print("\n   Solution:")
                print("   1. Create .env file")
                print("   2. Add: GEMINI_API_KEY=your_key_here")
                print("   3. Run this test again")

    except Exception as e:
        print(f"\n   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*60)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(quick_test())
