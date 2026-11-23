# BỘ SƠ ĐỒ TRỰC QUAN (MERMAID DIAGRAMS) — TEAM TCQL (RMIT HACK-A-VENTURE 2026)

## Sơ đồ 1: Luồng Tấn công Chia nhỏ Tiền (Smurfing) & Lỗ hổng của Hệ thống SIMO 1.0 Hiện tại
*(Chèn vào **Mục 2.2. Problem Statement & Market Pain**)*

```mermaid
flowchart LR
    Victim["Victim Account (Manipulated by Scam)"] -->|"150M VND Stolen"| PrimaryMule["Primary Mule Account (Fresh Unreported Account)"]
    
    subgraph SmurfingLoop["High-Velocity Automated Smurfing (30 - 60 Seconds)"]
        PrimaryMule -->|"9.3M VND (Evades 10M Biometrics)"| Mule1["Fresh Mule 1 (Bank A)"]
        PrimaryMule -->|"9.5M VND (Evades 10M Biometrics)"| Mule2["Fresh Mule 2 (Bank B)"]
        PrimaryMule -->|"9.2M VND (Evades 10M Biometrics)"| Mule3["Fresh Mule 3 (Bank C)"]
        PrimaryMule -->|"x13 Parallel Sub-10M Transfers"| MuleN["Fresh Mules 4..16 (Banks D..Z)"]
    end

    Mule1 --> ShellCorp["Shell Company / Funnel Account"]
    Mule2 --> ShellCorp
    Mule3 --> ShellCorp
    MuleN --> ShellCorp

    ShellCorp -->|"Cash Out < 120s"| CryptoExit["Crypto P2P / Cross-Border Exit (Funds Lost)"]

    SIMO["Current SBV SIMO 1.0 (Static Blacklist)"] -.->|"Blind to Fresh Mules & 67.3% Alerts Ignored"| PrimaryMule

    style Victim fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#000
    style PrimaryMule fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#000
    style ShellCorp fill:#fca5a5,stroke:#b91c1c,stroke-width:2px,color:#000
    style CryptoExit fill:#991b1b,stroke:#7f1d1d,stroke-width:2px,color:#fff
    style SIMO fill:#e2e8f0,stroke:#64748b,stroke-width:2px,stroke-dasharray: 5 5,color:#000
```

---

## Sơ đồ 2: Kiến trúc Tổng thể 2 Tầng & Luồng Xử lý Thời gian thực (< 500ms SLA)
*(Chèn vào **Mục 2.3. Solution Architecture & FinTech Integration**)*

```mermaid
flowchart TD
    Transfer["Customer Initiates Transfer on Banking App"] --> Switch["NAPAS247 / VietQR National Switch"]
    Switch -->|"Kafka Stream (Salted SHA-256 IDs, Amount, Timestamp)"| Tier1

    subgraph MuleHunterCore["MULEHUNTER AI CORE ENGINE ('SIMO 2.0' — Total End-to-End SLA < 500ms)"]
        Tier1["TIER 1: FAST PATH (< 50ms) Memgraph C++ In-Memory Graph (3-Hop Cycle, Degree Spike & Pass-Through Velocity Filter)"]
        Tier2["TIER 2: DEEP GNN PATH (< 300ms) 2-Hop Ego-Graph Extraction + Decoupled APAN / GraphSAGE on ONNX Runtime"]
        
        Tier1 -->|"Anomalous Subgraph (~10% Traffic)"| Tier2
    end

    Tier1 -->|"Benign Traffic (~90% Cleared in < 30ms)"| Allow
    Tier2 --> Router{"Decision Router (Mule Risk Score 0.0 - 1.0)"}

    Router -->|"Risk Score < 0.60 (Low Risk)"| Allow["ALLOW INSTANT SETTLEMENT"]
    Router -->|"Risk Score 0.60 - 0.85 (Medium-High Smurfing Risk)"| StepUp["DYNAMIC STEP-UP BIOMETRICS (Force Decision 2345 Liveness + VNeID API Check)"]
    Router -->|"Risk Score > 0.85 (Critical Fraud Ring)"| Block["AUTOMATED CIRCUIT BREAKER (15-Min Freeze + Real-Time Sync to SIMO & A05 STR)"]

    StepUp -->|"Biometrics Verified"| Allow
    StepUp -->|"Biometrics Failed / Bot Detected"| Block

    style Transfer fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#000
    style Switch fill:#dbeafe,stroke:#1d4ed8,stroke-width:2px,color:#000
    style Tier1 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#000
    style Tier2 fill:#fefce8,stroke:#ca8a04,stroke-width:2px,color:#000
    style Router fill:#1e293b,stroke:#0f172a,stroke-width:2px,color:#fff
    style Allow fill:#dcfce7,stroke:#15803d,stroke-width:2px,color:#000
    style StepUp fill:#ffedd5,stroke:#ea580c,stroke-width:2px,color:#000
    style Block fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#000
```

