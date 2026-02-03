def tinhTongSoChan(list):
    tong = 0
    for num in list:
        if num % 2 == 0:
            tong += num
    return tong

inputList = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, inputList.split(',')))

tongChan = tinhTongSoChan(numbers)
print("Tổng các số chẵn trong danh sách là: ", tongChan)

