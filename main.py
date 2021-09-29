from simpflex_lib import SimplexAlgorithm


if __name__ == '__main__':
    print("\nЛАБОРАТОРНАЯ РАБОТА №1.")
    print('ТЕМА: "Симплекс-метод в прямой задаче линейного программирования".')
    print("Вариант №5.\n")

    c_vector_1 = [6, 6, 6]
    a_matrix_1 = [[4, 1, 1],
                  [1, 2, 0],
                  [0, 0.5, 4]]
    b_vector_1 = [5, 3, 8]

    simplex_algorithm_lab_1 = SimplexAlgorithm(c_vector_1, a_matrix_1, b_vector_1)
    simplex_algorithm_lab_1.find_optimal_solution()

    print("\nЛАБОРАТОРНАЯ РАБОТА №2.")
    print('ТЕМА: "Симплекс-метод в двойственной задаче линейного программирования".')
    print("Вариант №5.\n")

    c_vector_2 = [3, 3, 7]
    a_matrix_2 = [[1, 1, 1],
                  [1, 4, 0],
                  [0, 0.5, 3]]
    b_vector_2 = [3, 5, 7]

    simplex_algorithm_lab_2 = SimplexAlgorithm(c_vector_2, a_matrix_2, b_vector_2,
                                               var_name="y", func_name="G", mode="ДЗ ЛП")
    simplex_algorithm_lab_2.find_optimal_solution()
