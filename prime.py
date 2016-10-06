n = 600851475143
p = 2
while p * p < n:
    while n % p == 0:
        n = n / p
    p = p + 1
print (n)