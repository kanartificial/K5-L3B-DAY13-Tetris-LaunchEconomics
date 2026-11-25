# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | 994 / 1.200 = **82,83%** |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại (`duoc_xem_lai = 1`) | (41 + 7) / 177 = **27,12%** |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | 51 / 1.200 = **4,25%** |
| Dùng | Tỉ lệ yêu cầu nhóm can thiệp được mở bằng trợ lý | Số yêu cầu nhóm can thiệp có ít nhất một lần mở bằng trợ lý chia tổng số yêu cầu nhóm can thiệp | Không cần tính |
| An toàn | Tỉ lệ yêu cầu hoàn sai số tiền trong mẫu kiểm toán | Số yêu cầu đã kiểm toán có số tiền đã hoàn khác số tiền đúng chia tổng số yêu cầu đã kiểm toán | Không cần tính |

Chỉ số trong đợt chạy thử là **82,83%** (chỉ số chính), tính trên 1.200 yêu cầu giả lập (`src/logix_requests.csv`). Đợt chạy thử không có nhóm đối chứng.

## Danh sách event

Ít nhất sáu event, mỗi event có `trace_id` để nối với trace của agent.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | `request_id`, `created_at`, `loai`, `so_tien`, `arm`, `trace_id` | Khi khách gửi yêu cầu |
| `agent_run_completed` | Agent | `request_id`, `attempt`, `tokens_in`, `tokens_out`, `tool_calls`, `status`, `trace_id` | Sau mỗi lần chạy, kể cả khi lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | `request_id`, `staff_id`, `so_tien_de_xuat`, `trace_id` | Khi gợi ý hiển thị |
| `staff_review_decision` | Giao diện nhân viên | `request_id`, `quyet_dinh_xem_lai` (`giu`/`sua`/`bo`), `phut_xem_lai`, `trace_id` | Khi nhân viên chốt quyết định xem lại |
| `staff_rework_completed` | Giao diện nhân viên | `request_id`, `phut_lam_lai`, `ly_do`, `trace_id` | Khi nhân viên làm lại xong |
| `refund_ledger_write` | Dịch vụ sổ cái | `request_id`, `idempotency_key`, `so_tien`, `ket_qua`, `trace_id` | Khi có kết quả ghi sổ |
| `handoff_to_staff` | Agent | `request_id`, `reason`, `tom_tat`, `trace_id` | Khi chuyển yêu cầu cho nhân viên |
| `ticket_closed` | Hệ thống ticket | `request_id`, `closed_at`, `trace_id` | Khi đóng yêu cầu |
| `ticket_reopened` | Hệ thống ticket | `request_id`, `reopened_at`, `ly_do`, `trace_id` | Khi yêu cầu được mở lại |
| `audit_sample_checked` | Kế toán | `request_id`, `so_tien_da_hoan`, `so_tien_dung`, `trace_id` | Khi chốt kết quả kiểm toán từng yêu cầu trong mẫu hằng tuần |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, ghi event dùng để tính. Chỉ số nào không tính được từ danh sách event thì chưa đo được.

- Dùng `request_id` để đếm mỗi yêu cầu một lần. Dùng `trace_id` của từng lần chạy để nối với trace agent qua `agent_run_completed` và `request_id` để nối các event cấp yêu cầu.
- **Đóng trong 24 giờ và không mở lại trong 7 ngày:** lấy mẫu số và thời điểm tạo từ `refund_request_created`. Dùng lần đóng đầu tiên trong `ticket_closed` để kiểm tra mốc 24 giờ, rồi dùng `ticket_reopened` để kiểm tra 7 ngày sau khi đóng.
- **Bỏ qua gợi ý:** từ `staff_review_decision`, chia số yêu cầu có quyết định cuối là `sua` hoặc `bo` cho số yêu cầu có quyết định xem lại.
- **Lỗi lọt đến khách:** dùng `ticket_closed` và `ticket_reopened` để đếm yêu cầu mở lại trong 7 ngày sau lần đóng đầu tiên, chia cho tổng số yêu cầu từ `refund_request_created`.
- **Mở bằng trợ lý:** một yêu cầu được tính là đã mở bằng trợ lý khi thao tác mở khởi động một lần chạy. Đếm yêu cầu nhóm can thiệp có `agent_run_completed` (kể cả lần chạy lỗi), chia tổng số yêu cầu thuộc nhóm này theo `arm` của `refund_request_created`. Nếu thao tác mở có thể xảy ra mà không khởi động lần chạy, cần thêm event ghi nhận thao tác mở để đo đủ.
- **Hoàn sai số tiền:** dùng `audit_sample_checked` để so sánh hai số tiền và tính tỉ lệ trên các yêu cầu đã kiểm toán.
- Với hai chỉ số dùng mốc 7 ngày, chỉ chốt số liệu khi đã đủ thời gian theo dõi.

## E2 · Rủi ro kinh tế

Tác động kinh tế lấy từ các mục B1, B4 và A4 trong [bảng chi phí](bang_chi_phi.md).

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | Chi phí mỗi việc thành công tăng 51,8%, lên 6.787 đ [simulated, B1] | Tỉ lệ làm lại theo tuần > 7%. Đợt chạy thử có 48/982 ca làm lại (4,9%) trong phạm vi pilot [simulated] | Thu hẹp về `noi_dia` và rà 20 trace làm lại | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài trong phạm vi `noi_dia` và `hang_nang` | 11.743 đ/việc thành công nếu làm lại 9 phút/ca (0,98 lần mức 12.000 đ), hoặc 12.415 đ nếu làm lại 15,3 phút/ca (1,03 lần) [simulated, B4] | Tỉ lệ yêu cầu được xem lại vẫn > 50% ở cuối bước rollout 25% | Giảm tỉ lệ xem lại theo từng bậc khi tỉ lệ sửa hoặc bỏ gợi ý < 15% và các ngưỡng an toàn của pilot được đáp ứng | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Chi phí cố định 40 triệu đ/tháng tương đương 1.185 đ/việc thành công ở 45.000 yêu cầu/tháng và 2.370 đ/việc khi còn 22.500 yêu cầu/tháng [simulated, A4] | Số việc thành công theo tuần < 50% kế hoạch | Tạm dừng mở rộng pilot và rà soát hợp đồng chi phí cố định | PM trợ lý hoàn phí |
