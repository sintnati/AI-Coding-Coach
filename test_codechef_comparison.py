"""
Test with a known valid CodeChef username to verify the implementation works.
"""
import asyncio
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv
load_dotenv()

async def test_with_valid_user():
    """Test with tourist - a famous competitive programmer."""
    from services.fetcher.codechef_fetcher import fetch_codechef

    # Test 1: Known valid user
    print("="*60)
    print("TEST 1: Testing with 'tourist' (known valid CodeChef user)")
    print("="*60)

    result1 = await fetch_codechef("tourist")
    print(f"Result: {result1}")

    if result1 and result1.get("stats"):
        print(f"\n✓ SUCCESS with 'tourist'!")
        print(f"   Stats: {result1['stats']}")
    else:
        print(f"\n✗ FAILED even with known valid user")

    # Test 2: Your username
    print("\n" + "="*60)
    print("TEST 2: Testing with 'kashyap1311' (your username)")
    print("="*60)

    result2 = await fetch_codechef("kashyap1311")
    print(f"Result: {result2}")

    if result2 and result2.get("stats"):
        print(f"\n✓ SUCCESS with your username!")
        print(f"   Stats: {result2['stats']}")
    else:
        print(f"\n✗ FAILED with your username")
        print(f"\n   This means:")
        print(f"   - Your username might not exist on CodeChef")
        print(f"   - Or your profile is private")
        print(f"   - Or the username is spelled incorrectly")

    # Test 3: Invalid username
    print("\n" + "="*60)
    print("TEST 3: Testing with 'nonexistentuser123456' (invalid)")
    print("="*60)

    result3 = await fetch_codechef("nonexistentuser123456")
    print(f"Result: {result3}")

    if result3 and result3.get("stats"):
        print(f"\n✗ Unexpected success with invalid user")
    else:
        print(f"\n✓ Correctly returned empty for invalid user")

    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)

    if result1 and result1.get("stats"):
        print("✓ CodeChef fetcher WORKS correctly!")
        if not (result2 and result2.get("stats")):
            print("✗ Issue is with YOUR USERNAME 'kashyap1311'")
            print("\nPlease verify:")
            print("1. Go to https://www.codechef.com/users/kashyap1311")
            print("2. Does it show a profile or redirect to homepage?")
            print("3. If redirects, your username is incorrect or profile is private")
    else:
        print("✗ CodeChef fetcher has implementation issues")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(test_with_valid_user())
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
