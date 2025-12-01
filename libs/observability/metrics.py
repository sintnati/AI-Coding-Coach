"""
Observability utilities: metrics, health checks, and monitoring.
"""
import time
import logging
from typing import Dict, Any
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Simple metrics collector for monitoring."""

    def __init__(self):
        self.metrics = defaultdict(lambda: {"count": 0, "total_time": 0, "errors": 0})
        self.lock = threading.Lock()
        logger.info("Metrics collector initialized")

    def record_request(self, endpoint: str, duration: float, success: bool = True):
        """Record a request metric."""
        with self.lock:
            self.metrics[endpoint]["count"] += 1
            self.metrics[endpoint]["total_time"] += duration
            if not success:
                self.metrics[endpoint]["errors"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        with self.lock:
            result = {}
            for endpoint, data in self.metrics.items():
                avg_time = data["total_time"] / data["count"] if data["count"] > 0 else 0
                result[endpoint] = {
                    "requests": data["count"],
                    "avg_response_time": round(avg_time, 3),
                    "errors": data["errors"],
                    "error_rate": round(data["errors"] / data["count"] * 100, 2) if data["count"] > 0 else 0
                }
            return result

    def reset(self):
        """Reset all metrics."""
        with self.lock:
            self.metrics.clear()
            logger.info("Metrics reset")


# Global metrics instance
metrics_collector = MetricsCollector()


def get_health_status() -> Dict[str, Any]:
    """Get system health status."""
    import psutil
    import os

    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "system": {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_mb": round(memory_info.rss / 1024 / 1024, 2),
                "memory_percent": process.memory_percent()
            },
            "metrics": metrics_collector.get_metrics()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }


class RequestTimer:
    """Context manager for timing requests."""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.start_time = None
        self.success = True

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.success = exc_type is None
        metrics_collector.record_request(self.endpoint, duration, self.success)

        if self.success:
            logger.info(f"{self.endpoint} completed in {duration:.3f}s")
        else:
            logger.error(f"{self.endpoint} failed after {duration:.3f}s: {exc_val}")

        return False  # Don't suppress exceptions
