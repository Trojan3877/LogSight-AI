"""
Module: streaming.py

Purpose:
--------
Simulates streaming log ingestion in batch windows.

Design Rationale:
-----------------
Real-world systems process logs incrementally.

We simulate:
- Micro-batch ingestion
- Sliding window detection
- Real-time anomaly flagging

Production Considerations:
--------------------------
- Replace with Kafka consumer
- Add backpressure handling
- Integrate async processing
"""

import time
import pandas as pd
import numpy as np
from core.preprocessing import LogPreprocessor
from core.anomaly_model import LogAnomalyDetector


def simulate_stream(df: pd.DataFrame, batch_size: int = 50):
    preprocessor = LogPreprocessor()
    model = LogAnomalyDetector()

    features = preprocessor.transform(df)
    model.fit(features)

    results = []

    for i in range(0, len(df), batch_size):
        batch = features[i:i + batch_size]

        anomalies = model.detect_anomalies(batch)

        results.append({
            "batch_start": i,
            "batch_end": i + len(batch),
            "anomalies_detected": int(np.sum(anomalies))
        })

        time.sleep(0.1)  # simulate processing delay

    return results