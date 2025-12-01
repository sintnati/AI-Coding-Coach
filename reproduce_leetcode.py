import asyncio
import logging
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from services.fetcher.leetcode_fetcher import fetch_leetcode

async def main():
    # Test with a known valid handle (e.g., 'tourist' or a generic one if known,
    # but 'tourist' is mainly Codeforces. Let's use a common one or just 'test')
    # Better to use a real one if possible, or just a placeholder that might exist.
    # 'leetcode' is a user.
    username = "leetcode"
    print(f"Fetching data for user: {username}")

    try:
        result = await fetch_leetcode(username)
        print(f"Result type: {type(result)}")
        if isinstance(result, dict):
            print(f"Keys: {result.keys()}")
            if "stats" in result:
                print(f"Stats: {result['stats']}")
            if "activities" in result:
                print(f"Activities count: {len(result['activities'])}")
                if result['activities']:
                    print(f"First activity: {result['activities'][0]}")
        else:
            print(f"Result: {result}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
