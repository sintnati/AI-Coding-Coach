from datetime import datetime, timedelta
from collections import defaultdict


def normalize_activities(raw_data):
    """
    Normalize and enrich activities from all platforms.
    Adds growth metrics, time analysis, and platform statistics.

    Args:
        raw_data: List of activities OR Dict with 'activities' and 'stats'
    """
    activities = []
    fetched_stats = {}

    # Handle different input formats
    if isinstance(raw_data, dict) and "activities" in raw_data:
        # New format from fetch_all
        activities = raw_data.get("activities", [])
        fetched_stats = raw_data.get("stats", {})
    elif isinstance(raw_data, list):
        # Legacy format or simple list
        # Flatten if needed (in case raw_data is a list of lists)
        for item in raw_data:
            if isinstance(item, list):
                activities.extend(item)
            elif isinstance(item, dict):
                activities.append(item)

    # Sort by timestamp (newest first)
    activities.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

    # Calculate growth metrics
    growth_data = calculate_growth_metrics(activities, fetched_stats)

    # Add metadata
    for activity in activities:
        # Add human-readable date
        if activity.get("timestamp"):
            activity["date"] = datetime.fromtimestamp(activity["timestamp"]).strftime("%Y-%m-%d")

        # Normalize verdict/status
        verdict = activity.get("verdict", "").upper()
        activity["is_solved"] = verdict in ["OK", "ACCEPTED", "AC", "COMPLETED"]

    return {
        "activities": activities,
        "growth_metrics": growth_data,
        "total_count": len(activities),
        "platforms": list(set(a.get("platform") for a in activities if a.get("platform")))
    }


def calculate_growth_metrics(activities, fetched_stats=None):
    """
    Calculate growth metrics including:
    - Problems solved per platform
    - Activity over time
    - Streak information
    - Average solve time

    Args:
        activities: List of activity dicts
        fetched_stats: Dict of platform stats (optional)
    """
    if not activities and not fetched_stats:
        return {}

    if fetched_stats is None:
        fetched_stats = {}

    platform_stats = defaultdict(lambda: {"total": 0, "solved": 0, "solved_problems": set(), "languages": set()})
    daily_activity = defaultdict(int)
    monthly_activity = defaultdict(int)

    for activity in activities:
        platform = activity.get("platform", "unknown")
        timestamp = activity.get("timestamp", 0)

        if timestamp:
            date = datetime.fromtimestamp(timestamp)
            day_key = date.strftime("%Y-%m-%d")
            month_key = date.strftime("%Y-%m")

            daily_activity[day_key] += 1
            monthly_activity[month_key] += 1

        platform_stats[platform]["total"] += 1

        verdict = activity.get("verdict", "").upper()
        if verdict in ["OK", "ACCEPTED", "AC", "COMPLETED"]:
            # Count unique solved problems, not all submissions
            # Use platform + problem_id for uniqueness (same problem ID can exist on different platforms)
            problem_id = activity.get("id", "").strip()
            if problem_id:  # Only count if problem ID exists and is not empty
                unique_key = f"{platform}:{problem_id}"
                platform_stats[platform]["solved_problems"].add(unique_key)

        if activity.get("language"):
            platform_stats[platform]["languages"].add(activity["language"])

    # Convert solved_problems set to count and remove from stats
    import logging
    logger = logging.getLogger(__name__)

    for platform in platform_stats:
        # Calculate from activities
        calculated_solved = len(platform_stats[platform]["solved_problems"])
        total_submissions = platform_stats[platform]["total"]

        # Check if we have fetched stats for this platform
        p_stats = fetched_stats.get(platform, {})

        # Use fetched total_solved if available and greater than calculated
        # (fetched should be the source of truth for total solved)
        fetched_solved = p_stats.get("total_solved", 0)

        if fetched_solved > 0:
            logger.info(f"Using fetched stats for {platform}: {fetched_solved} solved (calculated: {calculated_solved})")
            platform_stats[platform]["solved"] = fetched_solved
        else:
            logger.info(f"Using calculated stats for {platform}: {calculated_solved} unique solved problems")
            platform_stats[platform]["solved"] = calculated_solved

        # Add other stats if available
        if p_stats:
            for key, value in p_stats.items():
                if key != "total_solved":
                    platform_stats[platform][key] = value

        del platform_stats[platform]["solved_problems"]  # Remove set, keep only count

    # Convert sets to lists for JSON serialization
    for platform in platform_stats:
        platform_stats[platform]["languages"] = list(platform_stats[platform]["languages"])

    # Calculate streak
    streak_info = calculate_streak(daily_activity)

    # Calculate time-based metrics
    if activities:
        # Count only unique days with actual activity, not the date range
        days_active = len(daily_activity) if daily_activity else 0

        if days_active > 0:
            avg_per_day = len(activities) / days_active
        else:
            avg_per_day = 0
    else:
        days_active = 0
        avg_per_day = 0

    return {
        "platform_stats": dict(platform_stats),
        "daily_activity": dict(daily_activity),
        "monthly_activity": dict(monthly_activity),
        "streak": streak_info,
        "days_active": days_active,
        "avg_problems_per_day": round(avg_per_day, 2),
        "total_platforms": len(platform_stats)
    }


def calculate_streak(daily_activity):
    """Calculate current and longest streak."""
    if not daily_activity:
        return {"current": 0, "longest": 0}

    sorted_dates = sorted(daily_activity.keys(), reverse=True)

    # Current streak
    current_streak = 0
    today = datetime.now().date()

    for date_str in sorted_dates:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        expected_date = today - timedelta(days=current_streak)

        if date == expected_date:
            current_streak += 1
        else:
            break

    # Longest streak
    longest_streak = 0
    temp_streak = 1

    sorted_dates_asc = sorted(daily_activity.keys())
    for i in range(1, len(sorted_dates_asc)):
        prev_date = datetime.strptime(sorted_dates_asc[i-1], "%Y-%m-%d").date()
        curr_date = datetime.strptime(sorted_dates_asc[i], "%Y-%m-%d").date()

        if (curr_date - prev_date).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    longest_streak = max(longest_streak, temp_streak)

    return {
        "current": current_streak,
        "longest": longest_streak
    }
