import requests
import json
import sys
import datetime

def log(msg):
    with open("reproduce_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {msg}\n")

def test_analyze():
    url = "http://localhost:8080/analyze"
    payload = {
        "user_id": "test_user",
        "handles": {
            "codeforces": "tourist",
            "leetcode": "leetcode"
        }
    }

    log(f"Sending request to {url}...")
    log(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=30)
        log(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            log("Success!")
            data = response.json()
            log(f"Keys in response: {list(data.keys())}")
        else:
            log("Failed!")
            log(response.text)

    except Exception as e:
        log(f"Error: {e}")
        log("Is the server running?")

if __name__ == "__main__":
    # Clear log file
    with open("reproduce_log.txt", "w") as f:
        f.write("Starting reproduction script\n")
    test_analyze()
