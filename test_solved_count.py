"""
Test script to debug solved problem counting
"""
import asyncio
import sys
import os
import json

sys.path.append(os.getcwd())

async def test_solved_counting():
    from services.fetcher.codeforces_fetcher import fetch_codeforces
    from services.preprocessor.preprocess import normalize_activities

    print("=" * 60)
    print("TESTING SOLVED PROBLEM COUNTING")
    print("=" * 60)
    print()

    # Fetch some data
    print("[TEST] Fetching Codeforces data for 'tourist'...")
    activities = await fetch_codeforces("tourist")

    print(f"Fetched {len(activities)} total submissions")

    # Show sample activities
    print("\nSample activities (first 5):")
    for i, act in enumerate(activities[:5]):
        print(f"{i+1}. ID: {act.get('id')}, Title: {act.get('title')}, Verdict: {act.get('verdict')}")

    # Count solved manually
    solved_activities = [a for a in activities if a.get('verdict', '').upper() in ['OK', 'ACCEPTED', 'AC', 'COMPLETED']]
    print(f"\nTotal solved submissions: {len(solved_activities)}")

    # Get unique solved problem IDs
    unique_solved_ids = set()
    for act in solved_activities:
        problem_id = act.get('id', '')
        if problem_id:
            unique_solved_ids.add(problem_id)

    print(f"Unique solved problem IDs: {len(unique_solved_ids)}")
    print(f"Unique IDs: {sorted(list(unique_solved_ids))[:10]}")

    # Process through normalize_activities
    print("\n[TEST] Processing through normalize_activities...")
    processed = normalize_activities(activities)

    platform_stats = processed.get('growth_metrics', {}).get('platform_stats', {})
    for platform, stats in platform_stats.items():
        print(f"\n{platform.upper()} Platform Stats:")
        print(f"  Total submissions: {stats.get('total', 0)}")
        print(f"  Solved (unique problems): {stats.get('solved', 0)}")

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_solved_counting())

