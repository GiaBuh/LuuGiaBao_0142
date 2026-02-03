def daoNguocList(lst):
    return lst[::-1]

inputList = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, inputList.split(',')))

listDaoNguoc = daoNguocList(numbers)

print("Danh sách sao khi đảo ngược: ", listDaoNguoc)