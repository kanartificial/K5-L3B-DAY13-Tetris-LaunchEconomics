# Bảng chi phí · Nhiệm vụ A và B

Số tính bằng `src/lab13.py`. Mọi con số tính từ cột `_simulated` ghi nhãn `simulated`. Mỗi câu trả lời không quá ba dòng, có ít nhất một con số.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Kết quả của nhóm |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 |

**Kết luận:** Cả ba phép thử đáp án biết trước đều đạt. Kết quả tính toán khớp với giá trị kỳ vọng của công thức.

## A2 · Mô hình chi phí từ trace

| Khoản | Số tiền (đ) | Nguồn | Nhãn |
| --- | ---: | --- | --- |
| Token | 245.585 | `logix_runs.csv` | Đo từ trace |
| Tool | 84.000 | `logix_runs.csv` | Đo từ trace |
| Trong đó, chi phí lần chạy thứ 2 và 3 | 93.804 | `attempt > 1` | Đo từ trace |
| Xem lại | 1.780.000 | `phut_xem_lai_simulated` | simulated |
| Làm lại | 2.264.000 | `phut_lam_lai_simulated` | simulated |
| Tổng chi phí | 4.373.585 | Token + Tool + Xem lại + Làm lại | |
| Số việc thành công | 978 | `ket_qua == thanh_cong` | |
| Chi phí mỗi việc thành công (CPS) | 4.472 | Tổng chi phí / Số việc thành công | |
| Hóa đơn token và tool chia cho số yêu cầu | 274,7 | (Token + Tool) / 1.200 | |

- Chi phí mỗi việc thành công gấp bao nhiêu lần "hoá đơn chia số yêu cầu"? ...
- Khoản nào chiếm tỉ trọng lớn nhất trong tổng chi phí, bao nhiêu phần trăm? ...

- CPS cao gấp **16,3 lần** hóa đơn token và tool chia cho số yêu cầu. Điều này cho thấy chi phí nhân sự xem lại và làm lại chiếm phần đáng kể trong tổng chi phí.
- Khoản chiếm tỷ trọng lớn nhất là **làm lại: 51,8%** tổng chi phí, tiếp theo là xem lại: 40,7%.
- Chi phí lần chạy thứ 2 và 3 là 93.804đ, được thống kê riêng để đánh giá chi phí chạy lại, không cộng thêm vào tổng CPS vì token và tool đã bao gồm mọi lần chạy.

## A3 · Tách theo loại yêu cầu

| Loại | Số yêu cầu | Tỉ lệ thành công | Số lần chạy mỗi yêu cầu | Chi phí mỗi việc thành công | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: | ---: |
| noi_dia | 824 | 95,0% | 1,11 | 2.696 | 0,22x |
| hang_nang | 158 | 74,1% | 1,47 | 8.221 | 0,69x |
| quoc_te | 150 | 27,3% | 2,32 | 22.515 | 1,88x |
| doi_tac | 68 | 54,4% | 1,88 | 10.215 | 0,85x |

- Loại nào không đáng để trợ lý xử lý? Với loại đó, cho chạy lại tới 3 lần có giúp không? ...
- Loại `quoc_te` không phù hợp để trợ lý tự xử lý theo mô hình hiện tại vì CPS đạt 22.515đ, cao hơn 1,88 lần chi phí nhân viên tự xử lý (12.000đ).
- Cho chạy lại đến 3 lần không giải quyết được vấn đề vì tỉ lệ thành công ở lần chạy thứ 3 chỉ còn 2,2% đối với yêu cầu quốc tế.
- Nên ưu tiên trợ lý xử lý `noi_dia` và `hang_nang`; cân nhắc chuyển `quoc_te` sang nhân viên xử lý.


## A4 · Chi phí cố định (phạm vi noi_dia + hang_nang)

| Khối lượng | Việc thành công mỗi tháng | Chi phí cố định mỗi việc | Chi phí mỗi việc thành công + cố định | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: |
| 45.000 yêu cầu/tháng | 33.750 | 1.185 | 4.599 | 0,38x |
| Một nửa khối lượng (22.500) | 16.875 | 2.370 | 5.784 | 0,48x |

- Chi phí cố định có đổi kết luận không? Ở khối lượng nào? ...
- Chi phí cố định không làm thay đổi kết luận: trợ lý vẫn có chi phí thấp hơn nhân viên tự xử lý ở cả hai mức khối lượng.
- Khi khối lượng giảm một nửa, chi phí cố định phân bổ trên mỗi việc thành công tăng từ 1.185đ lên 2.370đ.
- Vì vậy, duy trì khối lượng xử lý lớn giúp tận dụng hiệu quả hơn khoản đầu tư cố định 40 triệu đồng/tháng.

## B1 · Đổi từng yếu tố

