import aiohttp
import asyncio
import json
from urllib.parse import quote

async def fetch_codechef(username):
    print(f"Fetching CodeChef for {username}...")
    base_url = "https://www.codechef.com/api/user/profile"
    async with aiohttp.ClientSession() as session:
        encoded_username = quote(username)
        async with session.get(f"{base_url}/{encoded_username}", headers={"Cache-Control": "no-cache"}) as response:
            if response.status != 200:
                print(f"CodeChef Error: {response.status}")
                return
            data = await response.json()
            # Print keys of data['data'] to see what's available
            if 'data' in data:
                print("CodeChef Data Keys:", data['data'].keys())
                # Check for stats
                print("CodeChef Stats:", json.dumps(data['data'].get('user_details', {}), indent=2)[:200]) # Print first 200 chars
            else:
                print("No data found")

async def fetch_leetcode(username):
    print(f"Fetching LeetCode for {username}...")
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
    }
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"query": query, "variables": {"username": username}}, headers={"Content-Type": "application/json"}) as response:
            if response.status != 200:
                print(f"LeetCode Error: {response.status}")
                return
            data = await response.json()
            print("LeetCode Data:", json.dumps(data, indent=2))

async def main():
    await fetch_codechef("tourist") # Famous CP profile
    await fetch_leetcode("neal_wu") # Famous CP profile

if __name__ == "__main__":
    asyncio.run(main())
