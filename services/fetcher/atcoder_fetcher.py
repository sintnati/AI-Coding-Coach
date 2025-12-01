import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)

# Timeout configuration
FETCH_TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)


async def fetch_atcoder(username: str):
    """
    Fetch AtCoder user statistics and recent submissions.
    Uses AtCoder's public API (unofficial - Kenkoooo).

    Args:
        username: AtCoder username

    Returns:
        Dict with 'activities' (list of submissions) and 'stats' (user info)
    """
    submissions_url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions"
    user_info_url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/info"
    logger.info(f"Fetching AtCoder data for {username} via Kenkoooo API (note: may have 15-30min delay)")

    try:
        async with aiohttp.ClientSession(timeout=FETCH_TIMEOUT) as session:
            # Fetch both submissions and user info in parallel
            submissions_task = session.get(
                submissions_url,
                params={"user": username, "from_second": 0},
                headers={"Cache-Control": "no-cache"}
            )
            user_info_task = session.get(
                user_info_url,
                params={"user": username},
                headers={"Cache-Control": "no-cache"}
            )

            submissions_response, user_info_response = await asyncio.gather(submissions_task, user_info_task, return_exceptions=True)

            # Process submissions
            activities = []
            if not isinstance(submissions_response, Exception):
                if submissions_response.status == 200:
                    submissions = await submissions_response.json()
                    if submissions:
                        # Get last 100 submissions
                        for submission in submissions[:100]:
                            activities.append({
                                "platform": "atcoder",
                                "id": f"{submission.get('contest_id', '')}-{submission.get('problem_id', '')}",
                                "title": submission.get("problem_id", "Unknown"),
                                "tags": [],  # AtCoder API doesn't provide tags easily
                                "verdict": submission.get("result", "UNKNOWN"),
                                "timestamp": submission.get("epoch_second", 0),
                                "contest": submission.get("contest_id", ""),
                                "language": submission.get("language", "")
                            })
                        logger.info(f"Successfully fetched {len(activities)} AtCoder submissions for {username}")
                    else:
                        logger.warning(f"No submissions found for AtCoder username: {username}")
                else:
                    logger.warning(f"AtCoder submissions API returned status {submissions_response.status} for username: {username}")
            else:
                logger.error(f"Error fetching AtCoder submissions: {submissions_response}")

            # Process user info
            stats = {}
            if not isinstance(user_info_response, Exception):
                if user_info_response.status == 200:
                    user_info = await user_info_response.json()
                    if user_info:
                        stats = {
                            "rating": user_info.get("rating", 0),
                            "highest_rating": user_info.get("highest_rating", 0),
                            "rank": user_info.get("rank", 0),
                            "accepted_count": user_info.get("accepted_count", 0)
                        }
                        logger.info(f"AtCoder stats for {username}: rating={stats['rating']}, highest_rating={stats['highest_rating']}, accepted_count={stats['accepted_count']}")
                    else:
                        logger.warning(f"No user info found for AtCoder username: {username}")
                else:
                    logger.warning(f"AtCoder user info API returned status {user_info_response.status} for username: {username}")
            else:
                logger.error(f"Error fetching AtCoder user info: {user_info_response}")

            return {
                "activities": activities,
                "stats": stats
            }

    except asyncio.TimeoutError:
        logger.error(f"Timeout fetching AtCoder data for username: {username}")
        return {"activities": [], "stats": {}}
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching AtCoder data for {username}: {e}")
        return {"activities": [], "stats": {}}
    except Exception as e:
        logger.error(f"Unexpected error fetching AtCoder data for {username}: {e}", exc_info=True)
        return {"activities": [], "stats": {}}
