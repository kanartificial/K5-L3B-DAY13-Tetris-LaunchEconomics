"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=GIA_VAO, gia_ra=GIA_RA, gia_tool=GIA_TOOL, luong_phut=LUONG_PHUT,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, chay_lai, xem_lai, lam_lai, tong, thanh_cong, cps, hoa_don_moi_yc.
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × luong_phut. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    chay_lai = (tien_token + tien_tool)[runs['attempt'] > 1].sum()
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(
        token=tien_token.sum(),
        tool=tien_tool.sum(),
        chay_lai=chay_lai,
        xem_lai=xem_lai,
        lam_lai=lam_lai,
        tong=tong,
        thanh_cong=thanh_cong,
        cps=tong / thanh_cong,
        hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs),
    )


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)

    print('=== A1 · Ba phép thử đáp án biết trước ===')
    kiem_tra_dap_an_biet_truoc()
    print(f'so_lan_chay_ky_vong(0.8, 2)               = {so_lan_chay_ky_vong(0.8, 2):.2f}')
    print(f'so_lan_chay_ky_vong(0.8)                  = {so_lan_chay_ky_vong(0.8):.2f}')
    print(f'he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) = {he_so_chi_phi_moi_viec_thanh_cong(0.8, 3):.2f}')

    print('\n=== A2 · Mô hình chi phí từ trace ===')
    ket_qua = mo_hinh(runs, reqs)
    for ten, gia_tri in ket_qua.items():
        if ten == 'hoa_don_moi_yc':
            print(f'{ten:16s} {gia_tri:>14,.1f}')
        else:
            print(f'{ten:16s} {gia_tri:>14,.0f}')
    print(f'Ti le CPS / hoa_don_moi_yc : {ket_qua["cps"] / ket_qua["hoa_don_moi_yc"]:.1f}x')
    print(f'Ti trong lam_lai [sim]     : {ket_qua["lam_lai"] / ket_qua["tong"] * 100:.1f}%')
    print(f'Ti trong xem_lai [sim]     : {ket_qua["xem_lai"] / ket_qua["tong"] * 100:.1f}%')
    khong_tc = len(reqs) - ket_qua['thanh_cong']
    cp_he_thong_moi_yc = (ket_qua['tong'] + khong_tc * BASELINE) / len(reqs)
    print(f'Chi phi ca he thong / yc [sim]: {cp_he_thong_moi_yc:,.0f} d ({cp_he_thong_moi_yc / BASELINE:.2f}x baseline)')

    print('\n=== A3 · Tách theo loại yêu cầu ===')
    print(f'{"Loai":12s} {"So YC":>6s} {"Ti le TC":>9s} {"Lan chay/YC":>12s} {"CPS [sim]":>12s} {"So 12k":>8s}')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        sub = reqs[reqs['loai'] == loai]
        kq = mo_hinh(runs, sub)
        ti_le_tc = kq['thanh_cong'] / len(sub) * 100
        lan_chay_tb = sub['so_lan_chay'].mean()
        print(f'{loai:12s} {len(sub):6d} {ti_le_tc:8.1f}% {lan_chay_tb:12.2f} {kq["cps"]:12,.0f} {kq["cps"] / BASELINE:7.2f}x')

    print('\nTi le status == ok theo loai va lan thu (attempt):')
    runs_loai = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    runs_loai['is_ok'] = runs_loai['status'] == 'ok'
    bang_ok = runs_loai.pivot_table(index='loai', columns='attempt', values='is_ok', aggfunc='mean') * 100
    print(bang_ok.loc[['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']].round(1).to_string())

    print('\n=== A4 · Chi phí cố định (phạm vi noi_dia + hang_nang) ===')
    CHI_PHI_CO_DINH = 40_000_000
    KHOI_LUONG_THANG = 45_000
    pham_vi = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    kq_pv = mo_hinh(runs, pham_vi)
    ti_le_tc_mau = kq_pv['thanh_cong'] / len(reqs)
    print(f'CPS bien doi pham vi [sim]: {kq_pv["cps"]:,.0f} d ({kq_pv["thanh_cong"]} viec TC / {len(reqs)} mau)')
    for nhan, khoi_luong in [('45.000 yc/thang', KHOI_LUONG_THANG), ('Mot nua (22.500)', KHOI_LUONG_THANG // 2)]:
        viec_tc_thang = khoi_luong * ti_le_tc_mau
        co_dinh_moi_viec = CHI_PHI_CO_DINH / viec_tc_thang
        tong_cps = kq_pv['cps'] + co_dinh_moi_viec
        print(f'{nhan:18s} | TC/thang: {viec_tc_thang:8,.0f} | Co dinh/viec: {co_dinh_moi_viec:6,.0f} d | CPS+CD [sim]: {tong_cps:6,.0f} d ({tong_cps / BASELINE:.2f}x)')

    # TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    # TODO CP4 · Nhiệm vụ D: cỡ mẫu.
    #   from statsmodels.stats.proportion import proportion_effectsize
    #   from statsmodels.stats.power import NormalIndPower