| Kịch bản | Cách tính | Chi phí mỗi việc thành công | Thay đổi (%) |
| --- | --- | ---: | ---: |
| Giá token gấp đôi | 52 đ và 260 đ cho 1.000 token; giá tool giữ nguyên | 4.723 đ | +5,6% |
| Giá token giảm một nửa | 13 đ và 65 đ; giá tool giữ nguyên | 4.346 đ | -2,8% |
| Tỉ lệ xem lại gấp đôi | Tiền xem lại × 2 | 6.292 đ | +40,7% |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại ÷ 2 | 3.562 đ | -20,3% |
| Số ca làm lại gấp đôi | Tiền làm lại × 2 | 6.787 đ | +51,8% |
| Số ca làm lại giảm một nửa | Tiền làm lại ÷ 2 | 3.315 đ | -25,9% |
| Lương nhân viên tăng 25% | 2.500 đ mỗi phút | 5.506 đ | +23,1% |
| Chỉ cho chạy tối đa 2 lần | Bỏ lần chạy có attempt > 2; yêu cầu có so_lan_chay > 2 coi là chuyen_nhan_vien | 4.237 đ | -5,2% |
| Chỉ cho chạy 1 lần | Như trên với giới hạn 1 | 4.111 đ | -8,1% |

**Nhận xét:** Chi phí làm lại là yếu tố ảnh hưởng lớn nhất đến CPS (+51,8% khi tăng gấp đôi), tiếp theo là chi phí xem lại (+40,7%). Trong khi đó, giá token tăng gấp đôi chỉ khiến CPS tăng 5,6%. Vì vậy, nhóm nên ưu tiên tối ưu quy trình xem lại và giảm số ca làm lại thay vì chỉ tập trung giảm chi phí token.


## B2 · Đổi một cặp và xếp hạng

- Giá token gấp đôi cùng lúc tỉ lệ xem lại gấp đôi: ...
- Xếp hạng ba yếu tố ảnh hưởng mạnh nhất: 1. ... · 2. ... · 3. ...

- Giá token gấp đôi cùng lúc tỉ lệ xem lại gấp đôi: **6.543 đ (+46,3%)** [sim].
- Xếp hạng ba yếu tố ảnh hưởng mạnh nhất:
  1. Số ca làm lại tăng gấp đôi: **+51,8%**.
  2. Tỉ lệ xem lại tăng gấp đôi: **+40,7%**.
  3. Lương nhân viên tăng 25%: **+23,1%**.

## B3 · Giới hạn chạy lại có thật sự rẻ hơn

| Giới hạn | Tổng chi phí trợ lý | Số yêu cầu không thành công | Chi phí cả hệ thống | Chi phí mỗi việc thành công |
| --- | ---: | ---: | ---: | ---: |
| 1 lần | 3.621.781 đ [sim] | 319 | 7.449.781 đ [sim] | 4.111 đ [sim] |
| 2 lần | 4.093.220 đ [sim] | 234 | 6.901.220 đ [sim] | 4.237 đ [sim] |
| 3 lần | 4.373.585 đ [sim] | 222 | 7.037.585 đ [sim] | 4.472 đ [sim] |

- Giới hạn nào rẻ nhất cho công ty? Có trùng với giới hạn cho chi phí mỗi việc thành công thấp nhất không? ...

- **Giới hạn 2 lần chạy rẻ nhất cho công ty**, với chi phí cả hệ thống là 6.901.220 đ.
- Không trùng với giới hạn có CPS thấp nhất: giới hạn 1 lần có CPS thấp nhất (4.111 đ), nhưng có tới 319 yêu cầu không thành công và chi phí cả hệ thống cao nhất (7.449.781 đ).
- Giới hạn 3 lần giúp giảm số yêu cầu thất bại xuống 222, nhưng chi phí cả hệ thống tăng lên 7.037.585 đ.

**Kết luận:** Giới hạn 2 lần chạy là phương án cân bằng tốt nhất giữa chi phí trợ lý và chi phí xử lý các yêu cầu không thành công.


## B4 · Nếu phải xem lại tất cả

- Chi phí mỗi việc thành công khi xem lại 100% (`noi_dia` + `hang_nang`), so với 12.000 đ: ...
- Kết quả này nói gì về thứ pilot cần học được? ...

- Chi phí mỗi việc thành công khi xem lại 100% (`noi_dia` + `hang_nang`), so với 12.000 đ:
  - Kịch bản dễ cho (làm lại 9 phút/ca): **11.743 đ/việc**, tương đương 0,98 lần baseline, thấp hơn baseline một chút.
  - Kịch bản theo thời gian làm lại trung bình thực tế (15,3 phút/ca): **12.415 đ/việc**, tương đương 1,03 lần baseline, cao hơn baseline khoảng 3,5%.
  - Thời gian xem lại hòa vốn lần lượt không quá 5,1 phút/ca và 4,8 phút/ca.

- Kết quả này cho thấy hiệu quả kinh tế của trợ lý phụ thuộc rất lớn vào thời gian nhân viên phải xem lại và làm lại. Nếu phải xem lại toàn bộ yêu cầu và thời gian làm lại theo mức trung bình thực tế, chi phí trợ lý có thể cao hơn phương án nhân viên tự xử lý. Vì vậy, pilot cần đo lường thực tế thời gian review, tỷ lệ rework, thời gian xử lý lại và tỷ lệ thành công cuối cùng. Mục tiêu không chỉ là giảm chi phí token mà còn phải giảm khối lượng công việc thủ công của nhân viên.
