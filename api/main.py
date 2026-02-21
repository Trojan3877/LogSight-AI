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