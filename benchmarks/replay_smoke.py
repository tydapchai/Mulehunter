import argparse
import json
from pathlib import Path
import time

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--out", type=Path, default=Path("artifacts/replay-smoke.json"))
    args = parser.parse_args()
    expected = {
        "normal": ("ALLOW", None), "fan_in": (None, "fan_in"),
        "fan_out": ("STEP_UP", "fan_out"), "cycle": (None, "cycle"),
        "pass_through": (None, "pass_through"), "high_risk": ("BLOCK_AND_HOLD", "fan_out"),
    }
    results = {}
    with httpx.Client(base_url=args.host, timeout=20) as api:
        for scenario, (decision, rule) in expected.items():
            start = time.perf_counter()
            identifiers = api.post(f"/v1/replay/{scenario}").raise_for_status().json()["transactions"]
            records = []
            for identity in identifiers:
                deadline = time.monotonic() + 15
                while True:
                    response = api.get(f"/v1/decisions/{identity}")
                    if response.status_code != 404 or time.monotonic() >= deadline:
                        records.append(response.raise_for_status().json())
                        break
                    time.sleep(.05)
            last = records[-1]
            if decision:
                assert last["decision"] == decision, (scenario, last)
            if rule:
                assert rule in last["rule_hits"], (scenario, last)
            results[scenario] = {
                "decision": last["decision"], "rule_hits": last["rule_hits"],
                "risk_score": last["risk_score"], "model_version": last["model_version"],
                "replay_to_decisions_ms": round((time.perf_counter() - start) * 1000, 2),
            }
            if last["decision"] == "STEP_UP":
                resolution = api.post(f"/v1/decisions/{identifiers[-1]}/verify", json={"verified": True})
                assert resolution.raise_for_status().json()["status"] == "SETTLED"
    args.out.parent.mkdir(exist_ok=True, parents=True)
    args.out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
