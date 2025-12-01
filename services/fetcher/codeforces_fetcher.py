import aiohttp
import asyncio
import logging
from urllib.parse import quote
from .leetcode_fetcher import fetch_leetcode
from .hackerrank_fetcher import fetch_hackerrank
from .codechef_fetcher import fetch_codechef
from .atcoder_fetcher import fetch_atcoder

from .gemini_scraper import scrape_profile

logger = logging.getLogger(__name__)

# Timeout configuration
FETCH_TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)


async def fetch_codeforces(handle: str):
    """
    Fetch Codeforces user submissions and user info.

    Args:
        handle: Codeforces username

    Returns:
        Dict with 'activities' (list of submissions) and 'stats' (user info)
    """
    # URL encode the handle to handle special characters
    encoded_handle = quote(handle)
    submissions_url = f"https://codeforces.com/api/user.status?handle={encoded_handle}"
    user_info_url = f"https://codeforces.com/api/user.info?handles={encoded_handle}"

    try:
        async with aiohttp.ClientSession(timeout=FETCH_TIMEOUT) as session:
            # Fetch both submissions and user info in parallel
            submissions_task = session.get(submissions_url, headers={"Cache-Control": "no-cache"})
            user_info_task = session.get(user_info_url, headers={"Cache-Control": "no-cache"})

            submissions_response, user_info_response = await asyncio.gather(submissions_task, user_info_task)

            # Process submissions
            activities = []
            if submissions_response.status == 200:
                submissions_data = await submissions_response.json()
                if submissions_data.get("status") == "OK":
                    for item in submissions_data.get("result", [])[:100]:  # Limit to 100 most recent
                        prob = item.get("problem", {})
                        activities.append({
                            "platform": "codeforces",
                            "id": f"{prob.get('contestId','')}-{prob.get('index','')}",
                            "title": prob.get("name", "Unknown"),
                            "tags": prob.get("tags", []),
                            "verdict": item.get("verdict", "UNKNOWN"),
                            "timestamp": item.get("creationTimeSeconds", 0)
                        })
                    logger.info(f"Successfully fetched {len(activities)} Codeforces submissions for {handle}")
                else:
                    logger.warning(f"Codeforces submissions API error for handle {handle}: {submissions_data.get('comment', 'Unknown error')}")
            else:
                logger.warning(f"Codeforces submissions API returned status {submissions_response.status} for handle: {handle}")

            # Process user info
            stats = {}
            if user_info_response.status == 200:
                user_info_data = await user_info_response.json()
                if user_info_data.get("status") == "OK":
                    users = user_info_data.get("result", [])
                    if users:
                        user = users[0]
                        stats = {
                            "rating": user.get("rating", 0),
                            "max_rating": user.get("maxRating", 0),
                            "rank": user.get("rank", "unrated"),
                            "max_rank": user.get("maxRank", "unrated"),
                            "contribution": user.get("contribution", 0),
                            "friend_of_count": user.get("friendOfCount", 0)
                        }
                        logger.info(f"Codeforces stats for {handle}: rating={stats['rating']}, rank={stats['rank']}, max_rating={stats['max_rating']}")
                    else:
                        logger.warning(f"No user info found in Codeforces API response for handle: {handle}")
                else:
                    logger.warning(f"Codeforces user info API error for handle {handle}: {user_info_data.get('comment', 'Unknown error')}")
            else:
                logger.warning(f"Codeforces user info API returned status {user_info_response.status} for handle: {handle}")

            return {
                "activities": activities,
                "stats": stats
            }

    except asyncio.TimeoutError:
        logger.error(f"Timeout fetching Codeforces data for handle: {handle}")
        return {"activities": [], "stats": {}}
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching Codeforces data for {handle}: {e}")
        return {"activities": [], "stats": {}}
    except Exception as e:
        logger.error(f"Unexpected error fetching Codeforces data for {handle}: {e}", exc_info=True)
        return {"activities": [], "stats": {}}


