# simplex_algorithm

Вывод в консоль файла main.py:

    ЛАБОРАТОРНАЯ РАБОТА №1.
    ТЕМА: "Симплекс-метод в прямой задаче линейного программирования".
    Вариант №5.

    Исходные данные:
    c = [6, 6, 6]
    A = [[4, 1, 1], [1, 2, 0], [0, 0.5, 4]]
    b = [5, 3, 8]

    Решаемая задача: Прямая задача линейного программирования.

    Составленная изначально симплекс-таблица:
    +----+----+----+-----+----+
    |    | S0 | x1 |  x2 | x3 |
    +----+----+----+-----+----+
    | x4 | 5  | 4  |  1  | 1  |
    | x5 | 3  | 1  |  2  | 0  |
    | x6 | 8  | 0  | 0.5 | 4  |
    | F  | 0  | 6  |  6  | 6  |
    +----+----+----+-----+----+

    Замена разрешающих строки и столбца: x4 и x1.
    +----+------+-------+------+-------+
    |    |  S0  |   x4  |  x2  |   x3  |
    +----+------+-------+------+-------+
    | x1 | 1.25 |  0.25 | 0.25 |  0.25 |
    | x5 | 1.75 | -0.25 | 1.75 | -0.25 |
    | x6 | 8.0  |  0.0  | 0.5  |  4.0  |
    | F  | -7.5 |  -1.5 | 4.5  |  4.5  |
    +----+------+-------+------+-------+
    Проверка при округленных значениях x1 = 1.25, x2 = 0, x3 = 0:
    F = 6*x1 + 6*x2 + 6*x3 = 6*1.25 + 6*0 + 6*0 = 7.5

    Замена разрешающих строки и столбца: x5 и x2.
    +----+-------+-------+-------+-------+
    |    |   S0  |   x4  |   x5  |   x3  |
    +----+-------+-------+-------+-------+
    | x1 |  1.0  |  0.29 | -0.14 |  0.29 |
    | x2 |  1.0  | -0.14 |  0.57 | -0.14 |
    | x6 |  7.5  |  0.07 | -0.29 |  4.07 |
    | F  | -12.0 | -0.86 | -2.57 |  5.14 |
    +----+-------+-------+-------+-------+
    Проверка при округленных значениях x1 = 1.0, x2 = 1.0, x3 = 0:
    F = 6*x1 + 6*x2 + 6*x3 = 6*1.0 + 6*1.0 + 6*0 = 12.0

    Замена разрешающих строки и столбца: x6 и x3.
    +----+--------+-------+-------+-------+
    |    |   S0   |   x4  |   x5  |   x6  |
    +----+--------+-------+-------+-------+
    | x1 |  0.47  |  0.28 | -0.12 | -0.07 |
    | x2 |  1.26  | -0.14 |  0.56 |  0.04 |
    | x3 |  1.84  |  0.02 | -0.07 |  0.25 |
    | F  | -21.47 | -0.95 | -2.21 | -1.26 |
    +----+--------+-------+-------+-------+
    Проверка при округленных значениях x1 = 0.47, x2 = 1.26, x3 = 1.84:
    F = 6*x1 + 6*x2 + 6*x3 = 6*0.47 + 6*1.26 + 6*1.84 = 21.42

    Найдено оптимальное решение системы.


    ЛАБОРАТОРНАЯ РАБОТА №2.
    ТЕМА: "Симплекс-метод в двойственной задаче линейного программирования".
    Вариант №5.

    Исходные данные:
    c = [3, 3, 7]
    A = [[1, 1, 1], [1, 4, 0], [0, 0.5, 3]]
    b = [3, 5, 7]

    Решаемая задача: Двойственная задача линейного программирования.

    Преобразованные данные:
    c' = [-3, -5, -7]
    A' = [[-1, -1, 0], [-1, -4, -0.5], [-1, 0, -3]]
    b' = [-3, -3, -7]

    Составленная изначально симплекс-таблица:
    +----+----+----+----+------+
    |    | S0 | y1 | y2 |  y3  |
    +----+----+----+----+------+
    | y4 | -3 | -1 | -1 |  0   |
    | y5 | -3 | -1 | -4 | -0.5 |
    | y6 | -7 | -1 | 0  |  -3  |
    | G  | 0  | -3 | -5 |  -7  |
    +----+----+----+----+------+

    Замена разрешающих строки и столбца: y6 и y3.
    +----+-------+-------+------+-------+
    |    |   S0  |   y1  |  y2  |   y6  |
    +----+-------+-------+------+-------+
    | y4 |  -3.0 |  -1.0 | -1.0 |  -0.0 |
    | y5 | -1.83 | -0.83 | -4.0 | -0.17 |
    | y3 |  2.33 |  0.33 | -0.0 | -0.33 |
    | G  | 16.33 | -0.67 | -5.0 | -2.33 |
    +----+-------+-------+------+-------+
    Проверка при округленных значениях y1 = 0, y2 = 0, y3 = 2.33:
    G = -3*y1 - 5*y2 - 7*y3 = -3*0 - 5*0 - 7*2.33 = -16.31

    Замена разрешающих строки и столбца: y5 и y1.
    +----+------+------+------+------+
    |    |  S0  |  y5  |  y2  |  y6  |
    +----+------+------+------+------+
    | y4 | -0.8 | -1.2 | 3.8  | 0.2  |
    | y1 | 2.2  | -1.2 | 4.8  | 0.2  |
    | y3 | 1.6  | 0.4  | -1.6 | -0.4 |
    | G  | 17.8 | -0.8 | -1.8 | -2.2 |
    +----+------+------+------+------+
    Проверка при округленных значениях y1 = 2.2, y2 = 0, y3 = 1.6:
    G = -3*y1 - 5*y2 - 7*y3 = -3*2.2 - 5*0 - 7*1.6 = -17.8

    Замена разрешающих строки и столбца: y4 и y5.
    +----+-------+-------+-------+-------+
    |    |   S0  |   y4  |   y2  |   y6  |
    +----+-------+-------+-------+-------+
    | y5 |  0.67 | -0.83 | -3.17 | -0.17 |
    | y1 |  3.0  |  -1.0 |  1.0  |  0.0  |
    | y3 |  1.33 |  0.33 | -0.33 | -0.33 |
    | G  | 18.33 | -0.67 | -4.33 | -2.33 |
    +----+-------+-------+-------+-------+
    Проверка при округленных значениях y1 = 3.0, y2 = 0, y3 = 1.33:
    G = -3*y1 - 5*y2 - 7*y3 = -3*3.0 - 5*0 - 7*1.33 = -18.31

    Найдено оптимальное решение системы.

