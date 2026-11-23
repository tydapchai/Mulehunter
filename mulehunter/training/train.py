import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn

from mulehunter.features import encode
from mulehunter.graph import History, inspect
from .dataset import read_events
from .metrics import best_f1_threshold, metrics
from .model import Calibrated, GraphSAGE
from .synthetic import generate
from .splits import write_splits


def export(model, inputs, path):
    torch.onnx.export(model, inputs, path, input_names=["features", "adjacency", "candidate"],
                      output_names=["score"], dynamic_axes={name: {0: "batch"} for name in
                      ("features", "adjacency", "candidate", "score")}, opset_version=17, dynamo=False)
    import onnxruntime as ort
    session = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
    names = ("features", "adjacency", "candidate")
    actual = session.run(None, dict(zip(names, (part.numpy() for part in inputs))))[0]
    np.testing.assert_allclose(actual, model(*inputs).detach().numpy(), rtol=0, atol=1e-4)


def main():
    cli = argparse.ArgumentParser()
    source = cli.add_mutually_exclusive_group(required=True)
    source.add_argument("--csv", type=Path)
    source.add_argument("--synthetic", action="store_true")
    cli.add_argument("--out", type=Path, default=Path("artifacts"))
    cli.add_argument("--limit", type=int, default=20000, help="Maximum CSV rows for the local run")
    cli.add_argument("--stride", type=int, default=1, help="Select every Nth original CSV row")
    cli.add_argument("--epochs", type=int, default=12)
    cli.add_argument("--seed", type=int, default=42)
    cli.add_argument("--onnx", action="store_true")
    args = cli.parse_args()
    if args.stride < 1 or args.limit < 0 or args.epochs < 1:
        cli.error("Use positive stride and epochs, and a nonnegative limit.")
    torch.set_num_threads(2)
    torch.manual_seed(args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.csv
    if args.synthetic:
        path = args.out / "synthetic.csv"
        generate(path, seed=args.seed)
    rows = read_events(path, args.limit, args.stride)
    if len(rows) < 20:
        raise SystemExit("At least 20 rows are required.")
    train_cut, test_cut = [rows[int(len(rows) * ratio)][0].timestamp for ratio in (0.70, 0.85)]
    history = History()
    snapshots = []
    labels = []
    splits = []
    unseen = []
    train_accounts = set()
    counts = []
    for event, label in rows:
        split = 0 if event.timestamp < train_cut else 1 if event.timestamp < test_cut else 2
        accounts = {event.source_account, event.target_account}
        unseen.append(not accounts.issubset(train_accounts))
        if split == 0:
            train_accounts.update(accounts)
        snapshot = inspect(event, history.adjacent)
        snapshots.append(encode(snapshot))
        counts.append(len(snapshot[-1]))
        labels.append(label)
        splits.append(split)
        history.add(event)
    splits = np.asarray(splits)
    masks = [np.flatnonzero(splits == value) for value in range(3)]
    y = torch.tensor(labels, dtype=torch.float32).reshape(-1, 1)
    if any(len(set(y[index, 0].tolist())) != 2 for index in masks):
        raise SystemExit("Each chronological split needs both classes. Increase --limit or choose a different CSV.")
    split_manifest = write_splits(rows, splits, args.out / "splits")
    x, a, c = (torch.from_numpy(np.stack(parts)) for parts in zip(*snapshots))
    del snapshots
    tabular = torch.cat((x[:, 0], x[:, 1], c), dim=1)
    mean = tabular[masks[0]].mean(0)
    scale = tabular[masks[0]].std(0).clamp_min(1e-4)
    tabular = (tabular - mean) / scale
    model = GraphSAGE()
    logistic = nn.Linear(tabular.shape[1], 1)
    optimizer = torch.optim.AdamW([*model.parameters(), *logistic.parameters()], lr=0.003)
    train, val, test = masks
    proportion = y[train].mean()
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=(1 - proportion) / proportion)
    best = -1
    for _ in range(args.epochs):
        for batch in torch.tensor(train)[torch.randperm(len(train))].split(128):
            optimizer.zero_grad()
            loss = loss_fn(model(x[batch], a[batch], c[batch]), y[batch])
            loss += loss_fn(logistic(tabular[batch]), y[batch])
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            scores = model(x[val], a[val], c[val]).flatten().numpy()
        ap = metrics(y[val, 0].numpy().astype(int), scores, scores > 0)["pr_auc_ap"]
        if ap > best:
            best = ap
            weights = {key: value.detach().clone() for key, value in model.state_dict().items()}
    model.load_state_dict(weights)
    model.eval()
    calibration = nn.Linear(1, 1)
    with torch.no_grad():
        calibration.weight.fill_(1)
        calibration.bias.zero_()
        logits = model(x[val], a[val], c[val])
    calibrator = torch.optim.LBFGS(calibration.parameters(), max_iter=50, line_search_fn="strong_wolfe")

    def closure():
        calibrator.zero_grad()
        loss = nn.functional.binary_cross_entropy_with_logits(calibration(logits), y[val])
        loss.backward()
        return loss

    calibrator.step(closure)
    slope = max(0.0, float(calibration.weight.detach().item()))
    intercept = float(calibration.bias.detach().item())
    calibrated = Calibrated(model, slope, intercept).eval()
    with torch.no_grad():
        validation_scores = calibrated(x[val], a[val], c[val]).flatten().numpy()
        scores = calibrated(x[test], a[test], c[test]).flatten().numpy()
        baseline = logistic(tabular[test]).sigmoid().flatten().numpy()
    truth = y[test, 0].numpy().astype(int)
    rules = np.asarray(counts)[test]
    pipeline = np.where(rules > 0, scores, 0)
    budget = int((rules > 0).sum())
    mask = np.asarray(unseen)[test]
    report = {}
    for name, values, alarms in [
        ("rules", rules, rules > 0), ("logistic", baseline, baseline >= .5),
        ("graphsage", scores, scores >= .60), ("pipeline", pipeline, pipeline >= .60),
    ]:
        top = np.zeros(len(test), dtype=bool)
        eligible = np.flatnonzero(rules > 0) if name == "pipeline" else np.arange(len(test))
        top[eligible[np.argsort(-values[eligible], kind="stable")[:budget]]] = True
        report[name] = metrics(truth, values, alarms)
        report[name]["recall_at_rules_budget"] = metrics(truth, values, top)["recall"]
        report[name]["unseen_in_train"] = metrics(truth[mask], values[mask], alarms[mask])
    threshold = best_f1_threshold(y[val, 0].numpy().astype(int), validation_scores)
    report["validation_operating_point"] = {
        "selection": "max_f1_on_validation",
        "threshold": threshold,
        "graphsage_test": metrics(truth, scores, scores >= threshold),
        "pipeline_test": metrics(truth, pipeline, (rules > 0) & (scores >= threshold)),
    }
    report["fast_path_positive_routing_recall"] = float((truth * (rules > 0)).sum() / truth.sum())
    with path.open("rb") as source_file:
        checksum = hashlib.file_digest(source_file, "sha256").hexdigest()
    manifest = {"source": "synthetic" if args.synthetic else path.name, "sha256": checksum,
                "rows": len(rows), "limit": args.limit, "stride": args.stride, "seed": args.seed, "epochs": args.epochs,
                "validation_timestamp": train_cut, "test_timestamp": test_cut,
                "splits": split_manifest, "torch": str(torch.__version__),
                "numpy": np.__version__, "gnn_backend": model.first.__class__.__module__}
    torch.save({"weights": weights, "slope": slope, "intercept": intercept}, args.out / "model.pt")
    for name, content in [("metrics", report), ("manifest", manifest)]:
        (args.out / f"{name}.json").write_text(json.dumps(content, indent=2), encoding="utf-8")
    with (args.out / "metrics.csv").open("w", newline="", encoding="utf-8") as file:
        columns = ["method", "count", "positives", "pr_auc_ap", "roc_auc", "precision",
                   "recall", "alerts_per_1000", "recall_at_rules_budget"]
        writer = csv.DictWriter(file, columns, extrasaction="ignore")
        writer.writeheader()
        for name in ("rules", "logistic", "graphsage", "pipeline"):
            writer.writerow({"method": name, **report[name]})
    if args.onnx:
        export(calibrated, (x[test[:32]], a[test[:32]], c[test[:32]]), args.out / "model.onnx")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
