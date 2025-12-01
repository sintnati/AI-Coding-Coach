"""
Test with actual user scenario to debug the counting issue
"""
import asyncio
import sys
import os
import json

sys.path.append(os.getcwd())

async def test_user_scenario():
    from services.fetcher.codeforces_fetcher import fetch_all
    from services.preprocessor.preprocess import normalize_activities

    print("=" * 60)
    print("TESTING USER SCENARIO - SOLVED COUNTING")
    print("=" * 60)
    print()

    # Simulate what happens when user submits
    # Let's create some test data that might match user's scenario
    test_activities = [
        {"platform": "codeforces", "id": "123-A", "title": "Problem 1", "verdict": "OK", "timestamp": 1000},
        {"platform": "codeforces", "id": "123-A", "title": "Problem 1", "verdict": "OK", "timestamp": 2000},  # Duplicate
        {"platform": "codeforces", "id": "123-A", "title": "Problem 1", "verdict": "WRONG_ANSWER", "timestamp": 1500},
        {"platform": "codeforces", "id": "456-B", "title": "Problem 2", "verdict": "OK", "timestamp": 3000},
        {"platform": "codeforces", "id": "789-C", "title": "Problem 3", "verdict": "OK", "timestamp": 4000},
        {"platform": "codeforces", "id": "456-B", "title": "Problem 2", "verdict": "OK", "timestamp": 5000},  # Duplicate
    ]

    print(f"Test data: {len(test_activities)} submissions")
    print("Breakdown:")
    for act in test_activities:
        print(f"  - {act['id']}: {act['verdict']}")

    # Process
    processed = normalize_activities(test_activities)
    platform_stats = processed.get('growth_metrics', {}).get('platform_stats', {})

    print("\nResults:")
    for platform, stats in platform_stats.items():
        print(f"\n{platform.upper()}:")
        print(f"  Total submissions: {stats.get('total', 0)}")
        print(f"  Unique solved problems: {stats.get('solved', 0)}")

    # Manual count
    solved_unique = set()
    for act in test_activities:
        if act.get('verdict', '').upper() in ['OK', 'ACCEPTED', 'AC', 'COMPLETED']:
            problem_id = act.get('id', '').strip()
            if problem_id:
                solved_unique.add(f"{act['platform']}:{problem_id}")

    print(f"\nExpected unique solved: {len(solved_unique)}")
    print(f"Expected IDs: {sorted(solved_unique)}")

    print()
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_user_scenario())

