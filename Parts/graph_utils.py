from manim import *
import math


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


def create_adjacency_digraph(matrix_data, layout="triangle", scale=1, edge_color=BLUE, edge_labels=False):
    """
    Create a directed graph from an adjacency matrix.

    Args:
        matrix_data: 2D list representing the adjacency matrix
        layout: Layout algorithm for graph positioning (default: "kamada_kawai")
                Can also be "triangle" for a fixed equilateral triangle layout (6 nodes)
        scale: Scale factor for the graph (default: 1.3)
        edge_color: Color for the edges (default: BLUE)
        edge_labels: If True, return (graph, labels_group) with edge weight labels

    Returns:
        DiGraph object, or (DiGraph, VGroup) if edge_labels=True
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

    # Handle custom triangle layout for 6-node graphs
    if layout == "triangle" and num_rows == 6:
        sqrt3 = math.sqrt(3)
        positions = {
            0: [-3, -sqrt3, 0],      # Base left
            1: [0, -sqrt3, 0],       # Base center
            2: [3, -sqrt3, 0],       # Base right
            3: [-1.5, 0, 0],         # Middle left
            4: [1.5, 0, 0],          # Middle right
            5: [0, sqrt3, 0]         # Top point
        }
        layout = positions
    else:
        positions = None

    graph = DiGraph(
        vertices=nodes,
        edges=edges,
        layout=layout,
        labels=labels,
        edge_config={"stroke_color": edge_color}
    ).scale(scale)

    if not edge_labels:
        return graph

    # Create edge weight labels
    weight_labels = VGroup()

    if positions is not None:
        # Use known positions for label placement
        for i, j in edges:
            weight = matrix_data[i][j]
            start = np.array(positions[i]) * scale
            end = np.array(positions[j]) * scale
            mid = (start + end) / 2
            # Offset perpendicular to edge
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.3
            label = Text(str(weight), font_size=20, color=YELLOW).move_to(mid + perp)
            weight_labels.add(label)
    else:
        # Use graph vertex positions after creation
        for i, j in edges:
            weight = matrix_data[i][j]
            start = graph.vertices[i].get_center()
            end = graph.vertices[j].get_center()
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.3
            label = Text(str(weight), font_size=20, color=YELLOW).move_to(mid + perp)
            weight_labels.add(label)

    return graph, weight_labels
