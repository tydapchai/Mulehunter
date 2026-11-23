# RMIT HACK-A-VENTURE 2026 — HỒ SƠ ĐỀ XUẤT Ý TƯỞNG VÒNG 1 (BẢN TIẾNG VIỆT CHI TIẾT CHO CẢ TEAM TECH & NON-TECH)

**Chủ đề Cuộc thi (Official Theme):** *Open Innovation for a Resilient and Sustainable Financial System in Vietnam*  
**Tên Dự án:** **MuleHunter AI: Lõi Trí tuệ Đồ thị Thời gian thực Nâng cấp Hệ thống SIMO & Kiến trúc Niềm tin Thanh toán Quốc gia**  
**Trụ cột chính (Primary Pillar):** **Pillar 5: Trust Architecture & Financial Integrity** *(Kiến trúc Niềm tin & Sự Toàn vẹn Tài chính)*  
**Trụ cột giao thoa (Intersecting Pillar):** **Pillar 2: Financial Infrastructure & Ecosystem Interoperability** *(Hạ tầng Tài chính & Khả năng Liên thông Hệ sinh thái)*  
**Mục tiêu Phát triển Bền vững (SDGs):** SDG 16 (Hòa bình, Công lý và Thể chế vững mạnh), SDG 9 (Công nghiệp, Đổi mới sáng tạo và Hạ tầng), SDG 8 (Việc làm bền vững và Tăng trưởng kinh tế)

---

## 1. Introduction (Giới thiệu Chủ đề Dự thi)

Được thực hiện bởi **Team TCQL** trong khuôn khổ cuộc thi **RMIT Hack-A-Venture 2026** với chủ đề *"Open Innovation for a Resilient and Sustainable Financial System in Vietnam"* (Đổi mới Mở vì một Hệ thống Tài chính Tự cường và Bền vững tại Việt Nam), bản đề xuất này giới thiệu **MuleHunter AI** — lõi Trí tuệ Nhân tạo Đồ thị (Graph Neural Network - GNN) liên ngân hàng thời gian thực, được thiết kế nhằm nâng cấp hệ thống phòng chống gian lận **SIMO** của Ngân hàng Nhà nước Việt Nam (NHNN) thành một hệ thống ngắt mạch cấu trúc tự động (**"SIMO 2.0"**). Giải pháp giải quyết trực diện bài toán của **Pillar 5: Trust Architecture & Financial Integrity** (Trụ cột chính) kết hợp giao thoa với **Pillar 2: Financial Infrastructure & Ecosystem Interoperability** (Trụ cột phụ), được trình bày xuyên suốt qua 6 phần cốt lõi theo đúng quy chuẩn của Ban Tổ chức dưới đây.

---

## 2. Proposal Structure (Cấu trúc Đề xuất Dự án)

### 2.1. Tóm tắt Dự án (Executive Summary)

Tính đến giữa năm 2026, quá trình chuyển đổi số ngành tài chính Việt Nam đã đạt những cột mốc lịch sử: gần **89% công dân từ 15 tuổi trở lên sở hữu tài khoản thanh toán**, hơn **95% giao dịch ngân hàng được xử lý qua kênh số**, và thanh toán không tiền mặt đạt **hơn 15 tỷ giao dịch chỉ trong 6 tháng đầu năm 2026** (tăng **34,28%** so với cùng kỳ năm 2025, đạt giá trị gấp **28 lần GDP**). Tuy nhiên, tốc độ thanh toán tức thời (NAPAS247, VietQR) cũng làm gia tăng rủi ro lừa đảo trực tuyến quy mô công nghiệp. Dù Ngân hàng Nhà nước (NHNN) đã đưa vào vận hành hệ thống **SIMO (Hệ thống thông tin hỗ trợ quản lý, giám sát và phòng ngừa rủi ro gian lận trong hoạt động thanh toán)** — phát đi **4,9 triệu lượt cảnh báo**, giúp **1,6 triệu khách hàng** tạm dừng giao dịch và bảo vệ **5.500 tỷ VNĐ** tính đến tháng 7/2026 — chính con số thống kê này lại phơi bày một lỗ hổng nghiêm trọng: **hơn 3,3 triệu lượt cảnh báo (67,3%) đã không thể ngăn khách hàng chuyển tiền**, đồng thời cơ chế danh sách đen tĩnh hoàn toàn "mù" trước các "tài khoản rác mới mở" (Fresh Mules) và thủ đoạn chia nhỏ dòng tiền dưới 10 triệu VNĐ (Smurfing).

