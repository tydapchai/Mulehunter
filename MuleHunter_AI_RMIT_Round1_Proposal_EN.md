# RMIT HACK-A-VENTURE 2026 — ROUND 1 IDEA PROPOSAL

**Competition Theme:** *Open Innovation for a Resilient and Sustainable Financial System in Vietnam*  
**Project Title:** **MuleHunter AI: Real-Time Interbank Graph Intelligence Engine Upgrading Vietnam’s SIMO & Payment Trust Architecture**  
**Primary Pillar:** **Pillar 5: Trust Architecture & Financial Integrity**  
**Intersecting Pillar:** **Pillar 2: Financial Infrastructure & Ecosystem Interoperability**  
**Target SDGs:** SDG 16 (Peace, Justice and Strong Institutions), SDG 9 (Industry, Innovation and Infrastructure), SDG 8 (Decent Work and Economic Growth)

---

## 1. Introduction

Submitted by **Team TCQL** for **RMIT Hack-A-Venture 2026** under the theme *"Open Innovation for a Resilient and Sustainable Financial System in Vietnam"*, this proposal introduces **MuleHunter AI**—a real-time interbank Graph Neural Network (GNN) intelligence engine designed to upgrade the State Bank of Vietnam’s (SBV) **SIMO** fraud-monitoring platform into an automated topological circuit breaker (**"SIMO 2.0"**). Positioned at the intersection of **Pillar 5: Trust Architecture & Financial Integrity** (Primary) and **Pillar 2: Financial Infrastructure & Ecosystem Interoperability** (Secondary), this document presents our comprehensive Round 1 Idea Proposal across six core areas: Executive Summary, Problem Statement & Market Pain, Solution Architecture & FinTech Integration, Market Size & Competitive Analysis, Strategic Contribution & Expected Impact, and Implementation Roadmap & Scalability.

---

## 2. Proposal Structure

### 2.1. Executive Summary

By mid-2026, Vietnam’s digital financial transformation reached a historic milestone: nearly **89% of citizens aged 15+ own a payment account**, over **95% of banking transactions occur digitally**, and cashless payments surged **34.28% YoY to exceed 15 billion transactions in 1H 2026** (reaching 28 times GDP). However, hyper-connected instant payment rails (NAPAS247, VietQR) have simultaneously exposed the ecosystem to industrial-scale cyber fraud. While the State Bank of Vietnam (SBV) introduced the **SIMO (Information System for Supporting Management, Monitoring and Prevention of Payment Fraud Risks)**—which issued **4.9 million alerts** and prevented **VND 5.5 trillion** in losses across **1.6 million transactions** by July 2026—official data reveals a critical vulnerability: **over 3.3 million alerts (67.3%) failed to stop transfers**, and static blacklists remain blind to unreported "fresh mule" accounts and automated sub-10-million-VND "smurfing" rings.

Aligning with **Pillar 5 (Trust Architecture & Financial Integrity)** and **Pillar 2 (Financial Infrastructure & Ecosystem Interoperability)**, we propose **MuleHunter AI**—a real-time interbank Graph Neural Network (GNN) intelligence layer that upgrades SIMO from a *reactive static blacklist* into a *proactive topological circuit breaker*. Combining **In-Memory Streaming Graphs (Memgraph)** with decoupled **GraphSAGE/APAN** inference, MuleHunter AI detects multi-hop laundering topologies (**Fan-out, Fan-in, Circular Routing**) across banks in **under 500 milliseconds**. Leveraging **Open APIs (Circular 64/2024/TT-NHNN)**, **VNeID/Project 06 identity verification**, and **Federated Graph Learning** (preserving privacy under **Decree 13/2023/ND-CP**), MuleHunter AI dynamically triggers step-up facial biometrics or freezes illicit dispersion in real time—reinforcing institutional trust and protecting trillions of VND across Vietnam’s financial system.

---

## 2.2. Problem Statement & Market Pain

### Specific Problem & Urgency in Vietnam’s Financial System
As Vietnam targets a cashless payment value of **30 times GDP by 2030** (Vietnam+, 2026), instant settlement rails have become the primary conduit for transnational cyber-fraud syndicates to launder stolen funds through networks of **Money Mule accounts** (rented, purchased, or shell-company accounts). Once a victim authorizes a transfer, syndicates disperse funds across 3–4 banking hops within **30 to 120 seconds**, converting proceeds into cryptocurrency (USDT P2P) before banks or police can intervene.

