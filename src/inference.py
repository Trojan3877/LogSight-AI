# src/inference.py

import numpy as np
import pandas as pd
from typing import Tuple


def _assign_severity(score: float) -> str:
    """
    Maps anomaly score to severity tier.
    """
    if score > 0.85:
        return "CRITICAL"
    elif score > 0.70:
        return "HIGH"
    elif score > 0.60:
        return "MEDIUM"
    else:
        return "LOW"


def classify_logs(
    df: pd.DataFrame,
    threshold: float = 0.60
) -> Tuple[pd.DataFrame, float]:
    """
    Core anomaly detection function.

    Parameters:
        df (pd.DataFrame): Input log dataframe
        threshold (float): Classification cutoff threshold

    Returns:
        Tuple[pd.DataFrame, float]:
            - Updated dataframe with predictions
            - Inference latency (seconds)
    """

    if "message" not in df.columns:
        raise ValueError("Input dataframe must contain a 'message' column.")

    start_time = pd.Timestamp.now()

    # Mock anomaly scoring (replace with real model later)
    np.random.seed(42)
    df = df.copy()
    df["anomaly_score"] = np.random.rand(len(df))

    df["prediction"] = df["anomaly_score"] > threshold
    df["severity"] = df["anomaly_score"].apply(_assign_severity)

    latency = (pd.Timestamp.now() - start_time).total_seconds()

    return df, latency