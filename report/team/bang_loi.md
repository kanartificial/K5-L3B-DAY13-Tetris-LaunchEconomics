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
| 6 | Do người dùng | Hệ thống | Không | ... |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Ngữ cảnh | Hệ thống | Không | ... |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Hệ thống | Hệ thống | Có | Hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Ngầm | Hệ thống | Không | ... |

**Tỉ lệ đồng thuận:** 17 / 20 = 85%

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- **Ca 6:** ...
- **Ca 8:** ...
- **Ca 20:** ...

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Event `refund_ledger_write` có `ket_qua = ngan_hang_tu_choi`, lý do sai số tài khoản; cảnh báo khi quá 1% lệnh hoàn/ngày | Kiểm tra độ dài và định dạng số tài khoản theo ngân hàng trước khi tạo lệnh; hiện tên chủ tài khoản để khách xác nhận | PM trợ lý hoàn phí |
| 2 | Hệ thống | `audit_sample_checked` riêng loại `hang_nang`, so `so_tien_da_hoan` với `so_tien_dung`; kèm `ticket_reopened` lý do hoàn thiếu; cảnh báo khi quá 2% đơn `hang_nang`/tuần | Lấy tham số loại hàng của tool tra giá từ trường cân nặng của đơn, không để trợ lý tự suy; chặn gửi nếu tham số không khớp cân nặng | Kỹ sư trưởng agent |
| 3 | Ngữ cảnh | `ticket_reopened` lý do "chưa nhận tiền" trong khi `refund_ledger_write` đã ok và đích là ví LogiX; theo tuần, ngưỡng 3% lệnh hoàn về ví | Hỏi khách chọn ví hay ngân hàng trước khi hoàn; tin nhắn ghi rõ "tiền đã về ví LogiX" kèm chỗ xem số dư | Trưởng nhóm CSKH |
| 11 | Giới hạn hệ thống | `handoff_to_staff` với `reason = dau_vao_khong_ho_tro` (tin nhắn thoại, ảnh); đếm theo ngày, xem xét thêm chuyển giọng nói thành chữ khi quá 5% yêu cầu/tuần | Nói rõ chưa nghe được tin nhắn thoại, đưa hai lựa chọn: nhập chữ hoặc chuyển nhân viên ngay | PM trợ lý hoàn phí |
| 12 | Ngầm | Từ `agent_run_completed`: token trung bình mỗi yêu cầu theo depot, hằng ngày; cảnh báo khi một depot vượt 1,5 lần trung vị các depot 3 ngày liên tiếp | Kiểm tra đủ trường trong kết quả tool; thiếu trường thì ghi event lỗi tool và chuyển nhân viên, không gọi lại nhiều lần | Kỹ sư trưởng agent |
