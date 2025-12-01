import asyncio
import aiohttp
import logging
import sys
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_leetcode_api(username: str):
    """Test LeetCode GraphQL API directly to see what's returned."""
    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
            profile {
                ranking
                reputation
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

    print(f"\n{'='*60}")
    print(f"Testing LeetCode API for username: {username}")
    print(f"{'='*60}\n")

    try:
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url,
                json={
                    "query": query,
                    "variables": {"username": username}
                },
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache"
                }
            ) as response:
                print(f"Response Status: {response.status}")

                if response.status != 200:
                    print(f"❌ API returned non-200 status: {response.status}")
                    return

                data = await response.json()

                # Pretty print the entire response
                print("\n📄 Full API Response:")
                print(json.dumps(data, indent=2))

                # Check for errors
                if "errors" in data:
                    print(f"\n❌ GraphQL Errors Found:")
                    print(json.dumps(data["errors"], indent=2))
                    return

                # Check data structure
                if "data" not in data:
                    print(f"\n❌ No 'data' field in response")
                    return

                print(f"\n✅ 'data' field exists")

                # Check matchedUser
                matched_user = data.get("data", {}).get("matchedUser")
                if matched_user is None:
                    print(f"❌ matchedUser is None - user '{username}' not found")
                    return

                if not matched_user:
                    print(f"❌ matchedUser is empty")
                    return

                print(f"✅ matchedUser exists")
                print(f"\n📊 User Data:")
                print(json.dumps(matched_user, indent=2))

                # Extract stats
                print(f"\n📈 Extracting Stats:")

                profile = matched_user.get("profile")
                if profile:
                    print(f"  ✅ Profile found:")
                    print(f"     - Ranking: {profile.get('ranking')}")
                    print(f"     - Reputation: {profile.get('reputation')}")
                else:
                    print(f"  ❌ No profile data")

                submit_stats = matched_user.get("submitStats")
                if submit_stats:
                    ac_submissions = submit_stats.get("acSubmissionNum", [])
                    print(f"  ✅ Submit stats found:")
                    print(f"     - AC Submissions: {len(ac_submissions)} entries")

                    for stat in ac_submissions:
                        difficulty = stat.get("difficulty", "")
                        count = stat.get("count", 0)
                        print(f"     - {difficulty}: {count}")
                else:
                    print(f"  ❌ No submitStats data")

                # Check submissions
                submissions = data.get("data", {}).get("recentSubmissionList", [])
                print(f"\n📝 Recent Submissions: {len(submissions)} found")
                if submissions:
                    print(f"  Sample submission:")
                    print(json.dumps(submissions[0], indent=2))

    except asyncio.TimeoutError:
        print(f"❌ Timeout error")
    except aiohttp.ClientError as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

async def main():
    # Test with a known valid username
    # You can replace this with your actual LeetCode username
    test_usernames = [
        "leetcode",  # Official LeetCode account
        # Add your username here to test
    ]

    for username in test_usernames:
        await test_leetcode_api(username)
        print("\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print("LeetCode API Diagnostic Tool")
    print("=" * 60)
    print("This tool will test the LeetCode GraphQL API directly")
    print("and show you exactly what data is being returned.")
    print("=" * 60)

    asyncio.run(main())
