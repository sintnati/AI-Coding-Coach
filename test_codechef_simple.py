"""
Direct simple test of CodeChef fetcher.
"""
import asyncio
import sys
import os
import logging

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv
load_dotenv()

async def main():
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Gemini API Key: {'Found' if api_key else 'NOT FOUND'}")
    if not api_key:
        print("ERROR: Set GEMINI_API_KEY in .env file")
        return

    print(f"API Key starts with: {api_key[:20]}...")

    # Import and test
    from services.fetcher.codechef_fetcher import fetch_codechef

    username = "kashyap1311"  # Your username
    print(f"\nTesting CodeChef for: {username}")
    print("="*60)

    try:
        result = await fetch_codechef(username)
        print(f"\nResult received:")
        print(f"Type: {type(result)}")
        print(f"Content: {result}")

        if result and isinstance(result, dict):
            print(f"\n✓ Success!")
            print(f"  Activities: {len(result.get('activities', []))}")
            print(f"  Stats: {result.get('stats', {})}")
        else:
            print(f"\n✗ Failed or empty result")
    except Exception as e:
        print(f"\n✗ Exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
