# ⚡ LogSight-AI: Real-Time Intelligent Log Analytics Engine

[![C++](https://img.shields.io/badge/Language-C%2B%2B17-blue?logo=cplusplus&logoColor=white&style=flat-square)](https://github.com/Trojan3877/LogSight-AI)
[![Python](https://img.shields.io/badge/Language-Python%203.10-3776AB?logo=python&logoColor=white&style=flat-square)](https://github.com/Trojan3877/LogSight-AI)
[![Docker Engine](https://img.shields.io/badge/Container-Docker%20Compose-2496ED?logo=docker&logoColor=white&style=flat-square)](https://github.com/Trojan3877/LogSight-AI)
[![Streamlit UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat-square)](https://github.com/Trojan3877/LogSight-AI)
[![License-MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)

LogSight-AI is a high-throughput AIOps log parsing and anomaly detection engine designed to monitor massive distributed applications, like Kubernetes clusters, with minimal latency. 

By marrying lower-level **C++ SIMD-accelerated tokenization** with high-level **Machine Learning clustering models (HDBSCAN & Isolation Forests)**, the system processes live infrastructure streams, structures raw text data on the fly, and flags structural and frequency variations in real-time.



System Architecture

LogSight-AI operates as an asynchronous multi-stage computing pipeline designed to handle extreme burst traffic without dropping telemetry contexts:

[ Kube Log Stream ]
│
▼
[ Ingestion Layer ] ──► (FastAPI Multi-Threaded Workers)
│
▼
[ Parsing Core ]    ──► (C++ Native Extension via SIMD Vectorization)
│
▼
[ Analytics Block ] ──► (HDBSCAN Density Clustering + Isolation Forest)
│
▼
[ Visualizer UI ]   ──► (Streamlit Analytics Dashboard @ Port 8501)


### Key Performance Specifications
* **Tokenization Throughput:** Scalable parsing capabilities handling up to **50,000+ lines/sec**.
* **Engine Core:** Native C++ integration compiled directly into Python bindings for optimal resource overhead mitigation.
* **AIOps Capability:** Dynamic profiling. The model isolates system abnormalities without requiring hardcoded, fragile regular expression parsing rule suites.

---

## 🚀 Sandbox Demo Environment

The project features a containerized local testing framework. This setup provisions a synthetic multi-component microservice log stream injector, the processing server cluster, and a frontend diagnostic interface simultaneously.

### Prerequisites
* Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine.

### Local Execution Instructions

1. **Clone the Infrastructure Repository:**
   ```bash
   git clone [https://github.com/Trojan3877/LogSight-AI.git](https://github.com/Trojan3877/LogSight-AI.git)
   cd LogSight-AI

2. Boot the Container Orchestration Stack:

Explore System Telemetry Interfaces:
​Streamlit Monitoring Interface: Open your web browser to http://localhost:8501 to view your real-time processing graphs and system anomaly flags.
​Inbound Traffic Port: The internal FastAPI backend runs active data socket listeners via http://localhost:8000.
Component Breakdown
​app_demo.py: Streamlit engine providing continuous, real-time analytics, monitoring processing speeds and emitting alarms during high-density structural code errors.
​log_simulator.py: A programmatic load injector simulating common microservices (auth-service, payment-gateway, etc.). It automatically creates synthetic fault variations every 15 seconds to evaluate pipeline accuracy.
​docker-compose.yml: Isolation network wrapping the system blocks cleanly into portable, easily auditable microservice segments.

Why use machine learning for logs instead of rules?

Rule-based systems:
- Break in dynamic environments  
- Require constant manual updates  

ML-based systems:
- Adapt to changing system behavior  
- Detect unknown patterns  
- Reduce human intervention  

 What type of machine learning is used?

The system focuses on:

- Time-series anomaly detection  
- Unsupervised / semi-supervised learning  
- Pattern recognition in log sequences  

Future improvements may include:
- Transformer-based anomaly detection  
- LSTM-based sequence modeling  

How is real-time performance handled?

- Streaming ingestion minimizes latency  
- Lightweight feature extraction ensures fast processing  
- Model inference is optimized for low-latency execution  
- Containerized deployment allows horizontal scaling  

How does the system scale?

LogSight-AI is designed with scalability in mind:

- Docker for containerization  
- Kubernetes for orchestration  
- Stateless services for horizontal scaling  
- Monitoring via Prometheus + Grafana  

How are anomalies defined?

Anomalies are deviations from learned normal behavior, such as:

- Sudden spikes in error logs  
- Unusual frequency patterns  
- Unexpected log sequences  
- Rare or unseen events  

What are the main engineering challenges?

- Handling high-volume log streams  
- Designing low-latency pipelines  
- Avoiding false positives in anomaly detection  
- Maintaining model performance over time  
- Ensuring system scalability  

How would you improve this system?

Planned enhancements include:

- LLM-based log summarization  
- Root cause analysis using AI agents  
- Kafka-based distributed streaming  
- Transformer-based anomaly detection  
- Multi-region observability  

How does this compare to industry tools?

LogSight-AI aligns with systems like:

- Datadog  
- Splunk  
- Elastic Observability  

However, it differentiates itself by:
- Integrating ML directly into the pipeline  
- Supporting real-time inference  
- Being fully customizable and extensible  

What did you learn from building this?

- Designing real-time ML systems  
- Building scalable data pipelines  
- Applying ML to infrastructure problems  
- Understanding observability engineering  
- Bridging DevOps and AI (AIOps)  

Why is this project important for AI engineering?

This project demonstrates:

- End-to-end ML system design  
- Real-time inference pipelines  
- Production-ready architecture  
- Practical application of AI to real-world systems  

How would this perform in production?

With proper deployment (Kubernetes + monitoring):

- Handles high-volume log streams  
- Scales horizontally  
- Provides low-latency anomaly detection  
- Integrates with alerting systems  

Who would use this system?

- DevOps Engineers  
- Site Reliability Engineers (SREs)  
- Cloud Infrastructure Teams  
- AI/ML Engineers working on AIOps  

What makes this project stand out?

- Combines AI + DevOps (rare skill combination)  
- Real-time system design (not batch ML)  
- Production-ready architecture  
- Focus on observability and reliability  

How does this relate to large-scale AI systems?

Large AI systems (OpenAI, Meta, Netflix) rely heavily on:

- Monitoring pipelines  
- Anomaly detection  
- Infrastructure observability  

LogSight-AI reflects these real-world engineering requirements.

Multi-cluster observability support
