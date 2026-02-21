# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

from src.inference import classify_logs

app = FastAPI(
    title="LogSight-AI API",
    description="REST API for ML-based log anomaly detection.",
    version="1.0.0"
)


class LogEntry(BaseModel):
    message: str
    timestamp: str = None
    log_level: str = None


@app.post("/predict")
def predict(logs: List[LogEntry], threshold: float = 0.60):
    try:
        df = pd.DataFrame([log.dict() for log in logs])
        results, latency = classify_logs(df, threshold)

        return {
            "latency_seconds": latency,
            "results": results.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))