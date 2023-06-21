import math

r = int(input("Enter the radius: "))
summation = 0

for x in range (-r,r):
    for y in range (-r,r):
        if (math.sqrt(x**2 + y**2) <= r):
            summation += 1

coef = 1/(r**2)

result = coef * summation

print(coef)

print(summation)

print(result)