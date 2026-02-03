def daoNguocChuoi(chuoi):
    return chuoi[::-1]
inputString = input("Nhập chuỗi cần đảo ngược: ")
print("Chuỗi sau khi đảo ngược: ", daoNguocChuoi(inputString))