async def fetch_all(handles: dict):
    """
    Fetch data from all supported platforms in parallel.

    Args:
        handles: Dictionary with platform names as keys and usernames as values
                Example: {
                    "codeforces": "tourist",
                    "leetcode": "username",
                    "codechef": "username",
                    "atcoder": "username",
                    "hackerrank": "username"
                }

    Returns:
        List of all activities from all platforms
    """
    if not handles:
        logger.warning("No handles dictionary provided")
        return []

    # Normalize handles: make keys lowercase and strip whitespace from values
    normalized_handles = {}
    for key, value in handles.items():
        # Handle None, empty strings, and whitespace-only strings
        if value is not None:
            if isinstance(value, str):
                normalized_value = value.strip()
                # Only add non-empty values after stripping
                if normalized_value:
                    normalized_key = key.lower().strip()
                    normalized_handles[normalized_key] = normalized_value
            elif value:  # Handle non-string truthy values
                normalized_key = key.lower().strip()
                normalized_handles[normalized_key] = str(value).strip()

    logger.info(f"Starting data fetch for platforms: {list(normalized_handles.keys())}")
    logger.info(f"Normalized handles: {normalized_handles}")

    tasks = []
    platform_names = []
    handle_values = []

    # Check each platform with normalized keys
    if normalized_handles.get("codeforces"):
        handle = normalized_handles["codeforces"]
        tasks.append(fetch_codeforces(handle))
        platform_names.append("codeforces")
        handle_values.append(handle)

    if normalized_handles.get("leetcode"):
        handle = normalized_handles["leetcode"]
        tasks.append(fetch_leetcode(handle))
        platform_names.append("leetcode")
        handle_values.append(handle)

    if normalized_handles.get("hackerrank"):
        handle = normalized_handles["hackerrank"]
        tasks.append(fetch_hackerrank(handle))
        platform_names.append("hackerrank")
        handle_values.append(handle)

    if normalized_handles.get("codechef"):
        handle = normalized_handles["codechef"]
        tasks.append(fetch_codechef(handle))
        platform_names.append("codechef")
        handle_values.append(handle)

    if normalized_handles.get("atcoder"):
        handle = normalized_handles["atcoder"]
        tasks.append(fetch_atcoder(handle))
        platform_names.append("atcoder")
        handle_values.append(handle)



    if not tasks:
        logger.warning(f"No valid platform handles provided. Input handles: {handles}, Normalized: {normalized_handles}")
        return []

    logger.info(f"Fetching data for {len(tasks)} platforms: {list(zip(platform_names, handle_values))}")

    # Gather all tasks with exception handling
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results and handle exceptions
    all_activities = []
    all_stats = {}

    for i, result in enumerate(results):
        platform = platform_names[i]
        handle = handle_values[i]

        if isinstance(result, Exception):
            logger.error(f"Error fetching data from {platform} for handle '{handle}': {result}")
            # Try Gemini scraping as fallback
            logger.info(f"Attempting Gemini scraping for {platform}/{handle}")
            try:
                gemini_result = await scrape_profile(platform, handle)
                if gemini_result and gemini_result.get("stats"):
                    logger.info(f"Gemini scraping successful for {platform}/{handle}")
                    all_stats[platform] = gemini_result.get("stats", {})
                else:
                    logger.warning(f"Gemini scraping returned no stats for {platform}/{handle}")
            except Exception as gemini_error:
                logger.error(f"Gemini scraping also failed for {platform}/{handle}: {gemini_error}")
            continue

        if result:
            # Check if result is the new dict structure or old list structure
            if isinstance(result, dict) and "activities" in result:
                activities = result.get("activities", [])
                stats = result.get("stats", {})

                all_activities.extend(activities)
                if stats:
                    all_stats[platform] = stats
                    logger.info(f"Added {len(activities)} activities and stats from {platform} (handle: {handle})")
                else:
                    # No stats from API, try Gemini scraping
                    logger.info(f"No stats from API for {platform}/{handle}, trying Gemini scraping")
                    try:
                        gemini_result = await scrape_profile(platform, handle)
                        if gemini_result and gemini_result.get("stats"):
                            all_stats[platform] = gemini_result.get("stats", {})
                            logger.info(f"Gemini scraping provided stats for {platform}/{handle}")
                    except Exception as gemini_error:
                        logger.error(f"Gemini scraping failed for {platform}/{handle}: {gemini_error}")
                    logger.info(f"Added {len(activities)} activities from {platform} (handle: {handle})")
            elif isinstance(result, list):
                # Legacy support for fetchers returning just a list
                all_activities.extend(result)
                logger.info(f"Added {len(result)} activities from {platform} (handle: {handle})")
            else:
                logger.warning(f"Unexpected data format from {platform} for handle '{handle}'")
        else:
            logger.warning(f"No data returned from {platform} for handle '{handle}'")
            # Try Gemini scraping as fallback
            logger.info(f"Attempting Gemini scraping for {platform}/{handle}")
            try:
                gemini_result = await scrape_profile(platform, handle)
                if gemini_result and gemini_result.get("stats"):
                    all_stats[platform] = gemini_result.get("stats", {})
                    logger.info(f"Gemini scraping successful for {platform}/{handle}")
                else:
                    logger.warning(f"Gemini scraping returned no data for {platform}/{handle}")
            except Exception as gemini_error:
                logger.error(f"Gemini scraping also failed for {platform}/{handle}: {gemini_error}")

    successful_platforms = [r for r in results if not isinstance(r, Exception) and r]
    failed_platforms = [platform_names[i] for i, r in enumerate(results) if isinstance(r, Exception) or not r]

    logger.info(f"Total activities fetched: {len(all_activities)} from {len(successful_platforms)} platforms")
    if failed_platforms:
        logger.warning(f"Failed to fetch data from platforms: {failed_platforms}")

    return {
        "activities": all_activities,
        "stats": all_stats
    }