Bám sát **Pillar 5 (Trust Architecture & Financial Integrity)** và giao thoa cùng **Pillar 2 (Financial Infrastructure & Ecosystem Interoperability)**, chúng tôi đề xuất **MuleHunter AI** — lớp Trí tuệ Nhân tạo Đồ thị (GNN) liên ngân hàng thời gian thực, nâng cấp SIMO từ *tra cứu danh sách đen thụ động* thành *hệ thống ngắt mạch cấu trúc chủ động ("SIMO 2.0")*. Kết hợp **Đồ thị Động trên RAM (Memgraph)** và mô hình **GraphSAGE/APAN** tách rời, MuleHunter AI phát hiện các hình thái rửa tiền đa bước (**Fan-out, Fan-in, Circular Routing**) xuyên ngân hàng trong **dưới 500 mili-giây**. Tận dụng **Open API (Thông tư 64/2024/TT-NHNN)**, định danh **VNeID/Đề án 06** và **Học liên kết (Federated Learning)** tuân thủ **Nghị định 13/2023/NĐ-CP**, giải pháp tự động ép quét sinh trắc học bổ sung hoặc phong tỏa tạm thời dòng tiền bẩn ngay lập tức — bảo vệ hàng chục nghìn tỷ đồng và củng cố niềm tin vào hệ thống tài chính số Việt Nam.

---

## 2.2. Đặt vấn đề & Nỗi đau Thị trường (Problem Statement & Market Pain)
*(Phần trọng tâm cho thành viên Non-Tech / Business phân tích số liệu từ Đề bài)*

### Vấn đề cụ thể & Tính cấp thiết trong Hệ thống Tài chính Việt Nam
Khi Việt Nam hướng tới mục tiêu giá trị thanh toán không tiền mặt đạt **30 lần GDP vào năm 2030** (Vietnam+, 2026), hạ tầng thanh toán tức thời liên ngân hàng đang bị các tổ chức tội phạm xuyên biên giới lợi dụng để tẩu tán tiền lừa đảo qua mạng lưới **Tài khoản Rác (Money Mule accounts)** (tài khoản thuê, mua hoặc công ty vỏ bọc). Ngay khi nạn nhân bấm chuyển tiền, các bot tự động chỉ mất **30 đến 120 giây** để phân tán tiền qua 3–4 tầng ngân hàng khác nhau trước khi rút ra tiền mã hóa (USDT P2P).

