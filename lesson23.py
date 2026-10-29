import json
import random

SAVE_FILE = "lesson23_save.json"


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [["." for x in range(width)] for y in range(height)]
        self.fires = {}
        self.clouds = set()
        self.weather = "ясно"
        self.turn = 0
        self.score = 0
        self.lives = 3
        self.water = 0
        self.capacity = 1

        self.make_river()
        self.make_trees()

        free = self.random_cells(3)
        if len(free) < 3:
            raise ValueError("На поле не хватает свободных клеток")

        self.hospital = free[0]
        self.shop = free[1]
        self.x, self.y = free[2]
        self.field[self.hospital[1]][self.hospital[0]] = "H"
        self.field[self.shop[1]][self.shop[0]] = "S"
        self.start_fire()

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def random_cells(self, count, kind="."):
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] == kind:
                    cells.append((x, y))
        random.shuffle(cells)
        return cells[:count]

    def make_river(self):
        x = random.randint(1, self.width - 2)
        for y in range(self.height):
            self.field[y][x] = "~"
            if random.random() < 0.25 and x + 1 < self.width:
                self.field[y][x + 1] = "~"
            x += random.choice([-1, 0, 1])
            x = max(1, min(self.width - 2, x))

    def make_trees(self):
        empty = self.random_cells(self.width * self.height // 3)
        for x, y in empty:
            self.field[y][x] = "T"

    def start_fire(self):
        trees = self.random_cells(1, "T")
        if trees:
            x, y = trees[0]
            self.field[y][x] = "F"
            self.fires[(x, y)] = 0

    def neighbours(self, x, y):
        cells = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.inside(nx, ny):
                cells.append((nx, ny))
        return cells

    def move(self, dx, dy):
        x = self.x + dx
        y = self.y + dy
        if not self.inside(x, y):
            print("Дальше край карты!")
            return False

        self.x, self.y = x, y
        if self.field[y][x] == "~":
            self.water = self.capacity
            print("Набрали воду из реки!")
        return True

    def put_out(self):
        if self.field[self.y][self.x] != "F":
            print("Здесь нет горящего дерева")
            return False
        if self.water == 0:
            print("Нет воды. Найдите реку!")
            return False

        self.field[self.y][self.x] = "T"
        self.fires.pop((self.x, self.y), None)
        self.water -= 1
        self.score += 10
        print("Пожар потушен! +10 очков")
        return True

    def visit_hospital(self):
        if (self.x, self.y) != self.hospital:
            print("Сначала прилетите к госпиталю 🏥")
            return False
        if self.lives >= 5:
            print("Здоровье уже полное")
            return False
        if self.score < 10:
            print("Для лечения нужно 10 очков")
            return False

        self.score -= 10
        self.lives += 1
        print("Восстановлена одна жизнь!")
        return True

    def visit_shop(self):
        if (self.x, self.y) != self.shop:
            print("Сначала прилетите в магазин 🛒")
            return False
        if self.score < 20:
            print("Улучшение резервуара стоит 20 очков")
            return False

        self.score -= 20
        self.capacity += 1
        print("Вместимость резервуара увеличена!")
        return True

    def tick(self):
        self.turn += 1

        if self.turn % 4 == 0:
            self.weather = random.choice(["ясно", "облачно", "гроза"])

        self.clouds = set()
        if self.weather != "ясно":
            self.clouds = set(self.random_cells(max(1, self.width * self.height // 5)))

        new_fires = []
        for (x, y), age in list(self.fires.items()):
            age += 1
            if age >= 5:
                self.field[y][x] = "X"
                del self.fires[(x, y)]
                self.score -= 5
                print("Дерево сгорело. -5 очков")
            else:
                self.fires[(x, y)] = age
                chance = 0.18 if self.weather == "ясно" else 0.08
                for nx, ny in self.neighbours(x, y):
                    if self.field[ny][nx] == "T" and random.random() < chance:
                        new_fires.append((nx, ny))

        for x, y in new_fires:
            if self.field[y][x] == "T":
                self.field[y][x] = "F"
                self.fires[(x, y)] = 0

        if self.turn % 4 == 0 and random.random() < 0.65:
            self.start_fire()

        if random.random() < 0.35:
            empty = self.random_cells(1)
            if empty:
                x, y = empty[0]
                self.field[y][x] = "T"

        if self.weather == "гроза" and (self.x, self.y) in self.clouds:
            if random.random() < 0.3:
                self.lives -= 1
                print("Вертолёт попал под молнию! -1 жизнь")

        if self.field[self.y][self.x] == "F" and self.water == 0:
            if random.random() < 0.12:
                self.lives -= 1
                print("Огонь повредил вертолёт! -1 жизнь")

        if self.lives < 0:
            self.lives = 0

    def show(self):
        pictures = {
            ".": "🟩", "~": "🌊", "T": "🌲", "F": "🔥",
            "X": "🟫", "H": "🏥", "S": "🛒"
        }
        print("\n" + "=" * 45)
        print(f"Ход: {self.turn} | Погода: {self.weather} | Очки: {self.score}")
        print(f"Жизни: {self.lives} | Вода: {self.water}/{self.capacity}")
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) == (self.x, self.y):
                    line += "🚁"
                elif (x, y) in self.clouds and self.field[y][x] == ".":
                    line += "⛈️" if self.weather == "гроза" else "☁️"
                else:
                    line += pictures[self.field[y][x]]
            print(line)

        if self.field[self.y][self.x] == "F":
            print("Под вертолётом горящее дерево! Нажмите f, чтобы потушить.")
        elif (self.x, self.y) == self.hospital:
            print("Вы у госпиталя. Нажмите h для лечения за 10 очков.")
        elif (self.x, self.y) == self.shop:
            print("Вы у магазина. Нажмите b для улучшения за 20 очков.")

    def save(self):
        data = {
            "width": self.width, "height": self.height, "field": self.field,
            "x": self.x, "y": self.y, "score": self.score,
            "lives": self.lives, "water": self.water, "capacity": self.capacity,
            "turn": self.turn, "weather": self.weather,
            "hospital": list(self.hospital), "shop": list(self.shop),
            "fires": [[x, y, age] for (x, y), age in self.fires.items()]
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print("Игра сохранена в", SAVE_FILE)

    @classmethod
    def load(cls):
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        game = cls(data["width"], data["height"])
        game.field = data["field"]
        game.x, game.y = data["x"], data["y"]
        game.score = data["score"]
        game.lives = data["lives"]
        game.water = data["water"]
        game.capacity = data["capacity"]
        game.turn = data["turn"]
        game.weather = data["weather"]
        game.hospital = tuple(data["hospital"])
        game.shop = tuple(data["shop"])
        game.fires = {(x, y): age for x, y, age in data["fires"]}
        game.clouds = set()
        return game


def help_text():
    print("\nУправление:")
    print("w/a/s/d - вверх/влево/вниз/вправо")
    print("f - потушить дерево под вертолётом (нужна вода)")
    print("h - лечение в госпитале (10 очков)")
    print("b - улучшение бака в магазине (20 очков)")
    print("save - сохранить, load - загрузить, help - помощь, q - выход")
    print("🌲 дерево  🔥 пожар  🌊 река  🏥 госпиталь  🛒 магазин")
    print("Летайте над рекой, чтобы наполнить бак, и тушите пожары.")


def enter_size(text):
    while True:
        value = input(text)
        if value.isdigit() and 5 <= int(value) <= 20:
            return int(value)
        print("Введите число от 5 до 20")


def main():
    print("ЛЕСНОЙ ПАТРУЛЬ - игра про пожарный вертолёт")
    print("1 - новая игра, 2 - загрузить сохранение")
    choice = input("Ваш выбор: ").strip()

    if choice == "2":
        try:
            game = Game.load()
        except (OSError, ValueError, KeyError, TypeError):
            print("Не удалось загрузить сохранение. Начинаем новую игру.")
            width = enter_size("Ширина поля (5-20): ")
            height = enter_size("Высота поля (5-20): ")
            game = Game(width, height)
    else:
        width = enter_size("Ширина поля (5-20): ")
        height = enter_size("Высота поля (5-20): ")
        game = Game(width, height)

    help_text()

    while game.lives > 0:
        game.show()
        command = input("Ваш ход: ").strip().lower()
        action = False

        if command == "w":
            action = game.move(0, -1)
        elif command == "s":
            action = game.move(0, 1)
        elif command == "a":
            action = game.move(-1, 0)
        elif command == "d":
            action = game.move(1, 0)
        elif command == "f":
            action = game.put_out()
        elif command == "h":
            action = game.visit_hospital()
        elif command == "b":
            action = game.visit_shop()
        elif command == "save":
            game.save()
        elif command == "load":
            try:
                game = Game.load()
                print("Сохранение загружено")
            except (OSError, ValueError, KeyError, TypeError):
                print("Не удалось загрузить сохранение")
        elif command == "help":
            help_text()
        elif command == "q":
            print("До встречи!")
            return
        else:
            print("Неизвестная команда. Введите help для подсказки.")

        if action:
            game.tick()

    game.show()
    print("Игра окончена! Ваш счёт:", game.score)


if __name__ == "__main__":
    main()
