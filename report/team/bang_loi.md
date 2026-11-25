# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Võ Thị Kim Ý · Người gắn nhãn 2: Lý Hà Trân Trân (gắn trong 8 phút, không trao đổi)

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Hệ thống | Không | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Hệ thống | Có | Hệ thống |
| 1 | Do người dùng | Event `refund_ledger_write` có `ket_qua = ngan_hang_tu_choi`, lý do sai số tài khoản; cảnh báo khi quá 1% lệnh hoàn/ngày | Kiểm tra độ dài và định dạng số tài khoản theo ngân hàng trước khi tạo lệnh; hiện tên chủ tài khoản để khách xác nhận | PM trợ lý hoàn phí |
| 2 | Hệ thống | `audit_sample_checked` riêng loại `hang_nang`, so `so_tien_da_hoan` với `so_tien_dung`; kèm `ticket_reopened` lý do hoàn thiếu; cảnh báo khi quá 2% đơn `hang_nang`/tuần | Lấy tham số loại hàng của tool tra giá từ trường cân nặng của đơn, không để trợ lý tự suy; chặn gửi nếu tham số không khớp cân nặng | Kỹ sư trưởng agent |
| 3 | Ngữ cảnh | `ticket_reopened` lý do "chưa nhận tiền" trong khi `refund_ledger_write` đã ok và đích là ví LogiX; theo tuần, ngưỡng 3% lệnh hoàn về ví | Hỏi khách chọn ví hay ngân hàng trước khi hoàn; tin nhắn ghi rõ "tiền đã về ví LogiX" kèm chỗ xem số dư | Trưởng nhóm CSKH |
| 11 | Giới hạn hệ thống | `handoff_to_staff` với `reason = dau_vao_khong_ho_tro` (tin nhắn thoại, ảnh); đếm theo ngày, xem xét thêm chuyển giọng nói thành chữ khi quá 5% yêu cầu/tuần | Nói rõ chưa nghe được tin nhắn thoại, đưa hai lựa chọn: nhập chữ hoặc chuyển nhân viên ngay | PM trợ lý hoàn phí |
| 12 | Ngầm | Từ `agent_run_completed`: token trung bình mỗi yêu cầu theo depot, hằng ngày; cảnh báo khi một depot vượt 1,5 lần trung vị các depot 3 ngày liên tiếp | Kiểm tra đủ trường trong kết quả tool; thiếu trường thì ghi event lỗi tool và chuyển nhân viên, không gọi lại nhiều lần | Kỹ sư trưởng agent |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 18 / 20 = 90%

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- **Ca 6 (Do người dùng vs. Hệ thống):** Khách chọn sai danh mục ("Hoàn phí giao trễ" thay vì hàng vỡ), trợ lý làm đúng luồng đã chọn; việc trợ lý không nhận biết mâu thuẫn để gợi ý lại là việc cần cải thiện ở khâu khắc phục, nguyên nhân gốc vẫn là do người dùng nhập sai.
- **Ca 13 (Giới hạn hệ thống vs. Hệ thống):** Khách hỏi về hoàn phí bảo hiểm đối tác - nghiệp vụ nằm hoàn toàn ngoài phạm vi và dữ liệu của trợ lý, nên nguyên nhân gốc là giới hạn hệ thống kể cả khi câu trả lời của trợ lý chưa khéo léo.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed`; cảnh báo khi quá 2% số yêu cầu/ngày | Nhận diện mã sàn TMĐT và tra sang mã vận đơn; không tra được thì hướng dẫn kèm ảnh | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tin nhắn "đã hoàn" không có bản ghi sổ cái ok cùng `trace_id`; ngưỡng 0 ca | Chỉ báo "đã hoàn" khi sổ cái trả ok; lỗi 503 sau 3 lần thì báo "đang xử lý" và chuyển nhân viên | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Tỉ lệ mở lại vì số tiền mà kiểm tra thấy đúng, theo tuần | Mẫu tin nhắn luôn ghi cách tính: 30.000 đ × 50% = 15.000 đ | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Event `handoff_to_staff` với `reason = thieu_du_lieu`, theo loại yêu cầu | Giữ cách chuyển kèm tóm tắt; đưa `quoc_te` ra khỏi pilot | PM trợ lý hoàn phí |
| 17 | Ngầm | Kiểm tra mẫu 100 đơn/tuần so với bảng giá hiện hành; ngưỡng 1% đơn lệch | Xoá bộ nhớ đệm khi có bảng giá mới, ghi phiên bản bảng giá vào trace | Kế toán trưởng |
