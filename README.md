# LogSight-AI

> AI-powered log analysis and anomaly detection for modern infrastructure.

[![CI](https://github.com/Trojan3877/LogSight-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Trojan3877/LogSight-AI/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

## Overview

**LogSight-AI** ingests raw log streams, parses them into structured entries, and applies statistical anomaly detection to surface errors, unusual patterns, and error-rate spikes—without requiring a dedicated ML infrastructure.

## Features

- **Multi-format parser** – understands ISO 8601, syslog, nginx access logs, and generic level-prefixed lines.
- **Z-score anomaly detection** – flags log entries whose message length deviates significantly from the stream baseline.
- **Error-rate spike detection** – sliding-window analysis that highlights time windows with unusually high error rates.
- **Rich CLI** – colourised terminal output powered by [Rich](https://github.com/Textualize/rich).

## Installation

```bash
# From source
git clone https://github.com/Trojan3877/LogSight-AI.git
cd LogSight-AI
pip install -e .
```

## Usage

### Analyse a log file

```bash
logsight analyze /var/log/app.log
```

### Pipe from stdin

```bash
journalctl -n 1000 | logsight stdin
```

### Options

```
logsight analyze --help

Options:
  -t, --threshold FLOAT      Z-score threshold for anomaly detection.  [default: 2.5]
  -w, --window INTEGER       Window size for error-rate spike detection.  [default: 100]
  -s, --spike-threshold FLOAT  Error-rate fraction that constitutes a spike.  [default: 0.25]
  --no-anomalies             Skip printing individual anomalous entries.
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check logsight tests
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for details on the system design.

## License

MIT
