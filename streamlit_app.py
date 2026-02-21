# app/streamlit_app.py

import streamlit as st
import pandas as pd
import requests
import time

API_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="LogSight-AI", layout="wide")

st.title("LogSight-AI Dashboard")

st.markdown("""
Full-stack AI anomaly detection system.
Frontend (Streamlit) → Backend (FastAPI) → ML Inference Layer.
""")

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.header("Configuration")

uploaded_file = st.sidebar.file_uploader("Upload Log CSV", type=["csv"])

threshold = st.sidebar.slider(
    "Anomaly Threshold", 0.0, 1.0, 0.6, 0.05
)

# ------------------------
# MAIN LOGIC
# ------------------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    if "message" not in df.columns:
        st.error("CSV must contain a 'message' column.")
        st.stop()

    st.subheader("Raw Logs")
    st.dataframe(df.head())

    logs_payload = df.to_dict(orient="records")

    start_time = time.time()

    response = requests.post(
        API_URL,
        json=logs_payload,
        params={"threshold": threshold}
    )

    latency = time.time() - start_time

    if response.status_code != 200:
        st.error("API Error: " + response.text)
        st.stop()

    result = response.json()
    results_df = pd.DataFrame(result["results"])

    # ------------------------
    # METRICS
    # ------------------------
    st.subheader("System Metrics")

    col1, col2, col3 = st.columns(3)

    total = len(results_df)
    anomalies = results_df["prediction"].sum()
    anomaly_rate = anomalies / total

    col1.metric("Logs Processed", total)
    col2.metric("Anomalies", anomalies)
    col3.metric("API Latency (sec)", f"{latency:.3f}")

    # ------------------------
    # RESULTS
    # ------------------------
    st.subheader("Detection Results")

    show_only = st.checkbox("Show Anomalies Only")

    if show_only:
        display_df = results_df[results_df["prediction"]]
    else:
        display_df = results_df

    st.dataframe(display_df)

    # ------------------------
    # EXPORT
    # ------------------------
    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Results CSV",
        data=csv,
        file_name="logsight_results.csv",
        mime="text/csv",
    )

else:
    st.info("Upload a CSV file to begin.")