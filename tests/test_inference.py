# tests/test_inference.py

import pandas as pd
from src.inference import classify_logs


def test_prediction_column_exists():
    df = pd.DataFrame({
        "message": ["Service started", "Database error occurred"]
    })

    result, latency = classify_logs(df)

    assert "prediction" in result.columns
    assert "anomaly_score" in result.columns
    assert "severity" in result.columns
    assert isinstance(latency, float)


def test_invalid_input_raises_error():
    df = pd.DataFrame({"invalid_column": ["no message field"]})

    try:
        classify_logs(df)
    except ValueError as e:
        assert "message" in str(e)