import asyncio
import sys
import os
import time
from services.fetcher.hackerrank_fetcher import fetch_hackerrank

# Add current directory to path
sys.path.append(os.getcwd())

async def test_freshness():
    print("=" * 60)
    print("TESTING DATA FRESHNESS")
    print("=" * 60)
    print()

    # Test HackerRank freshness
    print("[TEST 1] Testing HackerRank timestamp...")
    try:
        # Using a known user or a dummy one if we can mock it, but for now let's try a real one if possible
        # or just check the logic if we can't hit the API reliably without a valid user.
        # Let's try a common username, if it fails we'll see.
        username = "tourist"
        result = await fetch_hackerrank(username)

        if result:
            print(f"✓ Successfully fetched {len(result)} items")
            item = result[0]
            timestamp = item.get('timestamp')
            current_time = int(time.time())

            print(f"  Item timestamp: {timestamp}")
            print(f"  Current time:   {current_time}")

            if abs(current_time - timestamp) < 60: # Should be very close as we just set it
                print("✓ Timestamp is fresh (within 60s)")
            else:
                print("✗ Timestamp is NOT fresh")
        else:
            print("⚠ No data returned (might be API issue or invalid user)")

    except Exception as e:
        print(f"✗ Error: {e}")
    print()

if __name__ == "__main__":
    asyncio.run(test_freshness())
