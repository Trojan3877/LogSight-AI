"""
Module: streamlit_app.py

Purpose:
--------
Enterprise UI layer for LogSight-AI.

Responsibilities:
- File upload
- API interaction
- Streaming simulation trigger
- Display anomaly metrics
- Render results cleanly

Design Rationale:
-----------------
UI must remain decoupled from model logic.

We treat this as:
Frontend → API → Core Services

Tradeoffs:
----------
+ Clean separation
+ Production-ready structure
- Requires API to run
"""

import streamlit as st
import pandas as pd
import requests
import logging

API_BASE_URL = "http://localhost:8000"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


st.set_page_config(page_title="LogSight-AI", layout="wide")

st.title("🔍 LogSight-AI Enterprise Log Anomaly Detection")


def call_api(endpoint: str, files=None, json=None):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", files=files, json=json)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


# File Upload Section
uploaded_file = st.file_uploader("Upload Log CSV", type=["csv"])

if uploaded_file:
    st.write("Uploading file for analysis...")

    result = call_api(
        "/analyze",
        files={"file": uploaded_file}
    )

    if result:
        st.subheader("📊 Detection Metrics")
        st.json(result["metrics"])

        st.subheader("⚡ Inference Latency (ms)")
        st.write(result["latency_ms"])


# Streaming Simulation
if st.button("Simulate Streaming Logs"):
    result = call_api("/stream")

    if result:
        st.subheader("🔄 Streaming Results")
        st.json(result)