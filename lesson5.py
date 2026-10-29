print("Задание 1. Описание числа")

number = int(input("Введите целое число: "))

if number == 0:
    print("нулевое число")
elif number > 0:
    if number % 2 == 0:
        print("положительное четное число")
    else:
        print("положительное нечетное число")
        print("число не является четным")
else:
    if number % 2 == 0:
        print("отрицательное четное число")
    else:
        print("отрицательное нечетное число")
        print("число не является четным")

print()
print("Задание 2. Гласные и согласные")

word = input("Введите слово маленькими латинскими буквами: ")

a = word.count("a")
e = word.count("e")
i = word.count("i")
o = word.count("o")
u = word.count("u")

vowels = a + e + i + o + u
consonants = len(word) - vowels

print("Гласных:", vowels)
print("Согласных:", consonants)

if a > 0:
    print("a:", a)
else:
    print("a:", False)

if e > 0:
    print("e:", e)
else:
    print("e:", False)

if i > 0:
    print("i:", i)
else:
    print("i:", False)

if o > 0:
    print("o:", o)
else:
    print("o:", False)

if u > 0:
    print("u:", u)
else:
    print("u:", False)

print()
print("Задание 3. Инвестиции")

x = float(input("Минимальная сумма инвестиций: "))
mike = float(input("Сколько долларов у Майкла: "))
ivan = float(input("Сколько долларов у Ивана: "))

if mike >= x and ivan >= x:
    print(2)
elif mike >= x:
    print("Mike")
elif ivan >= x:
    print("Ivan")
elif mike + ivan >= x:
    print(1)
else:
    print(0)
