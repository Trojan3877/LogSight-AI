# Contributing to LogSight-AI

We’re thrilled you’d like to help improve real-time log anomaly detection!  
Below is a short guide to get you productive quickly and keep the codebase healthy.

---

## 1 — Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.11 | anomaly engine, FastAPI |
| **GCC / Clang** | ≥ 11 | build SIMD tokenizer |
| **Docker** | 24+ | local container build |
| **Helm** | 3.14 | Kubernetes deploy |
| **pre-commit** | latest | auto style checks |

```bash
# One-time setup
python -m pip install --upgrade pip pre-commit
pre-commit install
