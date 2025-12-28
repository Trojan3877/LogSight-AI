"""
MLflow experiment tracking for prompts and models.
"""

import mlflow

def track_experiment(prompt_version, metric):
    mlflow.set_experiment("LogSight-AI")
    with mlflow.start_run():
        mlflow.log_param("prompt_version", prompt_version)
        mlflow.log_metric("incident_score", metric)