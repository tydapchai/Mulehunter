import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
import random


def generate(path, count=3000, seed=42):
    rng = random.Random(seed)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["Timestamp", "From Bank", "Account", "To Bank", "Account",
                         "Amount Paid", "Payment Currency", "Is Laundering"])
        for i in range(count):
            group, step = divmod(i, 5)
            suspicious = group % 6 == 0
            source = f"hub-{group}" if suspicious else f"customer-{rng.randrange(700)}"
            target = f"receiver-{group}-{step}" if suspicious else f"merchant-{rng.randrange(700)}"
            if suspicious and group % 12 == 0:
                source, target = target, source
            writer.writerow([(start + timedelta(seconds=i * 4)).isoformat(), "A", source,
                             "B", target, rng.randint(200, 12000), "VND",
                             int(suspicious and step >= 2)])
