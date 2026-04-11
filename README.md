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


## 🚀 How to Run

### Prerequisites

- Python 3.9+
- [Docker](https://docs.docker.com/get-docker/) (optional, for containerized runs)

---

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/Trojan3877/LogSight-AI.git
cd LogSight-AI

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install the package with all dependencies
pip install -e ".[dev]"

# 4. Verify the installation
logsight health
```

### Analyse a Log File

```bash
# Analyse a local log file
logsight analyze /var/log/syslog

# Pipe logs from stdin
cat app.log | logsight stdin

# Adjust thresholds
logsight analyze app.log --threshold 3.0 --window 200 --spike-threshold 0.3
```

---

### Environment Variables

Copy `.env.example` to `.env` and customise as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `LOGSIGHT_THRESHOLD` | `2.5` | Z-score threshold for anomaly detection |
| `LOGSIGHT_WINDOW` | `100` | Sliding-window size for spike detection |
| `LOGSIGHT_SPIKE_THRESHOLD` | `0.25` | Error-rate fraction that constitutes a spike |

---

### Docker

```bash
# Build the image
docker build -t logsight-ai:latest .

# Verify the container starts correctly
docker run --rm logsight-ai:latest health

# Analyse a log file from the host
docker run --rm \
  -v /var/log:/logs:ro \
  logsight-ai:latest analyze /logs/syslog
```

---

### Running Tests

```bash
# Run the full test suite
pytest

# Run with coverage report
pytest --cov=logsight --cov-report=term-missing
```

---

### CI/CD

GitHub Actions automatically runs linting and tests on every push and pull request (see `.github/workflows/ci.yml`).

---

## 📌 Future Improvements

- LLM-based log summarization
- Root cause analysis using AI agents
- Distributed log ingestion (Kafka integration)
- Advanced anomaly detection (transformers, LSTMs)



## ❓ Why did you build LogSight-AI?

Modern distributed systems generate massive volumes of logs, making manual monitoring inefficient and error-prone. LogSight-AI was built to automate log analysis using machine learning, enabling real-time anomaly detection and improving system reliability.

---

## ❓ What problem does this solve?

Traditional log monitoring systems rely on static rules and thresholds, which fail in dynamic environments. LogSight-AI solves this by:

- Learning patterns from historical log data  
- Detecting anomalies in real-time  
- Reducing alert fatigue through intelligent filtering  
- Improving incident response time  

---

## ❓ How does the system work end-to-end?

1. Logs are ingested from system sources  
2. Streaming pipeline processes incoming data  
3. Features are extracted (timestamps, frequency, patterns)  
4. Machine learning model evaluates log behavior  
5. Anomalies are detected and flagged  
6. Results are visualized in dashboards and alerts  

---

## ❓ Why use machine learning for logs instead of rules?

Rule-based systems:
- Break in dynamic environments  
- Require constant manual updates  

ML-based systems:
- Adapt to changing system behavior  
- Detect unknown patterns  
- Reduce human intervention  

---

## ❓ What type of machine learning is used?

The system focuses on:

- Time-series anomaly detection  
- Unsupervised / semi-supervised learning  
- Pattern recognition in log sequences  

Future improvements may include:
- Transformer-based anomaly detection  
- LSTM-based sequence modeling  

---

## ❓ How is real-time performance handled?

- Streaming ingestion minimizes latency  
- Lightweight feature extraction ensures fast processing  
- Model inference is optimized for low-latency execution  
- Containerized deployment allows horizontal scaling  

---

## ❓ How does the system scale?

LogSight-AI is designed with scalability in mind:

- Docker for containerization  
- Kubernetes for orchestration  
- Stateless services for horizontal scaling  
- Monitoring via Prometheus + Grafana  

---

## ❓ How are anomalies defined?

Anomalies are deviations from learned normal behavior, such as:

- Sudden spikes in error logs  
- Unusual frequency patterns  
- Unexpected log sequences  
- Rare or unseen events  

---

## ❓ What are the main engineering challenges?

- Handling high-volume log streams  
- Designing low-latency pipelines  
- Avoiding false positives in anomaly detection  
- Maintaining model performance over time  
- Ensuring system scalability  

---

## ❓ How would you improve this system?

Planned enhancements include:

- LLM-based log summarization  
- Root cause analysis using AI agents  
- Kafka-based distributed streaming  
- Transformer-based anomaly detection  
- Multi-region observability  

---

## ❓ How does this compare to industry tools?

LogSight-AI aligns with systems like:

- Datadog  
- Splunk  
- Elastic Observability  

However, it differentiates itself by:
- Integrating ML directly into the pipeline  
- Supporting real-time inference  
- Being fully customizable and extensible  

---

## ❓ What did you learn from building this?

- Designing real-time ML systems  
- Building scalable data pipelines  
- Applying ML to infrastructure problems  
- Understanding observability engineering  
- Bridging DevOps and AI (AIOps)  

---

## ❓ Why is this project important for AI engineering?

This project demonstrates:

- End-to-end ML system design  
- Real-time inference pipelines  
- Production-ready architecture  
- Practical application of AI to real-world systems  

---

## ❓ How would this perform in production?

With proper deployment (Kubernetes + monitoring):

- Handles high-volume log streams  
- Scales horizontally  
- Provides low-latency anomaly detection  
- Integrates with alerting systems  

---

## ❓ Who would use this system?

- DevOps Engineers  
- Site Reliability Engineers (SREs)  
- Cloud Infrastructure Teams  
- AI/ML Engineers working on AIOps  

---

## ❓ What makes this project stand out?

- Combines AI + DevOps (rare skill combination)  
- Real-time system design (not batch ML)  
- Production-ready architecture  
- Focus on observability and reliability  

---

## ❓ How does this relate to large-scale AI systems?

Large AI systems (OpenAI, Meta, Netflix) rely heavily on:

- Monitoring pipelines  
- Anomaly detection  
- Infrastructure observability  

LogSight-AI reflects these real-world engineering requirements.

Multi-cluster observability support
