print("Задание 1. Палиндром")

word = input("Введите слово: ")

if word == word[::-1]:
    print("yes")
else:
    print("no")

print()
print("Задание 2. Лишние пробелы")

text = input("Введите строку: ")

while "  " in text:
    text = text.replace("  ", " ")

print(text)
