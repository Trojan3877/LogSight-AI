"""
Log normalization and parsing.
"""

def parse_log(raw_log: dict) -> dict:
    return {
        "service": raw_log.get("service", "unknown"),
        "severity": raw_log.get("level", "INFO"),
        "content": raw_log.get("message", ""),
        "timestamp": raw_log.get("timestamp")
    }