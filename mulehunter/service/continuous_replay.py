import json
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query


def router(directory: Path):
    api = APIRouter(prefix="/v1/continuous-replay")

    @lru_cache(maxsize=3)
    def load(name):
        try:
            return json.loads((directory / f"{name}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise HTTPException(503, "Continuous replay artifacts are unavailable. Generate them with benchmarks.continuous_replay.") from exc

    @api.get("/metadata")
    def metadata():
        return load("feed")["metadata"]

    @api.get("/events")
    def events(offset: int = Query(0, ge=0), limit: int = Query(200, ge=1, le=500)):
        return load("feed")["events"][offset:offset + limit]

    @api.get("/graphs/{identity}")
    def graph(identity: str):
        result = load("graphs").get(identity)
        if result is None:
            raise HTTPException(404, "No investigation graph for this transaction")
        return result

    @api.get("/report")
    def report():
        return load("report")

    return api
