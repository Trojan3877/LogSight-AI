"""
Module: main.py

Purpose:
--------
Enterprise API layer for LogSight-AI.

Responsibilities:
- Accept log file uploads
- Run anomaly detection pipeline
- Return structured metrics
- Support streaming endpoint

Design Rationale:
-----------------
API-first design enables:
- Frontend decoupling
- Microservice deployment
- Horizontal scaling

Production Considerations:
--------------------------
- Add authentication
- Add rate limiting
- Add async processing
"""

from fastapi import FastAPI, UploadFile, File
import pandas as pd
import numpy as np
from core.ingestion import LogIngestionService
from core.preprocessing import LogPreprocessor
from core.anomaly_model import LogAnomalyDetector
from core.metrics import compute_classification_metrics, measure_inference_latency
from services.streaming import simulate_stream


app = FastAPI(title="LogSight-AI API")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    ingestion = LogIngestionService()
    preprocessor = LogPreprocessor()
    model = LogAnomalyDetector()

    df = pd.read_csv(file.file)

    df = ingestion._clean_dataframe(df)
    features = preprocessor.transform(df)

    model.fit(features)

    predictions = model.detect_anomalies(features)

    # Dummy ground truth (for demonstration)
    y_true = np.zeros(len(predictions))

    metrics = compute_classification_metrics(y_true, predictions)

    latency = measure_inference_latency(model, features)

    return {
        "metrics": metrics,
        "latency_ms": latency
    }


@app.post("/stream")
async def stream():
    df = pd.read_csv("data/sample_logs.csv")
    results = simulate_stream(df)

    return {
        "streaming_batches": results
    }