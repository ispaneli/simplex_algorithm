from copy import deepcopy

from prettytable import PrettyTable

from .matrix_math import matrix_transposition


class SimplexAlgorithm:
    """
    Симплекс-метод — алгоритм решения оптимизационной задачи линейного программирования
    путём перебора вершин выпуклого многогранника в многомерном пространстве.
    """

    def __init__(self, func_vector: list[int or float], a_matrix: list[list[int or float]],
                 b_vector: list[int or float],
                 *, mode: str = "ПЗ ЛП", var_name: str = "x", func_name: str = "F") -> None:
        """
        Инициализация объекта класса "SimplexAlgorithm".

        :param func_vector: Вектор целевой функции, то есть список коэффициентах [c1, ..., cn]
                                при переменных функции вида F = c1*x1 + ... + cn*xn.
        :param a_matrix: Матрица условий задачи.
        :param b_vector: Матрица ограничений.
        :param mode: Задача линейного программирования, которую нужно решить.
                     Поддерживаются прямая ("ПЗ ЛП") и двойственная ("ДЗ ЛП") задачи.
        :param var_name: Имя переменных в функции. Пример: в функции F = c1*x1 + ... + cn*xn, variable_name = "x".
        :param func_name: Имя функции. Пример: в функции F = c1*x1 + ... + cn*xn, function_name = "F".
        :return: None.
        """
        self._func_vector = func_vector
        self._a_matrix = a_matrix
        self._b_vector = b_vector

        self._mode = mode
        self._var_name = var_name
        self._func_name = func_name

        # Симплекс-таблица.
        self._table: list[list[int or float]] = NotImplemented

        # Список name-тэгов строк и столбовсимплекс-таблицы, используется для визуализации в консоли.
        self._row_names: list[str] = NotImplemented
        self._column_names: list[str] = NotImplemented

        # Список полных имен базисных переменных функции.
        # Пример: F = c1*x1 + ... + cn*xn, то variables = ["x1", ..., "xn"].
        self._basic_vars: list[str] = NotImplemented

        self._was_solved = False
        self._optimal_solution_was_found = False

    def find_optimal_solution(self) -> None:
        """
        Поиск оптимального решения задачи линейного программирования Симплекс-методом.
        Основная функция пользовательского интерфейса.

        :return: None.
        """
        if self._was_solved:
            print("Задача уже была решена:")
            self.print_simplex_table()
            self.print_simplex_table_check()

            if self._optimal_solution_was_found:
                print("Было найдено оптимальное решение системы.\n")
            else:
                print("Система не имеет оптимальных решений.\n")
            return

        print(f"Исходные данные:\nc = {self._func_vector}\nA = {self._a_matrix}\nb = {self._b_vector}\n")
        self._check_mode()
        self._set_simplex_table()

        print("Составленная изначально симплекс-таблица:")
        self.print_simplex_table()
        print()

        while self.one_iteration_of_simplex_algorithm():
            self.print_simplex_table()
            self.print_simplex_table_check()
            print()

        self._was_solved = True

    def print_simplex_table(self) -> None:
        """
        Печатает симлпекс-таблицу в консоль.

        :return: None.
        """
        table_for_print = PrettyTable()

        table_for_print.field_names = [""] + self._column_names

        table_with_row_names = list()
        for name, row in zip(self._row_names, self._table):
            row_after_round = [round(elem, 2) for elem in row]
            table_with_row_names.append([name] + row_after_round)
        table_for_print.add_rows(table_with_row_names)

        print(table_for_print)

    def print_simplex_table_check(self) -> None:
        """
        Печатает проверку данных из симплекс-таблицы.
        Проверка заключается в подстановке значений, найденных симплекс-методом, в исходное уравнение.

        :return: None.
        """
        variables_to_values = {var: 0 for var in self._basic_vars}
        for index, row_name in enumerate(self._row_names[:-1]):
            if row_name in self._basic_vars:
                variables_to_values[row_name] = round(self._table[index][0], 2)

        values_of_variables = [f"{var} = {variables_to_values[var]}" for var in self._basic_vars]
        values_of_variables_as_str = ", ".join(values_of_variables)

        equation_1 = [f"{val}*{var}" for val, var in zip(self._func_vector, self._basic_vars)]
        equation_1_as_str = " + ".join(equation_1).replace("+ -", "- ")

        equation_2 = [f"{val}*{variables_to_values[var]}" for val, var in zip(self._func_vector, self._basic_vars)]
        equation_2_as_str = " + ".join(equation_2).replace("+ -", "- ")

        function_result = [val * variables_to_values[var] for val, var in zip(self._func_vector, self._basic_vars)]
        function_result = round(sum(function_result), 2)

        print(f"Проверка при округленных значениях {values_of_variables_as_str}:")
        print(f"{self._func_name} = {equation_1_as_str} = {equation_2_as_str} = {function_result}")

    def _check_mode(self) -> None:
        """
        Проверяет, правильно ли задана задача, которая решается симплекс-методом.

        Возможны 2 варианта:
            1) "ПЗ ЛП" - решается "Прямая задача линейного программирования";
            2) "ДЗ ЛП" - решается "Двойственная задача линейного программирования".

        "ДЗ ЛП" требует дополнительно преобразования входных данных:
            1) Поменять вектора c и b местами;
            2) Транспонировать матрицу A;
            3) Умножить все элементы векторов c и b и матрицы A на (-1).

        :return: None
        """
        if self._mode == "ПЗ ЛП":
            print(f"Решаемая задача: Прямая задача линейного программирования.\n")
            return
        elif self._mode == "ДЗ ЛП":
            print(f"Решаемая задача: Двойственная задача линейного программирования.\n")
        else:
            err_text = "The value of the SimplexAlgorithm.mode must be "
            err_text += '"ПЗ ЛП" (Прямая задача линейного программирования) or '
            err_text += '"ДЗ ЛП" (Двойственная задача линейного программирования).'
            raise ValueError(err_text)

        self._func_vector, self._b_vector = self._b_vector, self._func_vector
        self._func_vector = [-elem for elem in self._func_vector]
        self._b_vector = [-elem for elem in self._b_vector]

        self._a_matrix = matrix_transposition(self._a_matrix)
        self._a_matrix = [[-elem for elem in row] for row in self._a_matrix]

        print(f"Преобразованные данные:\nc' = {self._func_vector}\nA' = {self._a_matrix}\nb' = {self._b_vector}\n")

    def _set_simplex_table(self) -> None:
        """
        Составляет изначальную симплекс-таблицу.

        Инициализирует переменные:
            1) self._table;
            2) self._basic_vars;
            3) self._column_names;
            4) self._row_names.

        :return: None.
        """
        self._table = deepcopy(self._a_matrix)

        self._basic_vars = [f"{self._var_name}{i + 1}" for i in range(len(self._func_vector))]
        self._column_names = ["S0"] + self._basic_vars

        non_basic_vars = [f"{self._var_name}{i + len(self._func_vector) + 1}" for i in range(len(self._b_vector))]
        self._row_names = non_basic_vars + [self._func_name]

        for index, b_item in enumerate(self._b_vector):
            self._table[index] = [b_item] + self._table[index]

        self._table.append([0] + self._func_vector)

    def one_iteration_of_simplex_algorithm(self):
        """
        Производит одну полную итерацию симплекс-метода.

        :return: 1) True - когда итерация завершилась успешно;
                 2) False - когда система была признана решенной или не имеющей оптимальных решений.
        """
        # 1а. Поиск индекса разрешающего столбца в столбце пересечений S0 со строками с переменными.
        index_of_pivot_column = self._find_index_of_pivot_column_in_s0_column()
        if index_of_pivot_column is None:
            return False

        # 1б. Поиск индекса разрешающего столбца в строке пересечений F со столбцами с переменными.
        if index_of_pivot_column is NotImplemented:
            index_of_pivot_column = self._find_index_of_pivot_column_in_function_row()
        if index_of_pivot_column is None:
            return False

        # 2. Поиск индекса разрешающей строки.
        index_of_pivot_row = self._find_index_of_pivot_row(index_of_pivot_column)

        # 3. Замена name-тэгов разрешающих столбца и строки.
        pivot_row = self._row_names[index_of_pivot_row]
        pivot_column = self._column_names[index_of_pivot_column]
        print(f"Замена разрешающих строки и столбца: {pivot_row} и {pivot_column}.")
        self._row_names[index_of_pivot_row], self._column_names[index_of_pivot_column] = pivot_column, pivot_row

        # 4. Пересчет симплекс-таблицы.
        self._recalculate_simplex_table(index_of_pivot_row, index_of_pivot_column)
        return True

    def _find_index_of_pivot_column_in_s0_column(self) -> int or NotImplemented or None:
        """
        Поиск индекса разрешающего столбца в столбце пересечений S0 со строками с переменными.

        Также включена проверка всех строк, в которых элементы на пересечении с S0 меньше 0.

        Выбирается наименьшее значение S0 из имеющихся отрицательных.
        Выбирается наименьшее значение в строке с отрицательным элементом на пересечении с S0, тоже отрицательное.

        :return: 1) int: Индекс разрешающего столбца;
                 2) NotImplemented: В векторе пересечений S0 и переменных нет отрицальных элементов,
                                    индекс разрещающего столбца не был найден;
                 3) None: Было выяснено, что система не имеет оптимальных решений.
        """
        index_of_pivot_column = NotImplemented
        vector_of_s0 = [row[0] for row in self._table[:-1]]
        min_s0 = min(vector_of_s0)

        for row_index, elem_of_column in enumerate(vector_of_s0):
            if elem_of_column < 0:
                min_elem_in_row = min(self._table[row_index][1:])
                if min_elem_in_row >= 0:
                    print("Система не имеет оптимальных решений.\n")
                    return None

                if elem_of_column == min_s0:
                    index_of_pivot_column = self._table[row_index][1:].index(min_elem_in_row) + 1

        return index_of_pivot_column

    def _find_index_of_pivot_column_in_function_row(self) -> int or None:
        """
        Поиск индекса разрешающего столбца в строке пересечений F со столбцами с переменными.

        Также включена проверка: должен быть хотя бы один положительный элемент.

        :return: 1) int: Индекс разрешающего столбца;
                 2) None: Оптимальное решение системы уже найдено.
        """
        function_vector = self._table[-1][1:]

        if max(function_vector) > 0:
            min_positive_elem_of_function = min([elem for elem in function_vector if elem > 0])
            return function_vector.index(min_positive_elem_of_function) + 1
        else:
            print("Найдено оптимальное решение системы.\n")
            self._optimal_solution_was_found = True
            return None

    def _find_index_of_pivot_row(self, index_of_pivot_column: int) -> int:
        """
        Поиск индекса разрешающей строки.

        :param index_of_pivot_column: Индекс разрешающего стобца.
        :return: Индекса разрешающей строки.
        """
        s0_divided_by_pivot_column = list()
        for row in self._table[:-1]:
            if row[index_of_pivot_column] and row[0] and row[0] / row[index_of_pivot_column] > 0:
                s0_divided_by_pivot_column.append(row[0] / row[index_of_pivot_column])
            else:
                s0_divided_by_pivot_column.append(float("inf"))

        return s0_divided_by_pivot_column.index(min(s0_divided_by_pivot_column))

    def _recalculate_simplex_table(self, index_of_pivot_row: int, index_of_pivot_column: int) -> None:
        """
        Пересчитываем все элементы симплекс таблицы по алгоритму.

        Алгоритм пересчета:
            1) Новый центральный элемент - это старый центральный элемент, возведенный в степень (-1);
            2) Новый элементы разрешающей строки - старые элементы разрешающей строки, деленный на старый центральный;
            3) Новые элементы разрешающего столбца - старые элементы разрешающего столбца,
               деленный на старый центральный, умноженные на (-1);
            4) Все новые другие элементы - старые элементы, из которых вычли произведение соотвествующих им
               старых элементов разрешающей строки и разрешающего столбоца
               (у них такой же индекс, как у другого элемента), деленное на старый центральный.


        p.s. Центральный элемент - это элемент на пересечении разрешающей строки и разрешающего столбца.

        :param index_of_pivot_row:
        :param index_of_pivot_column:
        :return:
        """
        new_table = deepcopy(self._table)
        central_elem = self._table[index_of_pivot_row][index_of_pivot_column]

        for row_index, column in enumerate(self._table):
            for column_index, elem in enumerate(column):
                if row_index == index_of_pivot_row and column_index == index_of_pivot_column:
                    new_table[row_index][column_index] = 1 / central_elem
                elif row_index == index_of_pivot_row:
                    new_table[row_index][column_index] = elem / central_elem
                elif column_index == index_of_pivot_column:
                    new_table[row_index][column_index] = -elem / central_elem
                else:
                    elem_of_pivot_row = self._table[index_of_pivot_row][column_index]
                    elem_of_pivot_column = self._table[row_index][index_of_pivot_column]

                    new_table[row_index][column_index] = elem - elem_of_pivot_row * elem_of_pivot_column / central_elem

        self._table = new_table
