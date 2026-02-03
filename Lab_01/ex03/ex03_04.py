def tryCapPhanTu(tupleData):
    first = tupleData[0]
    last = tupleData[-1]
    return first, last


inputTuple = eval(input("Nhập tuple (ex: 1,2,3): "))
first, last = tryCapPhanTu(inputTuple)

print("Phần tử đầu tiên: ", first)
print("Phần tử cuối cùng: ", last)
