"""
Comprehensive diagnostic tool to test data fetching from all platforms.
This will show you exactly what data is being fetched and where issues are.
"""
import asyncio
import sys
import os
import json
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.getcwd())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import fetchers
from services.fetcher.codeforces_fetcher import fetch_all

async def diagnose_fetching(handles):
    """
    Diagnose data fetching for given handles.

    Args:
        handles: Dict of platform handles
    """
    print("\n" + "="*80)
    print("DATA FETCHING DIAGNOSTIC TOOL")
    print("="*80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTesting with handles: {json.dumps(handles, indent=2)}")

    # Check environment
    print("\n" + "-"*80)
    print("ENVIRONMENT CHECK")
    print("-"*80)

    gemini_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

    if gemini_key:
        print(f"✅ GEMINI_API_KEY: Set ({gemini_key[:20]}...{gemini_key[-4:]})")
    else:
        print("❌ GEMINI_API_KEY: NOT SET")
        print("   → Gemini scraping will NOT work")
        print("   → Create .env file with your API key")

    print(f"   GEMINI_MODEL: {gemini_model}")

    # Fetch data
    print("\n" + "-"*80)
    print("FETCHING DATA")
    print("-"*80)

    try:
        result = await fetch_all(handles)

        print(f"\nResult type: {type(result)}")
        print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")

        # Analyze activities
        print("\n" + "-"*80)
        print("ACTIVITIES")
        print("-"*80)

        activities = result.get("activities", []) if isinstance(result, dict) else result
        print(f"Total activities fetched: {len(activities)}")

        if activities:
            # Group by platform
            by_platform = {}
            for activity in activities:
                platform = activity.get("platform", "unknown")
                by_platform.setdefault(platform, []).append(activity)

            for platform, acts in by_platform.items():
                print(f"\n{platform.upper()}:")
                print(f"  - Activities: {len(acts)}")
                if acts:
                    print(f"  - Sample: {acts[0]}")
        else:
            print("❌ No activities fetched")

        # Analyze stats
        print("\n" + "-"*80)
        print("STATISTICS")
        print("-"*80)

        stats = result.get("stats", {}) if isinstance(result, dict) else {}

        if stats:
            print(f"Platforms with stats: {list(stats.keys())}")
            for platform, platform_stats in stats.items():
                print(f"\n{platform.upper()}:")
                print(json.dumps(platform_stats, indent=2))
        else:
            print("❌ No stats fetched")
            print("\nPossible reasons:")
            print("  1. APIs failed and Gemini scraping is not set up")
            print("  2. Usernames are incorrect")
            print("  3. Profiles are not public")

        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)

        platforms_tested = len(handles)
        platforms_with_data = len(stats)

        print(f"\nPlatforms tested: {platforms_tested}")
        print(f"Platforms with stats: {platforms_with_data}")
        print(f"Success rate: {platforms_with_data}/{platforms_tested} ({100*platforms_with_data/platforms_tested if platforms_tested > 0 else 0:.0f}%)")

        if platforms_with_data == 0:
            print("\n❌ NO DATA FETCHED FROM ANY PLATFORM")
            print("\nNext steps:")
            print("  1. Set up .env file with GEMINI_API_KEY")
            print("  2. Run: python setup_gemini.py")
            print("  3. Verify usernames are correct and profiles are public")
            print("  4. Run this diagnostic again")
        elif platforms_with_data < platforms_tested:
            print(f"\n⚠️  PARTIAL SUCCESS ({platforms_with_data}/{platforms_tested} platforms)")
            failed = set(handles.keys()) - set(stats.keys())
            print(f"\nFailed platforms: {failed}")
            print("\nCheck:")
            print("  - Are these usernames correct?")
            print("  - Are these profiles public?")
        else:
            print("\n✅ SUCCESS! All platforms fetched correctly")

        return result

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Main diagnostic function."""
    print("\nThis tool will test data fetching from coding platforms.")
    print("It will show you exactly what data is being fetched and where issues are.\n")

    # Get handles from user
    print("Enter your usernames for each platform (press Enter to skip):\n")

    handles = {}

    platforms = ["leetcode", "codeforces", "codechef", "atcoder", "hackerrank"]

    for platform in platforms:
        username = input(f"{platform.capitalize()}: ").strip()
        if username:
            handles[platform] = username

    if not handles:
        print("\n❌ No handles provided. Using example handles for testing...\n")
        handles = {
            "leetcode": "leetcode",
            "codeforces": "tourist"
        }

    # Run diagnostic
    await diagnose_fetching(handles)

    print("\n" + "="*80)
    print("Diagnostic complete!")
    print("="*80)
    print()


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
