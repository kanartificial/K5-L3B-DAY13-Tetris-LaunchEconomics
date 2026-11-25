# Báo cáo cá nhân — KhongNgocAnh-2A202603974

## 1. Thông tin thành viên

- Họ tên: Khổng Ngọc Anh
- MSSV: 2A202603974
- Email: 26ai.anhkn2@vinuni.edu.vn
- GitHub: `kanartificial`
- Vai trong nhóm: Người viết code

## 2. Phần việc phụ trách

- Khởi tạo repo nhóm (`K5-L3B-DAY13-Tetris-LaunchEconomics`) và thiết lập môi trường chạy Python trong `src/`.
- Viết và chạy `src/lab13.py` cho các checkpoint **CP1 (Nhiệm vụ A)**, **CP2 (Nhiệm vụ B)** và **CP4 (Nhiệm vụ D)**.
- Xuất số liệu kiểm chứng để **Người kiểm số** đối chiếu và điền vào `report/team/bang_chi_phi.md`, `report/team/pilot_plan.yaml`.
- Cập nhật danh sách thành viên trong `TEAM.md`.

## 3. Đóng góp cụ thể

- **CP1 · Mô hình chi phí (A1–A4):**
  - Cài đặt 3 hàm A1 (`so_lan_chay_ky_vong`, `ti_le_thanh_cong`, `he_so_chi_phi_moi_viec_thanh_cong`) đạt cả 3 phép thử đáp án biết trước (`1,20` · `1,25` · `1,25`).
  - Cài đặt hàm `mo_hinh(runs, reqs, ...)` tính tổng chi phí `4.373.585 đ`, `978` việc thành công, **CPS = `4.472 đ`** (`simulated`), gấp `16,3×` hoá đơn token + tool mỗi yêu cầu (`274,7 đ`).
  - Tách chi phí theo 4 loại yêu cầu (`noi_dia`: `2.696 đ`, `hang_nang`: `8.221 đ`, `quoc_te`: `22.515 đ`, `doi_tac`: `10.215 đ`, `simulated`) và bảng tỉ lệ `status == 'ok'` theo lần thử `1/2/3`, chứng minh `quoc_te` không đáng xử lý và chạy lại không giúp.
  - Tính chi phí cố định `40 triệu đ/tháng` cho phạm vi `noi_dia` + `hang_nang`: `4.599 đ` (`0,38×`, `simulated`) ở `45.000 yc/tháng` và `5.784 đ` (`0,48×`, `simulated`) ở `22.500 yc/tháng`.
- **CP2 · Phân tích độ nhạy (B1–B4):**
  - Chạy 9 kịch bản đổi từng yếu tố (B1) kèm kiểm tra đối xứng, kịch bản đổi một cặp Token ×2 + Xem lại ×2 (`6.543 đ`, `+46,3%`, `simulated`, B2), xác định 3 yếu tố nhạy nhất: làm lại (`+51,8%`), xem lại (`+40,7%`), lương (`+23,1%`).
  - Tính chi phí cả hệ thống theo giới hạn 1, 2, 3 lần chạy (B3), xác nhận giới hạn **2 lần chạy** rẻ nhất cho công ty (`6.901.220 đ`, `simulated`).
  - Tính kịch bản xem lại 100% cho `noi_dia` + `hang_nang` (B4): `11.743 đ` (`0,98×`, làm lại 9 phút/ca) và `12.415 đ` (`1,03×`, làm lại thực tế TB `15,3 phút/ca`, `simulated`), kèm mức hoà vốn xem lại `≤ 5,1 phút` và `≤ 4,8 phút`.
- **CP4 · Cỡ mẫu và cơ sở luật an toàn (D1, D3):**
  - Cài đặt `co_mau` và dùng `statsmodels` (`proportion_effectsize`, `NormalIndPower`) tính đủ 5 câu D1: `1.251 yc/nhóm` (+5 điểm), `3.103 yc/nhóm` / `84 NV > 40` (m=75), trần `1.000` (20 NV/nhóm), trần `300` (6 depot/nhóm), và mức chênh +6 điểm (`859/nhóm`, `m ≥ 299 yc/NV`, `DE = 6,96`, power `0,64` nếu tác động thật là +5 điểm).
  - Tính tỉ lệ `mo_lai_trong_7_ngay` hiện tại: `4,25%` (`51/1.200`) toàn bộ và `3,97%` (`39/982`) trong phạm vi pilot làm căn cứ đặt luật dừng an toàn.

## 4. Bằng chứng

- **Commits đã thực hiện trên nhánh `main`:**
  - `e7b8766` — `code + TEAM.md`: hoàn thiện code CP1 (A1–A4) trong `src/lab13.py` và điền bảng thành viên `TEAM.md`.
  - `b90b7da` — `CP2`: hoàn thiện code CP2 (B1–B4) trong `src/lab13.py`.
  - `756bf83` — `code CP4`: hoàn thiện code CP4 (D1, D3) trong `src/lab13.py`.
- **File chính:** `src/lab13.py`, `TEAM.md`.
- **Kết quả chạy `python lab13.py`:** `Ba phép thử đáp án biết trước: ĐẠT`; khớp 100% số đối chiếu ở A2–A4, B1–B4 và D1/D3.

## 5. Công cụ AI đã dùng

- **Antigravity (Gemini):** hỗ trợ tóm tắt yêu cầu từng checkpoint, viết khung code và bảng in kết quả trong `src/lab13.py`, rà soát thiếu sót hồ sơ theo `SUBMISSION.md`.
- **Cách tự kiểm tra:** chạy trực tiếp `./.venv/bin/python lab13.py` trong `src/`, xác nhận 3 phép thử A1 đạt (`assert`), tự kiểm tra tính đối xứng độ nhạy B1, kiểm tra cú pháp YAML của `pilot_plan.yaml` bằng `yaml.safe_load`, và đối chiếu từng con số với slide chữa cùng người kiểm số.

## 6. Tự đánh giá

Hoàn thành đúng tiến độ và chính xác toàn bộ phần code CP1, CP2 và CP4, cung cấp số liệu kịp thời cho các thành viên hoàn thiện hồ sơ nhóm. Qua bài lab, tôi nắm rõ cách xây dựng mô hình chi phí thật (CPS) có tính cả chi phí vận hành của con người, phân tích độ nhạy và tính cỡ mẫu theo cụm khi thiết kế pilot. Điểm cần cải thiện là phối hợp cập nhật `TEAM.md` và báo cáo cá nhân sớm hơn thay vì đợi đến cuối buổi.
