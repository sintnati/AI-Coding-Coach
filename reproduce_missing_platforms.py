import asyncio
import logging
from services.fetcher.codeforces_fetcher import fetch_all

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_fetch_all():
    handles = {
        "codeforces": "tourist",
        "leetcode": "tourist", # Just using a dummy name, might not exist but should trigger the fetch attempt
        "codechef": "tourist",
        "hackerrank": "tourist",
        "atcoder": "tourist"
    }

    logger.info("Testing fetch_all with handles: %s", handles)
    results = await fetch_all(handles)

    # Check what platforms were actually attempted/fetched
    # Since fetch_all returns a list of activities and a dict of stats, we can check the stats keys
    # However, fetch_all returns a dict with 'activities' and 'stats'

    stats = results.get("stats", {})
    activities = results.get("activities", [])

    logger.info("Fetched stats keys: %s", list(stats.keys()))

    # We expect codechef, hackerrank, etc. to be present if the logic was there
    # Even if they fail, the current implementation of fetch_all logs "Starting data fetch for platforms: ..."
    # We can inspect the logs to see what was attempted.

    missing_platforms = []
    for platform in ["codechef", "hackerrank", "atcoder"]:
        if platform not in stats and not any(a.get('platform') == platform for a in activities):
             # This is a weak check because fetch might fail, but if the code doesn't even try, it won't be there.
             # A better check is to see if the code even *tries* to fetch them.
             # But based on code reading, we know it won't.
             pass

    print("\n--- Analysis ---")
    if "codechef" not in stats and not any(a.get('platform') == "codechef" for a in activities):
        print("CodeChef data missing (Expected if logic is missing)")

    if "hackerrank" not in stats and not any(a.get('platform') == "hackerrank" for a in activities):
        print("HackerRank data missing (Expected if logic is missing)")

if __name__ == "__main__":
    asyncio.run(test_fetch_all())
