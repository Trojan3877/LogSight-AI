"""
collector.py
──────────────────────────────────────────────────────────────────────────────
Tails container log files (or journald) and streams each line to the C++ SIMD
tokenizer via cffi, then forwards the token IDs over gRPC to the Anomaly
Engine. Designed to run as a sidecar in Kubernetes.

Structure
─────────
 • LogTailer        → async generator yielding raw log lines
 • TokenizerBridge  → Python ↔ C++ wrapper (libtok.so)
 • GRPCSender       → async stub to anomaly-engine service
 • main()           → wires components; handles back-pressure

Quantifiable target: ≥ 50 000 lines/s @ ≤ 1 CPU core.

NOTE: gRPC stubs generated from proto (`proto/logsight.proto`) are imported
as `from logsight_pb2_grpc import LogStreamStub` etc.
"""

from __future__ import annotations
import os
import asyncio
import aiofiles
import grpc
import time
from collections import deque
from pathlib import Path
import cffi
import logsight_pb2 as pb
import logsight_pb2_grpc as pbg

# ─────────────────────────── Tokenizer bridge ──────────────────────────────
ffi = cffi.FFI()
lib = ffi.dlopen("src/cpp/libtok.so")

ffi.cdef(
    """
    int tokenize_line(const char* line, int* out_ids, int max_ids);
"""
)

MAX_IDS = 64


class TokenizerBridge:
    __slots__ = ("_buf", "_out")

    def __init__(self):
        self._buf = ffi.new("char[]", 4096)
        self._out = ffi.new("int[]", MAX_IDS)

    def tokenize(self, line: str) -> list[int]:
        encoded = line.encode("utf-8")[:4095]
        self._buf[: len(encoded)] = encoded
        self._buf[len(encoded)] = 0  # NUL-terminate

        n = lib.tokenize_line(self._buf, self._out, MAX_IDS)
        return [self._out[i] for i in range(n)]


# ───────────────────────────── Log tailer ───────────────────────────────────
async def log_tailer(path: Path):
    async with aiofiles.open(path, "r") as f:
        await f.seek(0, os.SEEK_END)  # start at EOF
        while True:
            line = await f.readline()
            if not line:
                await asyncio.sleep(0.05)
                continue
            yield line.strip("\n")


# ───────────────────────────── gRPC sender ─────────────────────────────────
class GRPCSender:
    def __init__(self, target: str = "anomaly-engine:50051"):
        self.target = target
        self.channel: grpc.aio.Channel | None = None
        self.stub: pbg.LogStreamStub | None = None

    async def __aenter__(self):
        self.channel = grpc.aio.insecure_channel(self.target)
        self.stub = pbg.LogStreamStub(self.channel)
        return self

    async def __aexit__(self, *_exc):
        if self.channel:
            await self.channel.close()

    async def send(self, token_ids: list[int]):
        req = pb.LogTokens(tokens=token_ids, ts=int(time.time() * 1e9))
        await self.stub.Push(req, timeout=2.0)


# ───────────────────────────── main pipeline ───────────────────────────────
async def main():
    log_path = Path(os.getenv("LOG_PATH", "/var/log/containers/app.log"))
    tokenizer = TokenizerBridge()
    buffer: deque[list[int]] = deque(maxlen=1000)

    async with GRPCSender() as sender:
        async for line in log_tailer(log_path):
            token_ids = tokenizer.tokenize(line)
            buffer.append(token_ids)

            # simple backpressure: flush in batches of 200 lines
            if len(buffer) >= 200:
                while buffer:
                    await sender.send(buffer.popleft())


if __name__ == "__main__":
    asyncio.run(main())
