"""
Simple clustering placeholder for incident grouping.
"""

from collections import defaultdict

def cluster_logs(logs):
    clusters = defaultdict(list)
    for log in logs:
        clusters[log["service"]].append(log)
    return clusters