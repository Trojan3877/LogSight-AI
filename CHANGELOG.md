# Changelog
All notable changes to **LogSight-AI** will be documented in this file.  
This project follows **Semantic Versioning 2.0.0** and the  
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) specification.

---

## [Unreleased]
### Added
- OpenAPI spec, community templates, and nightly load-test workflow.
- Documentation site auto-deploy via MkDocs + Mike.
- Grafana dashboard screenshot in `docs/`.
### Changed
- (placeholder – populate with upcoming edits)

---

## [0.1.0] – 2025-07-03
### Added
- C++ SIMD tokenizer (`simd_tokenizer.cpp`, `libtok.so`).
- Python modules: `collector.py`, `anomaly.py`, `api.py`.
- gRPC proto (`proto/logsight.proto`) + generated stubs.
- Unit & integration tests with coverage upload to Codecov.
- Multi-stage Dockerfile; GHCR publish workflow with Cosign signatures.
- Trivy container-scan workflow + SPDX SBOM artifact.
- Helm chart: `values.yaml`, deployment, service, HPA, chart metadata.
- Ansible blue-green playbook with secret rotation.
- OTEL collector manifest for traces.
- Prometheus metrics & Grafana dashboard JSON.
- Makefile, pre-commit hooks, `.dockerignore`, `requirements.txt`.
- Professional README with badges, KPIs, and architecture visual.

[Unreleased]: https://github.com/Trojan3877/LogSight-AI/compare/v0.1.0...HEAD  
[0.1.0]: https://github.com/Trojan3877/LogSight-AI/releases/tag/v0.1.0
