def matrix_transposition(matrix: list[list[int or float]]) -> list[list[int or float]]:
    """
    Транспонирует матрицу.

    :param matrix: Матрица до транспонирования.
    :return: Матрица после транспонирования.
    """
    transposed_matrix = [[row[index] for row in matrix] for index in range(len(matrix[0]))]
    return transposed_matrix
