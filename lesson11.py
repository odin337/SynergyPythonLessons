print("Задание 1. Факториалы")


def factorial(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result


number = int(input("Введите натуральное число: "))
answer = factorial(number)
print("Факториал:", answer)

factorials = []
for i in range(answer, 0, -1):
    factorials.append(factorial(i))

print(factorials)

print()
print("Задание 2. База данных питомцев")

import collections

pets = {
    1: {
        "Мухтар": {
            "Вид питомца": "собака",
            "Возраст питомца": 9,
            "Имя владельца": "Павел"
        }
    },
    2: {
        "Каа": {
            "Вид питомца": "желторотый питон",
            "Возраст питомца": 19,
            "Имя владельца": "Саша"
        }
    }
}

last_id = collections.deque(pets, maxlen=1)[0] if pets else 0


def get_pet(ID):
    return pets[ID] if ID in pets else False


def get_suffix(age):
    if 11 <= age % 100 <= 14:
        return "лет"
    if age % 10 == 1:
        return "год"
    if 2 <= age % 10 <= 4:
        return "года"
    return "лет"


def pets_list():
    if not pets:
        print("Список питомцев пуст")
    for ID in pets:
        name = list(pets[ID].keys())[0]
        print(ID, "-", name)


def create():
    global last_id
    name = input("Кличка питомца: ")
    kind = input("Вид питомца: ")
    age = int(input("Возраст питомца: "))
    owner = input("Имя владельца: ")

    last_id += 1
    pets[last_id] = {
        name: {
            "Вид питомца": kind,
            "Возраст питомца": age,
            "Имя владельца": owner
        }
    }
    print("Питомец добавлен. ID:", last_id)


def read():
    ID = int(input("ID питомца: "))
    pet = get_pet(ID)
    if not pet:
        print("Питомец не найден")
        return

    name = list(pet.keys())[0]
    info = pet[name]
    print(f'Это {info["Вид питомца"]} по кличке "{name}". '
          f'Возраст питомца: {info["Возраст питомца"]} {get_suffix(info["Возраст питомца"])}. '
          f'Имя владельца: {info["Имя владельца"]}')


def update():
    ID = int(input("ID питомца: "))
    if not get_pet(ID):
        print("Питомец не найден")
        return

    name = input("Новая кличка: ")
    kind = input("Новый вид питомца: ")
    age = int(input("Новый возраст: "))
    owner = input("Новое имя владельца: ")

    pets[ID] = {
        name: {
            "Вид питомца": kind,
            "Возраст питомца": age,
            "Имя владельца": owner
        }
    }
    print("Данные обновлены")


def delete():
    ID = int(input("ID питомца: "))
    if get_pet(ID):
        del pets[ID]
        print("Питомец удален")
    else:
        print("Питомец не найден")


command = ""
while command != "stop":
    print("\nКоманды: create, read, update, delete, list, stop")
    command = input("Введите команду: ").strip().lower()

    if command == "create":
        create()
    elif command == "read":
        read()
    elif command == "update":
        update()
    elif command == "delete":
        delete()
    elif command == "list":
        pets_list()
    elif command != "stop":
        print("Неизвестная команда")
