<!-- Core Tech -->
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Kafka](https://img.shields.io/badge/Kafka-Event%20Streaming-black?logo=apachekafka)
![Transformer](https://img.shields.io/badge/AI-Transformer--Based-purple)
![LLM](https://img.shields.io/badge/LLM-Claude--Compatible-orange)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-lightblue?logo=mlflow)
![Prometheus](https://img.shields.io/badge/Observability-Prometheus-red?logo=prometheus)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)
![n8n](https://img.shields.io/badge/Automation-n8n-EA4B71?logo=n8n)
![License](https://img.shields.io/badge/License-MIT-green)

<!-- Architecture -->
![Event Driven](https://img.shields.io/badge/Architecture-Event--Driven-blueviolet)
![Human in the Loop](https://img.shields.io/badge/Design-Human--in--the--Loop-success)
![Observability First](https://img.shields.io/badge/Focus-Observability--First-critical)
![Stars](https://img.shields.io/github/stars/Trojan3877/LogSight-AI?style=flat)
![Forks](https://img.shields.io/github/forks/Trojan3877/LogSight-AI?style=flat)
![Issues](https://img.shields.io/github/issues/Trojan3877/LogSight-AI)
<!-- Portfolio Signal -->
![L7 Quality](https://img.shields.io/badge/Engineering-L7--Quality-informational)
![OpenAI Aligned](https://img.shields.io/badge/Aligned-OpenAI--Residency-black)
LogSight-AI
Transformer-Based Log Intelligence & Incident Reasoning System
🧠 Overview
LogSight-AI is a scalable, event-driven system that transforms high-volume system logs into actionable, explainable incident intelligence. Instead of treating logs as raw text, the system applies transformer-based embeddings and constrained LLM reasoning to surface summaries, incident clusters, and root-cause hypotheses—while preserving observability, traceability, and human oversight.
This project focuses on judgment, system design, and reliability, not just model output.
🎯 System Goals
Reduce cognitive load from noisy logs
Surface meaning, not just alerts
Support human-in-the-loop decision-making
Maintain transparency and observability
Constrain LLM behavior intentionally

flowchart LR
    A[Log Sources] --> B[Kafka]
    B --> C[Log Processing]
    C --> D[Transformer Embeddings]
    D --> E[LLM Reasoning<br/>Claude-Compatible]
    E --> F[Incident Intelligence]
    F --> G[Streamlit Dashboard]
    E --> H[MLflow]
    E --> I[Prometheus]
    G --> J[n8n Workflows]

🔌 Core Components
Event Streaming
Kafka (Docker) for real-time log ingestion
Decouples producers from downstream analysis
Semantic Processing
Transformer-based embeddings for log representation
Enables clustering and semantic similarity
LLM Reasoning Layer
Pluggable Claude-compatible interface
Used for:
Log summarization
Incident explanation
Root-cause hypotheses
Explicitly constrained and partially mocked for clarity and safety
Observability & Evaluation
Prometheus for latency, throughput, and error metrics
MLflow for prompt versions, experiments, and evaluation tracking
Human Interface
Streamlit dashboard for live summaries and confidence display
n8n workflows for alerts and escalations
⚡ Quickstart
This quickstart runs LogSight-AI locally using Docker for Kafka and Python 3.11 for all services.
LLM reasoning is Claude-compatible and mocked by default for clarity and safety.
1️⃣ Prerequisites
Make sure you have the following installed:
Python 3.11
Docker & Docker Compose
Git
Verify versions:

Bash
python --version
docker --version
docker compose version
2️⃣ Clone the Repository

Bash
git clone https://github.com/Trojan3877/LogSight-AI.git
cd LogSight-AI
3️⃣ Start Kafka (Docker)
This launches Kafka and Zookeeper locally.

Bash
docker compose up -d
Confirm Kafka is running:

Bash
docker ps
You should see kafka and zookeeper containers.
4️⃣ Set Up Python Environment
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
Install dependencies:

Bash
pip install -r requirements.txt
5️⃣ Start Streaming Logs
In one terminal, run the Kafka log producer:

Bash
python ingestion/kafka_producer.py
This simulates application logs being streamed into Kafka.
6️⃣ Launch the Streamlit Dashboard
In a second terminal:

Bash
streamlit run ui/streamlit_app.py
Open your browser to:
C

http://localhost:8501
You should see:
Incident summary
Root-cause hypothesis
Confidence indicator






<div style="position: relative; padding-bottom: 62.5%; height: 0;"><iframe src="https://www.loom.com/embed/6e2b46fdb34749f494e851267bab3ba7" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>











Design Questions & Reflections
Q: Why use LLMs for log analysis at all?
A: Logs often encode context and intent that rule-based systems miss. LLMs help summarize and reason over patterns, but only when constrained and observable.
Q: Why not fully automate incident response?
A: Automation without understanding is risky. This system prioritizes decision support over autonomous action.
Q: What are the main trade-offs?
A: Depth of reasoning versus latency, and flexibility versus predictability. The system favors clarity and trust over maximal automation.
Q: Where does this system still fall short?
A: LLM reasoning can still be brittle. That’s why outputs are treated as hypotheses, not truth.
🚧 Limitations
LLM outputs are non-deterministic
Some components are mocked for scope clarity
Not production-hardened for untrusted inputs
🔮 Future Improvements
Uncertainty-aware outputs
Automated prompt evaluation suites
Multi-model reasoning comparison
Live retraining with feedback loops

