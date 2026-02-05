from manim import *


def create_adjacency_digraph(matrix_data, layout="kamada_kawai", scale=1.3, edge_color=BLUE):
    """
    Create a directed graph from an adjacency matrix.

    Args:
        matrix_data: 2D list representing the adjacency matrix
        layout: Layout algorithm for graph positioning (default: "kamada_kawai")
        scale: Scale factor for the graph (default: 1.3)
        edge_color: Color for the edges (default: BLUE)

    Returns:
        DiGraph object representing the adjacency matrix
    """
    num_rows = len(matrix_data)
    num_cols = len(matrix_data[0])

    nodes = list(range(num_rows))
    edges = [
        (i, j) for i in range(num_rows) for j in range(num_cols) if matrix_data[i][j] != 0
    ]

    return DiGraph(
        vertices=nodes,
        edges=edges,
        layout=layout,
        labels=True,
        edge_config={"stroke_color": edge_color}
    ).scale(scale)
