"""
Gemini-based profile scraper for coding platforms.
Fetches profile pages and uses Gemini AI to extract statistics.
"""
import aiohttp
import logging
import os
import json
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Profile URL templates
PROFILE_URLS = {
    "leetcode": "https://leetcode.com/{username}/",
    "codeforces": "https://codeforces.com/profile/{username}",
    "codechef": "https://www.codechef.com/users/{username}",
    "atcoder": "https://atcoder.jp/users/{username}",
    "hackerrank": "https://www.hackerrank.com/profile/{username}"
}

# Timeout configuration
FETCH_TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)


async def fetch_page_html(url: str) -> Optional[str]:
    """Fetch HTML content from a URL."""
    try:
        async with aiohttp.ClientSession(timeout=FETCH_TIMEOUT) as session:
            async with session.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url}: status {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


async def extract_stats_with_gemini(platform: str, username: str, html_content: str) -> Dict:
    """
    Use Gemini AI to extract statistics from profile HTML.

    Args:
        platform: Platform name (leetcode, codeforces, etc.)
        username: Username
        html_content: HTML content of profile page

    Returns:
        Dict with extracted stats
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set in environment")
        return {}

    # Create platform-specific prompt
    prompts = {
        "leetcode": """Extract the following from this LeetCode profile:
- total_solved: total problems solved
- easy_solved: easy problems solved
- medium_solved: medium problems solved
- hard_solved: hard problems solved
- ranking: global ranking number
- reputation: reputation points
- acceptance_rate: acceptance rate percentage""",

        "codeforces": """Extract the following from this CodeForces profile:
- rating: current rating
- max_rating: maximum rating achieved
- rank: current rank (e.g., "Expert", "Candidate Master")
- max_rank: maximum rank achieved
- contribution: contribution points
- total_solved: total problems solved (if visible)""",

        "codechef": """Extract the following from this CodeChef profile:
- rating: current rating
- stars: star rating (e.g., "4★", "5★")
- global_rank: global rank
- country_rank: country rank
- total_solved: total problems solved (if visible)""",

        "atcoder": """Extract the following from this AtCoder profile:
- rating: current rating
- highest_rating: highest rating achieved
- rank: rank/color (e.g., "cyan", "blue")
- total_solved: total problems solved (if visible)""",

        "hackerrank": """Extract the following from this HackerRank profile:
- total_score: total score/points
- badges: number of badges
- certificates: number of certificates
- tracks: list of track names and scores"""
    }

    platform_prompt = prompts.get(platform, "Extract all visible statistics")

    prompt = f"""You are a data extraction assistant. Analyze this {platform} profile page HTML and extract user statistics.

Username: {username}

{platform_prompt}

HTML Content (first 50000 chars):
{html_content[:50000]}

Return ONLY a valid JSON object with the extracted data. Use 0 or null for fields that are not visible.
Example format: {{"total_solved": 150, "rating": 1500, "rank": "Expert"}}

JSON:"""

    try:
        # Call Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 1000
            }
        }

        async with aiohttp.ClientSession(timeout=FETCH_TIMEOUT) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    logger.error(f"Gemini API error: {response.status}")
                    return {}

                result = await response.json()

                # Extract text from response
                if "candidates" in result and len(result["candidates"]) > 0:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]

                    # Parse JSON from response
                    # Remove markdown code blocks if present
                    text = text.strip()
                    if text.startswith("```json"):
                        text = text[7:]
                    if text.startswith("```"):
                        text = text[3:]
                    if text.endswith("```"):
                        text = text[:-3]
                    text = text.strip()

                    stats = json.loads(text)
                    logger.info(f"Gemini extracted stats for {platform}/{username}: {stats}")
                    return stats
                else:
                    logger.error(f"No candidates in Gemini response")
                    return {}

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        logger.debug(f"Response text: {text}")
        return {}
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}", exc_info=True)
        return {}


async def scrape_profile(platform: str, username: str) -> Dict:
    """
    Scrape a user's profile using Gemini AI.

    Args:
        platform: Platform name (leetcode, codeforces, etc.)
        username: Username

    Returns:
        Dict with 'activities' and 'stats'
    """
    logger.info(f"Scraping {platform} profile for {username} using Gemini")

    # Get profile URL
    url_template = PROFILE_URLS.get(platform)
    if not url_template:
        logger.error(f"Unknown platform: {platform}")
        return {"activities": [], "stats": {}}

    url = url_template.format(username=username)
    logger.info(f"Fetching profile page: {url}")

    # Fetch HTML
    html_content = await fetch_page_html(url)
    if not html_content:
        logger.error(f"Failed to fetch profile page for {platform}/{username}")
        return {"activities": [], "stats": {}}

    logger.info(f"Fetched {len(html_content)} chars of HTML for {platform}/{username}")

    # Extract stats with Gemini
    stats = await extract_stats_with_gemini(platform, username, html_content)

    # Return in standard format
    # Note: We don't extract activities from profile pages, only stats
    return {
        "activities": [],  # Profile pages don't show detailed activity history
        "stats": stats
    }
