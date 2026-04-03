# Metrics

## Key Metrics Produced by LogSight-AI

| Metric | Description | Produced by |
|---|---|---|
| `total` | Total number of parsed log entries | `compute_stats()` |
| `error_count` | Number of ERROR + CRITICAL entries | `compute_stats()` |
| `warning_count` | Number of WARNING entries | `compute_stats()` |
| `error_rate` | `error_count / total` | `WindowStats.error_rate` |
| `top_messages` | Top-10 most frequent messages | `compute_stats()` |
| `anomalies` | List of flagged anomalous entries | `detect_anomalies()` |
| `spike_windows` | Indices of windows with high error rate | `error_rate_spike()` |

## Thresholds (Defaults)

| Parameter | Default | Description |
|---|---|---|
| `zscore_threshold` | `2.5` | Entries beyond this many standard deviations are flagged |
| `window_size` | `100` | Number of entries per sliding window |
| `spike_threshold` | `0.25` | Error fraction (25 %) that triggers a spike alert |

## Interpreting Results

- An **error rate ≥ 10 %** is highlighted in red in the CLI output.
- **Anomaly detection** surfaces the top 20 anomalous entries by default; pass `--no-anomalies` to suppress them.
- **Spike detection** is reported by the starting line index of each affected window, making it straightforward to locate the problematic time range.
