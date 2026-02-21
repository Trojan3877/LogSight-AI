from functools import lru_cache
import json
import hashlib

def generate_cache_key(payload: List[LogEntry], threshold: float):
    raw = json.dumps([log.model_dump() for log in payload], sort_keys=True)
    key_string = raw + str(threshold)
    return hashlib.sha256(key_string.encode()).hexdigest()
cache_store = {}
@app.post("/predict")
async def predict(logs: List[LogEntry], threshold: float = 0.60):

    cache_key = generate_cache_key(logs, threshold)

    if cache_key in cache_store:
        return {
            "cached": True,
            **cache_store[cache_key]
        }

    df = pd.DataFrame([log.model_dump() for log in logs])
    results, latency = classify_logs(df, threshold)

    response = {
        "cached": False,
        "latency_seconds": latency,
        "log_count": len(results),
        "results": results.to_dict(orient="records")
    }

    cache_store[cache_key] = response

    return response



# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import asyncio

from src.inference import classify_logs

app = FastAPI(
    title="LogSight-AI API",
    description="Async REST API for ML-based log anomaly detection.",
    version="1.1.0"
)


class LogEntry(BaseModel):
    message: str
    timestamp: str | None = None
    log_level: str | None = None


@app.post("/predict")
async def predict(logs: List[LogEntry], threshold: float = 0.60):
    try:
        # Simulate async behavior (future streaming compatibility)
        await asyncio.sleep(0)

        df = pd.DataFrame([log.model_dump() for log in logs])

        results, latency = classify_logs(df, threshold)

        return {
            "latency_seconds": latency,
            "log_count": len(results),
            "results": results.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))