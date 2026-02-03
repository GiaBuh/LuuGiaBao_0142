def chiaHetCho5(soNhiPhan):
    soThapPhan = int(soNhiPhan,2)
    if soThapPhan % 5 == 0:
        return True
    return False

chuoiSoNhiPhan = input("Nhập số nhị phân (phân tách bởi dấu phẩy): ")
listSoNhiPhan = chuoiSoNhiPhan.split(',')
soChiaHetCho5 = []
for so in listSoNhiPhan:
    if(chiaHetCho5(so)):
        soChiaHetCho5.append(so)

if len(soChiaHetCho5) > 0:
    ketQua = ','.join(soChiaHetCho5)
    print("Các số nhị phân chia hết cho 5 là: ", ketQua)
else:
    print("Không có số nhị phân nào chia hết cho 5") 