### Root Causes, Affected Groups & Limitations of Existing Solutions
1. **The 67.3% "Advisory Conversion Gap" in SBV’s Current SIMO System:** By July 2026, SIMO generated **4.9 million fraud alerts**, yet only **1.6 million prompted customers to cancel transactions** (Nguoi Quan Sat, 2026; VietNamNet, 2026b). Because SIMO operates as an *advisory warning pop-up*, **3.3 million warned transactions still proceeded**—largely because victims under psychological manipulation (e.g., deepfake police impersonation scams) are coerced into ignoring warnings.
2. **Reactive "Cold-Start" Blindness to Fresh Mules:** SIMO relies on post-mortem reporting: an account is blacklisted only *after* prior victims suffer losses and file complaints. Criminal rings bypass SIMO by continuously rotating newly opened worker/student accounts ("fresh mules") that have zero negative history in SIMO.
3. **Sub-10-Million VND "High-Velocity Smurfing" (Evading Decision 2345):** To bypass SBV’s **Decision 2345/QD-NHNN** (requiring facial biometrics for transfers $>10$ million VND per transaction or $>20$ million VND daily), syndicates use automated bots to split a 150-million-VND theft into **16 parallel transfers of 9.3 million VND** across multiple banks, flying completely under biometric radar.
4. **Fragmented Single-Bank Visibility (Pillar 2 Gap):** Legacy bank AML systems (Oracle Mantas, SAS) inspect isolated transactions within a single bank’s silo. Bank A cannot see that funds sent to Bank B were immediately fractured across 10 accounts at Bank C and D.

| Dimension | Legacy Bank AML (Siloed Rules) | Current SBV SIMO System (1.0) | Critical Unsolved Market Pain |
| :--- | :--- | :--- | :--- |
| **Core Mechanism** | Single-bank tabular rules | Centralized static blacklist lookup | Blind to multi-bank network topologies |
| **Fresh Mule Detection** | Fails (No prior bad record) | Fails (Not yet reported by victims) | Zero-day mules launder money undetected |
| **Enforcement Action** | Post-event batch review | Advisory pop-up (**67.3% ignored**) | Manipulated victims still complete transfers |
| **False Positive Rate** | 90% – 95% (Rule fatigue) | High False Negatives on new accounts | Severe compliance bottleneck & user friction |

---

## 2.3. Solution Architecture & FinTech Integration

### Proposed Solution & Core Features
Inspired by global benchmarks cited in Pillar 5 and Pillar 2—specifically **Visa AI-Powered Fraud Detection**, **Singapore’s Singpass/COSMIC**, and **PayNow**—**MuleHunter AI** acts as an interoperable, real-time graph intelligence engine plugged directly into **NAPAS247 / SIMO**:
1. **Zero-Day Topological Mule Detection:** Instead of checking whether an account is on a static blacklist, MuleHunter AI evaluates live structural behavior: *Fan-Out (Smurfing $<10$M VND)*, *Fan-In (Funneling to shell corporations)*, *Circular Wash Loops ($A \to B \to C \to A$)*, and *Pass-Through Velocity* (funds held $<60\text{s}$, end-of-day balance $\approx 0$).
2. **Dynamic Step-Up Biometrics (Closing the Smurfing Loophole):** When a sub-10-million-VND transfer exhibits a suspicious subgraph (`Mule Risk Score` $0.60 - 0.85$), MuleHunter AI overrides static thresholds and forces an immediate **Decision 2345 facial liveness + VNeID verification challenge**, breaking psychological scam coercion.
3. **Automated 15-Minute Circuit Breaker (Closing SIMO’s 67.3% Gap):** When `Mule Risk Score` $>0.85$ (confirming active multi-hop dispersion or known fraud ring proximity), the system shifts from *advisory warning* to *active protection*—issuing a `BLOCK_AND_HOLD` command to freeze downstream hop transfers for 15 minutes while alerting bank fraud teams.
4. **Privacy-Preserving Federated Graph Learning:** Commercial banks collaboratively train the shared GNN model on local fraud patterns by exchanging encrypted mathematical gradients (`FedAvg`) rather than raw customer records.

### End-to-End Operational Workflow & System Topology

