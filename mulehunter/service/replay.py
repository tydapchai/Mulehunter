import argparse
from datetime import datetime, timedelta, timezone
from uuid import uuid4


SCENARIOS = {
    "normal": [("alice", "shop")],
    "fan_in": [("alice", "hub"), ("bob", "hub"), ("carol", "hub")],
    "fan_out": [("hub", "alice"), ("hub", "bob"), ("hub", "carol")],
    "cycle": [("alice", "bob"), ("bob", "carol"), ("carol", "alice")],
    "high_risk": [("hub", "alice"), ("hub", "bob"), ("hub", "carol")],
    "pass_through": [("alice", "hub"), ("hub", "shop")],
}


def scenario(name):
    prefix = uuid4().hex
    start = datetime.now(timezone.utc)
    amounts = (100000, 50, 4500) if name == "high_risk" else (8500,) * len(SCENARIOS[name])
    return [
        {"transaction_id": f"{prefix}-{i}", "source_account": f"{prefix}:{sender}",
         "target_account": f"{prefix}:{recipient}", "amount": amounts[i], "currency": "VND",
         "timestamp": (start + timedelta(seconds=4 * i)).isoformat()}
        for i, (sender, recipient) in enumerate(SCENARIOS[name])
    ]


def main():
    import json
    import os
    import signal
    import time
    import httpx
    from kafka import KafkaConsumer

    cli = argparse.ArgumentParser()
    cli.add_argument("--consume", action="store_true", required=True)
    cli.parse_args()
    broker = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
    stopping = False

    def stop(_signal, _frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    consumer = KafkaConsumer("transfers", bootstrap_servers=broker, group_id="mulehunter",
                             auto_offset_reset="earliest", enable_auto_commit=False,
                             heartbeat_interval_ms=3000, session_timeout_ms=10000)
    try:
        with httpx.Client(base_url=os.environ.get("SCREEN_URL", "http://localhost:8000"), timeout=10) as api:
            while not stopping:
                batches = consumer.poll(timeout_ms=1000, max_records=1)
                for messages in batches.values():
                    message = messages[0]
                    for attempt in range(5):
                        try:
                            response = api.post("/v1/screen", json=json.loads(message.value))
                            if response.status_code < 500:
                                if response.is_error:
                                    print(response.status_code, response.text, flush=True)
                                consumer.commit()
                                break
                        except httpx.RequestError as exc:
                            print(exc, flush=True)
                        if stopping:
                            break
                        time.sleep(attempt + 1)
                    else:
                        raise RuntimeError("Replay failed repeatedly. Kafka offset retained.")
    finally:
        consumer.close(autocommit=False)


if __name__ == "__main__":
    main()
