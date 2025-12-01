"""
Enhanced logging middleware for debugging analysis issues.
This will log all requests and responses to help diagnose problems.
"""
import logging
import json
import time
from functools import wraps

logger = logging.getLogger(__name__)

def log_request_response(func):
    """Decorator to log request and response details."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()

        # Log request
        logger.info(f"=" * 80)
        logger.info(f"REQUEST to {func.__name__}")
        logger.info(f"Args: {args}")
        logger.info(f"Kwargs: {kwargs}")

        try:
            result = await func(*args, **kwargs)

            # Log response
            duration = time.time() - start_time
            logger.info(f"RESPONSE from {func.__name__} (took {duration:.2f}s)")

            if isinstance(result, dict):
                # Log summary of dict response
                logger.info(f"Response keys: {list(result.keys())}")

                if "activities" in result:
                    logger.info(f"Activities count: {len(result['activities'])}")

                if "stats" in result:
                    logger.info(f"Stats: {json.dumps(result['stats'], indent=2)}")

                if "growth_metrics" in result:
                    metrics = result["growth_metrics"]
                    if "platform_stats" in metrics:
                        logger.info(f"Platform stats:")
                        for platform, stats in metrics["platform_stats"].items():
                            logger.info(f"  {platform}: {stats}")
            else:
                logger.info(f"Response type: {type(result)}, length: {len(result) if hasattr(result, '__len__') else 'N/A'}")

            logger.info(f"=" * 80)
            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"ERROR in {func.__name__} (after {duration:.2f}s): {e}", exc_info=True)
            logger.info(f"=" * 80)
            raise

    return wrapper


# Example usage in app.py:
# from debug_logging import log_request_response
#
# @log_request_response
# async def analyze(req: LinkRequest):
#     ...