```
[Customer Initiates Transfer] ──> [NAPAS247 / VietQR Switch] ──> (Kafka Stream: Salted Hash IDs, Amount, Time)
                                                                                 │
┌────────────────────────────────────────────────────────────────────────────────┴───────────────────────────┐
│ MULEHUNTER AI — INTERBANK TRUST & GRAPH ENGINE (End-to-End SLA < 500ms)                                    │
│  [TIER 1: FAST PATH (<50ms)] Memgraph C++ In-Memory: 3-Hop Cycle, Degree Spike & Pass-Through Filter       │
│               └──> (If Anomalous ~10%) ──> [TIER 2: DEEP GNN PATH (<300ms)] 2-Hop Ego-Graph + ONNX GNN      │
└────────────────────────────────────────────────────────────────────────────────┬───────────────────────────┘
                                                                                 ▼
      ┌──────────────────────────────────────────────────────────────────────────┼───────────────────────────┐
      ▼ (Risk Score < 0.60)                        ▼ (Score 0.60 - 0.85)                                     ▼ (Score > 0.85)
 [ALLOW INSTANT SETTLEMENT]           [DYNAMIC STEP-UP BIOMETRICS]                              [AUTOMATED CIRCUIT BREAKER]
 (90%+ Benign Traffic <30ms)          (Force Decision 2345 Liveness + VNeID API)                (15-Min Hold + Auto-Update SIMO & A05)
```

### Technology Stack & Open Innovation Enablement
To achieve sub-second graph inference across $>15$ billion annual transactions, MuleHunter AI adapts the **APAN (Asynchronous Propagation Attention Network)** architecture developed by **Ant Group / Alipay** (*ACM SIGMOD 2021*) and **TigerGraph’s 100ms payment SLA**:
* **Streaming & In-Memory Graph (Tier 1):** **Apache Kafka** + **Memgraph (C++)** execute sub-50ms Cypher queries to filter 90% of normal transfers and flag sudden degree spikes.
* **Inductive Graph AI (Tier 2):** **PyTorch Geometric (PyG)** running **GraphSAGE** and **CARE-GNN** compiled on **ONNX Runtime** ($<250\text{ms}$ inference on 2-hop ego-graphs).
* **Open Innovation Ecosystem:** Enabled by **Circular 64/2024/TT-NHNN (Open APIs)** for standardized bank-fintech telemetry, **Flower (`flwr`)** for decentralized Federated Learning, and **Project 06 (C06/VNeID) APIs** (Vietnam’s equivalent to *Singpass*) to cross-verify account holder legitimacy.

### Technical, Regulatory & Data Barriers vs. Mitigations
* **Barrier 1: Data Privacy (Decree 13/2023/ND-CP) & Banking Secrecy.**
  * *Mitigation:* Account numbers and CCCD IDs undergo **Salted SHA-256 Hashing** at the switch level. Banks share zero raw PII; model intelligence is synchronized exclusively via **Federated Learning weight updates**.
* **Barrier 2: Real-Time Throughput Bottlenecks.**
  * *Mitigation:* Asynchronous background embedding propagation decouples heavy graph traversal from synchronous payment authorization, keeping P99 latency $<400\text{ms}$.

---

## 2.4. Market Size & Competitive Analysis

### Target Market & Customer Segmentation
* **Primary B2B / B2G Customers:**
  1. **State Bank of Vietnam (SBV) & NAPAS:** Deploying MuleHunter AI as the analytical "SIMO 2.0" core across the national payment switch.
  2. **46 Commercial Banks & 50+ Payment Intermediaries (e-Wallets):** Tier-1 banks (Vietcombank, BIDV, VietinBank, MB, Techcombank) and e-wallets (MoMo, VNPay, ZaloPay) processing $>95\%$ of transactions digitally.
* **Key Beneficiaries:** **89% of Vietnamese citizens aged 15+** owning payment accounts and **900,000+ MSMEs** protected from cyber-fraud losses.

