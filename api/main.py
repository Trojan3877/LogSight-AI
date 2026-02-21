 # api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import asyncio
import json
import hashlib

from src.inference import classify_logs

app = FastAPI()

class LogEntry(BaseModel):
    message: str
    timestamp: str | None = None
    log_level: str | None = None


# -------------------------
# CACHE
# -------------------------
cache_store = {}

def generate_cache_key(payload: List[LogEntry], threshold: float):
    raw = json.dumps([log.model_dump() for log in payload], sort_keys=True)
    return hashlib.sha256((raw + str(threshold)).encode()).hexdigest()


# -------------------------
# STANDARD PREDICTION
# -------------------------
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


# -------------------------
# STREAMING SIMULATION
# ADD THIS SECTION BELOW
# -------------------------
@app.post("/stream")
async def stream_predict(logs: List[LogEntry], threshold: float = 0.60):

    streamed_results = []

    for log in logs:
        df = pd.DataFrame([log.model_dump()])
        results, latency = classify_logs(df, threshold)

        streamed_results.append({
            "result": results.to_dict(orient="records"),
            "latency": latency
        })

        await asyncio.sleep(0.05)

    return {
        "stream_mode": True,
        "streamed_count": len(streamed_results),
        "results": streamed_results
    }