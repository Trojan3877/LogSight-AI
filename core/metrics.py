"""
Module: metrics.py

Purpose:
--------
Provides evaluation metrics for anomaly detection performance,
including classification quality and system-level performance.

This module is responsible for:
- Computing precision, recall, F1-score
- Generating confusion matrices
- Calculating ROC-AUC
- Tracking inference latency
- Structuring evaluation outputs

Design Rationale:
-----------------
Enterprise ML systems must quantify:

1. Detection accuracy
2. False positive rate (alert fatigue risk)
3. False negative rate (missed incident risk)
4. Inference latency
5. System reliability

We centralize metric computation here to:
- Decouple evaluation from modeling
- Support production reporting
- Enable future dashboard integrations

Complexity:
-----------
Metric computation: O(n)

Tradeoffs:
----------
+ Clear evaluation transparency
+ Supports monitoring extensions
- Requires labeled data for full evaluation

Production Considerations:
--------------------------
- Integrate with Prometheus/Grafana
- Log metrics to MLflow
- Track drift over time
"""

from typing import Dict
import time
import numpy as np
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Compute core classification metrics.

    Parameters:
    ----------
    y_true : Ground truth labels (1 = anomaly, 0 = normal)
    y_pred : Predicted labels (1 = anomaly, 0 = normal)

    Returns:
    --------
    Dictionary of evaluation metrics.
    """

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0
    false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn
    }


def compute_roc_auc(
    y_true: np.ndarray,
    anomaly_scores: np.ndarray
) -> float:
    """
    Compute ROC-AUC score using anomaly scores.

    Lower scores indicate higher anomaly likelihood
    for Isolation Forest.

    We invert scores for proper ROC interpretation.
    """

    try:
        return roc_auc_score(y_true, -anomaly_scores)
    except ValueError:
        return 0.0


def measure_inference_latency(model, X: np.ndarray) -> float:
    """
    Measure inference time in milliseconds.

    Useful for enterprise SLAs.
    """

    start_time = time.time()
    model.predict(X)
    end_time = time.time()

    latency_ms = (end_time - start_time) * 1000
    return latency_ms