### Market Sizing & Demand
* **Evidence-Based Demand:** In 1H 2026 alone, Vietnam recorded **15+ billion cashless transactions** (+34.28% YoY), while SIMO flagged **4.9 million risky transfers** by July 2026 (SBV, 2026; VnEconomy, 2026). APAC RegTech/AML spending is expanding at **18.4% CAGR**.
* **TAM (ASEAN Region):** ASEAN Banking AML, Fraud Detection & RegTech software market $\approx \mathbf{\$1.4\text{ Billion USD/year}}$.
* **SAM (Vietnam Financial Sector):** Cybersecurity, AML compliance, and fraud prevention expenditure across 46 banks, 50+ e-wallets, and national clearing infrastructure $\approx \mathbf{\$120\text{ Million USD/year}}$.
* **SOM (3-Year Target):** Securing SIMO/NAPAS integration plus 15 commercial banks $\approx \mathbf{\$8.5\text{ Million USD/year}}$.

### Revenue Model & Financial Sustainability
1. **Annual Enterprise Licensing ($60,000 – $150,000/year per bank):** Tiered subscription for local Federated Edge Nodes, SIEM connectors, and Visual Investigation Dashboards.
2. **Micro-API Screening Fee:** **$0.0002 (5 VND)** per high-risk interbank transaction routed through Tier-2 GNN graph inspection.
3. **RegTech Automation Add-On:** Automated Suspicious Transaction Report (STR) generation and forensic graph export for SBV and Ministry of Public Security (A05) audits.
* **Cost Structure & Margin:** Compute infrastructure (40%), R&D (35%), and compliance audits (25%), achieving a sustainable **>75% Gross Margin**.

### Competitive Landscape & Unique Selling Proposition (USP)

| Dimension | Legacy Bank AML (SAS, Oracle) | Global Graph AI (Quantexa) | Current SBV SIMO (1.0) | **MuleHunter AI ("SIMO 2.0")** |
| :--- | :--- | :--- | :--- | :--- |
| **Ecosystem Scope** | ❌ Siloed within 1 bank | ⚠️ Single-enterprise focus | ✅ National database | ✅ **National Interbank Live Graph** |
| **Fresh Mule Catch** | ❌ Rule-based (Delayed) | ✅ Network entity resolution | ❌ Reactive blacklist only | ✅ **Proactive Zero-Day Topology** |
| **Enforcement** | ❌ Post-event batch review | ⚠️ 1–5s latency | ⚠️ Advisory (**67.3% ignored**) | ✅ **<350ms Step-Up & Circuit Breaker** |
| **Vietnam Legal Fit** | ⚠️ Costly customization | ❌ $1M+ cost, PII barriers | ✅ Native SBV system | ✅ **Decree 13, QĐ 2345 & TT 64 Native** |

* **USP & Defensible Moat:** MuleHunter AI is the **only sub-500ms, privacy-preserving interbank Graph AI engine tailored to upgrade Vietnam’s SIMO and Decision 2345 architecture**. Its **Federated Learning network effect** creates a compounding collective intelligence moat that isolated vendors cannot replicate.

---

## 2.5. Strategic Contribution & Expected Impact

### Strengthening Vietnam’s Financial System & Measurable Indicators
MuleHunter AI directly bridges the gap between rapid digital payment growth and institutional trust:

| Measurable Indicator (KPI) | Current Baseline (2026) | MuleHunter AI Target | Evaluation Method |
| :--- | :--- | :--- | :--- |
| **SIMO Alert Prevention Conversion** | **32.7%** (1.6M / 4.9M alerts) | **> 85%** (via Step-Up & Hold) | Ratio of flagged transfers successfully stopped |
| **End-to-End Screening Latency** | Hours (Batch) / Static Lookup | **< 350 ms (P99 < 500 ms)** | Real-time Kafka/Locust telemetry |
| **Zero-Day Fresh Mule Recall** | < 15% (Unreported in SIMO) | **> 88% (AUC-ROC > 0.93)** | Validation on IBM AML & pilot bank streams |
| **False Positive Alert Rate** | 90% – 95% (Legacy rules) | **< 15% (70%+ reduction)** | Compliance officer Precision@K audit |

### Sustainability, Risk Management & Stakeholder Balance
* **Self-Sustaining Economics:** Preventing an additional VND 5–10 trillion in annual fraud losses delivers immediate ROI to banks and regulators, funding operations entirely through B2B/B2G licensing without external subsidies.
* **Adversarial Resilience:** To counter criminals camouflaging mules with small legitimate purchases, our **CARE-GNN** reinforcement learning module dynamically prunes noisy benign edges, maintaining high precision while avoiding wrongful account freezes for honest citizens.

