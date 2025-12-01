import aiohttp
import asyncio
import logging
import time
from urllib.parse import quote

logger = logging.getLogger(__name__)

# Timeout configuration
FETCH_TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)


async def fetch_hackerrank(username: str):
    """
    Fetch HackerRank user statistics.
    Note: HackerRank doesn't have a public API for submissions,
    so we'll fetch what we can from their public profile.

    Args:
        username: HackerRank username

    Returns:
        Dict with 'activities' (track summaries) and 'stats' (scores)
    """
    # URL encode the username to handle special characters
    encoded_username = quote(username)
    profile_url = f"https://www.hackerrank.com/rest/hackers/{encoded_username}/scores_elo"

    try:
        async with aiohttp.ClientSession(timeout=FETCH_TIMEOUT) as session:
            async with session.get(profile_url, headers={"Cache-Control": "no-cache"}) as response:
                if response.status != 200:
                    logger.warning(f"HackerRank API returned status {response.status} for username: {username}")
                    return {"activities": [], "stats": {}}

                data = await response.json()

                activities = []
                stats = {"tracks": {}}

                # HackerRank API is limited, we'll create summary entries
                # based on available data
                models = data.get("models", [])

                if not models:
                    logger.warning(f"No track data found for HackerRank username: {username}")
                    return {"activities": [], "stats": {}}

                for model in models:
                    track = model.get("track", "")
                    score = model.get("score", 0)

                    if score > 0:
                        activities.append({
                            "platform": "hackerrank",
                            "id": f"{track}-summary",
                            "title": f"{track} Track",
                            "tags": [track],
                            "verdict": "Completed",
                            "timestamp": int(time.time()),  # Use current time as approximation since API doesn't provide it
                            "score": score
                        })
                        stats["tracks"][track] = score

                logger.info(f"Successfully fetched {len(activities)} HackerRank tracks for {username}")
                return {
                    "activities": activities,
                    "stats": stats
                }

    except asyncio.TimeoutError:
        logger.error(f"Timeout fetching HackerRank data for username: {username}")
        return {"activities": [], "stats": {}}
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching HackerRank data for {username}: {e}")
        return {"activities": [], "stats": {}}
    except Exception as e:
        logger.error(f"Unexpected error fetching HackerRank data for {username}: {e}", exc_info=True)
        return {"activities": [], "stats": {}}
