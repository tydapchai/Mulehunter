# MuleHunter AI

Local MVP that screens a simulated interbank transfer, detects transaction patterns and, when the rules flag it, scores it with a two-layer GraphSAGE model. FastAPI serves the Cytoscape dashboard and the screening API. Memgraph stores the transaction history and decisions. Kafka carries replay events.

## Review the project

| Location | Contents |
| --- | --- |
| `data/raw/` | Original IBM AML CSV. This is a local input and is ignored by Git. |
| `mulehunter/graph.py`, `mulehunter/features.py` | Time-bounded history, pattern rules, two-hop subgraph and shared model input encoding. |
| `mulehunter/training/` | Dataset preparation, chronological split generation, baselines, GraphSAGE, calibration and ONNX export. |
| `mulehunter/service/` | Screening, decisions, storage and Kafka producer/consumer. |
| `web/` | Transfer form, scenarios and graph dashboard. Cytoscape.js and its license are bundled for offline use. |
| `benchmarks/`, `tests/` | Locust load driver, HTTP/Kafka replay checks and service tests. |
| `artifacts/<run>/` | Split CSVs, manifest, model checkpoint, ONNX model and quality metrics for one run. |

Start with a run's `manifest.json`. Inspect row counts, positive counts, timestamps and hashes, then open `splits/train.csv`, `splits/validation.csv` and `splits/test.csv`. Use `metrics.csv` for the comparison and `metrics.json` for subgroup results and the validation-selected operating point. Raw files go under `data/raw/` and generated splits live alongside the run that produced them.

## Run the demo

```powershell
docker compose up --build -d
curl.exe http://127.0.0.1:8000/health
```

Open **http://127.0.0.1:8000**. Run **Normal transfer**, **Fan-out (step-up demo)** and **High-risk fan-out (hold demo)** with the default synthetic checkpoint. Click a row to inspect the graph and use **Simulate pass** or **Simulate failure** to resolve a step-up. The app records a hold expiry 15 minutes after screening. Expiry changes the visible status and leaves settlement to manual review. Kafka replay results appear as each message is processed.

The synthetic model is tuned for the demo scenarios. Use the IBM AML model to inspect its observed behavior in the same stack.

```powershell
$env:MODEL_RUN = 'ibm-aml'
docker compose up --build -d
```

Run a separate stack for load tests using `$env:APP_PORT = '8001'` and `docker compose -p mulehunter-bench up --build -d`. Use one API worker per stack. The in-process transaction lock orders graph reads, policy decisions and writes within that worker.

For a quick run with SQLite and direct replay, install `requirements.txt` and run `python -m uvicorn mulehunter.service.api:create_app --factory`.

## Train and reproduce results

