from manim import *

# The 6x6 sparse adjacency matrix used in Chapter0 Scene2 and Scene3
CHAPTER0_MATRIX_DATA = [
    [0, 1, 0, 2, 0, 0],
    [0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 9],
    [0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 2, 0]
]


def create_labeled_matrix(matrix_data, scale=1.5, v_buff=0.5, h_buff=0.5):
    """
    Create a matrix with row and column labels.

    Args:
        matrix_data: 2D list of matrix values
        scale: Scale factor for the matrix
        v_buff: Vertical buffer between matrix entries
        h_buff: Horizontal buffer between matrix entries

    Returns:
        Tuple of (Matrix, row_labels list, col_labels list)
    """
    num_rows = len(matrix_data)
    num_cols = len(matrix_data[0])

    matrix = Matrix(matrix_data, v_buff=v_buff, h_buff=h_buff).scale(scale)
    row_labels = [Tex(str(i)) for i in range(num_rows)]
    col_labels = [Tex(str(j)) for j in range(num_cols)]

    for i, label in enumerate(row_labels):
        label.next_to(matrix.get_rows()[i], LEFT * 3)
    for j, label in enumerate(col_labels):
        label.next_to(matrix.get_columns()[j], UP * 1.5)

    return matrix, row_labels, col_labels


def hide_zero_entries(matrix, matrix_data):
    """
    Set opacity to 0 for all zero entries in a matrix.

    Args:
        matrix: Manim Matrix object
        matrix_data: 2D list of the original matrix values

    Returns:
        List of animations to fade out zero entries
    """
    num_cols = len(matrix_data[0])
    zero_positions = [
        (i, j) for i in range(len(matrix_data))
        for j in range(num_cols) if matrix_data[i][j] == 0
    ]
    return [
        matrix.get_entries()[i * num_cols + j].animate.set_opacity(0)
        for i, j in zero_positions
    ]


def get_non_zero_positions(matrix_data):
    """
    Get positions and values of non-zero entries in a matrix.

    Args:
        matrix_data: 2D list of matrix values

    Returns:
        List of tuples (row, col, value) for non-zero entries
    """
    num_rows = len(matrix_data)
    num_cols = len(matrix_data[0])
    return [
        (i, j, matrix_data[i][j])
        for i in range(num_rows) for j in range(num_cols) if matrix_data[i][j] != 0
    ]


def get_zero_positions(matrix_data):
    """
    Get positions of zero entries in a matrix.

    Args:
        matrix_data: 2D list of matrix values

    Returns:
        List of tuples (row, col) for zero entries
    """
    num_rows = len(matrix_data)
    num_cols = len(matrix_data[0])
    return [
        (i, j)
        for i in range(num_rows) for j in range(num_cols) if matrix_data[i][j] == 0
    ]
