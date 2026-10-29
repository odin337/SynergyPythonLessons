import curses
import json
import locale
import random
import sys
import time
import unicodedata
from pathlib import Path

SAVE_FILE = Path(__file__).with_name('lesson23_save.json')
TICK_SECONDS = 0.75

PICTURES = {
    '.': '🟩',
    '~': '🌊',
    'T': '🌲',
    'F': '🔥',
    'X': '🟫',
    'H': '🏥',
    'S': '🛒',
}

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [['.' for _ in range(width)] for _ in range(height)]
        self.fires = {}
        self.clouds = set()
        self.weather = 'ясно'
        self.turn = 0
        self.score = 0
        self.lives = 5
        self.capacity = 1
        self.water = 1
        self.last_damage = -30
        self.message = 'Бак полон. Можно лететь.'

        self.make_river()
        self.make_trees()

        free = self.random_cells(2)
        self.hospital = free[0]
        self.shop = free[1]
        self.field[self.hospital[1]][self.hospital[0]] = 'H'
        self.field[self.shop[1]][self.shop[0]] = 'S'

        river = [(x, y) for y in range(height) for x in range(width)
                 if self.field[y][x] == '~']
        self.x, self.y = min(river, key=lambda p: abs(p[1] - height // 2))

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def random_cells(self, count, kind='.'):
        available = [(x, y) for y in range(self.height)
                     for x in range(self.width) if self.field[y][x] == kind]
        return random.sample(available, min(count, len(available)))

    def make_river(self):
        x = self.width // 2
        for y in range(self.height):
            self.field[y][x] = '~'
            if random.random() < 0.20 and x + 1 < self.width:
                self.field[y][x + 1] = '~'
            x = max(1, min(self.width - 2, x + random.choice([-1, 0, 1])))

    def make_trees(self):
        for x, y in self.random_cells(self.width * self.height // 3):
            self.field[y][x] = 'T'

    def start_fire(self):
        if len(self.fires) >= 5:
            return
        trees = self.random_cells(1, 'T')
        if trees:
            x, y = trees[0]
            self.field[y][x] = 'F'
            self.fires[(x, y)] = 0
            self.message = 'В лесу пожар!'

    def neighbours(self, x, y):
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if self.inside(nx, ny):
                yield nx, ny

    def move(self, dx, dy):
        nx = self.x + dx
        ny = self.y + dy
        if not self.inside(nx, ny):
            self.message = 'Край карты.'
            return
        self.x, self.y = nx, ny
        cell = self.field[ny][nx]
        if cell == '~':
            self.water = self.capacity
            self.message = 'Бак наполнен водой.'
        elif cell == 'F':
            self.message = 'Пожар под вертолётом. F/А — тушить.'
        elif cell == 'H':
            self.message = 'Госпиталь. Лечение — 10 очков (H/Р).'
        elif cell == 'S':
            self.message = 'Магазин. Новый бак — 20 очков (B/И).'

    def put_out(self):
        if self.field[self.y][self.x] != 'F':
            self.message = 'Под вертолётом нет пожара.'
        elif self.water == 0:
            self.message = 'Вода кончилась. Летите к реке.'
        else:
            self.field[self.y][self.x] = 'T'
            self.fires.pop((self.x, self.y), None)
            self.water -= 1
            self.score += 10
            self.message = 'Пожар потушен! +10 очков.'

    def visit_hospital(self):
        if (self.x, self.y) != self.hospital:
            self.message = 'Нужно быть в госпитале.'
        elif self.lives >= 5:
            self.message = 'У вас уже 5 жизней.'
        elif self.score < 10:
            self.message = 'Лечение стоит 10 очков.'
        else:
            self.score -= 10
            self.lives += 1
            self.message = 'Восстановлена одна жизнь.'

    def visit_shop(self):
        if (self.x, self.y) != self.shop:
            self.message = 'Нужно быть в магазине.'
        elif self.score < 20:
            self.message = 'Улучшение стоит 20 очков.'
        else:
            self.score -= 20
            self.capacity += 1
            self.message = 'Бак улучшен. Заправьтесь на реке.'

    def tick(self):
        self.turn += 1

        if self.turn % 25 == 0:
            self.weather = random.choice(['ясно', 'облачно', 'гроза'])

        self.clouds = set()
        if self.weather != 'ясно':
            self.clouds = set(self.random_cells(max(1, self.width * self.height // 14)))

        new_fires = set()
        for (x, y), age in list(self.fires.items()):
            age += 1
            if age >= 20:
                self.field[y][x] = 'X'
                del self.fires[(x, y)]
                self.score -= 2
                self.message = 'Одно дерево сгорело. -2 очка.'
            else:
                self.fires[(x, y)] = age
                if age % 5 == 0 and len(self.fires) + len(new_fires) < 5:
                    for nx, ny in self.neighbours(x, y):
                        if self.field[ny][nx] == 'T' and random.random() < 0.05:
                            new_fires.add((nx, ny))

        for x, y in new_fires:
            if self.field[y][x] == 'T' and len(self.fires) < 5:
                self.field[y][x] = 'F'
                self.fires[(x, y)] = 0

        if self.turn >= 8 and (self.turn - 8) % 12 == 0:
            if not self.fires or random.random() < 0.7:
                self.start_fire()

        if self.turn % 6 == 0:

            cells = self.random_cells(1, 'X') if random.random() < 0.2 else self.random_cells(1)
            if cells:
                x, y = cells[0]
                self.field[y][x] = 'T'

        if self.turn - self.last_damage >= 18:
            if self.weather == 'гроза' and (self.x, self.y) in self.clouds:
                if random.random() < 0.06:
                    self.lives -= 1
                    self.last_damage = self.turn
                    self.message = 'Молния задела вертолёт! -1 жизнь.'
            elif self.field[self.y][self.x] == 'F' and self.water == 0:
                if random.random() < 0.08:
                    self.lives -= 1
                    self.last_damage = self.turn
                    self.message = 'Огонь повредил вертолёт! -1 жизнь.'

    def save(self):
        data = {
            'width': self.width, 'height': self.height, 'field': self.field,
            'x': self.x, 'y': self.y, 'fires': [[x, y, age] for (x, y), age in self.fires.items()],
            'clouds': [list(p) for p in self.clouds],
            'hospital': list(self.hospital), 'shop': list(self.shop),
            'weather': self.weather, 'turn': self.turn, 'score': self.score,
            'lives': self.lives, 'water': self.water, 'capacity': self.capacity,
            'last_damage': self.last_damage,
        }
        with open(SAVE_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        self.message = 'Игра сохранена.'

    @classmethod
    def load(cls):
        with open(SAVE_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        game = cls.__new__(cls)
        game.width = data['width']
        game.height = data['height']
        game.field = data['field']
        if not (5 <= game.width <= 20 and 5 <= game.height <= 20):
            raise ValueError('Неверный размер карты')
        if len(game.field) != game.height or any(len(row) != game.width for row in game.field):
            raise ValueError('Повреждено поле')
        game.x, game.y = data['x'], data['y']
        game.hospital = tuple(data['hospital'])
        game.shop = tuple(data['shop'])
        if not game.inside(game.x, game.y):
            raise ValueError('Неверные координаты вертолёта')
        game.fires = {(x, y): age for x, y, age in data['fires']}
        game.clouds = {tuple(p) for p in data.get('clouds', [])}
        game.weather = data['weather']
        game.turn = data['turn']
        game.score = data['score']
        game.lives = data['lives']
        game.water = data['water']
        game.capacity = data['capacity']
        game.last_damage = data.get('last_damage', -30)
        game.message = 'Игра загружена.'
        return game

def print_at(screen, y, x, text, style=0):
    height, width = screen.getmaxyx()
    if not (0 <= y < height and 0 <= x < width - 1):
        return

    available = width - x - 1
    visible = ''
    for char in str(text):
        if unicodedata.combining(char):
            visible += char
            continue
        size = 2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1
        if size > available:
            break
        visible += char
        available -= size
    if visible:
        try:
            screen.addstr(y, x, visible, style)
        except curses.error:
            pass

def draw(screen, game, paused=False, ascii_mode=False, game_over=False):
    screen.erase()
    h, w = screen.getmaxyx()
    if h < 14 or w < 28:
        print_at(screen, 0, 0, 'Слишком маленькое окно.')
        print_at(screen, 1, 0, 'Увеличьте окно терминала.')
        print_at(screen, 2, 0, 'Q/Й — выход')
        screen.refresh()
        return False

    view_h = min(game.height, h - 10)
    view_w = min(game.width, (w - 4) // 2)
    x0 = max(0, min(game.x - view_w // 2, game.width - view_w))
    y0 = max(0, min(game.y - view_h // 2, game.height - view_h))
    print_at(screen, 0, 0, 'ЛЕСНОЙ ПАТРУЛЬ  🚁', curses.A_BOLD)
    print_at(screen, 1, 0, f'Тик: {game.turn}  Очки: {game.score}  Жизни: {game.lives}')
    print_at(screen, 2, 0, f'Вода: {game.water}/{game.capacity}  Погода: {game.weather}  Пожары: {len(game.fires)}')
    if game_over:
        print_at(screen, 3, 0, 'Игра окончена. R/К — заново, Q/Й — выход', curses.A_BOLD)
    elif paused:
        print_at(screen, 3, 0, 'Пауза. Пробел — продолжить', curses.A_BOLD)
    elif game.turn < 8:
        print_at(screen, 3, 0, 'Пока всё спокойно.')
    else:
        print_at(screen, 3, 0, 'Тушите пожары и берегите лес.')

    print_at(screen, 4, 0, '┌' + '─' * (view_w * 2) + '┐')
    ascii_pics = {'.': ' .', '~': '~~', 'T': ' T', 'F': '!!', 'X': ' x', 'H': ' H', 'S': ' $'}
    for row in range(view_h):
        py = 5 + row
        y = y0 + row
        print_at(screen, py, 0, '│')
        for col in range(view_w):
            x = x0 + col
            cell = game.field[y][x]
            if (x, y) == (game.x, game.y):
                symbol = '🚁' if not ascii_mode else '[]'
                style = curses.A_BOLD
            elif (x, y) in game.clouds and cell == '.':
                symbol = ('⛈️' if game.weather == 'гроза' else '☁️') if not ascii_mode else '##'
                style = 0
            else:
                symbol = PICTURES.get(cell, '❔') if not ascii_mode else ascii_pics.get(cell, ' ?')
                style = 0
            print_at(screen, py, 1 + 2 * col, symbol, style)
        print_at(screen, py, 1 + view_w * 2, '│')
    bottom = 5 + view_h
    print_at(screen, bottom, 0, '└' + '─' * (view_w * 2) + '┘')
    print_at(screen, bottom + 1, 0, f'Карта {game.width}x{game.height}   Позиция: {game.x + 1}, {game.y + 1}   V/М — графика')
    print_at(screen, bottom + 2, 0, 'WASD/ЦФЫВ/стрелки — полёт   F/А — вода   H/Р — госпиталь')
    print_at(screen, bottom + 3, 0, 'B/И — магазин   P/З — сохранить   L/Д — загрузить   Пробел — пауза   Q/Й — выход')
    print_at(screen, bottom + 4, 0, game.message, curses.A_BOLD)
    screen.refresh()
    return True

def read_size(prompt):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and 5 <= int(answer) <= 20:
            return int(answer)
        print('Введите целое число от 5 до 20.')

RU_KEYS = {
    'ц': 'w', 'ф': 'a', 'ы': 's', 'в': 'd',
    'а': 'f', 'р': 'h', 'и': 'b', 'з': 'p',
    'д': 'l', 'м': 'v', 'й': 'q', 'к': 'r',
}

def normalize_key(key):
    if isinstance(key, str):
        key = key.casefold()
        return RU_KEYS.get(key, key)
    return key

def handle_key(game, key):
    if key in ('w', curses.KEY_UP):
        game.move(0, -1)
    elif key in ('s', curses.KEY_DOWN):
        game.move(0, 1)
    elif key in ('a', curses.KEY_LEFT):
        game.move(-1, 0)
    elif key in ('d', curses.KEY_RIGHT):
        game.move(1, 0)
    elif key == 'f':
        game.put_out()
    elif key == 'h':
        game.visit_hospital()
    elif key == 'b':
        game.visit_shop()
    elif key == 'p':
        try:
            game.save()
        except OSError:
            game.message = 'Ошибка сохранения файла.'
    elif key == 'l':
        try:
            game = Game.load()
        except (OSError, ValueError, KeyError, TypeError):
            game.message = 'Не удалось загрузить сохранение.'
    return game

def play(screen, game):
    screen.keypad(True)
    screen.timeout(50)
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    paused = False
    ascii_mode = False
    next_tick = time.monotonic() + TICK_SECONDS
    draw(screen, game)

    while True:
        try:
            key = normalize_key(screen.get_wch())
        except curses.error:
            key = None
        now = time.monotonic()
        over = game.lives <= 0
        small = screen.getmaxyx()[0] < 14 or screen.getmaxyx()[1] < 28
        changed = key is not None

        if key in ('q', '\x1b'):
            return f'Игра закрыта. Очки: {game.score}'
        if key == 'v':
            ascii_mode = not ascii_mode
        elif key == ' ' and not over:
            paused = not paused
            next_tick = now + TICK_SECONDS
        elif key == 'r' and over:
            game = Game(game.width, game.height)
            paused = False
            next_tick = now + TICK_SECONDS
        elif key is not None and not over and not paused and not small:
            game = handle_key(game, key)

        if not over and not paused and not small and now >= next_tick:
            game.tick()
            next_tick = now + TICK_SECONDS
            changed = True

        if paused or small:
            next_tick = now + TICK_SECONDS

        if changed:
            draw(screen, game, paused, ascii_mode, game.lives <= 0)

def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print('Запустите игру в терминале.')
        return
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        pass
    print('ЛЕСНОЙ ПАТРУЛЬ')
    print('1 — новая игра, 2 — продолжить')
    choice = input('Ваш выбор: ').strip()
    if choice == '2':
        try:
            game = Game.load()
        except (OSError, ValueError, KeyError, TypeError):
            print('Сохранение не найдено. Начинаем новую игру.')
            game = Game(read_size('Ширина поля (5-20): '), read_size('Высота поля (5-20): '))
    else:
        game = Game(read_size('Ширина поля (5-20): '), read_size('Высота поля (5-20): '))

    try:
        print(curses.wrapper(play, game))
    except curses.error:
        print('Ошибка отображения. Проверьте размер окна терминала.')
    except KeyboardInterrupt:
        print('Игра закрыта.')

if __name__ == '__main__':
    main()
