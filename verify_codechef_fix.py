"""
Simple test to verify CodeChef fetcher is working with Gemini scraper.
"""
import asyncio
import logging
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

async def test_codechef():
    """Test the updated CodeChef fetcher."""
    from services.fetcher.codechef_fetcher import fetch_codechef

    # Test with a well-known CodeChef user
    test_username = "gennady.korotkevich"  # Famous competitive programmer

    print("="*60)
    print(f"Testing CodeChef Fetcher (Gemini Scraper)")
    print(f"Username: {test_username}")
    print("="*60)

    result = await fetch_codechef(test_username)

    print(f"\n✓ Result Type: {type(result)}")

    if isinstance(result, dict):
        activities = result.get("activities", [])
        stats = result.get("stats", {})

        print(f"✓ Structure: Correct (dict with 'activities' and 'stats')")
        print(f"✓ Activities count: {len(activities)}")
        print(f"✓ Stats: {stats}")

        if stats:
            print(f"\n✓✓ SUCCESS! CodeChef data fetched successfully")
            print(f"   Stats keys: {list(stats.keys())}")
            return True
        else:
            print(f"\n✗ WARNING: Stats dictionary is empty")
            print(f"   This might indicate:")
            print(f"   - Gemini API key not configured")
            print(f"   - Network issue")
            print(f"   - User doesn't exist")
            return False
    else:
        print(f"✗ FAIL: Wrong return type")
        return False

async def main():
    # Check if Gemini API key is set
    from dotenv import load_dotenv
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("⚠️  WARNING: GEMINI_API_KEY not found in environment")
        print("   Please set it in your .env file")
        print("   Get your key from: https://aistudio.google.com/app/apikey")
        return

    success = await test_codechef()

    print("\n" + "="*60)
    if success:
        print("✓ CodeChef fetcher is working correctly!")
    else:
        print("✗ CodeChef fetcher test failed")
    print("="*60)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
