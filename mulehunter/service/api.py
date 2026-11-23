from dataclasses import asdict
import hashlib
import json
import logging
import math
import os
from pathlib import Path
from threading import Lock
import time
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import AwareDatetime, BaseModel, Field

from mulehunter.features import encode
from mulehunter.graph import Transfer, inspect
from .continuous_replay import router as continuous_replay_router
from .replay import SCENARIOS, scenario
from .store import MemgraphStore, SQLiteStore


class Request(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")
    source_account: str = Field(min_length=1, max_length=128)
    target_account: str = Field(min_length=1, max_length=128)
    amount: float = Field(gt=0, le=1e15, allow_inf_nan=False)
    currency: str = Field(pattern="^[A-Z]{3}$")
    timestamp: AwareDatetime

    def event(self):
        fields = self.model_dump()
        fields["timestamp"] = self.timestamp.timestamp()
        return Transfer(**fields)


class Resolution(BaseModel):
    verified: bool


class Scorer:
    def __init__(self, path):
        self.path = path
        self.session = None
        self.version = hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.is_file() else None

    def load(self):
        import onnxruntime as ort
        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(self.path), sess_options=options,
                                            providers=["CPUExecutionProvider"])
        self.version = hashlib.sha256(self.path.read_bytes()).hexdigest()[:12]

    def __call__(self, snapshot):
        if self.session is None:
            self.load()
        inputs = dict(zip(("features", "adjacency", "candidate"),
                          (part[None] for part in encode(snapshot))))
        score = float(self.session.run(None, inputs)[0][0, 0])
        if not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("Model returned an invalid probability")
        return score


def policy(score):
    if score is None or score < .60:
        return "ALLOW"
    if score <= .85:
        return "STEP_UP"
    return "BLOCK_AND_HOLD"


def create_app(store=None, scorer=None):
    app = FastAPI(title="MuleHunter AI")
    uri = os.getenv("MEMGRAPH_URI")
    store = store or (MemgraphStore(uri) if uri else SQLiteStore(os.getenv("SQLITE_PATH", "demo.db")))
    scorer = scorer or Scorer(Path(os.getenv("MODEL_PATH", "artifacts/synthetic/model.onnx")))
    lock = Lock()
    producer = None

    def run(operation):
        with lock:
            try:
                return store.run(operation)
            except HTTPException:
                raise
            except Exception as exc:
                logging.getLogger(__name__).exception("Screening dependency failed")
                raise HTTPException(503, "Screening dependency unavailable") from exc

    @app.get("/health")
    def health():
        run(lambda tx: tx.get("__health__"))
        return {"status": "ok", "model_version": scorer.version, "graph_store": type(store).__name__}

    @app.post("/v1/screen")
    def screen(request: Request):
        start = time.perf_counter()
        event = request.event()

        def process(tx):
            previous = tx.get(event.transaction_id)
            if previous:
                if previous["event"] != asdict(event):
                    raise HTTPException(409, "Transaction ID already used with different data")
                return previous["result"]
            nodes, edges, _, _, _, hits = snapshot = inspect(
                event, tx.adjacent, fast_only_when_clean=True,
                adjacent_many=getattr(tx, "adjacent_many", None),
            )
            score = scorer(snapshot) if hits else None
            decision = policy(score)
            result = {
                "transaction_id": event.transaction_id, "decision": decision, "risk_score": score,
                "rule_hits": hits, "path": "deep" if hits else "fast",
                "model_version": scorer.version if hits else None,
                "status": {"ALLOW": "SETTLED", "STEP_UP": "PENDING_VERIFICATION",
                           "BLOCK_AND_HOLD": "HELD"}[decision],
                "hold_until": time.time() + 900 if decision == "BLOCK_AND_HOLD" else None,
            }
            if decision == "ALLOW":
                tx.add(event)
            result["latency_ms"] = (time.perf_counter() - start) * 1000
            tx.save(event.transaction_id, {"result": result, "event": asdict(event),
                                          "graph": {"nodes": sorted(set(nodes).union(
                                              endpoint for edge in edges for endpoint in
                                              (edge.source_account, edge.target_account))),
                                              "edges": [asdict(edge) for edge in edges]}})
            return result

        result = run(process)
        return {**result, "latency_ms": (time.perf_counter() - start) * 1000}

    @app.get("/v1/decisions/{identity}")
    def decision(identity: str):
        record = run(lambda tx: tx.get(identity))
        if not record:
            raise HTTPException(404, "Transaction not found")
        result = dict(record["result"])
        if result["status"] == "HELD" and time.time() >= result["hold_until"]:
            result["status"] = "HOLD_EXPIRED"
        return {**result, "event": record["event"], "graph": record["graph"]}

    @app.post("/v1/decisions/{identity}/verify")
    def verify(identity: str, resolution: Resolution):
        def process(tx):
            record = tx.get(identity)
            if not record:
                raise HTTPException(404, "Transaction not found")
            result = record["result"]
            if result["status"] != "PENDING_VERIFICATION":
                raise HTTPException(409, "Transaction is not awaiting verification")
            if resolution.verified:
                event = Transfer(**record["event"])
                tx.add(Transfer(event.transaction_id, event.source_account, event.target_account,
                                event.amount, event.currency, max(event.timestamp, time.time())))
            result["status"] = "SETTLED" if resolution.verified else "REJECTED"
            tx.save(identity, record)
            return result

        return run(process)

    @app.post("/v1/replay/{name}")
    def replay(name: str):
        nonlocal producer
        if name not in SCENARIOS:
            raise HTTPException(404, "Unknown replay")
        events = scenario(name)
        broker = os.getenv("KAFKA_BOOTSTRAP")
        if broker:
            from kafka import KafkaProducer
            try:
                with lock:
                    if producer is None:
                        producer = KafkaProducer(bootstrap_servers=broker, max_block_ms=5000,
                                                 value_serializer=lambda item: json.dumps(item).encode())
                    for item in events:
                        producer.send("transfers", item, key=events[0]["transaction_id"].encode()).get(timeout=8)
            except Exception as exc:
                raise HTTPException(503, "Kafka replay unavailable") from exc
        else:
            for item in events:
                screen(Request.model_validate(item))
        return {"transactions": [event["transaction_id"] for event in events]}

    app.include_router(continuous_replay_router(Path(os.getenv(
        "CONTINUOUS_REPLAY_PATH", "artifacts/continuous-replay",
    ))))
    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[2] / "web", html=True))
    return app
