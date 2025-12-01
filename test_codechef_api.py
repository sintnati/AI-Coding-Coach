"""
Quick test of CodeChef API endpoint.
"""
import requests
import json

username = "kashyap1311"
url = f"https://www.codechef.com/api/user/profile/{username}"

print(f"Testing CodeChef API: {url}")
print("=" * 60)

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print("\nResponse content:")
    print(response.text[:2000])  # First 2000 chars

    if response.status_code == 200:
        data = response.json()
        print("\n\nParsed JSON:")
        print(json.dumps(data, indent=2)[:3000])  # First 3000 chars
except Exception as e:
    print(f"Error: {e}")