### 4 Nguyên nhân Gốc rễ & Hạn chế của Giải pháp Hiện tại (Dẫn chứng trực tiếp từ Đề bài RMIT)
1. **Khoảng trống chuyển đổi 67,3% của Hệ thống SIMO hiện tại:** Theo số liệu của Vụ Thanh toán NHNN được trích dẫn trong đề bài (Nguoi Quan Sat, 2026; VietNamNet, 2026b), tính đến cuối tháng 7/2026, SIMO đã phát ra **4,9 triệu cảnh báo**, nhưng chỉ có **1,6 triệu giao dịch được dừng lại**. Điều đó có nghĩa là **3,3 triệu giao dịch (67,3%) vẫn tiếp tục chuyển tiền dù đã có cảnh báo đỏ** — bởi SIMO hiện chỉ là *popup khuyến cáo*, trong khi nạn nhân bị thao túng tâm lý (Deepfake giả danh công an, viện kiểm sát đe dọa) vẫn bị ép bấm "Tiếp tục".
2. **Độ trễ Hậu kiểm & Điểm mù "Tài khoản rác mới mở" (Cold-Start Blindness):** Một tài khoản chỉ bị đưa vào danh sách SIMO *sau khi* đã có nạn nhân bị lừa và trình báo. Tội phạm dễ dàng vô hiệu hóa SIMO bằng cách liên tục thu mua các tài khoản sinh viên/công nhân mới mở ("Fresh Mules") chưa từng có tiền án trên hệ thống.
3. **Thủ đoạn "Smurfing < 10 triệu VNĐ" lách Quyết định 2345/QĐ-NHNN:** Để né quy định bắt buộc quét khuôn mặt khi chuyển $>10$ triệu VNĐ/lần hoặc $>20$ triệu VNĐ/ngày, tội phạm dùng script tự động chia nhỏ 150 triệu VNĐ thành **16 lệnh chuyển 9,3 triệu VNĐ đồng thời** sang 16 tài khoản rác ở các ngân hàng khác nhau.
4. **Sự phân mảnh dữ liệu giữa các Ngân hàng (Nỗi đau của Pillar 2):** Các hệ thống AML truyền thống (SAS, Oracle Mantas) chỉ nhìn thấy giao dịch nằm trong nội bộ 1 ngân hàng. Ngân hàng A hoàn toàn không biết khoản tiền vừa chuyển sang Ngân hàng B đã bị xé lẻ đi 10 ngân hàng khác trong 15 giây tiếp theo.

| Tiêu chí đối chiếu | Hệ thống AML Ngân hàng Cũ | Hệ thống SIMO Hiện tại (1.0) | Khoảng trống Thị trường chưa được giải quyết |
| :--- | :--- | :--- | :--- |
| **Cơ chế cốt lõi** | Quy tắc đơn lẻ nội bộ 1 ngân hàng | Tra cứu danh sách đen (Blacklist) tĩnh | Mù trước cấu trúc mạng lưới đa ngân hàng |
| **Bắt tài khoản rác mới** | Thất bại (Chưa có lịch sử xấu) | Thất bại (Chưa bị nạn nhân tố cáo) | Tài khoản rác "Zero-day" tẩu tán tiền trót lọt |
| **Hành động can thiệp** | Kiểm tra hậu kiểm cuối ngày (Batch) | Chỉ hiện popup (**67,3% vẫn chuyển**) | Nạn nhân bị thao túng tâm lý vẫn mất tiền |
| **Tỷ lệ Báo động giả** | Cực cao (90% – 95%) | Bỏ lọt tội phạm mới (False Negative cao) | Quá tải nhân sự thẩm định tuân thủ |

---

## 2.3. Kiến trúc Giải pháp & Tích hợp FinTech (Solution Architecture & FinTech Integration)
*(Phần trọng tâm cho thành viên Tech thiết kế kiến trúc)*

### Giải pháp Đề xuất & 4 Tính năng Đột phá
Lấy cảm hứng từ các hình mẫu quốc tế được Ban tổ chức nêu trong Pillar 5 và Pillar 2 — cụ thể là **Visa AI-Powered Fraud Detection**, **Singpass/COSMIC (Singapore)** và **PayNow/Pix** — **MuleHunter AI** đóng vai trò là lớp trí tuệ đồ thị liên thông tích hợp thẳng vào **NAPAS247 và SIMO**:
1. **Phát hiện Hình thái Tài khoản Rác Zero-Day (Topological Detection):** Không cần đợi tài khoản có tên trong danh sách đen, hệ thống bắt trực tiếp hành vi cấu trúc đồ thị: *Fan-Out (Chia nhỏ tiền $<10$ triệu)*, *Fan-In (Gom tiền về công ty ma)*, *Circular Routing (Vòng tròn $A \to B \to C \to A$)*, và *Pass-Through Velocity* (tiền dừng lại $<60$ giây, số dư cuối ngày $\approx 0$).
2. **Kích hoạt Sinh trắc học Động (Dynamic Step-Up Biometrics — Bịt lỗ hổng Smurfing):** Khi một giao dịch 9,5 triệu VNĐ có điểm rủi ro đồ thị trung bình-cao (`Mule Risk Score` $0,60 - 0,85$), MuleHunter AI lập tức ghi đè ngưỡng tĩnh và **ép ứng dụng ngân hàng kích hoạt quét khuôn mặt Liveness (Quyết định 2345) + đối soát VNeID**, cắt đứt kịch bản thao túng tâm lý hoặc bot tự động.
3. **Cầu dao Ngắt mạch Tự động 15 Phút (Automated Circuit Breaker — Bịt lỗ hổng 67,3% của SIMO):** Khi `Mule Risk Score` $>0,85$, hệ thống chuyển từ *khuyên bảo* sang *chặn chủ động*: phát lệnh `BLOCK_AND_HOLD` đóng băng tạm thời việc tẩu tán tiền sang bước tiếp theo trong 15 phút và cảnh báo khẩn cấp cho ngân hàng.
4. **Học liên kết Đồ thị Bảo mật (Federated Graph Learning):** Các ngân hàng cùng huấn luyện mô hình GNN trên dữ liệu nội bộ và chỉ gửi tham số toán học (`FedAvg Gradients`) về trung tâm, bảo mật tuyệt đối dữ liệu khách hàng.

