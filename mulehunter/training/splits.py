from dataclasses import asdict
import csv
from datetime import datetime, timezone
import hashlib


def write_splits(rows, assignments, destination):
    destination.mkdir(exist_ok=True)
    columns = ["transaction_id", "source_account", "target_account", "amount",
               "currency", "timestamp", "label"]
    manifest = {}
    for index, name in enumerate(("train", "validation", "test")):
        path = destination / f"{name}.csv"
        selected = [row for row, split in zip(rows, assignments) if split == index]
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, columns)
            writer.writeheader()
            for event, label in selected:
                writer.writerow({**asdict(event), "label": label,
                                 "timestamp": datetime.fromtimestamp(event.timestamp, timezone.utc).isoformat()})
        with path.open("rb") as stream:
            checksum = hashlib.file_digest(stream, "sha256").hexdigest()
        manifest[name] = {"file": f"splits/{path.name}", "rows": len(selected),
                          "positives": sum(label for _, label in selected), "sha256": checksum}
    return manifest
