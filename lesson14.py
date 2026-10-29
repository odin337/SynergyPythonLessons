print("Урок 14. Рекурсия")

my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def show_list(numbers, index=0):
    if index == len(numbers):
        print("Конец списка")
        return

    print(numbers[index])
    show_list(numbers, index + 1)


show_list(my_list)
