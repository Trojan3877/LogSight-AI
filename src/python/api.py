"""
api.py
──────────────────────────────────────────────────────────────────────────────
FastAPI layer that:

• exposes
    GET  /            → {"status": "ok"}
    GET  /alerts      → last N anomaly alerts (JSON)
    GET  /metrics     → Prometheus exposition format
• registers OpenTelemetry tracing if OTEL_EXPORTER_OTLP_ENDPOINT is set
• pushes every alert into an in-memory deque (backed by Snowflake already
  handled in anomaly.py)

Starts on :9000 inside Docker/Helm.

The module can be started stand-alone (`python api.py`) or imported by uvicorn.
"""

from __future__ import annotations

import os
from collections import deque
from typing import Deque, Dict, List

import fastapi
from fastapi import FastAPI
from pydantic import BaseModel
import prometheus_client as prom
from prometheus_client import Gauge
from prometheus_client import CONTENT_TYPE_LATEST

# ── OpenTelemetry (optional) ────────────────────────────────────────────────
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    OTEL_ENABLED = bool(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))
except ImportError:
    OTEL_ENABLED = False


# ── Alert storage (simple) ──────────────────────────────────────────────────
ALERT_BUFFER: Deque[Dict] = deque(maxlen=1000)

ALERT_GAUGE = Gauge("alerts_buffer_size", "Number of alerts stored in buffer")

# ── Pydantic schema for JSON responses ─────────────────────────────────────
class Alert(BaseModel):
    ts_ns: int
    score: float
    token_count: int


# ── FastAPI init ────────────────────────────────────────────────────────────
app = FastAPI(
    title="LogSight-AI Alerts API",
    version="0.1.0",
    docs_url="/docs",
)

# OTEL instrumentation
if OTEL_ENABLED:
    tp = TracerProvider()
    tp.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")))
    )
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tp)


# ── Route definitions ──────────────────────────────────────────────────────
@app.get("/")
async def health():
    return {"status": "ok"}


@app.get("/alerts", response_model=List[Alert])
async def get_alerts(limit: int = 100):
    """Return latest `limit` alerts (default 100)."""
    return list(ALERT_BUFFER)[-limit:]


@app.get("/metrics")
async def metrics():
    ALERT_GAUGE.set(len(ALERT_BUFFER))
    return prom.generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# ── Helper for AnomalyEngine to push alerts here ────────────────────────────
def push_alert(row: Dict):
    ALERT_BUFFER.append(row)


# ── uvicorn entrypoint ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=9000, reload=False)
