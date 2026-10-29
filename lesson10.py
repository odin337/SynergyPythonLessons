print("Задание 1. Словарь питомцев")

pets = {}

name = input("Кличка питомца: ")
kind = input("Вид питомца: ")
age = int(input("Возраст питомца: "))
owner = input("Имя владельца: ")

pets[name] = {
    "Вид питомца": kind,
    "Возраст питомца": age,
    "Имя владельца": owner
}

pet_name = list(pets.keys())[0]
pet_info = list(pets.values())[0]

if 11 <= age % 100 <= 14:
    suffix = "лет"
elif age % 10 == 1:
    suffix = "год"
elif 2 <= age % 10 <= 4:
    suffix = "года"
else:
    suffix = "лет"

print(f'Это {pet_info["Вид питомца"]} по кличке "{pet_name}". '
      f'Возраст питомца: {pet_info["Возраст питомца"]} {suffix}. '
      f'Имя владельца: {pet_info["Имя владельца"]}')

print()
print("Задание 2. Степени чисел")

my_dict = {}

for number in range(10, -6, -1):
    my_dict[number] = number ** number

print(my_dict)
