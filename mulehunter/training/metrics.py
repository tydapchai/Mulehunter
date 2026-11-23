import numpy as np


def metrics(labels, scores, alarms):
    labels, scores, alarms = map(np.asarray, (labels, scores, alarms))
    size = len(labels)
    positives = labels.sum()
    negatives = size - positives
    order = np.argsort(-scores, kind="stable")
    ends = np.flatnonzero(np.r_[scores[order][1:] != scores[order][:-1], True]) if size else []
    tp = np.cumsum(labels[order])[ends] if size else np.array([])
    fp = np.asarray(ends) + 1 - tp
    precision = tp / np.maximum(tp + fp, 1)
    recall = tp / max(positives, 1)
    hits = labels[alarms].sum()
    return {
        "count": size, "positives": int(positives),
        "pr_auc_ap": float(np.sum(np.diff(np.r_[0, recall]) * precision)) if positives else None,
        "roc_auc": float(np.sum(np.diff(np.r_[0, fp / negatives]) *
                               (np.r_[0, recall][:-1] + recall) / 2)) if positives and negatives else None,
        "precision": float(hits / alarms.sum()) if alarms.any() else 0,
        "recall": float(hits / positives) if positives else None,
        "alerts_per_1000": float(1000 * alarms.mean()) if size else 0,
    }


def best_f1_threshold(labels, scores):
    order = np.argsort(-scores, kind="stable")
    ordered = scores[order]
    ends = np.flatnonzero(np.r_[ordered[1:] != ordered[:-1], True])
    hits = np.cumsum(labels[order])[ends]
    f1 = 2 * hits / (ends + 1 + labels.sum())
    return float(ordered[ends[np.argmax(f1)]])