### Justification of Selected UN SDGs
* **SDG 16 (Peace, Justice and Strong Institutions — Target 16.4 & 16.a):** Directly disrupts organized cybercrime and illicit financial flows across Vietnam, equipping regulators (SBV) and law enforcement (A05) with transparent, court-admissible topological evidence.
* **SDG 9 (Industry, Innovation and Infrastructure — Target 9.1):** Modernizes Vietnam’s core financial infrastructure (SIMO & NAPAS) through interoperable Open APIs and distributed Graph AI.
* **SDG 8 (Decent Work and Economic Growth — Target 8.10):** Safeguards the life savings and working capital of 89% of banked citizens and SMEs, ensuring inclusive participation in Vietnam’s digital economy.

---

## 2.6. Implementation Roadmap & Scalability

### Quarterly Milestone Plan (MVP to National Integration)

| Stage | Timeline | Key Milestones & Validation Deliverables | Dependencies & Partners |
| :--- | :--- | :--- | :--- |
| **Stage 1: MVP & Benchmark** | **Q1 2027** | • Train GraphSAGE/CARE-GNN on **IBM AML** & **Elliptic++** datasets (AUC > 0.92).<br>• Deploy **Memgraph** + **FastAPI/ONNX** engine; verify <350ms SLA on simulated VietQR smurfing. | Open-source stack (`PyG`, `Memgraph`, `Flower`); Cloud GPU testbed. |
| **Stage 2: Sandbox & Federated Node** | **Q2 2027** | • Enter SBV Regulatory Sandbox (**Decree 94/2025/ND-CP**).<br>• Validate Salted SHA-256 hashing & **Flower** Federated Learning across **2 pilot banks** in shadow mode. | SBV Sandbox approval; Circular 09/2020/TT-NHNN security audit. |
| **Stage 3: SIMO 2.0 Live Pilot** | **Q3 2027** | • Integrate bidirectional API hooks with **SBV SIMO** and pilot banks' **Decision 2345 Step-Up Biometrics**.<br>• Roll out **Cytoscape.js + XAI Dashboard** for bank AML teams. | NAPAS / SIMO sandbox gateway; Project 06 (C06/VNeID) APIs. |
| **Stage 4: Ecosystem Scale** | **Q4 2027** | • Scale to **15+ commercial banks** and top e-wallets (MoMo, VNPay, ZaloPay) at **50,000+ TPS**.<br>• Automate real-time STR filings to SBV & Department A05. | Commercial SLA agreements; Tier-3 On-Premise Data Center. |

### Scalability, Infrastructure & Regional Expansion
1. **Sub-Linear Operating Cost ($O(k^d)$ Complexity):** Because inference extracts localized **2-hop ego-graphs** rather than traversing the entire national graph, compute costs scale with local neighborhood degree $k$ rather than total accounts $N$. Handling Vietnam’s 34.3% annual transaction growth requires only horizontal addition of stateless ONNX worker containers.
2. **Plug-and-Play Ecosystem Interoperability:** Built on **Circular 64 Open APIs** and **Kafka**, onboarding a new bank, e-wallet, or BNPL provider requires zero core architectural changes.
3. **ASEAN Regional Exportability:** Directly transferable to regional instant payment switches facing identical mule crises—including **PayNow/COSMIC (Singapore)**, **PromptPay (Thailand)**, and **Pix (Brazil)**.

---

## 2.7. References

