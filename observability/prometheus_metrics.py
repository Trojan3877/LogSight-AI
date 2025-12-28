"""
Prometheus metrics for pipeline observability.
"""

from prometheus_client import Counter, Histogram

LOGS_PROCESSED = Counter("logs_processed_total", "Total logs processed")
LLM_LATENCY = Histogram("llm_latency_seconds", "LLM processing latency")

def record_log():
    LOGS_PROCESSED.inc()

def record_latency(duration):
    LLM_LATENCY.observe(duration)