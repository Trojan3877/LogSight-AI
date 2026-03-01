"""
Module: ingestion.py

Purpose:
--------
Handles ingestion of structured log data from file-based sources.

Responsibilities:
- Load log data (CSV or structured input)
- Validate schema
- Handle missing or malformed entries
- Enforce required fields
- Prepare clean DataFrame for preprocessing

Design Rationale:
-----------------
Enterprise log systems must:

1. Validate schema before modeling
2. Fail fast on structural inconsistencies
3. Log ingestion errors
4. Prevent silent corruption

This module centralizes ingestion logic to:
- Avoid duplicating file handling logic
- Maintain data integrity guarantees
- Enable future streaming extension

Complexity:
-----------
File loading: O(n)
Validation: O(n)

Tradeoffs:
----------
+ Strong data integrity guarantees
+ Clear failure logging
- Slight overhead from validation checks

Production Considerations:
--------------------------
- Extend to support streaming sources (Kafka / WebSocket)
- Add schema versioning
- Add data drift detection
"""

from typing import List
import logging
import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


REQUIRED_COLUMNS = [
    "timestamp",
    "log_level",
    "message"
]


class LogIngestionService:
    """
    Enterprise-grade ingestion service for structured log datasets.
    """

    def __init__(self, required_columns: List[str] = None):
        self.required_columns = required_columns or REQUIRED_COLUMNS
        logger.info("LogIngestionService initialized.")


    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load log data from CSV file.

        Raises:
        -------
        FileNotFoundError if file does not exist.
        ValueError if schema is invalid.
        """

        logger.info(f"Loading log data from {file_path}")

        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            logger.error("File not found.")
            raise
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            raise

        self._validate_schema(df)
        df = self._clean_dataframe(df)

        logger.info("Log ingestion complete.")
        return df


    def _validate_schema(self, df: pd.DataFrame) -> None:
        """
        Ensure required columns exist.
        """

        missing_columns = [
            col for col in self.required_columns if col not in df.columns
        ]

        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            raise ValueError(
                f"Schema validation failed. Missing columns: {missing_columns}"
            )

        logger.info("Schema validation successful.")


    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean log dataset.

        - Drop completely empty rows
        - Remove rows with missing required fields
        - Normalize log levels
        """

        logger.info("Cleaning DataFrame...")

        df = df.dropna(how="all")

        for col in self.required_columns:
            df = df[df[col].notnull()]

        df["log_level"] = df["log_level"].str.upper()

        logger.info("Data cleaning complete.")
        return df.reset_index(drop=True)