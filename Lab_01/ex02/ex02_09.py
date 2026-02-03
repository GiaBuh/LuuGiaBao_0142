def isPrime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

number = int(input("Nhập số nguyên tố cần kiểm tra: "))
if isPrime(number):
    print(number, " là số nguyên tố")
else:
    print(number, " là không phải số nguyên tố")
