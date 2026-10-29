import random

print("Урок 13. Сложение матриц")

rows = int(input("Количество строк (например, 10): "))
cols = int(input("Количество столбцов (например, 10): "))

if rows <= 0 or cols <= 0:
    print("Размеры матрицы должны быть больше нуля")
else:
    matrix_1 = []
    matrix_2 = []
    matrix_3 = []

    for i in range(rows):
        row_1 = []
        row_2 = []
        for j in range(cols):
            row_1.append(random.randint(-20, 20))
            row_2.append(random.randint(-20, 20))
        matrix_1.append(row_1)
        matrix_2.append(row_2)

    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(matrix_1[i][j] + matrix_2[i][j])
        matrix_3.append(row)

    print("\nПервая матрица:")
    for row in matrix_1:
        print(row)

    print("\nВторая матрица:")
    for row in matrix_2:
        print(row)

    print("\nСумма матриц:")
    for row in matrix_3:
        print(row)
