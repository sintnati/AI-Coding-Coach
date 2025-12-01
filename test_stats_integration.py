import unittest
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from services.preprocessor.preprocess import normalize_activities

class TestStatsIntegration(unittest.TestCase):
    def test_normalize_activities_with_stats(self):
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

        # Run normalization
        result = normalize_activities(raw_data)

        # Verify growth metrics
        metrics = result.get("growth_metrics", {})
        platform_stats = metrics.get("platform_stats", {})

        # Check LeetCode stats
        self.assertIn("leetcode", platform_stats)
        self.assertEqual(platform_stats["leetcode"]["solved"], 500) # Should use fetched stats
        self.assertEqual(platform_stats["leetcode"]["ranking"], 12345)

        # Check CodeChef stats
        self.assertIn("codechef", platform_stats)
        self.assertEqual(platform_stats["codechef"]["solved"], 150) # Should use fetched stats
        self.assertEqual(platform_stats["codechef"]["stars"], "4")
        self.assertEqual(platform_stats["codechef"]["rating"], 1800)

        print("Verification successful: Preprocessor correctly uses fetched stats.")

if __name__ == "__main__":
    unittest.main()