### Luồng Vận hành & Sơ đồ Kiến trúc Tổng thể (End-to-End System Topology)

```
[Khách hàng bấm Chuyển tiền] ──> [Cổng Chuyển mạch NAPAS247 / VietQR] ──> (Kafka Stream: Salted Hash ID, Số tiền, Time)
                                                                                        │
┌───────────────────────────────────────────────────────────────────────────────────────┴──────────────────────┐
│ LÕI TRÍ TUỆ ĐỒ THỊ MULEHUNTER AI — "SIMO 2.0" (Tổng độ trễ cam kết SLA < 500ms)                              │
│  [TẦNG 1: FAST PATH (<50ms)] Memgraph C++ In-Memory: Lọc chu trình 3-Hop, Đột biến bậc nút & Tốc độ rút lõi   │
│               └──> (Nếu Bất thường ~10%) ──> [TẦNG 2: DEEP GNN PATH (<300ms)] Trích xuất 2-Hop + ONNX GNN     │
└───────────────────────────────────────────────────────────────────────────────────────┬──────────────────────┘
                                                                                        ▼
      ┌─────────────────────────────────────────────────────────────────────────────────┼──────────────────────┐
      ▼ (Risk Score < 0,60)                        ▼ (Score 0,60 - 0,85)                                       ▼ (Score > 0,85)
 [CHO PHÉP THANH TOÁN TỨC THÌ]        [ÉP QUÉT SINH TRẮC HỌC ĐỘNG]                              [NGẮT MẠCH TỰ ĐỘNG (15 PHÚT)]
 (90%+ Giao dịch sạch < 30ms)         (Kích hoạt QĐ 2345 + Đối soát VNeID)                      (Tạm giữ tiền + Cập nhật SIMO & A05)
```

### Công nghệ Cốt lõi & Thúc đẩy Đổi mới Mở (Open Innovation)
Để xử lý $>15$ tỷ giao dịch mỗi nửa năm với độ trễ mili-giây, MuleHunter AI áp dụng kiến trúc **APAN (Asynchronous Propagation Attention Network)** của **Ant Group / Alipay** (*ACM SIGMOD 2021*) và chuẩn SLA 100ms của **TigerGraph / Visa**:
* **Streaming & In-Memory Graph (Tầng 1):** **Apache Kafka** + **Memgraph (C++)** thực thi truy vấn Cypher trong $<50\text{ms}$.
* **Inductive Graph AI (Tầng 2):** **PyTorch Geometric (PyG)** chạy mô hình **GraphSAGE** và **CARE-GNN** trên **ONNX Runtime** ($<250\text{ms}$ trên đồ thị con 2-hop).
* **Liên thông Mở (Open Innovation):** Vận hành dựa trên chuẩn **Open API (Thông tư 64/2024/TT-NHNN)**, thư viện **Flower (`flwr`)** cho Federated Learning, và **API Đề án 06 (C06/VNeID)** (tương đương *Singpass* của Singapore) để xác thực nhân thân chủ tài khoản.

