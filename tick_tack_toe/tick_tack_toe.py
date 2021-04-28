def welcome():
    print("======================")
    print(" Игра Крестики-Нолики ")
    print("======================")
    print("  Чтобы сделать ход,  ")
    print("  введите числа: x y  ")
    print("  x - номер строки    ")
    print("  y - номер столбца   ")
    print("======================")


def show():
    """Вывод игрового поля 3х3 с нумерацией строк и столбцов"""
    print()
    print("    | 0 | 1 | 2 | ")
    print("  --------------- ")
    for i, row in enumerate(field):
        row_str = f"  {i} | {' | '.join(row)} | "
        print(row_str)
        print("  --------------- ")
    print()


def ask():
    while True:
        """Ввод игроком координат клетки для следующего хода"""
        cords = input("Введите числа x y, чтобы сделать ход: ").split()

        """Проверяем, что были введены 2 координаты"""
        if len(cords) != 2:
            print("Необходимо ввести 2 координаты!")
            continue

        """Присваиваем x и y строковые значения введенных символов"""
        x, y = cords

        """Проверяем, что были введены числа"""
        if not (x.isdigit()) or not (y.isdigit()):
            print("Необходимо ввести числа!")
            continue

        """Присваиваем x и y значения координат в виде целых чисел"""
        x, y = int(x), int(y)

        """Проверяем соответствуют ли координаты диапазону поля"""
        if 0 > x or x > 2 or 0 > y or y > 2:
            print("Введенные координаты, вне допустимого диапазона!")
            continue

        """Проверяем свободна ли клетка, которую указал игрок"""
        if field[x][y] != " ":
            print("Указанная клетка игрового поля - занята!")
            continue

        return x, y


def check_win():
    """Проверка строк на выигрышный случай"""
    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(field[i][j])
        if symbols == ["x", "x", "x"]:
            show()
            print("Результат игры: X - побеждает!")
            return True
        if symbols == ["0", "0", "0"]:
            show()
            print("Результат игры: 0 - побеждает!")
            return True

    """Проверка стобцов на выигрышный случай"""
    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(field[j][i])
        if symbols == ["x", "x", "x"]:
            show()
            print("Результат игры: X - побеждает!")
            return True
        if symbols == ["0", "0", "0"]:
            show()
            print("Результат игры: 0 - побеждает!")
            return True

    """Проверка диагонали ([0][0], [1][1], [2][2]) на выигрышный случай"""
    symbols = []
    for i in range(3):
        symbols.append(field[i][i])
    if symbols == ["x", "x", "x"]:
        show()
        print("Результат игры: X - побеждает!")
        return True
    if symbols == ["0", "0", "0"]:
        show()
        print("Результат игры: 0 - побеждает!")
        return True

    """Проверка диагонали ([0][2], [1][1], [2][0]) на выигрышный случай"""
    symbols = []
    for i in range(3):
        symbols.append(field[i][2-i])
    if symbols == ["x", "x", "x"]:
        show()
        print("Результат игры: X - побеждает!")
        return True
    if symbols == ["0", "0", "0"]:
        show()
        print("Результат игры: 0 - побеждает!")
        return True


"""Отображение приветствия и правил игры"""
welcome()

"""В начале игры значения игрового поля - пробелы"""
field = [[" "] * 3 for i in range(3)]
count = 0

while True:
    """Вывод указания: крестик или нолик делает текущий ход"""
    count += 1
    show()
    if count % 2 == 1:
        print("Ходит крестик!")
    else:
        print("Ходит нолик!")

    x, y = ask()

    """Присвоение ячейке игрового поля значения X или 0 после хода игрока"""
    if count % 2 == 1:
        field[x][y] = "x"
    else:
        field[x][y] = "0"

    """Проверка наличия выигрышной ситуации"""
    if check_win():
        break

    """Если за 9 ходов никто не победил - Ничья"""
    if count == 9:
        show()
        print("Результат игры: Ничья!")
        break
