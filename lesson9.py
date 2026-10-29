print("Задание 1. Различные числа")

n = int(input("Количество чисел: "))
numbers = list(map(int, input("Введите числа через пробел: ").split()))

print(len(set(numbers)))

print()
print("Задание 2. Общие числа")

first = set(map(int, input("Первый список: ").split()))
second = set(map(int, input("Второй список: ").split()))

print(len(first & second))

print()
print("Задание 3. Повторяющиеся числа")

numbers = list(map(int, input("Введите числа через пробел: ").split()))
seen = set()

for number in numbers:
    if number in seen:
        print("YES")
    else:
        print("NO")
        seen.add(number)
