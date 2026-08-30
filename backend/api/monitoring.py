"""Registre de métriques applicatives minimal et sans données personnelles."""

from __future__ import annotations

from collections import Counter
from threading import Lock


class MonitoringRegistry:
    """Agrège les requêtes du processus courant de manière thread-safe."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._request_count = 0
        self._error_count = 0
        self._total_latency_ms = 0.0
        self._max_latency_ms = 0.0
        self._status_counts: Counter[str] = Counter()
        self._endpoint_counts: Counter[str] = Counter()

    def record(self, method: str, path: str, status: int, latency_ms: float) -> None:
        with self._lock:
            self._request_count += 1
            self._error_count += int(status >= 400)
            self._total_latency_ms += latency_ms
            self._max_latency_ms = max(self._max_latency_ms, latency_ms)
            self._status_counts[str(status)] += 1
            self._endpoint_counts[f"{method} {path}"] += 1

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            average = (
                self._total_latency_ms / self._request_count
                if self._request_count
                else 0.0
            )
            error_rate = (
                self._error_count / self._request_count
                if self._request_count
                else 0.0
            )
            return {
                "scope": "current_process",
                "request_count": self._request_count,
                "error_count": self._error_count,
                "error_rate": round(error_rate, 4),
                "average_latency_ms": round(average, 2),
                "max_latency_ms": round(self._max_latency_ms, 2),
                "status_counts": dict(self._status_counts),
                "endpoint_counts": dict(self._endpoint_counts),
            }


monitoring_registry = MonitoringRegistry()
