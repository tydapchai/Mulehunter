# MULEHUNTER AI — MASTER PROJECT CONTEXT & HANDOFF (`CONTEXT.md`)

> **How to use this file on a new machine:**  
> When opening the `Fintech` workspace on another computer, start a new chat in Antigravity (or any AI coding assistant) and type:  
> **`"Đọc file CONTEXT.md trong thư mục gốc để nắm toàn bộ ngữ cảnh dự án MuleHunter AI (Team TCQL - RMIT Hack-A-Venture 2026) và làm việc tiếp với tôi."`**

---

## 1. Project & Competition Identity

- **Competition:** **RMIT Hack-A-Venture 2026**
- **Official Theme:** *"Open Innovation for a Resilient and Sustainable Financial System in Vietnam"*
- **Team Name:** **`TCQL`**
- **Project Title:** **MuleHunter AI: Real-Time Interbank Graph Intelligence Engine Upgrading Vietnam’s SIMO & Payment Trust Architecture** (*Lõi Trí tuệ Đồ thị Thời gian thực Nâng cấp Hệ thống SIMO & Kiến trúc Niềm tin Thanh toán Quốc gia*)
- **Primary Competition Pillar:** **Pillar 5: Trust Architecture & Financial Integrity** (Benchmarks cited in brief: *Singpass, Visa AI-Powered Fraud Detection*)
- **Intersecting Secondary Pillar:** **Pillar 2: Financial Infrastructure & Ecosystem Interoperability** (Benchmarks cited in brief: *PayNow Singapore, Pix Brazil*)
- **Target UN SDGs:**
  - **SDG 16** (*Peace, Justice and Strong Institutions* — Target 16.4 & 16.a: Disrupting illicit financial flows & organized cybercrime)
  - **SDG 9** (*Industry, Innovation and Infrastructure* — Target 9.1: Upgrading national financial infrastructure SIMO & NAPAS)
  - **SDG 8** (*Decent Work and Economic Growth* — Target 8.10: Protecting retail depositors & MSMEs in cashless economy)

---

## 2. Core Problem Statement & Official RMIT Benchmark Statistics

All proposals and presentations must cite these exact statistics from the official RMIT Hack-A-Venture 2026 *Background & Problem Statement* PDF (`docs_rmit/RMIT_HackAVenture_2026_Background_Problem_Statement.pdf`):

1. **Macro Digital Payment Growth in Vietnam:**
   - By end of 2025: **89% of citizens aged 15 and above own a bank payment account**.
   - At major Vietnamese financial institutions, **>95% of transactions are conducted via digital channels**.
   - In **1H 2026 (first 6 months of 2026)**: Cashless payment transactions reached **>15 billion transactions**, surging **+34.28% YoY** compared to 2025, with total transaction value reaching **28 times GDP** (targeting **30 times GDP by 2030**).
2. **State Bank of Vietnam (SBV) SIMO System Performance & The 67.3% Conversion Gap:**
   - **SIMO** (*Hệ thống thông tin hỗ trợ quản lý, giám sát và phòng ngừa rủi ro gian lận trong hoạt động thanh toán*) launched by SBV issued **4.9 million fraud alerts** by the end of **July 2026**.
   - These alerts prompted **1.6 million customers** to pause/cancel suspicious transfers, preventing **more than VND 5.5 trillion** (`5.500 tỷ đồng`) in potential fraud losses.
   - **Critical Pain Point #1 — The 67.3% Advisory Gap:** Out of 4.9 million alerts, **3.3 million warned transactions (67.3%) still proceeded** because SIMO currently acts only as an *advisory warning pop-up*, and victims under psychological coercion (e.g., deepfake police/prosecutor impersonation scams) are manipulated into clicking "Continue".
   - **Critical Pain Point #2 — Cold-Start Blindness to "Fresh Mules":** SIMO is a reactive static blacklist populated *post-mortem* (after prior victims lose money and report the account). Syndicates bypass SIMO by continuously rotating newly purchased/rented student & worker accounts (**Zero-Day Fresh Mules**) with zero prior blacklist records.
   - **Critical Pain Point #3 — Sub-10-Million VND "High-Velocity Smurfing" (Evading Decision 2345/QD-NHNN):** To evade SBV’s **Decision 2345/QD-NHNN** (which mandates facial liveness biometrics for transfers `>10 million VND/transaction` or `>20 million VND/day`), automated bots split a 150M VND theft into **16 parallel transfers of 9.3M VND** across multiple banks in 30–120 seconds.
   - **Critical Pain Point #4 — Single-Bank Silo Blindness:** Legacy rule-based AML systems (SAS, Oracle Mantas) only see transactions within a single bank and suffer **90%–95% False Positive rates**.

---

## 3. Solution Architecture: How MuleHunter AI ("SIMO 2.0") Works

MuleHunter AI upgrades SBV’s SIMO from a *reactive static blacklist* into a *real-time interbank topological circuit breaker* plugged into the **NAPAS247 / VietQR** payment switch:

