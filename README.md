# 🔍 LogSight-AI  
### Enterprise Log Anomaly Detection & Observability Platform

---

## 🏆 Badges

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![ML](https://img.shields.io/badge/IsolationForest-Unsupervised-orange)
![Architecture](https://img.shields.io/badge/Design-L6%20Enterprise-purple)

---

# 🧠 Overview

LogSight-AI is a scalable, API-first log anomaly detection platform designed for enterprise observability and security monitoring environments.

It supports:

- Structured log ingestion
- Feature engineering pipeline
- Unsupervised anomaly detection
- Streaming simulation
- API-first architecture
- Metrics evaluation layer
- Containerized deployment

---

# 🏗 System Architecture
User (UI) ↓ Streamlit Frontend ↓ FastAPI Backend ↓ Ingestion Layer ↓ Preprocessing Layer ↓ Isolation Forest Model ↓ Metrics Engine ↓ Structured JSON Output


# 📊 Metrics Tracked

| Metric | Purpose |
|--------|---------|
| Precision | Alert quality |
| Recall | Incident detection coverage |
| F1 Score | Balanced performance |
| False Positive Rate | Alert fatigue risk |
| False Negative Rate | Missed anomaly risk |
| Inference Latency | SLA compliance |


# ⚙️ Quick Start

## Local Development

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload

Streamlit:
Bash

streamlit run app/streamlit_app.py
🐳 Docker Deployment
Bash

docker-compose up --build
API: http://localhost:8000⁠�
UI: http://localhost:8501⁠�
Example Workflow
Upload CSV logs
Schema validated
Feature engineering applied
Isolation Forest trained
Anomalies detected
Metrics computed
Results returned via API
Production Roadmap
Redis caching
Kafka streaming ingestion
Model versioning (MLflow)
Concept drift detection
Transformer-based log embeddings
Prometheus monitoring integration

Why Isolation Forest?
Works without labeled anomaly data
Scales efficiently
Strong baseline for structured logs
Why API-first design?
Enables horizontal scaling
Supports microservices
Decouples frontend & backend
How would you improve this system?
Replace keyword features with embeddings
Add sequence modeling (LSTM/Transformer)
Add drift detection monitoring
Introduce real-time alert routing
How does this handle production load?
Stateless API
Containerized deployment
Ready for horizontal scaling behind load balancer
How do you reduce false positives?
Tune contamination parameter
Improve feature engineering
Add contextual aggregation
Incorporate feedback loop
👤 Author
Corey Leath
AI / ML Engineer | Systems Thinker | Enterprise Architect in Development