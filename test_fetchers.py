"""
Test script to verify fetcher improvements
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

async def test_fetchers():
    print("=" * 60)
    print("TESTING IMPROVED FETCHERS")
    print("=" * 60)
    print()

    from services.fetcher.codeforces_fetcher import fetch_codeforces, fetch_all

    # Test 1: Test with a known valid Codeforces handle
    print("[TEST 1] Testing Codeforces fetcher with valid handle...")
    try:
        result = await fetch_codeforces("tourist")
        if result:
            print(f"✓ Successfully fetched {len(result)} submissions")
            print(f"  Sample: {result[0]['title'] if result else 'N/A'}")
        else:
            print("⚠ No data returned (might be API issue)")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()

    # Test 2: Test with invalid handle
    print("[TEST 2] Testing Codeforces fetcher with invalid handle...")
    try:
        result = await fetch_codeforces("this_user_definitely_does_not_exist_12345")
        if not result:
            print("✓ Correctly returned empty list for invalid user")
        else:
            print(f"⚠ Unexpected: Got {len(result)} results")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()

    # Test 3: Test fetch_all with multiple platforms
    print("[TEST 3] Testing fetch_all with multiple platforms...")
    try:
        handles = {
            "codeforces": "tourist",
            # Add more if you want to test
        }
        result = await fetch_all(handles)
        if result:
            print(f"✓ Successfully fetched {len(result)} total activities")
            platforms = set(item['platform'] for item in result)
            print(f"  Platforms: {', '.join(platforms)}")
        else:
            print("⚠ No data returned")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()

    # Test 4: Test timeout handling
    print("[TEST 4] Testing timeout handling...")
    print("  (This should complete within 30 seconds)")
    import time
    start = time.time()
    try:
        # Test with potentially slow endpoint
        result = await fetch_all({"codeforces": "tourist"})
        elapsed = time.time() - start
        print(f"✓ Completed in {elapsed:.2f} seconds")
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Error after {elapsed:.2f} seconds: {e}")
    print()

    print("=" * 60)
    print("FETCHER TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_fetchers())
