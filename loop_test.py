x = 4
y = 4

for i in range(x):
    for j in range(y):
        print("{},{}".format(i,j))

print("---")

for i in range(x*y):
    print("{},{}".format(i//y,i%y))