---

## Sơ đồ 3: Mô hình Học liên kết Bảo mật (Federated Graph Learning) & Liên thông Open API
*(Chèn vào **Mục 2.3. Open Innovation & Privacy Mitigation**)*

```mermaid
flowchart TD
    subgraph Banks["Member Commercial Banks & e-Wallets (Raw Customer PII Never Leaves Bank — Decree 13 Compliant)"]
        BankA["Bank A Edge Node (Local GNN Training)"]
        BankB["Bank B Edge Node (Local GNN Training)"]
        BankC["Bank C / e-Wallet Node (Local GNN Training)"]
    end

    BankA <-->|"Encrypted Gradients & Global Weights (Flower FedAvg via Circular 64 Open API)"| Coordinator["MuleHunter AI Central Federated Coordinator & SIMO 2.0 Hub"]
    BankB <-->|"Encrypted Gradients & Global Weights (Flower FedAvg via Circular 64 Open API)"| Coordinator
    BankC <-->|"Encrypted Gradients & Global Weights (Flower FedAvg via Circular 64 Open API)"| Coordinator

    Coordinator <-->|"Identity & Biometric Verification"| VNeID["National Population Database (VNeID / Project 06 C06 API)"]
    Coordinator -->|"Automated STR & Forensic Evidence Graphs"| Regulators["SBV (AML Dept) & Ministry of Public Security (Dept A05)"]

    style Coordinator fill:#1e293b,stroke:#0f172a,stroke-width:2px,color:#fff
    style BankA fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#000
    style BankB fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#000
    style BankC fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#000
    style VNeID fill:#ecfdf5,stroke:#059669,stroke-width:2px,color:#000
    style Regulators fill:#fef2f2,stroke:#dc2626,stroke-width:2px,color:#000
```

---

## Sơ đồ 4: Lộ trình Triển khai Hàng quý (Visual Quarterly Implementation Roadmap)
*(Chèn vào **Mục 2.6. Implementation Roadmap & Scalability**)*

```mermaid
flowchart LR
    Q1["Q1 2027: Stage 1 (MVP & Benchmark) • Train GraphSAGE/CARE-GNN on IBM AML & Elliptic++ (AUC > 0.92) • Deploy Memgraph + ONNX (<350ms SLA)"] 
    --> Q2["Q2 2027: Stage 2 (SBV Sandbox) • Enter Decree 94/2025/ND-CP Sandbox • Validate Salted SHA-256 & Flower Federated Nodes with 2 Pilot Banks"]
    --> Q3["Q3 2027: Stage 3 (SIMO 2.0 Live Pilot) • Bidirectional API Sync with SBV SIMO & Decision 2345 Step-Up Biometrics • Launch XAI Dashboard"]
    --> Q4["Q4 2027: Stage 4 (Ecosystem Scale) • Scale to 15+ Commercial Banks & Top e-Wallets (50,000+ TPS) • Regional Export (PayNow / PromptPay)"]

    style Q1 fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#000
    style Q2 fill:#fefce8,stroke:#ca8a04,stroke-width:2px,color:#000
    style Q3 fill:#ecfdf5,stroke:#059669,stroke-width:2px,color:#000
    style Q4 fill:#fdf2f8,stroke:#db2777,stroke-width:2px,color:#000
```

---

## Sơ đồ 5: 4 Hình thái Đồ thị Rửa tiền (Money Laundering Topologies)
*(Chèn vào **Mục 2.8. Appendix A**)*

```mermaid
flowchart LR
    subgraph P1["1. Fan-Out (Smurfing < 10M VND)"]
        V1["Victim"] -->|"9.5M"| M1["Mule 1"]
        V1 -->|"9.8M"| M2["Mule 2"]
        V1 -->|"9.2M"| M3["Mule 3"]
    end

    subgraph P2["2. Fan-In (Funnel to Shell Corp)"]
        F1["Mule A"] -->|"9.9M"| S1["Shell Company"]
        F2["Mule B"] -->|"9.7M"| S1
        F3["Mule C"] -->|"9.4M"| S1
    end

    subgraph P3["3. Circular Routing (Wash Loop)"]
        C1["Account A"] --> C2["Account B"]
        C2 --> C3["Account C"]
        C3 --> C4["Account D"]
        C4 --> C1
    end

    style V1 fill:#fee2e2,stroke:#dc2626,color:#000
    style S1 fill:#fee2e2,stroke:#dc2626,color:#000
    style C1 fill:#fef3c7,stroke:#d97706,color:#000
```
