print("Задание 1. Перевернуть список")

n = int(input("Сколько чисел: "))
numbers = []

for i in range(n):
    number = int(input())
    numbers.append(number)

numbers.reverse()
print(*numbers)

print()
print("Задание 2. Сдвиг списка")

n = int(input("Сколько чисел: "))
numbers = list(map(int, input("Введите числа через пробел: ").split()))

numbers = [numbers[-1]] + numbers[:-1]
print(*numbers)

print()
print("Задание 3. Рыбаки и лодки")

m = int(input("Грузоподъемность лодки: "))
n = int(input("Количество рыбаков: "))
weights = []

for i in range(n):
    weights.append(int(input("Вес рыбака: ")))

weights.sort()
left = 0
right = n - 1
boats = 0

while left <= right:
    if weights[left] + weights[right] <= m:
        left += 1
    right -= 1
    boats += 1

print(boats)