Use Python 3.12 or newer with wheels available for your platform. Run from the project root.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
```

Get `HI-Small_Trans.csv` from the [IBM AML Kaggle dataset](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) and save it in `data/raw/`. When using Kaggle's download API, the single-file endpoint may serve CSV directly.

```powershell
.venv/Scripts/python -m mulehunter.training.train --csv data/raw/HI-Small_Trans.csv --stride 40 --limit 0 --out artifacts/ibm-aml --onnx
.venv/Scripts/python -m mulehunter.training.train --synthetic --out artifacts/synthetic --onnx
.venv/Scripts/python -m unittest discover -s tests -v
```

IBM AML input is sampled every 40th CSV row, then sorted by event time. The split cutoffs approximate 70/15/15 while keeping transactions with the same event timestamp together. Previous events can contribute graph context across split boundaries. Labels never enter graph features. Timestamp ties are excluded from candidate history. The loader treats IBM timestamps without offsets as UTC and maps payment currency names to three-letter codes. The current IBM run also uses the sampled graph, so intervening edges missing from the sample can alter both the rule hits and model input. The report records the **37 positive test transactions** and results should be read at that sample size. Offline history describes transfers in the source data. Live history contains only transfers settled in the demo.

Use `--out artifacts/<new-run>` for experiments so earlier split files and checkpoints remain available for comparison. `--limit 0` means no cap after sampling. Densifying the sample increases the memory footprint of the fixed-size graph tensors.

## Benchmark the application

```powershell
.venv/Scripts/python -m benchmarks.replay_smoke
.venv/Scripts/python -m benchmarks.latency --host http://127.0.0.1:8001
```

The full load profile defaults to 50/100/250 target requests per second, three runs per rate, 60 seconds of warm-up and 300 seconds of measurement per run. The JSON records achieved throughput, HTTP round-trip percentiles by path, errors and the fraction going to the model. Use `--warmup 3 --duration 10 --out artifacts/latency-smoke.json` for a short diagnostic. The replay report separately measures the elapsed time for a submitted Kafka scenario to become visible to the client, including polling.

## API behavior

- `POST /v1/screen` accepts a unique transaction ID, sender, recipient, amount, three-letter currency and timezone-aware timestamp. Reusing an ID with identical data returns the stored decision. A mismatched payload returns HTTP 409.
- `GET /v1/decisions/{id}` returns the decision, status, rules and a graph snapshot. `POST /v1/decisions/{id}/verify` accepts `{"verified": true}` or `false` for a pending step-up.
- `POST /v1/replay/{scenario}` enqueues a predefined scenario. SQLite mode screens those events directly.
- A dependency failure on the screening path returns HTTP 503. Thresholds remain 0.60 and 0.85 for the product demo. The quality report separately records an operating point chosen on validation data.

This MVP uses simulated payment actions. Integrations with bank identity and payment services are pilot work.

## Results from the local implementation

IBM AML used 126,959 chronologically split transactions. The test set contained 19,054 transactions and 37 positive labels.

| Method | ROC-AUC | Average precision | Recall at the rules alert budget |
| --- | ---: | ---: | ---: |
| Rules | 0.489 | 0.00191 | 5.4% |
| Logistic Regression | 0.719 | 0.00346 | 13.5% |
| GraphSAGE | 0.708 | 0.00336 | 5.4% |
| Fast Path plus GraphSAGE | 0.489 | 0.00206 | 5.4% |

Fast Path passed only 2 of 37 positives to the model. At the demo threshold of 0.60, the two-stage pipeline produced zero positive predictions on this test set. The sampled IBM run missed the proposed ROC-AUC target of 0.92. A denser graph benchmark would help quantify the effect of omitted transaction edges on routing recall.

The local smoke benchmark used the default synthetic model, Memgraph, one API worker and approximately 30% Deep Path traffic. Docker reported 16 logical CPUs and about 7.5 GiB of memory. Each rate had three 10-second measurements after a three-second warm-up.

| Target requests/s | Achieved requests/s | HTTP p99 range |
| ---: | ---: | ---: |
| 50 | 49.92–49.99 | 298–545 ms |
| 100 | 53.08–77.67 | 1,535–1,972 ms |
| 250 | 36.80–46.44 | 5,546–6,873 ms |

The graph grew across the nine runs as the service retained decisions and settled transfers. The short runs showed no HTTP errors among completed requests. Across the short runs, p99 exceeded 500 ms. The full five-minute profile remains unverified. See [latency results](artifacts/latency-final-smoke.json) for per-path percentiles and [Kafka restart replay](artifacts/replay-restart-smoke.json) for the scenario outcomes after restarting the consumer.



## Continuous IBM AML replay

The dashboard opens on **Continuous replay**. Select a screening mode and press **Start replay**. Use **Pause**, **Resume replay** or **Reset** to control playback. The investigation queue separates policy alerts from transfers with rule hits. Select a finding to inspect its preceding transfers, then review the two-mode evaluation at the end. The transfer form and isolated pattern scenarios are under **Technical tests**.

The replay is a playback of precomputed scores from the IBM AML ONNX checkpoint, separate from live screening via Kafka and Memgraph. It retains all transactions in the two-hour window. The first hour warms the graph and the second hour is scored. Both modes see the same historical transfers, with timestamps strictly before each candidate. Simulated decisions do not alter that history. The selected interval is an exploratory diagnostic with positive examples, rather than a new independent test set. Labels are used for evaluation and stored separately from the event feed.

```powershell
.venv/Scripts/python -m benchmarks.continuous_replay
docker compose up --build -d
```

| Mode | Scored | Positive skipped by Fast Path | Positive scored below 0.60 | Policy alerts |
| --- | ---: | ---: | ---: | ---: |
| Fast Path then GraphSAGE | 1,327 | 30 | 5 | 0 |
| GraphSAGE scores all | 8,071 | 0 | 35 | 0 |

The run warmed up on 8,213 transfers and evaluated 8,071 transfers, including 35 positive labels. See [continuous replay report](artifacts/continuous-replay/report.json).
