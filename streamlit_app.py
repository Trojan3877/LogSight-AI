import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from sklearn.cluster import KMeans

# ----------------------------------
# CONFIG
# ----------------------------------
st.set_page_config(page_title="LogSight-AI", layout="wide")

st.title("🔍 LogSight-AI Operational Dashboard")

st.markdown("""
AI-driven log anomaly detection system with performance metrics,
severity classification, clustering, and interactive monitoring.
""")

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.header("⚙️ Configuration")

uploaded_file = st.sidebar.file_uploader("Upload Log CSV", type=["csv"])

model_choice = st.sidebar.selectbox(
    "Select Model",
    ["Baseline Classifier", "Optimized Classifier", "Experimental Model"]
)

confidence_threshold = st.sidebar.slider(
    "Anomaly Confidence Threshold",
    0.0, 1.0, 0.6, 0.05
)

log_levels = st.sidebar.multiselect(
    "Filter Log Level",
    ["INFO", "WARN", "ERROR"],
    default=["INFO", "WARN", "ERROR"]
)

simulate_stream = st.sidebar.checkbox("Simulate Streaming")

# ----------------------------------
# MOCK MODEL
# Replace with real inference later
# ----------------------------------
def run_model(df):
    np.random.seed(42)
    df["anomaly_score"] = np.random.rand(len(df))
    df["prediction"] = df["anomaly_score"] > confidence_threshold

    # Severity tiers
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

# ----------------------------------
# MAIN
# ----------------------------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Simulate timestamp if missing
    if "timestamp" not in df.columns:
        df["timestamp"] = pd.date_range(
            end=datetime.now(), periods=len(df), freq="S"
        )

    if "log_level" not in df.columns:
        df["log_level"] = np.random.choice(
            ["INFO", "WARN", "ERROR"], size=len(df)
        )

    df = df[df["log_level"].isin(log_levels)]

    st.subheader("📄 Raw Logs")
    st.dataframe(df.head())

    start_time = time.time()

    if simulate_stream:
        placeholder = st.empty()
        processed_rows = []

        for i in range(len(df)):
            processed_rows.append(df.iloc[i])
            partial = pd.DataFrame(processed_rows)
            result = run_model(partial)

            with placeholder.container():
                st.dataframe(result.tail(5))

            time.sleep(0.02)

        final_df = result
    else:
        final_df = run_model(df)

    latency = time.time() - start_time

    # ----------------------------------
    # METRICS PANEL (Prometheus-style)
    # ----------------------------------
    st.subheader("📊 System Metrics")

    col1, col2, col3, col4 = st.columns(4)

    total_logs = len(final_df)
    anomalies = final_df["prediction"].sum()
    anomaly_rate = anomalies / total_logs

    col1.metric("Logs Processed", total_logs)
    col2.metric("Anomalies", anomalies)
    col3.metric("Anomaly Rate", f"{anomaly_rate:.2%}")
    col4.metric("Processing Latency (sec)", f"{latency:.2f}")

    # ----------------------------------
    # TIME SERIES VISUALIZATION
    # ----------------------------------
    st.subheader("📈 Time-Series Anomaly Trend")

    ts_data = final_df.set_index("timestamp")
    st.line_chart(ts_data["anomaly_score"])

    # ----------------------------------
    # FILTERED ANOMALIES
    # ----------------------------------
    st.subheader("🚨 Anomaly Table")

    show_only_anomalies = st.checkbox("Show Anomalies Only")

    if show_only_anomalies:
        display_df = final_df[final_df["prediction"] == True]
    else:
        display_df = final_df

    st.dataframe(display_df)

    # ----------------------------------
    # EXPORT RESULTS
    # ----------------------------------
    st.subheader("⬇️ Export Results")

    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="logsight_results.csv",
        mime="text/csv",
    )

    # ----------------------------------
    # CLUSTERING TAB
    # ----------------------------------
    st.subheader("🧠 Log Clustering (Semantic Grouping)")

    cluster_count = st.slider("Number of Clusters", 2, 6, 3)

    # Mock clustering using anomaly score
    clustering_data = final_df[["anomaly_score"]]
    kmeans = KMeans(n_clusters=cluster_count, random_state=42)
    final_df["cluster"] = kmeans.fit_predict(clustering_data)

    st.write("Cluster Distribution")
    st.bar_chart(final_df["cluster"].value_counts())

else:
    st.info("Upload a CSV log file to begin.")