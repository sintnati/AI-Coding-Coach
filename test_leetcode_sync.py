"""
Simple synchronous test for LeetCode fetcher.
This avoids async event loop issues on Windows.
"""
import requests
import json

def test_leetcode_graphql(username):
    """Test LeetCode GraphQL API with requests library."""
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
            submitStatsGlobal {
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
    }
    """

    print(f"\nTesting LeetCode API for: {username}")
    print("=" * 60)

    try:
        response = requests.post(
            url,
            json={"query": query, "variables": {"username": username}},
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # Check for errors
            if "errors" in data:
                print(f"❌ GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
                return False

            # Check matchedUser
            matched_user = data.get("data", {}).get("matchedUser")

            if matched_user is None:
                print(f"❌ User '{username}' not found")
                return False

            print(f"✅ User found: {matched_user.get('username')}")

            # Check submitStatsGlobal
            submit_stats_global = matched_user.get("submitStatsGlobal")
            if submit_stats_global:
                print(f"✅ submitStatsGlobal found")
                ac_nums = submit_stats_global.get("acSubmissionNum", [])
                for stat in ac_nums:
                    print(f"   {stat.get('difficulty')}: {stat.get('count')}")
            else:
                print(f"⚠️  No submitStatsGlobal")

            # Check submitStats
            submit_stats = matched_user.get("submitStats")
            if submit_stats:
                print(f"✅ submitStats found")
                ac_nums = submit_stats.get("acSubmissionNum", [])
                for stat in ac_nums:
                    print(f"   {stat.get('difficulty')}: {stat.get('count')}")
            else:
                print(f"⚠️  No submitStats")

            # Check profile
            profile = matched_user.get("profile")
            if profile:
                print(f"✅ Profile found")
                print(f"   Ranking: {profile.get('ranking')}")
                print(f"   Reputation: {profile.get('reputation')}")
            else:
                print(f"⚠️  No profile")

            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("LeetCode GraphQL API Test (Synchronous)")
    print("=" * 60)

    # Test with known usernames
    test_usernames = [
        "leetcode",  # Official account
        # Add your username here
    ]

    for username in test_usernames:
        result = test_leetcode_graphql(username)
        print(f"\nResult: {'✅ PASS' if result else '❌ FAIL'}\n")
