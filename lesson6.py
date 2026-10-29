print("Задание 1. Подсчет нулей")

n = int(input("Сколько чисел вводим: "))
zeros = 0

for i in range(n):
    number = int(input("Введите число: "))
    if number == 0:
        zeros += 1

print("Количество нулей:", zeros)

print()
print("Задание 2. Количество делителей")

x = int(input("Введите натуральное число: "))
count = 0
i = 1

while i * i <= x:
    if x % i == 0:
        count += 1
        if i != x // i:
            count += 1
    i += 1

print("Количество делителей:", count)

print()
print("Задание 3. Четные числа на отрезке")

a = int(input("Введите A: "))
b = int(input("Введите B: "))

for i in range(a, b + 1):
    if i % 2 == 0:
        print(i, end=" ")
print()