### 3.1. Three CoreMoney-Laundering Graph Topologies Detected
1. **Fan-Out (High-Velocity Smurfing `<10M VND`):** 1 victim account rapidly dispersing `<10M VND` transfers across $k$ recipient accounts within seconds.
2. **Fan-In (Aggregation Funnel):** Multiple mule accounts converging funds into a single shell-company account (often before exiting via Crypto P2P / USDT).
3. **Circular Routing / Wash Loops ($A \to B \to C \to A$) & Pass-Through Velocity:** Funds entering and exiting an account within `<60 seconds` with end-of-day balance $\approx 0$.

### 3.2. Two-Tier Hybrid Real-Time Pipeline (End-to-End SLA `< 500ms`)
Inspired by **Ant Group / Alipay’s APAN** (*Asynchronous Propagation Attention Network, ACM SIGMOD 2021*), **Visa AI-Powered Fraud Detection**, and **Singapore’s MAS COSMIC**:
- **Ingestion Layer:** **Apache Kafka** streams real-time transfer events (`tx_id`, `salted_sha256_sender`, `salted_sha256_receiver`, `amount`, `timestamp`, `device_hash`).
- **Tier 1 — Fast Path (`< 50ms`):** **Memgraph (C++ In-Memory Streaming Graph DB)** executes real-time Cypher rules (3-hop cycle check, out-degree spike, pass-through ratio). Clears ~90% of benign retail traffic in `<30ms`.
- **Tier 2 — Deep GNN Path (`< 300ms`):** For transfers flagged by Tier 1 or exhibiting neighborhood anomalies, extracts a localized **2-Hop Ego-Graph** (`O(k^d)` complexity, independent of national graph size $N$) and runs inductive **GraphSAGE** (with **CARE-GNN** camouflage-resistant edge pruning in the roadmap) compiled on **ONNX Runtime**.

### 3.3. Three-Tier Actionable Enforcement Policy (`Mule Risk Score` $\in [0, 1]$)
- **`Score < 0.60` $\to$ `ALLOW`:** Instant settlement (`<30ms`), zero friction for honest users.
- **`Score 0.60 – 0.85` $\to$ `DYNAMIC STEP-UP BIOMETRICS`:** Overrides static 10M VND thresholds on suspicious sub-10M smurfing transfers, forcing immediate **Decision 2345 Facial Liveness + Project 06 (C06/VNeID) identity verification** on the sender's banking app to break scammer psychological coercion.
- **`Score > 0.85` $\to$ `AUTOMATED 15-MINUTE CIRCUIT BREAKER (BLOCK_AND_HOLD)`:** Closes SIMO’s 67.3% advisory gap by temporarily freezing downstream dispersion hops for 15 minutes while pushing an **Explainable Subgraph Alert (XAI)** to bank compliance officers and synchronizing with **SBV SIMO & MPS A05**.

### 3.4. Vietnam Legal & Regulatory Compliance Built-In
- **Decree 13/2023/ND-CP (Personal Data Protection):** Zero raw PII is shared across banks; account numbers & CCCDs are anonymized via **Salted SHA-256 Hashing** at the switch, and cross-bank model training uses **Federated Graph Learning (`Flower / flwr`)** exchanging only encrypted mathematical gradients (`FedAvg`).
- **Circular 64/2024/TT-NHNN (Open APIs):** Standardized Open API hooks between commercial banks, e-wallets, NAPAS, and SIMO.
- **Decision 2345/QD-NHNN & Project 06 (VNeID):** Dynamic biometric step-up triggers.
- **Decree 94/2025/ND-CP (FinTech Regulatory Sandbox):** Target entry framework for Stage 2 SBV Sandbox testing with pilot banks.

---

## 4. Complete Directory & File Map of `d:\Fintech`

### A. RMIT Hack-A-Venture 2026 Round 1 Proposal Documents & Guidelines
| File Path | Description |
| :--- | :--- |
| `TCQL_Round_1_Submission_Updated.docx` | **FINAL English Word Proposal** formatted to match the exact RMIT Guideline PDF style (Orange `#F26522` Headings 1 & 2, Cover Page metadata, `#F26522`/`#FDE8D7` tables, Page footer, includes `1. Introduction` + `2.1–2.8`, strictly **1,954 words < 2,000-word limit**). *Rename to `TCQL_Round_1_Submission.docx` before uploading.* |
| `TCQL_Round_1_Submission_VI_Updated.docx` | **FINAL Vietnamese Word Proposal** with identical RMIT Guideline formatting and full Vietnamese content for both Tech and Non-Tech teammates. |
| `MuleHunter_AI_RMIT_Round1_Proposal_EN.md` | Markdown source of the English Round 1 Proposal (includes `1. Introduction` and `2.1–2.8`). |
| `MuleHunter_AI_RMIT_Round1_Proposal_VI.md` | Markdown source of the Vietnamese Round 1 Proposal (includes `1. Introduction` and `2.1–2.8`). |
| `docs_rmit/generate_docx.py` | Python (`python-docx`) generator script that builds both `.docx` files with exact RMIT styling. Run `python docs_rmit/generate_docx.py` anytime to regenerate the Word files. |
| `docs_rmit/RMIT_HackAVenture_2026_Round1_Guidelines.pdf` | Official RMIT Round 1 Guidelines PDF (scoring rubric, section template, visual formatting reference). |
| `docs_rmit/RMIT_HackAVenture_2026_Background_Problem_Statement.pdf` | Official RMIT Background & Problem Statement PDF (5 Pillars, SIMO stats, Vietnam payment stats, official references). |

