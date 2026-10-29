print("Урок 16. Классы и объекты")


class Kassa:
    def __init__(self, money=0):
        self.money = money

    def top_up(self, x):
        if x < 0:
            raise ValueError("Сумма должна быть положительной")
        self.money += x

    def count_1000(self):
        print("Целых тысяч в кассе:", self.money // 1000)

    def take_away(self, x):
        if x < 0:
            raise ValueError("Сумма должна быть положительной")
        if x > self.money:
            raise ValueError("В кассе недостаточно денег")
        self.money -= x


class Turtle:
    def __init__(self, x, y, s):
        if s <= 0:
            raise ValueError("Шаг должен быть больше нуля")
        self.x = x
        self.y = y
        self.s = s

    def go_up(self):
        self.y += self.s

    def go_down(self):
        self.y -= self.s

    def go_left(self):
        self.x -= self.s

    def go_right(self):
        self.x += self.s

    def evolve(self):
        self.s += 1

    def degrade(self):
        if self.s <= 1:
            raise ValueError("Шаг не может быть меньше единицы")
        self.s -= 1

    def count_moves(self, x2, y2):
        dx = abs(x2 - self.x)
        dy = abs(y2 - self.y)
        if dx % self.s != 0 or dy % self.s != 0:
            raise ValueError("Невозможно попасть в эту клетку с таким шагом")
        return dx // self.s + dy // self.s


print("Задание 1. Касса")
cash = Kassa(5500)
cash.top_up(2500)
cash.take_away(1000)
print("Осталось денег:", cash.money)
cash.count_1000()

print("\nЗадание 2. Черепашка")
turtle = Turtle(0, 0, 2)
turtle.go_up()
turtle.go_right()
print("Позиция:", turtle.x, turtle.y)
print("Шаг:", turtle.s)
print("До клетки (6, 4) нужно ходов:", turtle.count_moves(6, 4))
turtle.evolve()
print("Шаг после evolve:", turtle.s)
turtle.degrade()
print("Шаг после degrade:", turtle.s)
