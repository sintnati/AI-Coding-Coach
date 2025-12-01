"""
Test all platform fetchers to identify which ones work.
"""
import asyncio
import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv
load_dotenv()

async def test_platform(name, fetcher_func, username):
    """Test a single platform fetcher."""
    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print(f"{'='*60}")
    print(f"Username: {username}")

    try:
        result = await fetcher_func(username)

        if isinstance(result, dict):
            activities = result.get("activities", [])
            stats = result.get("stats", {})

            if activities or stats:
                print(f"✓ {name} WORKS")
                print(f"  - Activities: {len(activities)}")
                print(f"  - Stats: {list(stats.keys()) if stats else 'None'}")
                return True
            else:
                print(f"✗ {name} FAILED - No data returned")
                return False
        else:
            print(f"✗ {name} FAILED - Wrong format")
            return False

    except Exception as e:
        print(f"✗ {name} FAILED - Exception: {str(e)[:100]}")
        return False

async def main():
    print("="*60)
    print("PLATFORM COMPATIBILITY TEST")
    print("="*60)

    results = {}

    # Test LeetCode
    from services.fetcher.leetcode_fetcher import fetch_leetcode
    results['LeetCode'] = await test_platform(
        "LeetCode",
        fetch_leetcode,
        "leetcode"  # Known user
    )

    # Test Codeforces
    from services.fetcher.codeforces_fetcher import fetch_codeforces
    results['Codeforces'] = await test_platform(
        "Codeforces",
        fetch_codeforces,
        "tourist"  # Famous user
    )

    # Test AtCoder
    from services.fetcher.atcoder_fetcher import fetch_atcoder
    results['AtCoder'] = await test_platform(
        "AtCoder",
        fetch_atcoder,
        "tourist"  # Famous user
    )

    # Test HackerRank
    from services.fetcher.hackerrank_fetcher import fetch_hackerrank
    results['HackerRank'] = await test_platform(
        "HackerRank",
        fetch_hackerrank,
        "shashank21j"  # Example user
    )

    # Test CodeChef
    from services.fetcher.codechef_fetcher import fetch_codechef
    results['CodeChef'] = await test_platform(
        "CodeChef",
        fetch_codechef,
        "tourist"  # Famous user
    )

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    working = [name for name, works in results.items() if works]
    failing = [name for name, works in results.items() if not works]

    print(f"\n✓ WORKING PLATFORMS ({len(working)}):")
    for name in working:
        print(f"  - {name}")

    print(f"\n✗ FAILING PLATFORMS ({len(failing)}):")
    for name in failing:
        print(f"  - {name}")

    print(f"\n{'='*60}")
    print("RECOMMENDATION")
    print(f"{'='*60}")
    print(f"Keep: {', '.join(working)}")
    print(f"Remove: {', '.join(failing)}")

    return working, failing

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        working, failing = asyncio.run(main())

        # Save results
        with open("platform_test_results.txt", "w") as f:
            f.write("WORKING PLATFORMS:\n")
            for p in working:
                f.write(f"  - {p}\n")
            f.write("\nFAILING PLATFORMS:\n")
            for p in failing:
                f.write(f"  - {p}\n")

        print("\nResults saved to: platform_test_results.txt")

    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
