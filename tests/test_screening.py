import asyncio
from datetime import datetime, timedelta, timezone
import logging
import unittest

import httpx

from mulehunter.service.api import create_app, policy
from mulehunter.service.replay import scenario
from mulehunter.service.store import SQLiteStore


class FixedScorer:
    version = "test-model"

    def __init__(self, score):
        self.score = score

    def __call__(self, snapshot):
        if self.score is None:
            raise RuntimeError("simulated failure")
        return self.score


class ScreeningTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.scorer = FixedScorer(.60)
        self.store = SQLiteStore(":memory:")
        app = create_app(self.store, self.scorer)
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://local")
        self.addAsyncCleanup(self.client.aclose)
        self.addCleanup(self.store.db.close)

    async def send(self, event, status=200):
        response = await self.client.post("/v1/screen", json=event)
        self.assertEqual(response.status_code, status, response.text)
        return response.json()

    async def test_thresholds(self):
        for score, decision in ((None, "ALLOW"), (.599, "ALLOW"), (.60, "STEP_UP"),
                                (.85, "STEP_UP"), (.85001, "BLOCK_AND_HOLD")):
            self.assertEqual(policy(score), decision)

    async def test_patterns(self):
        self.scorer.score = .1
        for pattern in ("fan_in", "fan_out", "cycle", "pass_through"):
            for event in scenario(pattern):
                last = await self.send(event)
            self.assertIn(pattern, last["rule_hits"])

    async def test_step_up_and_idempotency(self):
        events = scenario("fan_in")
        for event in events:
            result = await self.send(event)
        identity = result["transaction_id"]
        self.assertEqual(result["decision"], "STEP_UP")
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM transfers").fetchone()[0], 2)
        resolved = await self.client.post(f"/v1/decisions/{identity}/verify", json={"verified": True})
        self.assertEqual(resolved.json()["status"], "SETTLED")
        retries = await asyncio.gather(*(self.send(events[-1]) for _ in range(3)))
        self.assertTrue(all(item["status"] == "SETTLED" for item in retries))
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM transfers").fetchone()[0], 3)
        await self.send({**events[-1], "amount": 4321}, status=409)

    async def test_hold_and_dependency_failure(self):
        self.scorer.score = None
        events = scenario("fan_out")
        for event in events[:-1]:
            await self.send(event)
        with self.assertLogs("mulehunter.service.api", level=logging.ERROR):
            await self.send(events[-1], status=503)
        self.assertIsNone(self.store.get(events[-1]["transaction_id"]))
        self.scorer.score = .95
        final = await self.send(events[-1])
        self.assertEqual(final["status"], "HELD")
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM transfers").fetchone()[0], 2)

    async def test_no_future_history(self):
        events = scenario("fan_out")
        for event in events[:2]:
            await self.send(event)
        earlier = datetime.fromisoformat(events[0]["timestamp"]) - timedelta(seconds=1)
        last = await self.send({**events[-1], "timestamp": earlier.astimezone(timezone.utc).isoformat()})
        self.assertEqual(last["path"], "fast")


if __name__ == "__main__":
    unittest.main()
