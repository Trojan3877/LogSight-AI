import numpy as np

def classify_logs(df, threshold=0.6):
    np.random.seed(42)
    df["anomaly_score"] = np.random.rand(len(df))
    df["prediction"] = df["anomaly_score"] > threshold

    def severity(score):
        if score > 0.85:
            return "CRITICAL"
        elif score > 0.7:
            return "HIGH"
        elif score > 0.6:
            return "MEDIUM"
        else:
            return "LOW"

    df["severity"] = df["anomaly_score"].apply(severity)
    return df