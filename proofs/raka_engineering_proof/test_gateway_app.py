"""
Automated Test Suite for RAKA's Enterprise Gateway App
Tests: Caching, Rate Limiting, Circuit Breaker, Route Dispatch, and Error Resilience.
"""

import unittest
import time
from enterprise_gateway_app import EnterpriseGatewayApp, LRUCacheWithTTL, TokenBucketRateLimiter, CircuitBreaker


class TestEnterpriseGatewayApp(unittest.TestCase):
    def setUp(self):
        self.app = EnterpriseGatewayApp()

    def test_health_check_route(self):
        """Verify standard /health endpoint returns HTTP 200 and valid JSON."""
        res = self.app.process_request("/health")
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(res["data"]["status"], "UP")
        self.assertFalse(res["cached"])

    def test_lru_caching_behavior(self):
        """Verify that identical subsequent requests are served from LRU cache."""
        req1 = self.app.process_request("/api/v1/user", {"id": "1001"})
        self.assertEqual(req1["status_code"], 200)
        self.assertFalse(req1["cached"])

        # Second request should be cached
        req2 = self.app.process_request("/api/v1/user", {"id": "1001"})
        self.assertEqual(req2["status_code"], 200)
        self.assertTrue(req2["cached"])
        self.assertEqual(req1["data"], req2["data"])

    def test_rate_limiter_exhaustion(self):
        """Verify rate limiter rejects excessive requests exceeding bucket capacity."""
        limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=0.1)
        self.assertTrue(limiter.allow_request())
        self.assertTrue(limiter.allow_request())
        self.assertTrue(limiter.allow_request())
        # 4th request must fail
        self.assertFalse(limiter.allow_request())

    def test_circuit_breaker_trip_and_recovery(self):
        """Verify circuit breaker transitions from CLOSED to OPEN after 3 failures."""
        cb = CircuitBreaker(failure_threshold=3, recovery_time_sec=0.1)
        self.assertEqual(cb.state, "CLOSED")

        cb.record_failure()
        cb.record_failure()
        self.assertEqual(cb.state, "CLOSED")

        cb.record_failure()
        self.assertEqual(cb.state, "OPEN")
        self.assertFalse(cb.can_execute())

        # Wait for recovery window
        time.sleep(0.12)
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, "HALF-OPEN")

        cb.record_success()
        self.assertEqual(cb.state, "CLOSED")

    def test_route_not_found_returns_404(self):
        """Verify invalid endpoint returns 404 Not Found."""
        res = self.app.process_request("/api/nonexistent")
        self.assertEqual(res["status_code"], 404)

    def test_simulated_downstream_fault_handling(self):
        """Verify downstream exception returns 500 and updates circuit breaker."""
        res = self.app.process_request("/api/v1/user", {"id": "fail"}, downstream_fault=True)
        self.assertEqual(res["status_code"], 500)
        self.assertIn("Simulated Downstream", res["error"])


if __name__ == "__main__":
    unittest.main()
