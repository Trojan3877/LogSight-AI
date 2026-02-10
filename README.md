# LogSight-AI

**Real-Time AI-Driven Log Intelligence & Incident Reasoning Platform**

LogSight-AI is a high-throughput AIOps and observability platform designed to ingest, process, and analyze large-scale system logs in real time. It combines fast SIMD-based tokenization, unsupervised machine learning, and explainable AI techniques to surface anomalies, cluster recurring patterns, and assist engineers with rapid incident understanding.



 Key Features

* **High-Throughput Log Ingestion**

  * Designed for streaming environments (Kubernetes, distributed systems)
  * Capable of handling tens of thousands of log lines per second

* **Ultra-Fast Tokenization Engine**

  * SIMD-accelerated tokenizer (C++ backend)
  * Optimized for structured and semi-structured log formats

* **Unsupervised Machine Learning**

  * HDBSCAN for log pattern clustering
  * Isolation Forest for anomaly detection
  * Transformer-based embeddings for semantic understanding

* **Explainable Incident Intelligence**

  * Cluster summaries and anomaly scores
  * Human-readable explanations of detected issues

* **Interactive Dashboard**

  * Streamlit-based UI for live monitoring
  * Visual inspection of clusters, anomalies, and trends



System Architecture

```
Log Sources
   │
   ▼
Ingestion Layer (Kafka / Streaming)
   │
   ▼
SIMD Tokenization Engine (C++)
   │
   ▼
Embedding + ML Pipeline (Python)
   │   ├─ HDBSCAN (Clustering)
   │   └─ Isolation Forest (Anomaly Detection)
   ▼
Incident Intelligence Layer
   │
   ▼
Streamlit Dashboard / API
```

---

## 🛠 Tech Stack

| Layer            | Technology                          |
| ---------------- | ----------------------------------- |
| Language         | Python, C++                         |
| Streaming        | Kafka (or mock streaming)           |
| ML               | Scikit-learn, HDBSCAN, Transformers |
| UI               | Streamlit                           |
| Containerization | Docker, Docker Compose              |
| Observability    | Custom metrics + logging            |

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Trojan3877/LogSight-AI.git
cd LogSight-AI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard

```bash
streamlit run ui/streamlit_app.py
```

> Optional: Docker and Kafka-based streaming support can be enabled using the provided Docker configuration.

---

## 📊 Usage Example

1. Stream or load log data into the ingestion layer
2. Logs are tokenized and embedded in real time
3. ML models cluster patterns and detect anomalies
4. Results are visualized in the Streamlit dashboard

**Outputs include:**

* Detected anomaly scores
* Clustered log patterns
* Explainable summaries for incidents

---

## 🧪 Testing

The project supports unit and integration testing using **pytest**.

```bash
pytest tests/
```

Future work includes adding CI-based automated testing and coverage reporting.

---

## 📁 Project Structure

```
LogSight-AI/
├── ingestion/        # Log ingestion and streaming
├── processing/       # Tokenization and preprocessing
├── modeling/         # ML models and embeddings
├── observability/    # Metrics and monitoring utilities
├── ui/               # Streamlit dashboard
├── tests/            # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🗺 Roadmap

* [ ] REST / FastAPI inference endpoint
* [ ] Kubernetes deployment manifests
* [ ] Prometheus & Grafana integration
* [ ] Advanced LLM-based incident explanations
* [ ] CI/CD with GitHub Actions

---

## 🤝 Contributing

Contributions are welcome. Please see `CONTRIBUTING.md` for guidelines on coding standards, testing, and pull requests.

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 👤 Author

**Corey Leath**
AI / ML Engineer | Software Engineer
GitHub: [https://github.com/Trojan3877](https://github.com/Trojan3877)

---

## ⭐ Why This Project Matters

LogSight-AI demonstrates production-oriented skills in:

* Real-time systems
* Machine learning for observability
* Scalable software architecture
* Explainable AI

It is designed as a portfolio-grade project aligned with industry AIOps, SRE, and ML platform engineering roles.
