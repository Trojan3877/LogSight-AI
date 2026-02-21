import pandas as pd
from src.inference import classify_logs

def test_prediction_column_exists():
    df = pd.DataFrame({"message": ["test log 1", "test log 2"]})
    result = classify_logs(df)
    assert "prediction" in result.columns