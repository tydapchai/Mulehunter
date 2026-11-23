# MULEHUNTER AI — KẾ HOẠCH TRIỂN KHAI KỸ THUẬT & HỒ SƠ THỰC THI
> **Dự án dự thi:** RMIT Hack-A-Venture 2026  
> **Trụ cột kết hợp:** Fraud Prevention & Security × RegTech / Open Data (SDG 8, 16)  
> **Mục tiêu:** Hệ thống Đồ thị Trí tuệ Nhân tạo (GNN) liên ngân hàng phát hiện mạng lưới tài khoản rác (Money Mule Networks) thời gian thực với độ trễ < 500ms.

---

## 1. TỔNG QUAN DỰ ÁN & BỐI CẢNH (EXECUTIVE SUMMARY)

### 1.1. Bối cảnh tại Việt Nam
* **Khoảng trống sau Quyết định 2345/QĐ-NHNN:** Quy định xác thực sinh trắc học khuôn mặt cho giao dịch trên 10 triệu VND/lần hoặc trên 20 triệu VND/ngày đã hạn chế tài khoản rác cá nhân đơn lẻ. Tuy nhiên, các tổ chức tội phạm tài chính chuyển dịch sang:
  * Sử dụng pháp nhân tài khoản doanh nghiệp "ma" (chưa bị siết sinh trắc học gắt gao như cá nhân).
  * Kỹ thuật "Smurfing" / "Scatter-Gather": Chia nhỏ dòng tiền thành hàng chục giao dịch dưới ngưỡng 10 triệu VND và luân chuyển qua mạng lưới nhiều ngân hàng chỉ trong 30–60 giây.
* **Hạn chế của hệ thống AML hiện tại:**
  * Dựa trên bộ quy tắc cứng (Rule-based) và mô hình học máy bảng tĩnh (Tabular ML như XGBoost/Random Forest).
  * Chỉ phân tích giao dịch đơn lẻ (Transaction-level) trong nội bộ một ngân hàng, hoàn toàn **mù** trước cấu trúc liên kết mạng lưới (Topology) liên ngân hàng.

### 1.2. Mục tiêu hệ thống MuleHunter AI
1. **Phát hiện theo hình thái mạng lưới (Network Topologies):** Tự động truy vết các mô hình rửa tiền kinh điển (Fan-out, Gathering, Circular Routing).
2. **Đảm bảo SLA thời gian thực:** Đưa ra điểm rủi ro và quyết định (Pass / Flag / Block) trong vòng **dưới 500ms**.
3. **Tuân thủ quyền riêng tư dữ liệu:** Ứng dụng mã hóa định danh và học liên kết (Federated Learning), bảo đảm tuân thủ Nghị định 13/2023/NĐ-CP và Luật Các tổ chức tín dụng.

---

## 2. KIẾN TRÚC HỆ THỐNG HAI TẦNG (TWO-TIER ARCHITECTURE)

Để xử lý hàng triệu giao dịch mà vẫn giữ độ trễ dưới 500ms, hệ thống áp dụng kiến trúc phân tầng:

```
[Luồng Giao dịch Liên ngân hàng] (Vietcombank, MB, Techcombank...)
                      │
                      ▼
     ┌────────────────────────────────────────────────┐
     │  API Gateway & Stream Ingestion (Apache Kafka) │
     └───────────────────────┬────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────────────┐    ┌──────────────────────────────────┐
│ TẦNG 1: FAST PATH (< 50ms)   │    │ TẦNG 2: DEEP GNN PATH (< 300ms)  │
│ In-Memory Graph (Memgraph)   │    │ Inference Engine (ONNX / PyG)    │
├──────────────────────────────┤    ├──────────────────────────────────┤
│ - Kiểm tra chu trình (Cycle) │    │ - Trích xuất 2-hop Subgraph      │
│ - Đột biến số bậc (Degree)   │    │ - GraphSAGE / RGCN Embeddings    │
│ - Tốc độ chuyển tiền (Velocity│   │ - Tính xác suất Mule Risk Score  │
└──────────────┬───────────────┘    └─────────────────┬────────────────┘
               │                                      │
               └──────────────────┬───────────────────┘
                                  ▼
                ┌───────────────────────────────────┐
                │ Decision Engine (Tổng độ trễ < 500ms)
                ├───────────────────────────────────┤
                │ Score < 0.60: Cho phép giao dịch  │
                │ 0.60 - 0.85: Thách thức sinh trắc │
                │ Score > 0.85: Tạm giữ & Cảnh báo  │
                └───────────────────────────────────┘
```

