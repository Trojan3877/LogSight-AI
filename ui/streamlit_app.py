import streamlit as st

st.title("LogSight-AI Dashboard")

st.subheader("Incident Summary")
st.write("Authentication service experiencing repeated failures.")

st.subheader("Root Cause Hypothesis")
st.write("Database outage downstream.")

st.subheader("Confidence")
st.progress(0.72)