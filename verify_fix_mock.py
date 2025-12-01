import asyncio
import logging
from unittest.mock import MagicMock, patch
import sys

# Mock the fetcher modules before importing codeforces_fetcher
sys.modules['services.fetcher.leetcode_fetcher'] = MagicMock()
sys.modules['services.fetcher.hackerrank_fetcher'] = MagicMock()
sys.modules['services.fetcher.codechef_fetcher'] = MagicMock()
sys.modules['services.fetcher.atcoder_fetcher'] = MagicMock()

from services.fetcher.codeforces_fetcher import fetch_all

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_fetch_all_logic():
    handles = {
        "codeforces": "tourist",
        "leetcode": "tourist",
        "codechef": "tourist",
        "hackerrank": "tourist",
        "atcoder": "tourist"
    }

    logger.info("Testing fetch_all logic with handles: %s", handles)

    # We need to patch the fetch functions inside codeforces_fetcher module
    # because they are imported there.
    with patch('services.fetcher.codeforces_fetcher.fetch_codeforces') as mock_cf, \
         patch('services.fetcher.codeforces_fetcher.fetch_leetcode') as mock_lc, \
         patch('services.fetcher.codeforces_fetcher.fetch_hackerrank') as mock_hr, \
         patch('services.fetcher.codeforces_fetcher.fetch_codechef') as mock_cc, \
         patch('services.fetcher.codeforces_fetcher.fetch_atcoder') as mock_ac:

        # Setup mocks to return dummy data
        mock_cf.return_value = {"activities": [], "stats": {"platform": "codeforces"}}
        mock_lc.return_value = {"activities": [], "stats": {"platform": "leetcode"}}
        mock_hr.return_value = {"activities": [], "stats": {"platform": "hackerrank"}}
        mock_cc.return_value = {"activities": [], "stats": {"platform": "codechef"}}
        mock_ac.return_value = {"activities": [], "stats": {"platform": "atcoder"}}

        results = await fetch_all(handles)

        # Verify that all fetch functions were called
        assert mock_cf.called, "fetch_codeforces was not called"
        assert mock_lc.called, "fetch_leetcode was not called"
        assert mock_hr.called, "fetch_hackerrank was not called"
        assert mock_cc.called, "fetch_codechef was not called"
        assert mock_ac.called, "fetch_atcoder was not called"

        logger.info("SUCCESS: All fetch functions were called correctly.")
        print("SUCCESS: All fetch functions were called correctly.")
        with open("verification_result.txt", "w") as f:
            f.write("SUCCESS: All fetch functions were called correctly.")

if __name__ == "__main__":
    asyncio.run(test_fetch_all_logic())
