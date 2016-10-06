total = 0
for natnum in range(1000):
    if (natnum%3 == 0 or natnum%5 == 0):
        total = total+natnum
print total