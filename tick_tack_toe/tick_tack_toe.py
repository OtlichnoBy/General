def welcome():
    """Отображение приветствия и правил игры"""
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
    """Ввод координат клетки для следующего хода и проверка их корректности"""
    while True:
        cords = input("Введите числа x y, чтобы сделать ход: ").split()  # Ввод координат клетки для следующего хода

        if len(cords) != 2:  # Проверяем, что были введены 2 координаты
            print("Необходимо ввести 2 координаты!")
            continue

        x, y = cords  # Присваиваем x и y строковые значения введенных символов

        if not (x.isdigit()) or not (y.isdigit()):  # Проверяем, что были введены числа
            print("Необходимо ввести числа!")
            continue

        x, y = int(x), int(y)  # Присваиваем x и y значения координат в виде целых чисел

        if 0 > x or x > 2 or 0 > y or y > 2:  # Проверяем соответствуют ли координаты диапазону поля
            print("Введенные координаты, вне допустимого диапазона!")
            continue

        if field[x][y] != " ":  # Проверяем свободна ли клетка, которую указал игрок
            print("Указанная клетка игрового поля - занята!")
            continue

        return x, y


def check_win():
    """Проверка выигрышных случаев"""
    for i in range(3):  # Проверка строк на выигрышный случай
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

    for i in range(3):  # Проверка стобцов на выигрышный случай
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

    symbols = []
    for i in range(3):  # Проверка диагонали ([0][0], [1][1], [2][2]) на выигрышный случай
        symbols.append(field[i][i])
    if symbols == ["x", "x", "x"]:
        show()
        print("Результат игры: X - побеждает!")
        return True
    if symbols == ["0", "0", "0"]:
        show()
        print("Результат игры: 0 - побеждает!")
        return True

    symbols = []
    for i in range(3):  # Проверка диагонали ([0][2], [1][1], [2][0]) на выигрышный случай
        symbols.append(field[i][2-i])
    if symbols == ["x", "x", "x"]:
        show()
        print("Результат игры: X - побеждает!")
        return True
    if symbols == ["0", "0", "0"]:
        show()
        print("Результат игры: 0 - побеждает!")
        return True


def start_game():
    """Запуск игры"""
    count = 0

    while True:  # Вывод указания: крестик или нолик делает текущий ход
        count += 1
        show()
        if count % 2 == 1:
            print("Ходит крестик!")
        else:
            print("Ходит нолик!")

        x, y = ask()

        if count % 2 == 1:  # Присвоение ячейке игрового поля значения X или 0 после хода игрока
            field[x][y] = "x"
        else:
            field[x][y] = "0"

        if check_win():  # Проверка наличия выигрышной ситуации
            break

        if count == 9:  # Если за 9 ходов никто не победил - ничья
            show()
            print("Результат игры: Ничья!")
            break


welcome()
field = [[" "] * 3 for i in range(3)]  # В начале игры значения игрового поля - пробелы
start_game()
