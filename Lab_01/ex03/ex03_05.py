def demSoLanXuatHien(lst):
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict

inputStr = input("Nhập danh sách các từ (cách nhau bằng dấu cách)")
wordList = inputStr.split()

soLanXuatHien = demSoLanXuatHien(wordList)
print("Số lần xuất hiện của các phần tử : ", soLanXuatHien)