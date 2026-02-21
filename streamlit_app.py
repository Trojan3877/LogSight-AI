import streamlit as st
import pandas as pd
import time
from datetime import datetime
from sklearn.metrics import classification_report
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="LogSight-AI Dashboard",
    layout="wide"
)

st.title("🔍 LogSight-AI Anomaly Detection Dashboard")

st.markdown(
    """
    Real-time log ingestion and anomaly detection platform.
    Demonstrates ML-driven log classification with performance metrics and filtering.
    """
)

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("Upload Log CSV", type=["csv"])

confidence_threshold = st.sidebar.slider(
    "Anomaly Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

simulate_stream = st.sidebar.checkbox("Simulate Streaming Mode")

# -----------------------------
# MOCK MODEL (Replace with real inference)
# -----------------------------
def mock_model_predict(df):
    np.random.seed(42)
    df["anomaly_score"] = np.random.rand(len(df))
    df["prediction"] = df["anomaly_score"].apply(
        lambda x: 1 if x > confidence_threshold else 0
    )
    return df

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Log Data")
    st.dataframe(df.head())

    if simulate_stream:
        st.subheader("📡 Streaming Simulation")

        placeholder = st.empty()
        progress_bar = st.progress(0)

        streamed_data = []

        for i in range(len(df)):
            streamed_data.append(df.iloc[i])
            partial_df = pd.DataFrame(streamed_data)

            processed_df = mock_model_predict(partial_df)

            with placeholder.container():
                st.dataframe(processed_df.tail(10))

            progress_bar.progress((i + 1) / len(df))
            time.sleep(0.05)

        final_df = processed_df

    else:
        final_df = mock_model_predict(df)

    # -----------------------------
    # METRICS SECTION
    # -----------------------------
    st.subheader("📈 Detection Metrics")

    total_logs = len(final_df)
    anomalies = final_df["prediction"].sum()
    anomaly_rate = anomalies / total_logs

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Logs Processed", total_logs)
    col2.metric("Anomalies Detected", anomalies)
    col3.metric("Anomaly Rate", f"{anomaly_rate:.2%}")

    # -----------------------------
    # FILTERING
    # -----------------------------
    st.subheader("🔎 Filtered Results")

    show_anomalies_only = st.checkbox("Show Anomalies Only")

    if show_anomalies_only:
        display_df = final_df[final_df["prediction"] == 1]
    else:
        display_df = final_df

    st.dataframe(display_df)

    # -----------------------------
    # VISUALIZATION
    # -----------------------------
    st.subheader("📊 Anomaly Score Distribution")

    st.bar_chart(final_df["anomaly_score"])

    # -----------------------------
    # PERFORMANCE SUMMARY
    # -----------------------------
    st.subheader("⚡ Performance Summary")

    st.markdown(
        f"""
        - Confidence Threshold: {confidence_threshold}
        - Total Logs: {total_logs}
        - Anomaly Rate: {anomaly_rate:.2%}
        """
    )

else:
    st.info("Upload a CSV log file to begin analysis.")