1. **Bank for International Settlements (BIS).** (2023). *Project Aurora: The power of data, technology and collaborative analysis in Anti-Money Laundering (AML)*. BIS Innovation Hub. https://www.bis.org/publ/othp64.htm
2. **Dou, Y., Liu, Z., Sun, L., Deng, Y., Peng, H., & Yu, P. S.** (2020). Enhancing Graph Neural Network-based Fraud Detectors against Camouflaged Fraudsters (CARE-GNN). *Proceedings of ACM CIKM '20*. https://arxiv.org/abs/2008.08692
3. **Government of Vietnam.** (2023). *Decree No. 13/2023/ND-CP on Protection of Personal Data*. Hanoi, Vietnam.
4. **Government of Vietnam.** (2025). *Decree No. 94/2025/ND-CP on Controlled Testing Mechanism (Regulatory Sandbox) for FinTech Solutions in the Banking Sector*. Hanoi, Vietnam.
5. **Monetary Authority of Singapore (MAS).** (2024). *MAS Launches COSMIC Platform to Strengthen Financial System's Defence Against Money Laundering*. https://www.mas.gov.sg
6. **Nguoi Quan Sat.** (2026, August). *Phó vụ trưởng Vụ Thanh toán NHNN: 1,6 triệu lượt khách hàng đã kịp dừng giao dịch, bảo vệ 5.500 tỷ đồng [Deputy Director of the SBV Payment Department: 1.6 million customers promptly stopped transactions, protecting 5,500 billion VND]*. https://nguoiquansat.vn/pho-vu-truong-vu-thanh-toan-nhnn-1-6-trieu-luot-khach-hang-da-kip-dung-giao-dich-bao-ve-5-500-ty-dong-truoc-nguy-co-lua-dao-309978.html
7. **Saigon Giai Phong.** (2026). *Cashless payment value reaches 28 times GDP in first half of 2026*. https://en.sggp.org.vn/cashless-payment-value-reaches-28-times-gdp-in-first-half-of-2026-post128778.html
8. **State Bank of Vietnam (SBV).** (2023). *Decision No. 2345/QD-NHNN on implementing safety and security solutions for online payments and bank card payments*.
9. **State Bank of Vietnam (SBV).** (2024). *Circular No. 64/2024/TT-NHNN regulating the implementation of Open Application Programming Interfaces (Open API) in the banking sector*.
10. **VietNamNet.** (2026a). *Vietnam anti-fraud banking system blocks $177 million in suspicious transfers*. https://vietnamnet.vn/en/vietnam-anti-fraud-banking-system-blocks-177-million-in-suspicious-transfers-2519899.html
11. **VietNamNet.** (2026b, August 13). *Vietnam bank alerts stop 1.6 million suspected scam transactions*. https://vietnamnet.vn/en/vietnam-bank-alerts-stop-1-6-million-suspected-scam-transactions-2545014.html
12. **Visa Inc.** (2025). *Visa AI-Powered Fraud Detection & Protect Solutions*. https://corporate.visa.com/en/solutions/visa-protect/insights/ai-fraud-detection.html
13. **VnEconomy.** (2026, August 12). *Vietnam’s cashless payment transactions rise 34.3% in first half*. https://en.vneconomy.vn/vietnams-cashless-payment-transactions-rise-343-in-first-half.htm
14. **Wang, X., et al.** (2021). APAN: Asynchronous Propagation Attention Network for Real-time Temporal Graph Embedding (Ant Group / Alipay). *Proceedings of ACM SIGMOD '21*. https://arxiv.org/abs/2012.06124
15. **Weber, M., et al.** (2019). Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics. *KDD '19 Workshop on Anomaly Detection in Finance*, MIT-IBM Watson AI Lab. https://arxiv.org/abs/1908.02591

---

## 2.8. Appendix (Optional Supplementary Material)

### Appendix A: Topological Money Laundering Signatures Detected by MuleHunter AI
```
1. FAN-OUT (Smurfing < 10M VND)      2. FAN-IN (Funnel to Shell Corp)     3. CIRCULAR ROUTING (Wash Loop)
       ┌─> [Mule 1] (9.5M)                [Mule 1] ─┐                        [Acc A] ──> [Acc B]
[Victim]─┼─> [Mule 2] (9.8M)              [Mule 2] ─┼─> [Shell Company]         ▲           │
       └─> [Mule 3] (9.2M)                [Mule 3] ─┘   (Crypto P2P Exit)    [Acc D] <── [Acc C]
```

### Appendix B: Verified Open-Source Repositories & Benchmark Datasets
* **Datasets:** [IBM Transactions for Anti-Money Laundering (Kaggle)](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) | [Elliptic++ Dataset (GitHub)](https://github.com/git-disl/EllipticPlusPlus)
* **Code Frameworks:** [PyTorch Geometric (`pyg-team/pytorch_geometric`)](https://github.com/pyg-team/pytorch_geometric) | [PyGOD (`pygod-team/pygod`)](https://github.com/pygod-team/pygod) | [Memgraph (`memgraph/memgraph`)](https://github.com/memgraph/memgraph) | [Flower Federated Learning (`adap/flower`)](https://github.com/adap/flower)
