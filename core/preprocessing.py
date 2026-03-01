"""
Module: preprocessing.py

Purpose:
--------
Transforms validated log DataFrame into numerical feature matrix
suitable for anomaly detection models.

Responsibilities:
- Timestamp feature extraction
- Log level encoding
- Message length features
- Keyword frequency features
- Feature normalization preparation

Design Rationale:
-----------------
Isolation Forest requires numerical input features.

We engineer structured log features that capture:

1. Temporal signals (hour-of-day anomalies)
2. Severity signals (log level)
3. Message length anomalies
4. Security-sensitive keywords

Feature Engineering Philosophy:
-------------------------------
We prioritize interpretable, low-dimensional features over
high-dimensional embeddings for baseline anomaly detection.

Complexity:
-----------
Feature extraction: O(n)

Tradeoffs:
----------
+ Interpretable
+ Low computational overhead
+ Easy to debug

- Does not capture semantic meaning
- No sequence awareness
- No contextual embeddings

Production Considerations:
--------------------------
- Extend with TF-IDF vectorization
- Replace keyword detection with embedding model
- Add rolling-window aggregation for time-series modeling
"""

from typing import List
import pandas as pd
import numpy as np
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


SECURITY_KEYWORDS = [
    "error",
    "failed",
    "unauthorized",
    "timeout",
    "exception",
    "denied",
    "critical"
]


class LogPreprocessor:
    """
    Enterprise-grade feature engineering for structured logs.
    """

    def __init__(self, keywords: List[str] = None):
        self.keywords = keywords or SECURITY_KEYWORDS
        logger.info("LogPreprocessor initialized.")


    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Convert cleaned log DataFrame into numerical feature matrix.

        Returns:
        --------
        np.ndarray feature matrix
        """

        logger.info("Beginning feature transformation...")

        features = pd.DataFrame()

        # 1️⃣ Temporal Features
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        features["hour_of_day"] = df["timestamp"].dt.hour.fillna(0)

        # 2️⃣ Log Level Encoding
        features["is_error"] = (df["log_level"] == "ERROR").astype(int)
        features["is_warning"] = (df["log_level"] == "WARNING").astype(int)
        features["is_info"] = (df["log_level"] == "INFO").astype(int)

        # 3️⃣ Message Length
        features["message_length"] = df["message"].astype(str).apply(len)

        # 4️⃣ Keyword Frequency Features
        message_series = df["message"].astype(str).str.lower()

        for keyword in self.keywords:
            features[f"keyword_{keyword}"] = message_series.str.contains(
                keyword
            ).astype(int)

        logger.info("Feature transformation complete.")

        return features.values