### Rào cản Kỹ thuật, Pháp lý & Giải pháp Giảm thiểu
* **Rào cản 1: Bảo vệ dữ liệu cá nhân (Nghị định 13/2023/NĐ-CP) & Bí mật ngân hàng.**
  * *Giảm thiểu:* Số tài khoản và CCCD được mã hóa một chiều (**Salted SHA-256 Hashing**) ngay tại cổng chuyển mạch. Dữ liệu định danh gốc không bao giờ rời khỏi ngân hàng; việc học máy liên ngân hàng chỉ trao đổi **trọng số Federated Learning**.
* **Rào cản 2: Áp lực độ trễ trên luồng thanh toán 24/7.**
  * *Giảm thiểu:* Lan truyền vector đặc trưng bất đồng bộ dưới nền (Asynchronous Propagation), giải phóng 90% giao dịch sạch ở Tầng 1 trong $<30\text{ms}$, đảm bảo P99 $<400\text{ms}$.

---

## 2.4. Quy mô Thị trường & Phân tích Cạnh tranh (Market Size & Competitive Analysis)

### Khách hàng Mục tiêu & Đối tượng Thụ hưởng
* **Khách hàng chính (B2B / B2G):**
  1. **Ngân hàng Nhà nước (NHNN) & NAPAS:** Tích hợp MuleHunter AI làm lõi phân tích nâng cấp "SIMO 2.0" trên cổng thanh toán quốc gia.
  2. **46 Ngân hàng Thương mại & 50+ Trung gian Thanh toán (Ví điện tử):** Các ngân hàng có $>95\%$ giao dịch số (Vietcombank, BIDV, VietinBank, MB, Techcombank) và ví điện tử (MoMo, VNPay, ZaloPay).
* **Người thụ hưởng:** **89% công dân Việt Nam từ 15 tuổi trở lên** có tài khoản thanh toán và **900.000+ doanh nghiệp MSME**.

### Quy mô Thị trường (TAM - SAM - SOM)
* **Dữ liệu Cầu Thị trường:** Nửa đầu năm 2026 ghi nhận **hơn 15 tỷ giao dịch không tiền mặt** (+34,28% YoY), trong khi SIMO phát hiện tới **4,9 triệu giao dịch nghi vấn** tính đến tháng 7/2026 (NHNN, 2026; VnEconomy, 2026). Chi tiêu cho RegTech/AML tại Châu Á - Thái Bình Dương tăng trưởng **18,4%/năm (CAGR)**.
* **TAM (Toàn khu vực ASEAN):** Thị trường phần mềm AML, Chống gian lận & RegTech ngành ngân hàng ASEAN đạt **1,4 tỷ USD/năm**.
* **SAM (Ngành Tài chính Việt Nam):** Ngân sách an ninh thanh toán, tuân thủ AML và chống gian lận của 46 ngân hàng, 50+ ví điện tử và hạ tầng chuyển mạch tại Việt Nam đạt **120 triệu USD/năm**.
* **SOM (Mục tiêu 3 năm đầu):** Triển khai tại SIMO/NAPAS và 15 ngân hàng thương mại đầu tiên, đạt doanh thu **8,5 triệu USD/năm** (~210 tỷ VNĐ/năm).

### Mô hình Doanh thu & Bền vững Tài chính
1. **Phí Bản quyền Hạ tầng Năm ($60.000 – $150.000/năm/ngân hàng):** Phí triển khai Node Federated Learning nội bộ, tích hợp SIEM và Dashboard điều tra đồ thị.
2. **Phí Vi mô theo Lượt Quét API (Micro-API Fee):** **5 VNĐ ($0,0002)/giao dịch** đối với các giao dịch rủi ro cao cần quét đồ thị sâu qua Tầng 2.
3. **Mô-đun Tự động hóa RegTech:** Tự động khởi tạo Báo cáo Giao dịch Đáng ngờ (STR) và trích xuất đồ thị pháp chứng số cho NHNN và Cục A05.
* **Cơ cấu chi phí & Lợi nhuận:** Hạ tầng GPU/Cloud (40%), R&D (35%), kiểm toán bảo mật (25%), mang lại **Biên lợi nhuận gộp (Gross Margin) > 75%**.

