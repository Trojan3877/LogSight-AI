LogSight-AI — Real-Time AIOps Log Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-AIOps-orange)
![Streaming](https://img.shields.io/badge/Data-Streaming-green)
![Logs](https://img.shields.io/badge/Logs-Analysis-blue)
![Anomaly Detection](https://img.shields.io/badge/Anomaly-Detection-critical)
![Time Series](https://img.shields.io/badge/Time--Series-Modeling-purple)
![Real-Time](https://img.shields.io/badge/Real--Time-Inference-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-blue?logo=kubernetes)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-black?logo=githubactions)
![Observability](https://img.shields.io/badge/Observability-Enabled-orange)
![Grafana](https://img.shields.io/badge/Grafana-Monitoring-orange?logo=grafana)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-yellow?logo=prometheus)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)
![Stars](https://img.shields.io/github/stars/Trojan3877/LogSight-AI?style=social)
![Forks](https://img.shields.io/github/forks/Trojan3877/LogSight-AI?style=social)



LogSight-AI is a **real-time AIOps platform** designed to ingest, analyze, and monitor log data streams using machine learning to detect anomalies, failures, and system irregularities.

The system bridges:
- Log ingestion pipelines
- Streaming analytics
- Machine learning inference
- Observability dashboards



 Core Capabilities

- Real-time log ingestion and parsing  
- Anomaly detection using ML models  
- Time-series pattern recognition  
- Alert generation for system anomalies  
- Monitoring dashboards (Streamlit / Grafana)  
- API-driven inference layer  



 System Architecture
Log Sources → Streaming Pipeline → Feature Extraction → ML Model → Anomaly Detection → Dashboard / Alerts




 Tech Stack

| Layer            | Technology |
|------------------|----------|
| Language         | Python |
| Backend API      | FastAPI |
| Dashboard        | Streamlit |
| ML Tracking      | MLflow |
| Containerization | Docker |
| Orchestration    | Kubernetes |
| Monitoring       | Prometheus + Grafana |



Data Flow

1. Logs are ingested from system sources  
2. Streaming pipeline processes events in real-time  
3. Features are extracted from log patterns  
4. ML model detects anomalies  
5. Results are visualized and monitored  



Use Cases

- Infrastructure monitoring  
- Failure detection  
- Incident response automation  
- Cloud system observability  
- DevOps / SRE automation  



Performance & Design Considerations

- Low-latency streaming inference  
- Scalable microservices architecture  
- Efficient memory usage for log parsing  
- Horizontal scaling via Kubernetes  
- Real-time dashboard updates  



Why This Project Matters

Modern systems generate massive volumes of logs.

This project demonstrates:
- Real-time AI system design  
- Production-grade observability architecture  
- ML applied to infrastructure reliability  
- End-to-end AIOps pipeline implementation  


 How to Run

### Start Backend
```bash
uvicorn main:app --reload
Run Dashboard
streamlit run app.py
📌 Future Improvements
LLM-based log summarization
Root cause analysis using AI agents
Distributed log ingestion (Kafka integration)
Advanced anomaly detection (transformers, LSTMs)
Multi-cluster observability support
