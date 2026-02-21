from fastapi import FastAPI
import pandas as pd
from src.inference import classify_logs

app = FastAPI()

@app.post("/predict")
def predict(logs: list):
    df = pd.DataFrame(logs)
    results = classify_logs(df)
    return results.to_dict(orient="records")