### Bảng Phân tích Cạnh tranh & Lợi thế Độc quyền (USP)

| Tiêu chí | Phần mềm AML Cũ (SAS, Oracle) | Kỳ lân Đồ thị Quốc tế (Quantexa) | Hệ thống SIMO Hiện tại (1.0) | **MuleHunter AI ("SIMO 2.0")** |
| :--- | :--- | :--- | :--- | :--- |
| **Phạm vi Giám sát** | ❌ Đóng kín trong 1 ngân hàng | ⚠️ Đơn lẻ từng tổ chức | ✅ Cơ sở dữ liệu quốc gia | ✅ **Đồ thị Động Liên ngân hàng Quốc gia** |
| **Bắt tài khoản rác mới** | ❌ Luật tĩnh (Chậm trễ) | ✅ Phân tích thực thể mạng lưới | ❌ Chỉ tra cứu Blacklist cũ | ✅ **Chủ động bắt hình thái Zero-Day** |
| **Cơ chế Can thiệp** | ❌ Hậu kiểm cuối ngày (Batch) | ⚠️ Độ trễ 1–5 giây | ⚠️ Khuyến cáo (**67,3% phớt lờ**) | ✅ **<350ms Ép quét mặt & Ngắt mạch** |
| **Tuân thủ Luật VN** | ⚠️ Tùy chỉnh đắt đỏ | ❌ Chi phí >1 triệu USD, vướng PII | ✅ Hệ thống nội địa của NHNN | ✅ **Chuẩn Nghị định 13, QĐ 2345 & TT 64** |

---

## 2.5. Đóng góp Chiến lược, Tác động Dự kiến & SDGs (Strategic Contribution & Impact)

### Chỉ số Đo lường Hiệu quả Định lượng (KPIs)

| Chỉ số Đo lường (KPI) | Thực trạng Hiện nay (Tháng 7/2026) | Mục tiêu của MuleHunter AI | Phương pháp Đánh giá |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ Chặn Thành công Giao dịch Lừa đảo** | **32,7%** (1,6M / 4,9M cảnh báo SIMO) | **> 85%** (Nhờ Step-Up & Ngắt mạch) | Tỷ lệ giao dịch rủi ro cao được ngăn chặn kịp thời |
| **Độ trễ Phê duyệt Toàn trình** | Nhiều giờ (Batch) / Tra cứu tĩnh | **< 350 ms (P99 < 500 ms)** | Đo kiểm telemetry thực tế qua Kafka / Locust |
| **Tỷ lệ Phát hiện Tài khoản Rác Mới (Recall)** | < 15% (Chưa có trong SIMO) | **> 88% (AUC-ROC > 0,93)** | Kiểm thử trên bộ dữ liệu IBM AML & luồng Pilot |
| **Tỷ lệ Cảnh báo Giả (False Positive)** | 90% – 95% (Hệ thống Rule-based) | **< 15% (Giảm hơn 70%)** | Đánh giá Precision@K từ chuyên viên tuân thủ |

### Đóng góp cho các Mục tiêu Phát triển Bền vững của Liên Hợp Quốc (SDG Alignment)
* **SDG 16 (Hòa bình, Công lý và Thể chế vững mạnh — Mục tiêu 16.4 & 16.a):** Trực tiếp ngăn chặn dòng tiền bất hợp pháp, tội phạm lừa đảo công nghệ cao và rửa tiền xuyên biên giới; cung cấp hồ sơ đồ thị pháp chứng minh bạch cho Ngân hàng Nhà nước và Bộ Công an (A05).
* **SDG 9 (Công nghiệp, Đổi mới sáng tạo và Hạ tầng — Mục tiêu 9.1):** Nâng cấp hạ tầng tài chính số cốt lõi của quốc gia (SIMO & NAPAS) bằng công nghệ AI đồ thị phân tán và chuẩn giao tiếp Open API.
* **SDG 8 (Việc làm bền vững và Tăng trưởng kinh tế — Mục tiêu 8.10):** Bảo vệ tài sản và vốn lưu động của 89% người dân trưởng thành cùng các hộ kinh doanh/MSME, củng cố niềm tin bền vững vào nền kinh tế không tiền mặt.

