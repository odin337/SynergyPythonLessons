print("Задание 1. Площадь и периметр прямоугольника")

a = float(input("Введите первую сторону: "))
b = float(input("Введите вторую сторону: "))

area = a * b
perimeter = 2 * (a + b)

print("Площадь:", area)
print("Периметр:", perimeter)

print()
print("Задание 2. Работа с пятизначным числом")

number = int(input("Введите пятизначное число: "))

units = number % 10
tens = number // 10 % 10
hundreds = number // 100 % 10
thousands = number // 1000 % 10
ten_thousands = number // 10000

result = tens ** units * hundreds / (ten_thousands - thousands)

print("Результат:", result)
