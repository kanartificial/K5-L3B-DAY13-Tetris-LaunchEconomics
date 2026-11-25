# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: Tetris · Lớp: L3B

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | CPS toàn bộ 4.472 đ [sim], gấp 16,3 lần hoá đơn token + tool chia số yêu cầu (274,7 đ); làm lại chiếm 51,8%, xem lại 40,7% tổng chi phí. Phạm vi pilot `noi_dia` + `hang_nang`: 3.414 đ biến đổi, cộng cố định 40 triệu đ/tháng thành 4.599 đ ở 45.000 yc/tháng [sim] (`bang_chi_phi.md` A2, A4) | Giả lập | Người viết code |
| 2 · Ba yếu tố nhạy nhất | 1. Số ca làm lại ×2: +51,8% (6.787 đ) · 2. Tỉ lệ xem lại ×2: +40,7% (6.292 đ) · 3. Lương +25%: +23,1% (5.506 đ) [sim]; giá token ×2 chỉ +5,6%. Giới hạn 2 lần chạy rẻ nhất cho cả hệ thống: 6.901.220 đ so với 7.037.585 đ (3 lần) và 7.449.781 đ (1 lần) [sim] (`bang_chi_phi.md` B1–B3) | Giả lập | Người kiểm số |
| 3 · So với nhân viên tự làm | Phạm vi pilot 4.599 đ = 0,38x mức 12.000 đ; còn 5.784 đ = 0,48x nếu khối lượng giảm một nửa [sim]. `quoc_te` 22.515 đ = 1,88x nên loại khỏi phạm vi. Nếu xem lại 100% thì 11.743–12.415 đ = 0,98–1,03x, mất lợi thế; chỉ hoà vốn khi xem lại ≤ 4,8–5,1 phút/ca [sim] (A3, A4, B4) | Giả lập | Người kiểm số |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Chỉ số trong đợt chạy thử: chính 82,83% (994/1.200), dùng (bỏ qua gợi ý) 27,12% (48/177), an toàn (mở lại 7 ngày) 4,25% (51/1.200), riêng phạm vi pilot 3,97%; chưa có đối chứng nên chưa kết luận được tác động. 10 event có `trace_id` (`chi_so.md` E1) | Xong, có bằng chứng | PM trợ lý hoàn phí |
| 5 · Bảng lỗi và cách khắc phục | 20 ca lỗi PAIR, hai bộ nhãn độc lập; đồng thuận 85% (17/20), lệch ở ca 6, 8, 20, đã thống nhất và có quy tắc; bảng khắc phục 5 ca (1, 2, 3, 11, 12) đủ 5 loại có event và ngưỡng đo được (`bang_loi.md`) | Xong, có bằng chứng | Người gắn nhãn 2 kiêm giữ hồ sơ |
| 6 · Pilot plan | Chia theo nhân viên, 20 người mỗi nhóm, `noi_dia` + `hang_nang`. Mức +5 điểm cần 1.251 yc/nhóm, chia theo nhân viên cần 84 người (có 40), nên chấp nhận mức chênh 6 điểm: 859/nhóm, ≥ 299 yc mỗi nhân viên (DE 6,96); power chỉ 0,64 nếu tác động thật là 5 điểm. 3 luật dừng (an toàn, chi phí, sử dụng); quyết định ngày 05/01/2027 (`pilot_plan.yaml`) | Xong, có bằng chứng | Giám đốc vận hành |
| 7 · Rủi ro kinh tế | Làm lại ×2: CPS +51,8% lên 6.787 đ; xem lại 100%: 11.743–12.415 đ (0,98–1,03x), mất lợi thế; khối lượng còn một nửa: cố định 2.370 đ/việc [sim] (`chi_so.md` E2) | Giả lập | PM trợ lý hoàn phí |

**Đề xuất: Go có điều kiện** cho pilot `noi_dia` + `hang_nang`. Chi phí trong phạm vi chỉ bằng 0,38x mức nhân viên tự làm [sim], nhưng có hai con số bất lợi: power 0,64 ở mức 5 điểm, và lợi thế chi phí mất hết nếu phải xem lại 100%.

- Sửa lỗi hoàn hai lần (ca 20) bằng khoá chống trùng, và chỉ báo "đã hoàn" khi sổ cái trả ok (ca 7) · Kỹ sư trưởng agent · kiểm tra trước ngày bắt đầu pilot.
- Ký chấp nhận mức chênh 6 điểm, power 0,64 nếu tác động thật là 5 điểm · Giám đốc vận hành · trước ngày bắt đầu pilot.
- Bật đủ 10 event có `trace_id`; thay phút xem lại, làm lại [sim] bằng phút đo thật · PM trợ lý hoàn phí · cuối tuần 1.
- Giảm tỉ lệ xem lại theo bậc; dừng mở rộng nếu tỉ lệ xem lại còn > 50% ở bước rollout 25% · Trưởng nhóm CSKH · cuối tuần 2.
