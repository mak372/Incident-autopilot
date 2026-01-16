"""Tonic integration for synthetic data generation.

Tonic provides realistic test data for:
- Generating incident scenarios
- Creating realistic metrics and logs
- Ensuring demo reliability
- Testing edge cases
"""
import os
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta


class TonicClient:
    """Client for Tonic synthetic data API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TONIC_API_KEY", "")
        self.base_url = "https://api.tonic.ai/v1"
    
    def generate_metrics_dataset(self, scenario: str, duration_minutes: int = 60) -> List[Dict[str, Any]]:
        """Generate realistic time-series metrics for a scenario using Tonic AI.
        
        Args:
            scenario: Type of scenario (latency_spike, error_rate, etc.)
            duration_minutes: Duration of metrics to generate
            
        Returns:
            List of metric data points with timestamps
        """
        # Try Tonic API first if available
        if self.api_key:
            print(f"   🔑 [TONIC] API key detected, calling Tonic API for synthetic data...")
            try:
                result = self._generate_with_tonic_api(scenario, duration_minutes)
                print(f"   ✅ [TONIC] Successfully generated data via REAL Tonic API!")
                return result
            except Exception as e:
                print(f"   ⚠️ [TONIC] API failed, using local generation: {e}")
        else:
            print(f"   ℹ️ [TONIC] No API key, using local synthetic data generation")
        
        # Fallback to local generation
        return self._generate_locally(scenario, duration_minutes)
    
    def _generate_with_tonic_api(self, scenario: str, duration_minutes: int) -> List[Dict[str, Any]]:
        """Generate data using Tonic API."""
        import requests
        
        response = requests.post(
            f"{self.base_url}/generate",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "dataType": "timeseries",
                "schema": {
                    "latency_p50": "float",
                    "latency_p95": "float", 
                    "latency_p99": "float",
                    "error_rate": "float",
                    "cpu_usage": "float",
                    "memory_usage": "float",
                    "request_rate": "float"
                },
                "count": duration_minutes,
                "scenario": scenario
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"[TONIC] ✅ Generated {duration_minutes} data points via API")
            return response.json().get("data", [])
        else:
            raise Exception(f"Tonic API returned {response.status_code}")
    
    def _generate_locally(self, scenario: str, duration_minutes: int) -> List[Dict[str, Any]]:
        """Local fallback data generation."""
        metrics = []
        now = datetime.utcnow()
        
        for i in range(duration_minutes):
            timestamp = now - timedelta(minutes=duration_minutes - i)
            
            if scenario == "latency_spike" and i > duration_minutes * 0.7:
                # Spike in last 30% of timeline
                latency_p99 = random.uniform(4000, 6000)
            else:
                latency_p99 = random.uniform(300, 500)
            
            metrics.append({
                "timestamp": timestamp.isoformat(),
                "latency_p50": random.uniform(100, 200),
                "latency_p95": random.uniform(250, 400),
                "latency_p99": latency_p99,
                "error_rate": random.uniform(0.05, 0.3),
                "cpu_usage": random.uniform(40, 70),
                "memory_usage": random.uniform(50, 75),
                "request_rate": random.uniform(80, 120)
            })
        
        return metrics
    
    def generate_log_entries(self, scenario: str, count: int = 100) -> List[str]:
        """Generate realistic log entries for a scenario.
        
        Args:
            scenario: Type of scenario
            count: Number of log entries to generate
            
        Returns:
            List of log entry strings
        """
        # In production, use Tonic to generate realistic logs
        
        templates = {
            "latency_spike": [
                "[ERROR] Database query timeout after 5000ms",
                "[WARN] Slow query detected: SELECT * FROM users WHERE...",
                "[INFO] Request processing took 4.5s",
                "[ERROR] Connection pool exhausted, waiting for available connection"
            ],
            "error_rate": [
                "[ERROR] Failed to connect to redis-cache: connection refused",
                "[ERROR] HTTP 500 from downstream service",
                "[WARN] Retry attempt 3/3 failed",
                "[ERROR] Circuit breaker opened for auth-service"
            ],
            "resource_saturation": [
                "[WARN] Memory usage at 89%, approaching limit",
                "[ERROR] OOMKilled - pod restarting",
                "[WARN] CPU throttling detected",
                "[INFO] GC pause took 2.3s"
            ]
        }
        
        log_templates = templates.get(scenario, ["[INFO] Normal operation"])
        return [random.choice(log_templates) for _ in range(count)]
    
    def generate_incident_scenario(self, incident_type: str) -> Dict[str, Any]:
        """Generate a complete incident scenario with all data.
        
        Args:
            incident_type: Type of incident to generate
            
        Returns:
            Complete incident scenario with metrics, logs, and metadata
        """
        return {
            "incident_type": incident_type,
            "metrics": self.generate_metrics_dataset(incident_type),
            "logs": self.generate_log_entries(incident_type),
            "metadata": {
                "service": f"service-{random.randint(1,5)}",
                "region": random.choice(["us-east-1", "us-west-2", "eu-west-1"]),
                "environment": "production"
            }
        }

