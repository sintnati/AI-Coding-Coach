import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Add current directory to path
sys.path.append(os.getcwd())

print("Starting verification...")

try:
    from services.preprocessor.preprocess import normalize_activities
    print("Import successful")

    # Mock data returned by fetch_all
    raw_data = {
        "activities": [
            {"platform": "leetcode", "id": "two-sum", "verdict": "AC", "timestamp": 1000},
            {"platform": "codechef", "id": "TEST", "verdict": "OK", "timestamp": 2000}
        ],
        "stats": {
            "leetcode": {
                "total_solved": 500,
                "easy_solved": 200,
                "medium_solved": 200,
                "hard_solved": 100,
                "ranking": 12345
            },
            "codechef": {
                "total_solved": 150,
                "stars": "4",
                "rating": 1800
            }
        }
    }

    print("Running normalize_activities...")
    # Run normalization
    result = normalize_activities(raw_data)

    # Verify growth metrics
    metrics = result.get("growth_metrics", {})
    platform_stats = metrics.get("platform_stats", {})

    print(f"Platform stats keys: {platform_stats.keys()}")

    # Check LeetCode stats
    lc_stats = platform_stats.get("leetcode", {})
    print(f"LeetCode Solved: {lc_stats.get('solved')} (Expected: 500)")

    if lc_stats.get("solved") == 500:
        print("PASS: LeetCode solved count correct")
    else:
        print("FAIL: LeetCode solved count incorrect")

    # Check CodeChef stats
    cc_stats = platform_stats.get("codechef", {})
    print(f"CodeChef Solved: {cc_stats.get('solved')} (Expected: 150)")

    if cc_stats.get("solved") == 150:
        print("PASS: CodeChef solved count correct")
    else:
        print("FAIL: CodeChef solved count incorrect")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
