import aiohttp
import asyncio
import logging
import json

logger = logging.getLogger(__name__)

# Timeout configuration
FETCH_TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)

async def fetch_leetcode(username: str):
    """
    Fetch LeetCode user statistics and recent submissions.
    Uses LeetCode's GraphQL API.

    Args:
        username: LeetCode username

    Returns:
        Dict with 'activities' (list of submissions) and 'stats' (user statistics)
    """
    url = "https://leetcode.com/graphql"

    # Query for user profile and submission stats
    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
            userCalendar {
                streak
                totalActiveDays
            }
            profile {
                ranking
                reputation
                starRating
            }
        }
        recentSubmissionList(username: $username, limit: 50) {
            title
            titleSlug
            timestamp
            statusDisplay
            lang
        }
    }
    """

    try:
        async with aiohttp.ClientSession(timeout=FETCH_TIMEOUT) as session:
            logger.info(f"Fetching LeetCode data for username: {username}")

            async with session.post(
                url,
                json={
                    "query": query,
                    "variables": {"username": username}
                },
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://leetcode.com/"
                }
            ) as response:
                logger.info(f"LeetCode API response status: {response.status}")

                if response.status != 200:
                    logger.warning(f"LeetCode API returned status {response.status} for username: {username}")
                    # Log response body for debugging
                    try:
                        error_body = await response.text()
                        logger.error(f"LeetCode API error body: {error_body[:500]}")
                    except:
                        pass
                    return {"activities": [], "stats": {}}

                data = await response.json()

                # Log the full response for debugging
                logger.debug(f"LeetCode API full response: {json.dumps(data, indent=2)[:1000]}")

                # Enhanced error logging
                if "errors" in data:
                    logger.error(f"LeetCode GraphQL API errors for username '{username}': {json.dumps(data.get('errors'), indent=2)}")
                    return {"activities": [], "stats": {}}

                # Validate data structure
                if "data" not in data:
                    logger.error(f"LeetCode API response missing 'data' field for username '{username}'")
                    return {"activities": [], "stats": {}}

                result = []
                user_data = data.get("data", {}).get("matchedUser")

                # Check if user exists
                if user_data is None:
                    logger.error(f"LeetCode user '{username}' not found. The username may be incorrect or the account may not exist.")
                    return {"activities": [], "stats": {}}

                if not user_data:
                    logger.warning(f"Empty user data for LeetCode username: {username}")
                    return {"activities": [], "stats": {}}

                logger.info(f"LeetCode user data keys: {list(user_data.keys())}")

                submissions = data.get("data", {}).get("recentSubmissionList", [])
                logger.info(f"Found {len(submissions)} recent submissions for {username}")

                for submission in submissions:
                    result.append({
                        "platform": "leetcode",
                        "id": submission.get("titleSlug", ""),
                        "title": submission.get("title", "Unknown"),
                        "tags": [],  # LeetCode doesn't provide tags in this API
                        "verdict": submission.get("statusDisplay", "UNKNOWN"),
                        "timestamp": int(submission.get("timestamp", 0)),
                        "language": submission.get("lang", "")
                    })

                logger.info(f"Successfully fetched {len(result)} LeetCode submissions for {username}")

                # Extract stats with validation
                stats = {
                    "total_solved": 0,
                    "easy_solved": 0,
                    "medium_solved": 0,
                    "hard_solved": 0,
                    "streak": 0,
                    "ranking": 0,
                    "reputation": 0
                }

                # Safely extract profile data
                profile = user_data.get("profile")
                if profile:
                    stats["ranking"] = profile.get("ranking", 0) or 0
                    stats["reputation"] = profile.get("reputation", 0) or 0
                    logger.info(f"LeetCode profile for {username}: ranking={stats['ranking']}, reputation={stats['reputation']}")
                else:
                    logger.warning(f"No profile data found for LeetCode user {username}")

                # Safely extract submission stats
                submit_stats_data = user_data.get("submitStatsGlobal")

                if submit_stats_data:
                    logger.info(f"submitStatsGlobal keys: {list(submit_stats_data.keys())}")

                    # AC Submissions (Solved)
                    ac_submissions = submit_stats_data.get("acSubmissionNum", [])
                    if ac_submissions:
                        logger.info(f"Found {len(ac_submissions)} AC submission categories")
                        for stat in ac_submissions:
                            count = stat.get("count", 0)
                            difficulty = stat.get("difficulty", "").strip()

                            logger.debug(f"Processing difficulty '{difficulty}' with count {count}")

                            if difficulty == "All":
                                stats["total_solved"] = count
                            elif difficulty == "Easy":
                                stats["easy_solved"] = count
                            elif difficulty == "Medium":
                                stats["medium_solved"] = count
                            elif difficulty == "Hard":
                                stats["hard_solved"] = count
                    else:
                        logger.warning(f"No acSubmissionNum array found for LeetCode user {username}")
                else:
                    logger.warning(f"No submitStatsGlobal data found for LeetCode user {username}")
                    logger.info(f"Available user_data keys: {list(user_data.keys())}")

                # Extract Calendar/Streak data
                user_calendar = user_data.get("userCalendar")
                if user_calendar:
                    current_streak = user_calendar.get("streak", 0)
                    stats["streak"] = current_streak if current_streak else 0
                    total_active = user_calendar.get("totalActiveDays", 0)
                    logger.info(f"LeetCode calendar for {username}: streak={stats['streak']}, totalActiveDays={total_active}")
                else:
                    logger.warning(f"No userCalendar data found for LeetCode user {username}")

                logger.info(f"LeetCode stats for {username}: {stats}")

                # Warn if total_solved is 0
                if stats["total_solved"] == 0:
                    logger.warning(f"LeetCode user {username} has 0 total solved problems. This may indicate an issue with the API response or the user has no accepted submissions.")

                return {
                    "activities": result,
                    "stats": stats
                }

    except asyncio.TimeoutError:
        logger.error(f"Timeout fetching LeetCode data for username: {username}")
        return {"activities": [], "stats": {}}
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching LeetCode data for {username}: {e}")
        return {"activities": [], "stats": {}}
    except Exception as e:
        logger.error(f"Unexpected error fetching LeetCode data for {username}: {e}", exc_info=True)
        return {"activities": [], "stats": {}}
