import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from services.analyser.analyze import analyze_user_activity

# Mock processed activities
activities = [{"platform": "codeforces", "title": "Test Problem", "verdict": "OK"}]

print("Calling analyze_user_activity...")
result = analyze_user_activity(activities)
print(f"Result type: {type(result)}")
print(f"Result: {result}")

if "raw_text" in result and "coroutine" in str(result["raw_text"]):
    print("BUG CONFIRMED: Async function called synchronously returned coroutine.")
else:
    print("Bug not reproduced exactly as expected, but check output.")
