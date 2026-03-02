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

# Symmetric 6x6 adjacency matrix for Chapter3 (undirected graph)
# Same structure as CHAPTER0 but with bidirectional edges
# Edges: 0↔1, 0↔3, 1↔2, 2↔4, 3↔4, 3↔5, 4↔5
CHAPTER3_MATRIX_DATA = [
    [0, 1, 0, 2, 0, 0],
    [1, 0, 5, 0, 0, 0],
    [0, 5, 0, 0, 5, 0],
    [2, 0, 0, 0, 2, 9],
    [0, 0, 5, 2, 0, 2],
    [0, 0, 0, 9, 2, 0]
]


def create_labeled_matrix(matrix_data, scale=1, v_buff=0.5, h_buff=0.5):
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
        label.next_to(matrix.get_rows()[i], LEFT * 4)
    for j, label in enumerate(col_labels):
        label.next_to(matrix.get_columns()[j], UP * 2)

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


def create_sparse_matrix(data, scale=0.6, v_buff=0.8, h_buff=1.0):
    """
    Create a matrix with zero entries hidden (opacity 0).

    This preserves matrix dimensions while visually hiding absent values.
    Use integer 0 for absent entries in the data.

    Args:
        data: 2D list of matrix values (use 0 for absent entries)
        scale: Scale factor for the matrix
        v_buff: Vertical buffer between entries
        h_buff: Horizontal buffer between entries

    Returns:
        Matrix with zero entries set to opacity 0
    """
    matrix = Matrix(data, v_buff=v_buff, h_buff=h_buff).scale(scale)

    num_cols = len(data[0])
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val == 0:
                matrix.get_entries()[i * num_cols + j].set_opacity(0)

    return matrix


# Chapter 5 example: 3 nodes, 3 directed edges
# e0: 0→1, e1: 1→2, e2: 0→2
CHAPTER5_EDGES = [(0, 1), (1, 2), (0, 2)]


def create_incidence_matrices(edges, n_nodes=None, scale=0.55,
                               node_color=BLUE, edge_color=GREEN):
    """
    Create S (source) and D (destination) incidence matrices from edge list.

    For directed graphs, the incidence relationship is captured by two matrices:
    - S (source): n×m matrix where S[i,e]=1 if node i is the source of edge e
    - D (destination): m×n matrix where D[e,j]=1 if node j is the destination of edge e

    Args:
        edges: List of (source, destination) tuples, e.g. [(0,1), (1,2), (0,2)]
        n_nodes: Number of nodes (auto-detected from max node index + 1 if None)
        scale: Matrix scale factor
        node_color: Color for node labels
        edge_color: Color for edge labels

    Returns:
        Tuple of (S_group, D_group, S_data, D_data) where:
        - S_group: VGroup with matrix, labels, and titles
        - D_group: VGroup with matrix, labels, and titles
        - S_data: Raw S matrix data (2D list, for computations)
        - D_data: Raw D matrix data (2D list, for computations)
    """
    n_nodes = n_nodes or (max(max(e) for e in edges) + 1)
    n_edges = len(edges)

    # S[node, edge] = 1 if node is source of edge
    S_data = [[0] * n_edges for _ in range(n_nodes)]
    for e_idx, (src, dst) in enumerate(edges):
        S_data[src][e_idx] = 1

    # D[edge, node] = 1 if node is destination of edge
    D_data = [[0] * n_nodes for _ in range(n_edges)]
    for e_idx, (src, dst) in enumerate(edges):
        D_data[e_idx][dst] = 1

    # Create S matrix visualization
    S_mat = create_sparse_matrix(S_data, scale=scale)

    S_row_labels = VGroup(*[
        Text(str(i), font_size=12, color=node_color).next_to(
            S_mat.get_rows()[i], LEFT, buff=0.25)
        for i in range(n_nodes)
    ])
    S_col_labels = VGroup(*[
        Text(f"e{j}", font_size=12, color=edge_color).next_to(
            S_mat.get_columns()[j], UP, buff=0.2)
        for j in range(n_edges)
    ])

    # Row/col titles
    S_row_title = Text("nodes", font_size=10, color=node_color).rotate(PI / 2)
    S_row_title.next_to(S_row_labels, LEFT, buff=0.15)
    S_col_title = Text("edges", font_size=10, color=edge_color)
    S_col_title.next_to(S_col_labels, UP, buff=0.1)

    S_group = VGroup(S_mat, S_row_labels, S_col_labels, S_row_title, S_col_title)
    S_group.matrix = S_mat

    # Create D matrix visualization
    D_mat = create_sparse_matrix(D_data, scale=scale)

    D_row_labels = VGroup(*[
        Text(f"e{i}", font_size=12, color=edge_color).next_to(
            D_mat.get_rows()[i], LEFT, buff=0.25)
        for i in range(n_edges)
    ])
    D_col_labels = VGroup(*[
        Text(str(j), font_size=12, color=node_color).next_to(
            D_mat.get_columns()[j], UP, buff=0.2)
        for j in range(n_nodes)
    ])

    D_row_title = Text("edges", font_size=10, color=edge_color).rotate(PI / 2)
    D_row_title.next_to(D_row_labels, LEFT, buff=0.15)
    D_col_title = Text("nodes", font_size=10, color=node_color)
    D_col_title.next_to(D_col_labels, UP, buff=0.1)

    D_group = VGroup(D_mat, D_row_labels, D_col_labels, D_row_title, D_col_title)
    D_group.matrix = D_mat

    return S_group, D_group, S_data, D_data