---

## 3. DANH MỤC CÔNG NGHỆ, MÃ NGUỒN & NGUỒN DỮ LIỆU XÁC THỰC

Tất cả các nguồn dưới đây là thư viện chuẩn quốc tế, mã nguồn mở khả dụng (không giả mạo link hay thông tin):

| Thành phần | Công nghệ / Thư viện | Đường dẫn / Mã nguồn thực tế |
| :--- | :--- | :--- |
| **Dataset chuẩn AML** | IBM AML Transaction Dataset | [Kaggle Dataset](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) |
| **Dataset Graph Benchmark** | Elliptic++ Dataset | [GitHub: git-disl/EllipticPlusPlus](https://github.com/git-disl/EllipticPlusPlus) |
| **Graph Neural Network** | PyTorch Geometric (PyG) | [GitHub: pyg-team/pytorch_geometric](https://github.com/pyg-team/pytorch_geometric) |
| **Graph Anomaly Detection** | PyGOD Toolkit | [GitHub: pygod-team/pygod](https://github.com/pygod-team/pygod) |
| **In-Memory Graph Database** | Memgraph (C++ In-memory) | [GitHub: memgraph/memgraph](https://github.com/memgraph/memgraph) |
| **Federated Learning** | Flower Framework (flwr) | [GitHub: adap/flower](https://github.com/adap/flower) |
| **Model Serving Tối ưu** | ONNX Runtime / TorchScript | [GitHub: microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |
| **Trực quan hóa Đồ thị** | Cytoscape.js / Streamlit | [GitHub: cytoscape/cytoscape.js](https://github.com/cytoscape/cytoscape.js) |

---

## 4. KẾ HOẠCH TRIỂN KHAI 4 TUẦN (4-WEEK SPRINT PLAN)

### Tuần 1: Chuẩn bị Dữ liệu & Xây dựng Mô hình GNN Cơ sở
* **Mục tiêu:** Xử lý dữ liệu đồ thị và huấn luyện mô hình phân loại tài khoản rác đạt AUC-ROC > 0.90.
* **Nhiệm vụ cụ thể:**
  1. Tải tập dữ liệu **IBM AML Dataset** (hoặc sinh đồ thị mô phỏng giao dịch tài khoản ngân hàng Việt Nam).
  2. Định nghĩa cấu trúc đồ thị không đồng nhất (Heterogeneous Graph):
     * **Nodes (Tài khoản):** Đặc trưng gồm số dư trung bình, tần suất giao dịch trong 1h, tỷ lệ tiền vào/ra (in/out ratio), tuổi tài khoản.
     * **Edges (Giao dịch):** Đặc trưng gồm số tiền, dấu thời gian (timestamp), kênh chuyển tiền (VietQR, Napas247, IB).
  3. Xây dựng mô hình **GraphSAGE / RGCN** bằng PyTorch Geometric.
  4. Đánh giá độ chính xác (Precision, Recall trên lớp thiểu số - minority class).

### Tuần 2: Xây dựng In-Memory Graph Pipeline (Fast Path)
* **Mục tiêu:** Thiết lập cơ sở dữ liệu đồ thị Memgraph và viết truy vấn phát hiện hình thái rửa tiền tức thì (< 50ms).
* **Nhiệm vụ cụ thể:**
  1. Khởi chạy Memgraph qua Docker container:
     ```bash
     docker run -p 7687:7687 -p 3000:3000 memgraph/memgraph-platform
     ```
  2. Viết các truy vấn Cypher phát hiện giao dịch chu trình và gom tiền (Fan-in/Fan-out).
  3. Viết script Python giả lập luồng giao dịch trực tiếp (Streaming Simulation) với tốc độ 500 - 1.000 giao dịch/giây bắn vào cổng Ingestion.

### Tuần 3: Tích hợp GNN Model Serving & Đo kiểm Độ trễ (< 500ms)
* **Mục tiêu:** Hoàn thiện API chấm điểm thời gian thực và đo kiểm SLA.
* **Nhiệm vụ cụ thể:**
  1. Xuất mô hình PyG sang **TorchScript / ONNX format** để tối ưu hóa tốc độ tính toán ma trận.
  2. Xây dựng dịch vụ Serving bằng **FastAPI**:
     * Nhận payload: `{source_acc, target_acc, amount, timestamp}`.
     * Trích xuất mạng con 2-hop (2-hop ego network) từ Memgraph.
     * Đưa ma trận đặc trưng vào GNN Inference Engine.
     * Trả về kết quả: `{risk_score, is_mule, flagged_pattern, execution_time_ms}`.
  3. Chạy kiểm thử tải (Load test) bằng Locust để chứng minh độ trễ P99 < 400ms.

### Tuần 4: Thiết kế Giao diện Trực quan hóa & Hoàn thiện Proposal / Pitch Deck
* **Mục tiêu:** Tạo trải nghiệm demo sống động (Live Demo) thuyết phục Ban giám khảo RMIT.
* **Nhiệm vụ cụ thể:**
  1. Xây dựng Dashboard bằng Streamlit + Cytoscape.js:
     * Cột trái: Form giả lập tài khoản người dùng thực hiện lệnh chuyển tiền.
     * Cột giữa: Đồ thị trực quan các nút tài khoản và các luồng tiền đang bay qua lại.
     * Cột phải: Log cảnh báo rủi ro thời gian thực.
  2. Kịch bản Demo thực chiến (The "Aha!" Moment):
     * Thực hiện 3 giao dịch gom tiền từ 3 tài khoản lạ vào 1 tài khoản đích.
     * Giao diện đồ thị lập tức đổi các nút này sang **màu đỏ cảnh báo**.
     * Giao dịch thứ 4 ngay lập tức bị chặn với thông báo: *"PHÁT HIỆN MẠNG LƯỚI TÀI KHOẢN RÁC (Độ trễ: 185ms)"*.
  3. Hoàn thiện tài liệu Word 1.500 từ theo tiêu chuẩn RMIT Hack-A-Venture.

---

## 5. MÃ NGUỒN THỰC THI THAM KHẢO (CODE BLUEPRINTS)

### 5.1. Truy vấn Cypher phát hiện Chu trình rửa tiền trong Memgraph
```cypher
// Phát hiện chu trình khép kín: A -> B -> C -> A trong khoảng thời gian ngắn
MATCH path = (a:Account)-[r1:TRANSFERRED]->(b:Account)-[r2:TRANSFERRED]->(c:Account)-[r3:TRANSFERRED]->(a:Account)
WHERE r1.timestamp < r2.timestamp 
  AND r2.timestamp < r3.timestamp
  AND duration.inSeconds(r1.timestamp, r3.timestamp).seconds <= 600
RETURN path, 
       reduce(total = 0, r in [r1, r2, r3] | total + r.amount) AS total_laundered_amount
LIMIT 10;
```

### 5.2. Cấu trúc Mô hình GraphSAGE Fraud Classifier (PyTorch Geometric)
```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class MuleFraudDetector(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels=2):
        super(MuleFraudDetector, self).__init__()
        # 2 lớp SAGEConv để tổng hợp thông tin lân cận 2-hop
        self.conv1 = SAGEConv(in_channels, hidden_channels, aggr='mean')
        self.conv2 = SAGEConv(hidden_channels, hidden_channels, aggr='mean')
        self.classifier = torch.nn.Linear(hidden_channels, out_channels)
        self.dropout = torch.nn.Dropout(p=0.3)

    def forward(self, x, edge_index):
        # x: Ma trận đặc trưng nút [num_nodes, in_channels]
        # edge_index: Ma trận liên kết đồ thị [2, num_edges]
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        
        out = self.classifier(x)
        return F.softmax(out, dim=1)
```

### 5.3. FastAPI Real-time Screening Endpoint
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="MuleHunter Real-Time Screening API")

class TransactionPayload(BaseModel):
    transaction_id: str
    source_account: str
    target_account: str
    amount: float
    timestamp: float

@app.post("/api/v1/screen-transaction")
async def screen_transaction(txn: TransactionPayload):
    start_time = time.perf_counter()
    
    # 1. Tầng Fast Path: Kiểm tra Memgraph in-memory (< 30ms)
    # fast_flag = check_in_memory_rules(txn.source_account, txn.target_account)
    
    # 2. Tầng Deep Path: GNN Subgraph Scoring (< 200ms)
    # risk_score = gnn_model_inference(txn)
    risk_score = 0.88  # Ví dụ minh họa
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    decision = "ALLOW"
    if risk_score > 0.85:
        decision = "BLOCK_AND_HOLD"
    elif risk_score > 0.60:
        decision = "CHALLENGE_BIOMETRICS"
        
    return {
        "transaction_id": txn.transaction_id,
        "decision": decision,
        "mule_risk_score": risk_score,
        "latency_ms": round(elapsed_ms, 2)
    }
```

---

## 6. HƯỚNG DẪN TRẢ LỜI PHẢN BIỆN TRƯỚC BAN GIÁM KHẢO (DEFENSE STRATEGY)

* **Câu hỏi 1: Làm sao các ngân hàng chịu chia sẻ dữ liệu với nhau khi có Nghị định 13/2023/NĐ-CP?**
  * *Trả lời:* MuleHunter AI không yêu cầu gom dữ liệu về một cơ sở dữ liệu chung. Thay vào đó:
    1. Triển khai tại tầng chuyển mạch quốc gia **NAPAS** – nơi đã có sẵn quyền tiếp cận luồng định tuyến liên ngân hàng đã được mã hóa (Hashed).
    2. Sử dụng cơ chế **Federated GNN (Học liên kết)**: Các ngân hàng giữ dữ liệu tại chỗ, chỉ gửi trọng số mô hình (Gradients) lên máy chủ trung tâm để học tri thức phát hiện gian lận.
* **Câu hỏi 2: Tại sao phải dùng GNN mà không dùng Rule-based hay XGBoost như hiện tại?**
  * *Trả lời:* Rule-based chỉ bắt được những gì đã biết trong quá khứ. XGBoost chỉ nhìn từng dòng giao dịch độc lập. Khi kẻ gian chia nhỏ tiền thành 5 giao dịch 9 triệu đồng qua 5 ngân hàng khác nhau, cả Rule và XGBoost đều coi đây là giao dịch bình thường. Chỉ có GNN nhìn thấy đồ thị hình nan quạt (Fan-out) và nhận diện được hành vi rửa tiền.
* **Câu hỏi 3: Độ trễ 500ms có làm nghẽn hệ thống chuyển tiền nhanh 24/7 không?**
  * *Trả lời:* Kiến trúc 2 tầng chia tách rủi ro. 90% giao dịch có cấu trúc đồ thị quen thuộc (sạch) được tầng Fast Path cho qua trong vòng 30ms. Chỉ 10% giao dịch có dấu hiệu bất thường mới kích hoạt tầng Deep GNN Inference (200–300ms), đảm bảo hệ thống không bao giờ bị nghẽn.