### B. Architecture Diagrams & Research Context
| File Path | Description |
| :--- | :--- |
| `MuleHunter_AI_Diagrams_Viewer.html` | **Interactive HTML Viewer** rendering 5 high-resolution Mermaid diagrams (1. End-to-End Architecture & 3-Tier Policy, 2. Real-Time Sequence Diagram, 3. Three Money Laundering Topologies, 4. Federated Graph Learning + Decree 13 Privacy, 5. SIMO 1.0 vs. SIMO 2.0 Funnel). Open in any browser to screenshot for Word/Slides. |
| `MuleHunter_AI_Mermaid_Diagrams.md` | Raw Mermaid.js source code for all 5 proposal diagrams. |
| `MuleHunter_AI_Context_Diagram_Format.drawio` | **System Context Diagram (Level 0 DFD)** in Draw.io format with 10 external entities and 20 non-overlapping parallel In/Out data-flow arrows. |
| `MuleHunter_AI_Context_Diagram.drawio` | Earlier version of the Draw.io System Context Diagram. |
| `CHAT_AML_GRAPH_RESEARCH.md` | Deep-dive academic & industry research notes (Alipay APAN SIGMOD 2021, BRIGHT, CARE-GNN, BIS Project Aurora, TigerGraph, Visa Protect, MAS COSMIC, IBM AML & Elliptic++ datasets). |
| `MULEHUNTER_AI_IMPLEMENTATION_PLAN.md` | Original 4-week technical implementation plan with Cypher queries, PyTorch Geometric code, and FastAPI architecture. |

### C. Working MVP Codebase (Built & Verified Locally)
| Path | Description |
| :--- | :--- |
| `README.md` | Detailed technical guide for running the local MVP, training on IBM AML (`HI-Small_Trans.csv`) or synthetic data, running Kafka/Memgraph via Docker Compose, and viewing benchmark results. |
| `mulehunter/graph.py`, `mulehunter/features.py` | Time-bounded transaction history, Tier-1 fast-path pattern rules (Fan-Out, Fan-In, 3-Hop Cycle, Pass-Through), 2-hop ego-graph extraction, and feature encoding. |
| `mulehunter/training/` | Chronological dataset splitting, Logistic Regression & Rule baselines, 2-layer GraphSAGE training, probability calibration, and ONNX export (`--onnx`). |
| `mulehunter/service/` | FastAPI screening service (`POST /v1/screen`, `GET /v1/decisions/{id}`, `POST /v1/decisions/{id}/verify`, `POST /v1/replay/{scenario}`), Memgraph/SQLite storage adapters, and Kafka producer/consumer. |
| `web/` | Interactive Frontend Dashboard (bundled offline Cytoscape.js graph visualizer, Continuous IBM AML Replay mode, Technical scenario testing, Step-Up verification simulator, and 15-minute hold expiry tracking). |
| `benchmarks/` & `tests/` | Unit & service tests (`python -m unittest discover -s tests -v`), Locust latency benchmark (`benchmarks/latency.py`), Kafka replay smoke checks (`benchmarks/replay_smoke.py`), and continuous replay evaluator (`benchmarks/continuous_replay.py`). |
| `artifacts/` | Trained checkpoints, ONNX models (`artifacts/synthetic/`, `artifacts/ibm-aml/`), continuous replay reports (`artifacts/continuous-replay/report.json`), and latency smoke JSONs. |
| `compose.yaml` & `Dockerfile` | Full containerized stack spinning up Memgraph, Kafka, and the MuleHunter AI FastAPI + Cytoscape web application on `http://127.0.0.1:8000`. |

---

## 5. Useful Commands When Resuming on Another Machine

### 1. Regenerate the RMIT Round 1 Word Proposals (`.docx`)
```powershell
pip install python-docx
python docs_rmit/generate_docx.py
```

### 2. Run the Full MVP Demo with Docker (Memgraph + Kafka + FastAPI + Cytoscape UI)
```powershell
docker compose up --build -d
curl.exe http://127.0.0.1:8000/health
# Then open http://127.0.0.1:8000 in your browser
```

### 3. Run the MVP Lightweight Mode (No Docker required — uses in-memory/SQLite)
```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m uvicorn mulehunter.service.api:create_app --factory --port 8000
```

### 4. Run Unit Tests
```powershell
.venv\Scripts\python -m unittest discover -s tests -v
```
