def xoaPhanTu(dic, key):
    if key in dic:
        del dic[key]
        return True
    return False

myDic = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

key_to_delete = 'b'
res = xoaPhanTu(myDic, key_to_delete)
if res:
    print("Phần tử đã xoá từ dictionary: ", myDic)
else:
    print("Không tìm thấy phần tử trong dictionary")