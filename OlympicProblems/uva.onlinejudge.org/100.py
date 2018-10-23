def f(i):
    z = 1
    while i > 1:
        z += 1
        if i % 2 == 0:
            i //= 2
        else:
            i = 3*i + 1
    return z

""" while True:
    line = input()
    if not line or line == "\n":
       break
    i, j = map(int, line.split(" "))
    l = [f(k) for k in range(i, j + 1)]
    print("{i} {j} {m}".format(i = i, j = j, m = max(l)))
 """
n = int(input())
s = ""
while n > 1:
    s = s + str(n) + " "
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3*n + 1
print(s + "1")