---

## 2.6. Lộ trình Triển khai & Khả năng Mở rộng (Implementation Roadmap & Scalability)

### Lộ trình Cột mốc theo Quý (Quarterly Milestone Plan)

| Giai đoạn | Thời gian | Cột mốc Kỹ thuật & Kiểm chứng Thực tế | Điều kiện & Đối tác Phụ thuộc |
| :--- | :--- | :--- | :--- |
| **Giai đoạn 1: MVP & Benchmark** | **Quý 1/2027** | • Huấn luyện GraphSAGE/CARE-GNN trên **IBM AML** & **Elliptic++** (AUC > 0,92).<br>• Dựng cụm **Memgraph** + **FastAPI/ONNX**, kiểm chứng SLA < 350ms. | Mã nguồn mở (`PyG`, `Memgraph`, `Flower`); Máy chủ GPU thử nghiệm. |
| **Giai đoạn 2: Sandbox & Federated** | **Quý 2/2027** | • Tham gia Sandbox NHNN (**Nghị định 94/2025/NĐ-CP**).<br>• Chạy thử nghiệm mã băm Salted SHA-256 & **Flower** Federated Learning với **2 ngân hàng Pilot** ở chế độ ẩn (Shadow mode). | Phê duyệt Sandbox của NHNN; Kiểm toán an ninh Thông tư 09/2020/TT-NHNN. |
| **Giai đoạn 3: Pilot SIMO 2.0** | **Quý 3/2027** | • Tích hợp API hai chiều với **SIMO** và kích hoạt **Sinh trắc học động Quyết định 2345**.<br>• Triển khai **Cytoscape.js + XAI Dashboard** cho đội ngũ AML ngân hàng. | Cổng API thử nghiệm NAPAS / SIMO; API Đề án 06 (C06/VNeID). |
| **Giai đoạn 4: Mở rộng Toàn quốc** | **Quý 4/2027** | • Mở rộng lên **15+ ngân hàng thương mại** và ví điện tử lớn (MoMo, VNPay, ZaloPay) ở mức chịu tải **50.000+ TPS**.<br>• Tự động hóa báo cáo STR thời gian thực. | Hợp đồng SLA thương mại; Hạ tầng Data Center chuẩn Tier-3 nội địa. |

### Khả năng Mở rộng & Hiệu quả Hạ tầng (Scalability)
1. **Chi phí vận hành tăng trưởng dưới tuyến tính ($O(k^d)$ Complexity):** Nhờ lấy mẫu đồ thị con cục bộ 2 bước (**2-hop Ego-Graph Sampling**), chi phí tính toán chỉ phụ thuộc vào số kết nối lân cận $k$ chứ không phình to theo tổng số tài khoản quốc gia $N$. Khi lưu lượng giao dịch của Việt Nam tăng 34,3%/năm, hệ thống chỉ cần mở rộng ngang (horizontal scaling) các container ONNX.
2. **Mở rộng sang khu vực ASEAN:** Kiến trúc hoàn toàn tương thích để xuất khẩu sang các hệ thống thanh toán tức thời trong khu vực như **PayNow/COSMIC (Singapore)**, **PromptPay (Thái Lan)** và **InstaPay (Philippines)**.

---

## 2.7. Tài liệu Tham khảo (References)
*(Bao gồm đầy đủ các nguồn báo chí và nghiên cứu chính thức từ trang 16–17 của tài liệu Background & Problem Statement của RMIT Hack-A-Venture 2026 như Nguoi Quan Sat 2026, Saigon Giai Phong 2026, VietNamNet 2026a/2026b, VnEconomy 2026, Visa 2025, cùng các bài báo khoa học của BIS Project Aurora, Ant Group SIGMOD 2021, MIT-IBM 2019).*
