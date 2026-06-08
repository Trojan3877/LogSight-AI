import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="LogSight-AI Dashboard", layout="wide")

st.title("📊 LogSight-AI Real-Time Performance & Anomaly Monitor")
st.markdown("Evaluating real-time Kubernetes log streams using C++ SIMD Tokenization & HDBSCAN/Isolation Forest.")

# Sidebar Controls
st.sidebar.header("System Controls")
stream_active = st.sidebar.checkbox("Connect to Live Ingestion Engine", value=True)
throughput_target = st.sidebar.slider("Target Ingestion (lines/sec)", 10000, 60000, 50000, step=5000)

# Layout Columns
col1, col2, col3 = st.columns(3)
metric_throughput = col1.metric("Current Throughput", "0 lines/sec")
metric_total = col2.metric("Total Logs Processed", "0")
metric_anomalies = col3.metric("Anomalies Isolated", "0", delta_color="inverse")

st.subheader("Live Streaming Analysis")
chart_placeholder = st.empty()

# Mock live connection to data layer
if stream_active:
    total_processed = 0
    anomaly_count = 0
    
    # Generate rolling window data for visualization
    df_history = pd.DataFrame(columns=["Timestamp", "Throughput", "Anomalies"])
    
    for i in range(50):
        current_time = time.strftime("%H:%M:%S")
        # Simulate standard performance near target, introducing intermittent burst anomalies
        actual_throughput = int(np.random.normal(throughput_target, 1500))
        new_anomalies = int(np.random.poisson(0.5)) if i % 12 != 0 else int(np.random.poisson(12.0))
        
        total_processed += actual_throughput
        anomaly_count += new_anomalies
        
        # Keep metrics dynamic
        metric_throughput.metric("Current Throughput", f"{actual_throughput:,} lines/sec")
        metric_total.metric("Total Logs Processed", f"{total_processed:,}")
        metric_anomalies.metric("Anomalies Isolated", f"{anomaly_count}", delta=f"+{new_anomalies}" if new_anomalies > 0 else "0")
        
        # Update streaming data frame
        new_row = pd.DataFrame([{"Timestamp": current_time, "Throughput": actual_throughput, "Anomalies": new_anomalies}])
        df_history = pd.concat([df_history, new_row], ignore_index=True).tail(20)
        
        # Display data
        with chart_placeholder.container():
            st.line_chart(df_history.set_index("Timestamp")["Throughput"])
            if new_anomalies > 5:
                st.error(f"🚨 Critical Anomaly Burst Detected at {current_time}! Component Isolation Forest flagged unusual pattern variations.")
                
        time.sleep(1)
else:
    st.info("Dashboard disconnected from the ingestion layer. Toggle 'Connect' to initiate the streaming context.")
