# Báo cáo cá nhân — LyHaTranTran-2A202603968

## 1. Thông tin thành viên

- Họ tên: Lý Hà Trân Trân
- MSSV: 2A202603968
- Email: 26ai.tranlht@vinuni.edu.vn
- Vai trong nhóm: người gắn nhãn 2 kiêm giữ hồ sơ

## 2. Phần việc phụ trách

- CP3: gắn nhãn độc lập 20 ca lỗi, so nhãn với người gắn nhãn 1, thống nhất các ca lệch, bảng khắc phục 5 ca.
- Giữ hồ sơ: điền `report/team/ho_so_launch_v0.md` dần theo từng checkpoint, chốt đề xuất cuối ở CP5.

## 3. Đóng góp cụ thể

- **Gắn nhãn (CP3):** tự gắn 20 ca, không trao đổi với người gắn nhãn 1. Đồng thuận 17/20 = 85%; ba ca lệch (6, 8, 20) được hai người thống nhất và ghi quy tắc phân biệt.
- **Bảng khắc phục:** 5 ca 1, 2, 3, 11, 12, mỗi loại một ca, có event, ngưỡng và tần suất phát hiện, người phụ trách là một vai trò.
- **Gỡ xung đột merge:** hai bộ nhãn nằm trên hai nhánh; khi merge, giữ đúng bộ nhãn người gắn nhãn 1 đã commit (`f3867a2`), tính lại đồng thuận từ 90% xuống 85% thay vì sửa nhãn cho khớp.
- **Hồ sơ launch v0:** điền đủ bảy mục với con số chính, trạng thái và vai trò phụ trách; đề xuất **Go có điều kiện** kèm hai con số bất lợi (power 0,64 ở mức 5 điểm; xem lại 100% làm chi phí lên 0,98–1,03x mức nhân viên tự làm [sim]).
- **CP4, CP5:** điền phần chú thích D1, D2 trong `pilot_plan.yaml`, bản nháp `group_report.md`.

## 4. Bằng chứng

- Commit: `e17a201` (CP3 bảng lỗi), `a06716c` (bảng khắc phục mới), `dbd5754` (merge, sửa đồng thuận 17/20), `15c1280` (hồ sơ CP5, pilot_plan, group_report); PR #1 nhánh `ho-so-launch-v0`.
- File: `report/team/bang_loi.md` (cột nhãn người 2, bảng khắc phục), `report/team/ho_so_launch_v0.md`, `report/team/group_report.md`.
- Con số chính: đồng thuận 85% (17/20); CPS phạm vi pilot 4.599 đ = 0,38x [sim]; n hiệu dụng 859 mỗi nhóm.

## 5. Công cụ AI đã dùng

- **Claude Code** trong VS Code:
  - Chạy `src/lab13.py` để lấy số và điền hồ sơ từ output.
  - Viết bảng khắc phục, phần chú thích D1–D2, bản nháp báo cáo nhóm.
  - Gỡ xung đột merge `bang_loi.md`.
- **Không dùng AI để gắn nhãn 20 ca hay chấm chéo.** AI chỉ đưa định nghĩa năm loại, nhãn do tôi tự gắn.
- **Cách tự kiểm tra:**
  - Đối chiếu từng con số trong hồ sơ với output `python lab13.py` và `bang_chi_phi.md`.
  - Chạy `yaml.safe_load` và `grep` dấu `?` cho `pilot_plan.yaml`.
  - Chạy `grep -rni production report/team` (không in gì).
  - Kiểm tra cột nhãn người 1 khớp commit của người gắn nhãn 1.
- **Lỗi AI gây ra và đã sửa:** một lần AI ghi đè nhầm dòng nhãn ca 9–13 khi sửa bảng khắc phục (commit `a06716c`). Lỗi được phát hiện khi gỡ xung đột và sửa ở commit `dbd5754`.

## 6. Tự đánh giá

- **Làm tốt:**
  - Gắn nhãn độc lập thật sự, không xem nhãn người 1 trước khi tự gắn.
  - Khi gỡ xung đột, chọn tính lại đồng thuận (90% xuống 85%) thay vì sửa nhãn cho khớp, để con số phản ánh đúng mức đồng thuận thật.
  - Mọi con số trong hồ sơ launch đều đối chiếu được với output `lab13.py` hoặc `bang_chi_phi.md`; đề xuất Go có điều kiện ghi rõ cả số bất lợi.
- **Chưa tốt:**
  - Để AI sửa trực tiếp `bang_loi.md` mà không xem kỹ diff trước khi commit, dẫn đến ghi đè nhầm nhãn ca 9–13 (`a06716c`). Lỗi chỉ được phát hiện muộn, lúc merge.
  - Làm trên nhánh riêng quá lâu mới merge nên xung đột lớn hơn cần thiết.
- **Lần sau:**
  - Luôn đọc `git diff` trước khi commit, nhất là khi AI sửa file có dữ liệu do người khác nhập.
  - Pull và merge `main` thường xuyên hơn, sau mỗi checkpoint.
- **Mức hoàn thành:** hoàn thành đủ phần việc được giao (gắn nhãn CP3, bảng khắc phục, hồ sơ launch v0 đến CP5).
