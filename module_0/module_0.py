import numpy as np


def game_core(number):
    """Начинаем сравнивать с середины списка, поэтому первое предпогалаемое
    число и шаг принимаем 50.  Если предполагаемое число меньше значения
    середины, то поиск осуществляется в первой половине элементов,
    иначе — во второй.  Находим значение серединного элемента в выбранной
    половине и сравниваем с предполагаемым числом.  Повторяем, пока не будет
    найдено загаданное число.  Если шаг равен 1, то уменьшаем предполагаемое
    число на 1, если оно больше загаданного и увеличиваем на 1, если меньше
    загаданного."""
    count = 0
    predict = 50
    step = 50

    while True:
        count += 1
        if number == predict:
            break

        elif step == 1 and number < predict:
            predict -= step
        elif step == 1 and number > predict:
            predict += step

        elif number > predict:
            predict += int(step / 2)
            step = int(step / 2)
        elif number < predict:
            predict -= int(step / 2)
            step = int(step / 2)


    return(count)


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число"""
    count_ls = []
    """Фиксируем random seed, чтобы ваш эксперимент был воспроизводим."""
    np.random.seed(1)
    random_array = np.random.randint(1, 101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return (score)


score_game(game_core)