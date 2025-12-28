"""
Pluggable LLM interface (Claude-compatible).
LLM calls are MOCKED intentionally.
"""

class LLMAnalyzer:
    def summarize(self, logs: list[str]) -> str:
        # MOCKED response – replace with Claude API
        return "Detected repeated authentication failures likely caused by DB outage."

    def root_cause(self, logs: list[str]) -> str:
        return "Probable root cause: downstream database unavailable."