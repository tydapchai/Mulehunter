import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

import numpy as np

from mulehunter.graph import History, WINDOW, inspect
from mulehunter.service.api import Scorer, policy
from mulehunter.training.dataset import read_events
from mulehunter.training.metrics import metrics


def run(rows, start, scorer):
    history = History()
    feed, graphs, labels, scores, routed = [], {}, [], [], []
    warmup_count = 0
    for event, label in rows:
        if event.timestamp < start:
            warmup_count += 1
        else:
            snapshot = inspect(event, history.adjacent)
            nodes, edges, _, _, _, hits = snapshot
            score = scorer(snapshot)
            gated = score if hits else None
            record = {"event": asdict(event), "rule_hits": hits,
                      "gated_score": gated, "all_score": score,
                      "gated_decision": policy(gated), "all_decision": policy(score)}
            feed.append(record)
            if hits or policy(score) != "ALLOW":
                graphs[event.transaction_id] = {
                    "nodes": sorted(set(nodes).union(
                        node for edge in edges for node in (edge.source_account, edge.target_account))),
                    "edges": [asdict(edge) for edge in edges],
                }
            labels.append(label)
            scores.append(score)
            routed.append(bool(hits))
        # Historical replay evaluates both policies against the same observed graph.
        history.add(event)
    y = np.asarray(labels, dtype=bool)
    scores, routed = np.asarray(scores), np.asarray(routed)
    summary = {}
    for mode, eligible in (("gated", routed), ("all", np.ones_like(routed))):
        alerts = eligible & (scores >= .60)
        false_alerts = int((alerts & ~y).sum())
        summary[mode] = {
            **metrics(y.astype(int), np.where(eligible, scores, 0), alerts),
            "true_alerts": int((alerts & y).sum()),
            "false_alerts": false_alerts,
            "false_alerts_per_1000": 1000 * false_alerts / len(y) if len(y) else 0,
            "positive_skipped": int((y & ~eligible).sum()),
            "positive_scored_below_threshold": int((y & eligible & ~alerts).sum()),
            "scored": int(eligible.sum()),
        }
    return warmup_count, feed, graphs, summary, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=Path("data/raw/HI-Small_Trans.csv"))
    parser.add_argument("--model", type=Path, default=Path("artifacts/ibm-aml/model.onnx"))
    parser.add_argument("--start", default="2022-09-10T11:00:00+00:00")
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--out", type=Path, default=Path("artifacts/continuous-replay"))
    args = parser.parse_args()
    start = datetime.fromisoformat(args.start)
    if start.utcoffset() is None or start.second or start.microsecond or args.minutes < 1:
        parser.error("Use a timezone-aware start on a minute boundary and positive minutes.")
    start = start.astimezone(timezone.utc)
    end = start + timedelta(minutes=args.minutes)
    warmup = start - timedelta(seconds=WINDOW)
    rows = read_events(args.csv, 0, bounds=(warmup, end))
    if not any(event.timestamp >= start.timestamp() for event, _ in rows):
        parser.error("No transactions in the requested scored interval.")
    scorer = Scorer(args.model)
    warmup_count, feed, graphs, summary, labels = run(rows, start.timestamp(), scorer)
    args.out.mkdir(parents=True, exist_ok=True)
    meta = {"source": args.csv.name, "model_version": scorer.version,
            "warmup_start": warmup.isoformat(), "start": start.isoformat(), "end": end.isoformat(),
            "warmup_count": warmup_count, "count": len(feed), "alert_threshold": .60,
            "graph_context": "observed historical transfers"}
    for name, value in (("report", {**meta, "modes": summary}),
                        ("feed", {"metadata": meta, "events": feed}),
                        ("graphs", graphs)):
        (args.out / f"{name}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2 if name == "report" else None), encoding="utf-8")
    with (args.out / "ground-truth.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["transaction_id", "is_laundering"])
        writer.writerows((item["event"]["transaction_id"], label) for item, label in zip(feed, labels))
    print(json.dumps({**meta, "modes": summary}, indent=2))


if __name__ == "__main__":
    main()
