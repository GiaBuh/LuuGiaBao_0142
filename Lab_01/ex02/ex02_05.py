soGioLam = float(input("Nhập số giờ làm mỗi tuần: "))
luongGio = float(input("Nhập thu lao trên mỗi giờ tiêu chuẩn: "))
soGioTieuChuan = 44
gioVuotChuan = max(0, soGioLam - soGioTieuChuan)

thucLinh = soGioTieuChuan * luongGio + gioVuotChuan * luongGio * 1.5

print(f"Số tiền thực lĩnh của nhân viên: {thucLinh}")
