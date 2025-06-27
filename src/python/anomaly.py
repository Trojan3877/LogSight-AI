"""
anomaly.py
──────────────────────────────────────────────────────────────────────────────
Consumes token-ID sequences from the Collector gRPC stream, maintains an
incremental **HDBSCAN** clustering model + **Isolation Forest** fallback, and
produces anomaly alerts with probability scores.

Design
──────
•  Vectorizer     – converts int tokens → sparse TF-IDF vector
•  HDBSCANWrapper – incremental density clustering (mini-batch)
•  IsoForestWrap  – backups when cluster density is insufficient
•  AnomalyEngine  – orchestrates, exposes .score() + gRPC Push()

Quantifiable targets:
    ▸ ≤ 800 ms end-to-end latency (P95)  
    ▸ < 3 false positives per 10 000 logs
"""

from __future__ import annotations
import os
import time
import grpc
import numpy as np
from collections import deque
from typing import List, Tuple

import hdbscan
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

import logsight_pb2 as pb
import logsight_pb2_grpc as pbg
from prometheus_client import Counter, Summary

# ── Prometheus metrics ──────────────────────────────────────────────────────
ALERT_COUNTER = Counter("alerts_total", "Total anomaly alerts emitted")
SCORE_LATENCY = Summary("score_latency_seconds", "Latency of Engine.score()")


# ── Vectorizer (token IDs -> TF-IDF) ─────────────────────────────────────────
class Vectorizer:
    """Light TF-IDF over hashed tokens."""

    def __init__(self, vocab_size: int = 65_537):
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            token_pattern=r"\S+",
            lowercase=False,
            max_features=vocab_size,
            dtype=np.float32,
        )

        # Fit with dummy tokens so .transform works immediately
        dummy = ["tok0 tok1"]
        self._vectorizer.fit(dummy)

    def transform(self, tokens: List[int]) -> np.ndarray:
        doc = " ".join(f"t{t}" for t in tokens)
        return self._vectorizer.transform([doc]).toarray()[0]


# ── HDBSCAN incremental wrapper ─────────────────────────────────────────────
class HDBSCANWrapper:
    """Mini-batch fit and score using distance to nearest cluster center."""

    def __init__(self, batch_size: int = 512):
        self._batch = batch_size
        self._buf: List[np.ndarray] = []
        self._clusterer: hdbscan.HDBSCAN | None = None

    def partial_fit(self, vec: np.ndarray):
        self._buf.append(vec)
        if len(self._buf) >= self._batch:
            data = np.vstack(self._buf)
            self._clusterer = hdbscan.HDBSCAN(min_cluster_size=8).fit(data)
            self._buf.clear()

    def score(self, vec: np.ndarray) -> float | None:
        if self._clusterer is None:
            return None
        # Distance to nearest cluster center (smaller => normal)
        dists = np.linalg.norm(self._clusterer.cluster_centers_ - vec, axis=1)
        return float(np.min(dists))


# ── IsolationForest fallback ────────────────────────────────────────────────
class IsoForestWrap:
    def __init__(self):
        self._clf = IsolationForest(contamination=0.01, n_estimators=100)
        self._warm = False
        self._buf: deque[np.ndarray] = deque(maxlen=5_000)

    def partial_fit(self, vec: np.ndarray):
        self._buf.append(vec)
        if len(self._buf) == self._buf.maxlen and not self._warm:
            data = np.vstack(self._buf)
            self._clf.fit(data)
            self._warm = True

    def score(self, vec: np.ndarray) -> float | None:
        if not self._warm:
            return None
        # Higher negative score => more anomalous
        return -float(self._clf.score_samples(vec.reshape(1, -1))[0])


# ── AnomalyEngine orchestrator ──────────────────────────────────────────────
class AnomalyEngine(pbg.LogStreamServicer):
    def __init__(self, snowflake_writer):
        self.vectorizer = Vectorizer()
        self.hdb = HDBSCANWrapper()
        self.iso = IsoForestWrap()
        self.snowflake = snowflake_writer  # callable(row: dict)

    @SCORE_LATENCY.time()
    def _process_tokens(self, tokens: List[int], ts_ns: int):
        vec = self.vectorizer.transform(tokens)

        # Online training
        self.hdb.partial_fit(vec)
        self.iso.partial_fit(vec)

        # Score
        hdb_score = self.hdb.score(vec)
        iso_score = self.iso.score(vec)

        # Combine (lower hdb distance = normal; lower iso score = normal)
        if hdb_score is not None and iso_score is not None:
            anomaly_score = (hdb_score * 0.6) + (iso_score * 0.4)
        else:
            anomaly_score = iso_score or (hdb_score or 0.0)

        if anomaly_score > 0.8:  # heuristic threshold
            ALERT_COUNTER.inc()
            self._emit_alert(tokens, anomaly_score, ts_ns)

    def _emit_alert(self, tokens, score, ts_ns):
        row = {
            "ts_ns": ts_ns,
            "score": round(score, 3),
            "token_count": len(tokens),
        }
        self.snowflake(row)

    # ── gRPC entrypoint ─────────────────────────────────────────────────
    async def Push(self, request, context):
        self._process_tokens(list(request.tokens), request.ts)
        return pb.Ack(status=True)


# ── Snowflake writer (placeholder) ──────────────────────────────────────────
def snowflake_writer(row: dict):
    # In prod, use snowflake-connector-python with async pool
    print("❄️  Snowflake row =", row)


# ── gRPC server bootstrap ──────────────────────────────────────────────────
async def serve():
    server = grpc.aio.server()
    pbg.add_LogStreamServicer_to_server(AnomalyEngine(snowflake_writer), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    print(f"🚀 anomaly-engine listening on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve())
