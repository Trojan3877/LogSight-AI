# app/streamlit_app.py

import streamlit as st
import pandas as pd
import requests
import time

# ----------------------------------
# CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="LogSight-AI Dashboard",
    layout="wide"
)

st.title("🔍 LogSight-AI Dashboard")

st.markdown("""
Full-stack AI anomaly detection system.

Frontend (Streamlit) → Backend (FastAPI) → ML Inference Layer  
Supports caching, streaming simulation, and threshold tuning.
""")

# ----------------------------------
# SIDEBAR CONTROLS
# ----------------------------------

st.sidebar.header("Configuration")

uploaded_file = st.sidebar.file_uploader("Upload Log CSV", type=["csv"])

threshold = st.sidebar.slider(
    "Anomaly Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.05
)

stream_mode = st.sidebar.checkbox("Enable Streaming Mode")

# Determine API endpoint
if stream_mode:
    API_URL = "http://localhost:8000/stream"
else:
    API_URL = "http://localhost:8000/predict"

# ----------------------------------
# MAIN LOGIC
# ----------------------------------

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Validate required column
    if "message" not in df.columns:
        st.error("CSV must contain a 'message' column.")
        st.stop()

    st.subheader("📄 Raw Log Sample")
    st.dataframe(df.head())

    logs_payload = df.to_dict(orient="records")

    # ----------------------------------
    # API REQUEST
    # ----------------------------------

    start_time = time.time()

    try:
        response = requests.post(
            API_URL,
            json=logs_payload,
            params={"threshold": threshold}
        )
    except Exception as e:
        st.error(f"API connection failed: {e}")
        st.stop()

    latency = time.time() - start_time

    if response.status_code != 200:
        st.error("API Error: " + response.text)
        st.stop()

    result = response.json()

    # ----------------------------------
    # STREAM MODE HANDLING
    # ----------------------------------

    if stream_mode:
        st.subheader("📡 Streaming Results")

        streamed_results = []

        for item in result["results"]:
            streamed_results.extend(item["result"])

        results_df = pd.DataFrame(streamed_results)

        st.write("Stream Mode Active")
    else:
        results_df = pd.DataFrame(result["results"])

        st.write("Cached:", result.get("cached", False))

    # ----------------------------------
    # METRICS PANEL
    # ----------------------------------

    st.subheader("📊 System Metrics")

    total_logs = len(results_df)
    anomalies = results_df["prediction"].sum()
    anomaly_rate = anomalies / total_logs if total_logs > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Logs Processed", total_logs)
    col2.metric("Anomalies Detected", anomalies)
    col3.metric("Anomaly Rate", f"{anomaly_rate:.2%}")
    col4.metric("API Latency (sec)", f"{latency:.3f}")

    # ----------------------------------
    # FILTERING OPTION
    # ----------------------------------

    st.subheader("🚨 Detection Results")

    show_only = st.checkbox("Show Anomalies Only")

    if show_only:
        display_df = results_df[results_df["prediction"] == True]
    else:
        display_df = results_df

    st.dataframe(display_df)

    # ----------------------------------
    # EXPORT OPTION
    # ----------------------------------

    st.subheader("⬇️ Export Results")

    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="logsight_results.csv",
        mime="text/csv",
    )

else:
    st.info("Upload a CSV file to begin analysis.")