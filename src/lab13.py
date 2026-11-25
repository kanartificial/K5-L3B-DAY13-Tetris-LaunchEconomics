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

    print('\n=== B1 · Bảng độ nhạy (đổi từng yếu tố) ===')
    kich_ban = {
        'Gia token gap doi':      dict(gia_vao=52, gia_ra=260),
        'Gia token giam mot nua': dict(gia_vao=13, gia_ra=65),
        'Xem lai gap doi':        dict(he_so_xem_lai=2.0),
        'Xem lai giam mot nua':   dict(he_so_xem_lai=0.5),
        'Lam lai gap doi':        dict(he_so_lam_lai=2.0),
        'Lam lai giam mot nua':   dict(he_so_lam_lai=0.5),
        'Luong tang 25%':         dict(luong_phut=2500),
        'Toi da 2 lan chay':      dict(max_lan_chay=2),
        'Chi 1 lan chay':         dict(max_lan_chay=1),
    }
    goc_cps = ket_qua['cps']
    print(f'{"Goc (A2)":25s} {goc_cps:8,.0f} d')
    kq_b1 = {}
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        pct = (cps / goc_cps - 1) * 100
        kq_b1[ten] = (cps, pct)
        print(f'{ten:25s} {cps:8,.0f} d ({pct:+6.1f}%)')

    # Tu kiem tra tinh doi xung giam mot nua == -1/2 gap doi
    for cap_doi, cap_nua in [
        ('Gia token gap doi', 'Gia token giam mot nua'),
        ('Xem lai gap doi', 'Xem lai giam mot nua'),
        ('Lam lai gap doi', 'Lam lai giam mot nua'),
    ]:
        assert abs(kq_b1[cap_nua][1] + kq_b1[cap_doi][1] / 2) < 1e-9

    print('\n=== B2 · Đổi một cặp và xếp hạng ===')
    cps_cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2.0)['cps']
    pct_cap = (cps_cap / goc_cps - 1) * 100
    print(f'Token x2 + Xem lai x2 [sim]: {cps_cap:,.0f} d ({pct_cap:+.1f}%)')
    print('Xep hang 3 yeu to manh nhat: 1. So ca lam lai (+51.8%) | 2. Ti le xem lai (+40.7%) | 3. Luong nhan vien (+23.1%)')

    print('\n=== B3 · Giới hạn chạy lại có thật sự rẻ hơn ===')
    print(f'{"Gioi han":10s} {"Tong tro ly [sim]":>18s} {"Khong TC":>10s} {"Ca he thong [sim]":>18s} {"CPS [sim]":>12s}')
    for gh in [1, 2, 3]:
        kq_gh = mo_hinh(runs, reqs, max_lan_chay=gh)
        khong_tc_gh = len(reqs) - kq_gh['thanh_cong']
        ca_he_thong = kq_gh['tong'] + khong_tc_gh * BASELINE
        print(f'{str(gh) + " lan":10s} {kq_gh["tong"]:18,.0f} {khong_tc_gh:10d} {ca_he_thong:18,.0f} {kq_gh["cps"]:12,.0f}')

    print('\n=== B4 · Nếu phải xem lại tất cả (noi_dia + hang_nang) ===')
    runs_pv = runs[runs['request_id'].isin(pham_vi['request_id'])]
    yc_co_ok = runs_pv.loc[runs_pv['status'] == 'ok', 'request_id'].nunique()
    so_ca_lam_lai_pv = int((pham_vi['ket_qua'] == 'lam_lai').sum())
    so_viec_tc_pv = int((pham_vi['ket_qua'] == 'thanh_cong').sum())
    token_tool_pv = kq_pv['token'] + kq_pv['tool']
    tien_xem_lai_100 = yc_co_ok * 5 * LUONG_PHUT

    phut_ll_tb = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()
    phut_ll_tv = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].median()

    print(f'So YC pham vi: {len(pham_vi)} | YC co it nhat 1 lan ok: {yc_co_ok} | Ca lam_lai: {so_ca_lam_lai_pv} | TC: {so_viec_tc_pv}')
    print(f'Token + tool pham vi: {token_tool_pv:,.0f} d | Xem lai 100% (5 phut): {tien_xem_lai_100:,.0f} d')
    print(f'Phut lam lai thuc te [sim] (toan bo ca lam_lai): TB = {phut_ll_tb:.1f} phut, trung vi = {phut_ll_tv:.1f} phut')

    for nhan, phut_ll in [('De cho (9 phut/ca)', 9.0), (f'Thuc te TB ({phut_ll_tb:.1f} phut/ca)', phut_ll_tb)]:
        tien_ll = so_ca_lam_lai_pv * phut_ll * LUONG_PHUT
        tong_b4 = token_tool_pv + tien_xem_lai_100 + tien_ll
        cps_b4 = tong_b4 / so_viec_tc_pv
        # Muc hoa von phut xem lai de cps_b4 <= BASELINE
        phut_hoa_von = (BASELINE * so_viec_tc_pv - token_tool_pv - tien_ll) / (yc_co_ok * LUONG_PHUT)
        print(f'  {nhan:26s} -> Lam lai: {tien_ll:10,.0f} d | Tong: {tong_b4:10,.0f} d | CPS [sim]: {cps_b4:6,.0f} d ({cps_b4 / BASELINE:.2f}x) | Hoa von xem lai <= {phut_hoa_von:.1f} phut')

    print('\n=== D1 · Cỡ mẫu cho pilot (baseline=0.70, alpha=0.05, power=0.80, ICC=0.02) ===')
    from statistics import NormalDist
    from statsmodels.stats.proportion import proportion_effectsize
    from statsmodels.stats.power import NormalIndPower

    def co_mau(p1, p2, alpha=0.05, power=0.80):
        za = NormalDist().inv_cdf(1 - alpha / 2)
        zb = NormalDist().inv_cdf(power)
        pb = (p1 + p2) / 2
        return math.ceil(
            (za * math.sqrt(2 * pb * (1 - pb))
             + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
            / (p2 - p1) ** 2
        )

    P1, ALPHA, POWER, ICC = 0.70, 0.05, 0.80, 0.02

    # a) Chia theo yeu cau (+5 diem)
    n_req_5 = co_mau(P1, 0.75, ALPHA, POWER)
    print(f'a) Chia theo yeu cau (+5 diem)           : {n_req_5:,d} yc/nhom')

    # b) Chia theo nhan vien, m = 75
    m_b = 75
    de_b = 1 + (m_b - 1) * ICC
    n_staff_b = math.ceil(n_req_5 * de_b)
    so_nv_nhom = math.ceil(n_staff_b / m_b)
    print(f'b) Theo nhan vien (m={m_b}, DE={de_b:.2f})      : {n_staff_b:,d} yc/nhom -> {so_nv_nhom} NV/nhom (tong {so_nv_nhom * 2} > 40: KHONG DU)')

    # c) 20 nhan vien moi nhom
    c_staff = 20
    n_eff_max_staff = c_staff / ICC
    print(f'c) 20 nhan vien/nhom (tran c/ICC)        : toi da {n_eff_max_staff:,.0f} < {n_req_5:,d} (KHONG DAT)')

    # d) 6 depot moi nhom
    c_depot = 6
    n_eff_max_depot = c_depot / ICC
    print(f'd) 6 depot/nhom (tran c/ICC)             : toi da {n_eff_max_depot:,.0f} < {n_req_5:,d} (KHONG DAT)')

    # e) Muc chenh 6 diem (+6 diem), 20 nhan vien moi nhom
    n_req_6 = co_mau(P1, 0.76, ALPHA, POWER)
    # Giai c_staff * m / (1 + (m - 1) * ICC) >= n_req_6
    # <=> m * (c_staff - n_req_6 * ICC) >= n_req_6 * (1 - ICC)
    m_e = math.ceil(n_req_6 * (1 - ICC) / (c_staff - n_req_6 * ICC))
    de_e = 1 + (m_e - 1) * ICC
    n_eff_e = c_staff * m_e / de_e
    print(f'e) Muc chenh +6 diem ({n_req_6:,d}/nhom), 20 NV : m >= {m_e} yc/NV (DE={de_e:.2f}, n_hieu_dung={n_eff_e:.1f})')

    # Power thuc te neu chon n=859 nhung tac dong that chi +5 diem
    es_5 = proportion_effectsize(0.75, P1)
    power_5_at_859 = NormalIndPower().power(effect_size=es_5, nobs1=n_req_6, alpha=ALPHA, ratio=1.0)
    print(f'   Power neu tac dong that chi +5 diem voi n={n_req_6}: {power_5_at_859:.2f}')

    print('\n=== D3 · Tỉ lệ mở lại trong 7 ngày hiện tại (cơ sở đặt luật an toàn) ===')
    mo_lai_toan_bo = reqs['mo_lai_trong_7_ngay'].mean() * 100
    so_mo_lai_toan_bo = int(reqs['mo_lai_trong_7_ngay'].sum())
    mo_lai_pv = pham_vi['mo_lai_trong_7_ngay'].mean() * 100
    so_mo_lai_pv = int(pham_vi['mo_lai_trong_7_ngay'].sum())
    print(f'Toan bo 1.200 yc              : {mo_lai_toan_bo:.2f}% ({so_mo_lai_toan_bo}/{len(reqs)})')
    print(f'Pham vi noi_dia + hang_nang   : {mo_lai_pv:.2f}% ({so_mo_lai_pv}/{len(pham_vi)})')
