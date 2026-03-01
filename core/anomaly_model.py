Module: anomaly_model.py

Purpose:

Implements unsupervised anomaly detection for structured log data using
Isolation Forest.

This module is responsible for:
- Training anomaly detection models
- Generating anomaly scores
- Producing binary anomaly classifications
- Providing structured outputs suitable for downstream services

Design Rationale:
-----------------
We use Isolation Forest because:

1. It performs well on high-dimensional sparse log feature vectors.
2. It does not require labeled anomaly data (unsupervised).
3. It scales efficiently for medium-to-large log datasets.
4. It isolates anomalies rather than modeling normal behavior density.

Isolation Forest works by:
- Randomly partitioning data using feature splits
- Measuring how quickly a sample is isolated
- Fewer splits → higher anomaly likelihood

Complexity:
-----------
Training Complexity:  O(n log n)
Inference Complexity: O(trees * depth)
Memory Complexity:    O(n)

Where:
- n = number of samples
- trees = number of estimators
- depth ≈ log(n)

Tradeoffs:
----------
+ Fast and scalable
+ No labeling required
+ Works well with sparse vectors

- Not sequence-aware (does not capture temporal log relationships)
- Limited explainability
- Sensitive to feature scaling
- Does not adapt automatically to concept drift

Production Considerations:
--------------------------
- Should be extended with sequence-aware models (LSTM / Transformer)
  for distributed system logs.
- Should integrate model versioning (MLflow) in production.
- Should include drift monitoring for real-time systems.
- Should support explainability layer for SOC use cases.

Failure Modes:
--------------
- Poor feature engineering → unreliable anomaly scores
- Highly imbalanced data → excessive false positives
- Log schema changes → model instability

Author:
-------
Corey Leath

Version:
--------
1.0.0
"""

from typing import Tuple
import logging
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import NotFittedError


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LogAnomalyDetector:
    """
    Enterprise-grade wrapper around Isolation Forest
    for structured log anomaly detection.
    """

    def __init__(
        self,
        n_estimators: int = 200,
        contamination: float = 0.05,
        random_state: int = 42
    ):
        """
        Initialize anomaly detector with configurable hyperparameters.

        Parameters:
        ----------
        n_estimators : int
            Number of trees in the forest.

        contamination : float
            Expected proportion of anomalies in the dataset.
            Controls decision boundary.

        random_state : int
            Ensures reproducibility.
        """

        self.n_estimators = n_estimators
        self.contamination = contamination
        self.random_state = random_state

        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=self.random_state,
            n_jobs=-1
        )

        self._is_fitted = False

        logger.info("LogAnomalyDetector initialized.")


    def fit(self, X: np.ndarray) -> None:
        """
        Train the anomaly detection model.

        Parameters:
        ----------
        X : np.ndarray
            2D feature matrix of log-derived numerical features.

        Raises:
        -------
        ValueError if input data is invalid.
        """

        if not isinstance(X, np.ndarray):
            raise ValueError("Input data must be a NumPy array.")

        if len(X.shape) != 2:
            raise ValueError("Input must be a 2D array.")

        logger.info("Scaling feature matrix...")
        X_scaled = self.scaler.fit_transform(X)

        logger.info("Training Isolation Forest model...")
        self.model.fit(X_scaled)

        self._is_fitted = True
        logger.info("Model training complete.")


    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate anomaly predictions.

        Parameters:
        ----------
        X : np.ndarray
            2D feature matrix.

        Returns:
        --------
        Tuple containing:
        - anomaly_labels (1 = normal, -1 = anomaly)
        - anomaly_scores (lower score = more anomalous)

        Raises:
        -------
        NotFittedError if model is not trained.
        """

        if not self._is_fitted:
            raise NotFittedError("Model must be fitted before prediction.")

        logger.info("Scaling input features for inference...")