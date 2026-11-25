# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: Tetris
- Lớp: L3B
- Thành viên: xem `TEAM.md`

## 2. Mục tiêu và cách tiếp cận

Dựng hồ sơ launch v0 cho trợ lý hoàn phí LogiX-VN để hội đồng Gate 2a quyết định có cho chạy pilot hay không. Nhóm trả lời ba câu hỏi theo thứ tự: mỗi việc thành công tốn bao nhiêu, pilot cần bao nhiêu mẫu để ra quyết định, và khi trợ lý hỏng thì ai phát hiện, sửa thế nào. Mọi con số do `src/lab13.py` tính từ hai file CSV giả lập; số từ cột `_simulated` ghi nhãn [sim].

## 3. Giải pháp

- **A · Chi phí** ([bang_chi_phi.md](bang_chi_phi.md)): tử số cộng mọi lần chạy kể cả lỗi, mẫu số chỉ đếm `thanh_cong`; tách theo loại yêu cầu; cộng chi phí cố định 40 triệu đ/tháng cho phạm vi pilot.
- **B · Độ nhạy** ([bang_chi_phi.md](bang_chi_phi.md)): đổi từng yếu tố, một cặp, giới hạn số lần chạy và kịch bản xem lại 100%.
- **C · Bảng lỗi** ([bang_loi.md](bang_loi.md)): hai người gắn nhãn độc lập 20 ca theo năm loại PAIR, so nhãn, thống nhất ca lệch, gán cách khắc phục cho 5 ca.
- **D · Pilot** ([pilot_plan.yaml](pilot_plan.yaml)): tính cỡ mẫu cho ba cách chia rồi mới chọn chia theo nhân viên; viết 3 luật dừng theo mẫu NẾU – TRONG – THÌ – KHÔNG THÌ.
- **E · Chỉ số và hồ sơ** ([chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)): tính thử ba chỉ số, liệt kê 10 event có `trace_id`, ba dòng rủi ro kinh tế, ghép thành hồ sơ một trang.

## 4. Kết quả

- Chi phí mỗi việc thành công 4.472 đ [sim], gấp 16,3 lần hoá đơn token + tool chia số yêu cầu; làm lại (51,8%) và xem lại (40,7%) chiếm gần hết chi phí.
- Phạm vi `noi_dia` + `hang_nang`: 4.599 đ kể cả chi phí cố định, bằng 0,38x mức 12.000 đ [sim]. `quoc_te` 22.515 đ (1,88x) nên bị loại.
- Ba yếu tố nhạy nhất: số ca làm lại (+51,8%), tỉ lệ xem lại (+40,7%), lương (+23,1%) [sim]. Giá token gấp đôi chỉ +5,6%.
- Xem lại 100% đẩy chi phí lên 11.743–12.415 đ (0,98–1,03x) [sim]: pilot phải học được cách giảm xem lại.
- Đồng thuận gắn nhãn 85% (17/20).
- Pilot chia theo nhân viên, 20 người mỗi nhóm, mức chênh 6 điểm, 859 mẫu hiệu dụng mỗi nhóm; power 0,64 nếu tác động thật là 5 điểm.
- Chỉ số trong đợt chạy thử: chính 82,83%, bỏ qua gợi ý 27,12%, mở lại 7 ngày 4,25%.
- **Đề xuất: Go có điều kiện** (bốn điều kiện, mỗi điều kiện có vai trò phụ trách, trong `ho_so_launch_v0.md`).
- Kết quả duyệt chéo nhóm nhận được từ hội đồng: ...

## 5. Khó khăn và cách xử lý

- Hai bộ nhãn bị ghi vào hai nhánh khác nhau, gây xung đột khi merge và một lần ghi nhầm cột nhãn người 1. Nhóm lấy bộ nhãn người 1 theo commit gốc của người gắn nhãn 1, tính lại đồng thuận từ 90% xuống 85% và thống nhất lại ba ca lệch (6, 8, 20).
- Mức +5 điểm cần 84 nhân viên trong khi công ty có 40. Nhóm chấp nhận mức chênh 6 điểm và ghi rõ power 0,64 thay vì giấu con số bất lợi.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Phút xem lại và làm lại là số giả lập; các kết luận chi phí cần chạy lại khi có phút đo thật sau tuần 1.
- Đợt chạy thử không có nhóm đối chứng, nên 82,83% chỉ là chỉ số trong đợt chạy thử, chưa phải tác động của trợ lý.
- Power 0,64 ở mức 5 điểm: pilot có thể bỏ sót một tác động thật nhưng nhỏ.

## 8. Tài liệu tham khảo

- `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`, `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`, `docs/du_lieu_va_cong_thuc.md`.
- Google PAIR, People + AI Guidebook, chương Errors + Graceful Failure.
