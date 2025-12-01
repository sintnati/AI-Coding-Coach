import asyncio
import logging
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from services.fetcher.codeforces_fetcher import fetch_codeforces, fetch_all
from services.fetcher.leetcode_fetcher import fetch_leetcode
from services.fetcher.codechef_fetcher import fetch_codechef
from services.fetcher.atcoder_fetcher import fetch_atcoder
from services.fetcher.hackerrank_fetcher import fetch_hackerrank

async def test_fetcher(fetcher_func, username, platform_name):
    """Test a single fetcher function."""
    print(f"\n{'='*60}")
    print(f"Testing {platform_name} fetcher with username: {username}")
    print(f"{'='*60}")

    try:
        result = await fetcher_func(username)

        # Validate structure
        if isinstance(result, dict):
            if "activities" in result and "stats" in result:
                print(f"✓ Correct structure returned")
                print(f"  - Activities count: {len(result['activities'])}")
                print(f"  - Stats keys: {list(result['stats'].keys())}")
                if result['stats']:
                    print(f"  - Stats values: {result['stats']}")
                else:
                    print(f"  - Warning: Stats is empty")

                # Show sample activity if available
                if result['activities']:
                    print(f"  - Sample activity: {result['activities'][0]}")
                else:
                    print(f"  - Warning: No activities found")

                return True
            else:
                print(f"✗ Incorrect structure - missing 'activities' or 'stats'")
                print(f"  - Keys found: {list(result.keys())}")
                return False
        else:
            print(f"✗ Wrong return type: {type(result)}")
            print(f"  - Expected: dict with 'activities' and 'stats'")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error(f"Error testing {platform_name}", exc_info=True)
        return False

async def test_fetch_all():
    """Test the fetch_all function with multiple platforms."""
    print(f"\n{'='*60}")
    print(f"Testing fetch_all with multiple platforms")
    print(f"{'='*60}")

    # Use test handles - these may or may not be valid
    handles = {
        "codeforces": "tourist",
        "leetcode": "leetcode",
    }

    try:
        result = await fetch_all(handles)

        if isinstance(result, dict):
            if "activities" in result and "stats" in result:
                print(f"✓ Correct structure returned from fetch_all")
                print(f"  - Total activities: {len(result['activities'])}")
                print(f"  - Platforms with stats: {list(result['stats'].keys())}")

                for platform, stats in result['stats'].items():
                    print(f"  - {platform} stats: {stats}")

                return True
            else:
                print(f"✗ Incorrect structure from fetch_all")
                return False
        else:
            print(f"✗ Wrong return type from fetch_all: {type(result)}")
            return False

    except Exception as e:
        print(f"✗ Error in fetch_all: {e}")
        logger.error("Error testing fetch_all", exc_info=True)
        return False

async def main():
    print("Starting fetcher verification tests...")
    print("Note: Some tests may fail if usernames don't exist or APIs are down")

    results = {}

    # Test individual fetchers with known usernames
    # Note: These are example usernames, they may or may not exist
    results['codeforces'] = await test_fetcher(fetch_codeforces, "tourist", "CodeForces")
    results['leetcode'] = await test_fetcher(fetch_leetcode, "leetcode", "LeetCode")
    results['codechef'] = await test_fetcher(fetch_codechef, "gennady.korotkevich", "CodeChef")
    results['atcoder'] = await test_fetcher(fetch_atcoder, "tourist", "AtCoder")
    results['hackerrank'] = await test_fetcher(fetch_hackerrank, "shashank21j", "HackerRank")

    # Test fetch_all
    results['fetch_all'] = await test_fetch_all()

    # Summary
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*60}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
