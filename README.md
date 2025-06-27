# 🔍 LogSight-AI

![Capstone](https://img.shields.io/badge/Project-Capstone-blueviolet?style=for-the-badge)
![Build](https://github.com/Trojan3877/LogSight-AI/actions/workflows/ci.yml/badge.svg?style=for-the-badge)
![Coverage](https://codecov.io/gh/Trojan3877/LogSight-AI/branch/main/graph/badge.svg?style=for-the-badge)
![Dependabot](https://img.shields.io/github/dependabot/updates/Trojan3877/LogSight-AI?style=for-the-badge)
![Container Scan](https://github.com/Trojan3877/LogSight-AI/actions/workflows/container-scan.yml/badge.svg?style=for-the-badge)
![Docs](https://img.shields.io/badge/Docs-GitHub%20Pages-informational?style=for-the-badge)

> **LogSight-AI**¹ ingests high-volume Kubernetes logs, embeds them with a C++ SIMD tokenizer, detects anomalies in real time via Python (HDBSCAN + isolation forest), and streams alerts to Snowflake for long-term forensics.  
> Built for SRE & AIOps teams who need sub-second detection at <0.001 $/1000 logs.

---

## 📂 Repo Structure

LogSight-AI/
├── src/
│ ├── python/
│ │ ├── collector.py # fluent-bit-style tailer → gRPC
│ │ ├── anomaly.py # HDBSCAN clustering + isolation forest
│ │ └── api.py # FastAPI alert endpoint + Prom metrics
│ ├── cpp/
│ │ ├── simd_tokenizer.cpp # ultra-fast log tokenization
│ │ └── libtok.so
├── infra/
│ ├── helm/logsight/
│ ├── ansible/blue_green.yml
│ ├── terraform/eks/
│ └── otel/otel-collector.yaml
├── tests/
│ └── test_anomaly.py
├── Dockerfile
└── docs/
├── flowchart.png
├── openapi.json
└── grafana_dashboard.json


[Flow-Chart](docs/flowchart.png)

1. **Sidecar Collector** tails container logs → gRPC stream  
2. **SIMD Tokenizer** (C++) splits & hashes tokens at &gt;1 GB/s  
3. **Anomaly Engine** (Python) updates HDBSCAN clusters in memory  
4. **Alerts API** exposes `/alerts` + Prometheus `/metrics`  
5. **Snowflake Task** ingests alerts nightly for cost analytics  
6. **Helm + Ansible** provide blue-green rollouts on EKS

---

## 📊 Quantifiable KPIs

| Metric | Target |
|--------|--------|
| **Throughput** | ≥ 50k logs/s per pod |
| **Detection Latency (P95)** | &lt; 800 ms |
| **False-Positive Rate** | &lt; 3 / 10k logs |
| **CPU Utilization** | &lt; 60 % at target throughput |
| **Cost / 1M logs** | &lt; 0.75 USD |

Metrics exported via Prometheus and nightly aggregated in **Snowflake** (`LOGSIGHT.METRICS`).




# LogSight-AI
LogSight-AI is a real-time AIOps platform that ingests Kubernetes logs at > 50 k lines/sec, tokenizes them with a C++ SIMD engine, clusters patterns on-the-fly using HDBSCAN + Isolation Forest
