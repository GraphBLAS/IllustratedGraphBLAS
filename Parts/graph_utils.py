from manim import *


def set_vertex_fill_preserve_label(vertex, color, opacity=1):
    """
    Set the fill color of a LabeledDot vertex while keeping the label black.

    Args:
        vertex: A LabeledDot vertex from a DiGraph
        color: The fill color to apply to the dot background
        opacity: The fill opacity (default: 1)
    """
    vertex.set_fill(color, opacity)
    # Reset the label (first submobject) to black
    if vertex.submobjects:
        vertex.submobjects[0].set_color(BLACK)


def animate_vertex_fill(vertex, color, opacity=1):
    """
    Create an animation that changes vertex fill while preserving label color.

    Args:
        vertex: A LabeledDot vertex from a DiGraph
        color: The target fill color
        opacity: The target fill opacity (default: 1)

    Returns:
        An animation that can be passed to self.play()
    """
    def update_func(v):
        set_vertex_fill_preserve_label(v, color, opacity)
        return v
    return ApplyFunction(update_func, vertex)


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

    # Create labels manually with color=BLACK to work around Manim bug
    # (DiGraph uses fill_color= but MathTex requires color=)
    labels = {v: MathTex(v, color=BLACK) for v in nodes}

    return DiGraph(
        vertices=nodes,
        edges=edges,
        layout=layout,
        labels=labels,
        edge_config={"stroke_color": edge_color}
    ).scale(scale)
