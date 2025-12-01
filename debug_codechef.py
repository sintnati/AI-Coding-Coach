"""
Debug script to test CodeChef fetching in isolation.
"""
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.getcwd())

async def test_codechef_direct():
    """Test CodeChef fetcher directly."""
    print("\n" + "="*60)
    print("TEST 1: Direct CodeChef Fetcher")
    print("="*60)

    from services.fetcher.codechef_fetcher import fetch_codechef

    username = "kashyap1311"  # Your username
    print(f"Testing with username: {username}")

    result = await fetch_codechef(username)
    print(f"\nResult: {result}")
    print(f"Type: {type(result)}")

    if isinstance(result, dict):
        print(f"Activities: {len(result.get('activities', []))}")
        print(f"Stats: {result.get('stats', {})}")

    return result

async def test_fetch_all():
    """Test the fetch_all function with CodeChef."""
    print("\n" + "="*60)
    print("TEST 2: fetch_all with CodeChef")
    print("="*60)

    from services.fetcher.codeforces_fetcher import fetch_all

    handles = {
        "codechef": "kashyap1311"  # Your username
    }

    print(f"Testing with handles: {handles}")

    result = await fetch_all(handles)
    print(f"\nResult: {result}")
    print(f"Type: {type(result)}")

    if isinstance(result, dict):
        print(f"Total Activities: {len(result.get('activities', []))}")
        print(f"Stats: {result.get('stats', {})}")

    return result

async def test_gemini_scraper():
    """Test Gemini scraper directly."""
    print("\n" + "="*60)
    print("TEST 3: Direct Gemini Scraper")
    print("="*60)

    from services.fetcher.gemini_scraper import scrape_profile

    username = "kashyap1311"
    print(f"Testing with username: {username}")

    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✓ Gemini API Key found: {api_key[:10]}...")
    else:
        print("✗ Gemini API Key NOT found!")

    result = await scrape_profile("codechef", username)
    print(f"\nResult: {result}")

    return result

async def main():
    print("CodeChef Fetcher Debug Test")
    print("="*60)

    # Test 1: Direct fetcher
    try:
        result1 = await test_codechef_direct()
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        logger.exception("Test 1 error")

    # Test 2: fetch_all
    try:
        result2 = await test_fetch_all()
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        logger.exception("Test 2 error")

    # Test 3: Gemini scraper
    try:
        result3 = await test_gemini_scraper()
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")
        logger.exception("Test 3 error")

    print("\n" + "="*60)
    print("Testing Complete")
    print("="*60)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
