# Architecture

## Overview

LogSight-AI is a lightweight Python package for real-time log parsing and anomaly detection. It is intentionally dependency-light and designed to run without a dedicated ML platform.

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────────────┐
│  Log source  │────▶│  parser module  │────▶│  analyzer module     │
│ (file/stdin) │     │  parse_line()   │     │  detect_anomalies()  │
└──────────────┘     │  parse_file()   │     │  error_rate_spike()  │
                     └─────────────────┘     └──────────────────────┘
                                                         │
                                                         ▼
                                             ┌──────────────────────┐
                                             │  CLI (click + rich)  │
                                             │  logsight analyze    │
                                             │  logsight stdin      │
                                             └──────────────────────┘
```

## Components

### `logsight.parser`

Converts raw log lines into structured `LogEntry` dataclass instances.

- Supports **ISO 8601**, **syslog**, **nginx access log**, and **generic level-prefixed** formats.
- Falls back to a `generic` pattern for unrecognised formats.
- Parses `LogLevel` (DEBUG / INFO / WARNING / ERROR / CRITICAL / UNKNOWN) with alias support (`WARN` → WARNING, `FATAL` → CRITICAL).

### `logsight.analyzer`

Performs statistical analysis on sequences of `LogEntry` objects.

| Function | Description |
|---|---|
| `compute_stats(entries)` | Returns `WindowStats` with counts, error rate, and top messages. |
| `detect_anomalies(entries)` | Z-score anomaly detection on message length; always flags ERROR/CRITICAL. |
| `error_rate_spike(entries)` | Sliding-window scan that reports windows exceeding a configurable error-rate fraction. |

### `logsight.cli`

Click-based CLI exposing two sub-commands:

- `logsight analyze <file>` – reads a file, prints stats and anomalies.
- `logsight stdin` – reads from standard input.

## Anomaly Detection Strategy

The current implementation uses **z-score on message length** as a proxy for "unusual" log entries. This is fast, requires no training data, and works well for detecting stack traces, multi-line exceptions encoded as single lines, or other structurally unusual messages.

Future improvements could include:
- TF-IDF log template extraction (drain algorithm).
- Isolation Forest on multiple features.
- Streaming / incremental analysis for very large log files.
