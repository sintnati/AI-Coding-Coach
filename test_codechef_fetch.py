"""
Test CodeChef fetching functionality.
"""
import asyncio
import logging
import sys
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from services.fetcher.codechef_fetcher import fetch_codechef
from services.fetcher.gemini_scraper import scrape_profile


async def test_codechef_api(username: str):
    """Test CodeChef API fetcher."""
    print(f"\n{'='*60}")
    print(f"Testing CodeChef API for username: {username}")
    print(f"{'='*60}\n")

    result = await fetch_codechef(username)

    print(f"\nResult type: {type(result)}")
    print(f"Result: {result}")

    if isinstance(result, dict):
        activities = result.get("activities", [])
        stats = result.get("stats", {})
        print(f"\n✅ Found {len(activities)} activities")
        print(f"✅ Stats: {stats}")
    elif isinstance(result, list):
        print(f"\n✅ Found {len(result)} activities (legacy format)")
    else:
        print(f"\n❌ Unexpected result format")

    return result


async def test_gemini_scraper(username: str):
    """Test Gemini profile scraper."""
    print(f"\n{'='*60}")
    print(f"Testing Gemini Scraper for CodeChef user: {username}")
    print(f"{'='*60}\n")

    result = await scrape_profile("codechef", username)

    print(f"\nResult type: {type(result)}")
    print(f"Result: {result}")

    if isinstance(result, dict):
        activities = result.get("activities", [])
        stats = result.get("stats", {})
        print(f"\n✅ Found {len(activities)} activities")
        print(f"✅ Stats: {stats}")
    else:
        print(f"\n❌ Unexpected result format")

    return result


async def main():
    # Test username - you can change this
    test_username = "kashyap1311"  # Replace with actual CodeChef username

    print("=" * 60)
    print("CodeChef Data Fetching Test")
    print("=" * 60)

    # Test 1: CodeChef API
    api_result = await test_codechef_api(test_username)

    # Test 2: Gemini Scraper (if API fails or as backup)
    print("\n\n")
    gemini_result = await test_gemini_scraper(test_username)

    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"API Result: {'✅ Success' if api_result else '❌ Failed'}")
    print(f"Gemini Result: {'✅ Success' if gemini_result else '❌ Failed'}")


if __name__ == "__main__":
    asyncio.run(main())
