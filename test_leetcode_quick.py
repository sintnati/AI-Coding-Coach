import asyncio
import aiohttp
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def quick_test():
    """Quick test of LeetCode API with timeout"""
    url = "https://leetcode.com/graphql"
    username = "leetcode"

    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
                totalSubmissionNum {
                    difficulty
                    count
                }
            }
            userCalendar {
                streak
            }
        }
    }
    """

    print(f"Testing LeetCode API for user: {username}")
    print("=" * 60)

    try:
        timeout = aiohttp.ClientTimeout(total=10, connect=5)
        print("Creating session...")

        async with aiohttp.ClientSession(timeout=timeout) as session:
            print("Sending POST request...")
            async with session.post(
                url,
                json={"query": query, "variables": {"username": username}},
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            ) as response:
                print(f"✅ Response received! Status: {response.status}")

                if response.status == 200:
                    data = await response.json()

                    if "data" in data and data["data"].get("matchedUser"):
                        user = data["data"]["matchedUser"]
                        print(f"\n✅ User found: {user.get('username')}")

                        # Check stats
                        if "submitStats" in user:
                            ac = user["submitStats"].get("acSubmissionNum", [])
                            total = user["submitStats"].get("totalSubmissionNum", [])
                            print(f"✅ AC Submissions: {len(ac)} categories")
                            print(f"✅ Total Submissions: {len(total)} categories")

                            for stat in ac:
                                if stat.get("difficulty") == "All":
                                    print(f"   Total Solved: {stat.get('count')}")

                            for stat in total:
                                if stat.get("difficulty") == "All":
                                    print(f"   Total Submissions: {stat.get('count')}")

                        # Check streak
                        if "userCalendar" in user:
                            streak = user["userCalendar"].get("streak", 0)
                            print(f"✅ Streak: {streak}")

                        print("\n✅ SUCCESS: API is working correctly!")
                    else:
                        print("❌ No user data in response")
                else:
                    print(f"❌ API returned status {response.status}")

    except asyncio.TimeoutError:
        print("❌ TIMEOUT: Request took too long")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(quick_test())
