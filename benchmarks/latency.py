import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json
import platform
import time
from pathlib import Path
from uuid import uuid4

import gevent
from locust import FastHttpUser, constant_pacing, task
from locust.env import Environment
import numpy as np


class ScreeningUser(FastHttpUser):
    wait_time = constant_pacing(1)

    def on_start(self):
        benchmark = self.environment.benchmark
        slot = benchmark["user_slot"]
        benchmark["user_slot"] += 1
        gevent.sleep(slot / benchmark["rate"])

    @task
    def screen(self):
        benchmark = self.environment.benchmark
        sequence = benchmark["sequence"]
        benchmark["sequence"] += 1
        name = f"{benchmark['prefix']}:{sequence}"
        group, step = divmod(sequence, 10)
        deep = step in (7, 8, 9)
        # A unique simple candidate, or a candidate sharing a pre-seeded sender.
        sender = f"{benchmark['prefix']}:seed:{group % 128}" if deep else name + ":a"
        event = {"transaction_id": name, "source_account": sender, "target_account": name + ":b",
                 "amount": 8500, "currency": "VND", "timestamp": datetime.now(timezone.utc).isoformat()}
        start = time.perf_counter()
        with self.client.post("/v1/screen", json=event, catch_response=True) as response:
            elapsed = (time.perf_counter() - start) * 1000
            if response.status_code == 200:
                try:
                    path = response.json()["path"]
                except (ValueError, KeyError):
                    response.failure("Response missing screening path")
                    path = "error"
            else:
                path = "error"
            if benchmark["collect"]:
                benchmark["samples"][path].append(elapsed)


def seed(host, prefix):
    import requests
    now = datetime.now(timezone.utc) - timedelta(minutes=1)
    with requests.Session() as client:
        for group in range(128):
            for i in range(2):
                sender = f"{prefix}:seed:{group}"
                payload = {"transaction_id": f"{sender}:{i}", "source_account": sender,
                           "target_account": f"{sender}:target:{i}", "amount": 8500,
                           "currency": "VND", "timestamp": (now + timedelta(seconds=i)).isoformat()}
                client.post(host + "/v1/screen", json=payload, timeout=10).raise_for_status()


def summarize(samples):
    return {"count": len(samples), **{
        f"p{percentile}_ms": round(float(np.percentile(samples, percentile)), 3) if samples else None
        for percentile in (50, 95, 99)
    }}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--rates", type=int, nargs="+", default=[50, 100, 250])
    parser.add_argument("--warmup", type=int, default=60)
    parser.add_argument("--duration", type=int, default=300)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", type=Path, default=Path("artifacts/latency.json"))
    parser.add_argument("--stack", default="compose-memgraph")
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    import requests
    health = requests.get(args.host + "/health", timeout=10)
    health.raise_for_status()
    runs = []
    for rate in args.rates:
        for repeat in range(1, args.repeats + 1):
            prefix = uuid4().hex[:12]
            seed(args.host, prefix)
            env = Environment(user_classes=[ScreeningUser], host=args.host)
            env.benchmark = {"sequence": 0, "user_slot": 0, "rate": rate, "prefix": prefix, "samples": defaultdict(list), "collect": False}
            runner = env.create_local_runner()
            runner.start(rate, spawn_rate=rate)
            gevent.sleep(args.warmup)
            env.benchmark["collect"] = True
            start = time.monotonic()
            gevent.sleep(args.duration)
            duration = time.monotonic() - start
            env.benchmark["collect"] = False
            runner.quit()
            samples = env.benchmark["samples"]
            good = samples["fast"] + samples["deep"]
            total = len(good) + len(samples["error"])
            run = {"target_rps": rate, "repeat": repeat, "duration_s": duration,
                   "achieved_rps": total / duration, "error_fraction": len(samples["error"]) / max(total, 1),
                   "seed_settled_edges": 256, "deep_fraction": len(samples["deep"]) / max(len(good), 1),
                   "all_successful": summarize(good), "fast": summarize(samples["fast"]),
                   "deep": summarize(samples["deep"])}
            runs.append(run)
            report = {"stack": args.stack, "host_platform": platform.platform(),
                      "processor": platform.processor(), "warmup_s": args.warmup,
                      "health": health.json(), "runs": runs}
            args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(json.dumps(run), flush=True)


if __name__ == "__main__":
    main()
