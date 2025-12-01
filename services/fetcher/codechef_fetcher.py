import logging

logger = logging.getLogger(__name__)


async def fetch_codechef(username: str):
    """
    Fetch CodeChef user statistics using Gemini AI web scraping.

    NOTE: CodeChef does not provide an official public API as of 2024.
    This implementation uses the Gemini scraper to extract data from
    the profile page: https://www.codechef.com/users/{username}

    Args:
        username: CodeChef username

    Returns:
        Dict with 'activities' (list, usually empty) and 'stats' (dict with user statistics)
    """
    # Import here to avoid circular dependency issues
    from .gemini_scraper import scrape_profile

    logger.info(f"Fetching CodeChef data for {username} using Gemini scraper")
    logger.info("Note: CodeChef has no official public API, using AI web scraping")

    try:
        # Use Gemini scraper to extract profile data
        result = await scrape_profile("codechef", username)

        if result and result.get("stats"):
            stats = result.get("stats", {})
            logger.info(f"Successfully scraped CodeChef stats for {username}: {stats}")
            return {
                "activities": [],  # Profile pages don't show detailed activity history
                "stats": stats
            }
        else:
            logger.warning(f"No stats extracted from CodeChef profile for {username}")
            return {
                "activities": [],
                "stats": {}
            }

    except Exception as e:
        logger.error(f"Error fetching CodeChef data for {username}: {e}", exc_info=True)
        return {
            "activities": [],
            "stats": {}
        }
