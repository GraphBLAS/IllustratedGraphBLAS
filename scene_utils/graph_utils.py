from manim import *
import math
import numpy as np


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


def create_small_graph_from_matrix(matrix_data, scale=0.3, directed=False, edge_color=BLUE, show_weights=False):
    """
    Create a small graph visualization from an adjacency matrix.
    Designed to be placed below matrices to show the graph structure.

    Args:
        matrix_data: 2D list representing the adjacency matrix
        scale: Scale factor for the graph (default: 0.3 for small display)
        directed: If True, use single arrows; if False, use double arrows for symmetric matrices
        edge_color: Color for the edges (default: BLUE)
        show_weights: If True, show edge weights (default: False)

    Returns:
        VGroup containing the graph visualization
    """
    num_nodes = len(matrix_data)

    # Create circular layout for arbitrary sized graphs
    positions = {}
    for i in range(num_nodes):
        angle = 2 * math.pi * i / num_nodes - math.pi / 2  # Start from top
        positions[i] = np.array([
            math.cos(angle) * 1.5,
            math.sin(angle) * 1.5,
            0
        ])

    # Create vertices as small labeled dots
    vertices = {}
    for i in range(num_nodes):
        label = MathTex(str(i), color=BLACK).scale(0.4)
        dot = LabeledDot(label, radius=0.2, fill_color=WHITE, fill_opacity=1)
        dot.move_to(positions[i])
        vertices[i] = dot

    # Find edges
    edges_data = []
    if directed:
        # For directed graphs, include all non-zero entries
        for i in range(num_nodes):
            for j in range(num_nodes):
                if matrix_data[i][j] != 0:
                    edges_data.append((i, j, matrix_data[i][j]))
    else:
        # For undirected, only use upper triangle (assumes symmetric)
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if matrix_data[i][j] != 0:
                    edges_data.append((i, j, matrix_data[i][j]))

    # Create edges
    edges = VGroup()
    weight_labels = VGroup()

    for i, j, weight in edges_data:
        start = positions[i]
        end = positions[j]

        if directed:
            arrow = Arrow(
                start, end,
                color=edge_color,
                buff=0.25,
                stroke_width=2,
                tip_length=0.1,
                max_tip_length_to_length_ratio=0.2
            )
        else:
            arrow = DoubleArrow(
                start, end,
                color=edge_color,
                buff=0.25,
                stroke_width=2,
                tip_length=0.08,
                max_tip_length_to_length_ratio=0.15
            )
        edges.add(arrow)

        if show_weights and weight != 1:
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.2
            label = Text(str(weight), font_size=12, color=YELLOW).move_to(mid + perp)
            weight_labels.add(label)

    # Combine into graph group
    graph = VGroup(edges, *vertices.values(), weight_labels)
    graph.vertices = vertices

    return graph.scale(scale)


def create_square_digraph(matrix_data, color, show_weights=False):
    """
    Create a directed graph from a 4x4 adjacency matrix with square layout.
    Used for element-wise operation visualizations.

    Args:
        matrix_data: 4x4 adjacency matrix
        color: Color for edges
        show_weights: If True, show edge weight labels

    Returns:
        VGroup containing the graph with vertices and edges attributes
    """
    n = len(matrix_data)
    positions = {
        0: np.array([-0.7, 0.7, 0]),
        1: np.array([0.7, 0.7, 0]),
        2: np.array([0.7, -0.7, 0]),
        3: np.array([-0.7, -0.7, 0]),
    }

    # Create vertices
    vertices = {}
    for i in range(n):
        label = MathTex(str(i), color=BLACK).scale(0.5)
        dot = LabeledDot(label, radius=0.2, fill_color=WHITE, fill_opacity=1)
        dot.move_to(positions[i])
        vertices[i] = dot

    # Create edges
    edges = VGroup()
    edge_labels = VGroup()
    for i in range(n):
        for j in range(n):
            if matrix_data[i][j] != 0:
                arrow = Arrow(
                    positions[i], positions[j],
                    color=color, buff=0.25, stroke_width=3,
                    tip_length=0.15, max_tip_length_to_length_ratio=0.25
                )
                edges.add(arrow)

                if show_weights:
                    weight = matrix_data[i][j]
                    weight_label = Text(str(weight), font_size=16, color=color)
                    # Position label at midpoint, offset perpendicular to edge
                    mid = (positions[i] + positions[j]) / 2
                    direction = positions[j] - positions[i]
                    perp = np.array([-direction[1], direction[0], 0])
                    perp = perp / np.linalg.norm(perp) * 0.15
                    weight_label.move_to(mid + perp)
                    edge_labels.add(weight_label)

    graph = VGroup(edges, edge_labels, *vertices.values())
    graph.vertices = vertices
    graph.edges = edges
    graph.edge_labels = edge_labels
    graph.positions = positions
    return graph


def create_multigraph_visual(nodes, edges, scale=0.8, node_radius=0.3):
    """
    Create a multi-graph visualization with curved parallel edges.

    Args:
        nodes: List of node positions as (x, y) tuples or dict of {node_id: (x, y)}
        edges: List of (source, target) tuples, can have duplicates
        scale: Scale factor for the graph
        node_radius: Radius of node circles

    Returns:
        VGroup containing vertices and edges, with vertices dict attached
    """
    # Convert nodes to dict if list
    if isinstance(nodes, list):
        positions = {i: np.array([*pos, 0]) for i, pos in enumerate(nodes)}
    else:
        positions = {k: np.array([*v, 0]) if len(v) == 2 else np.array(v) for k, v in nodes.items()}

    # Count edge occurrences between each pair
    edge_counts = {}
    for src, tgt in edges:
        key = (min(src, tgt), max(src, tgt))
        edge_counts[key] = edge_counts.get(key, 0) + 1

    # Track which instance we're on for each edge pair
    edge_instance = {}

    # Create vertices
    vertices = {}
    for i, pos in positions.items():
        label = MathTex(str(i), color=BLACK).scale(0.6)
        dot = LabeledDot(label, radius=node_radius, fill_color=WHITE, fill_opacity=1)
        dot.move_to(pos)
        vertices[i] = dot

    # Create edges with curves for parallel edges
    edge_mobjects = VGroup()
    for src, tgt in edges:
        key = (min(src, tgt), max(src, tgt))
        total = edge_counts[key]
        instance = edge_instance.get(key, 0)
        edge_instance[key] = instance + 1

        start = positions[src]
        end = positions[tgt]

        if total == 1:
            # Single edge: straight line
            edge = Arrow(
                start, end,
                color=BLUE,
                buff=node_radius + 0.05,
                stroke_width=3,
                tip_length=0.15,
                max_tip_length_to_length_ratio=0.2
            )
        else:
            # Multiple edges: use curves
            # Calculate curve angle based on instance
            curve_angle = (instance - (total - 1) / 2) * 0.4
            edge = CurvedArrow(
                start, end,
                angle=curve_angle,
                color=BLUE,
                stroke_width=3,
                tip_length=0.15
            )
            # Adjust for buff
            edge.shift(edge.get_start() - start)

        edge_mobjects.add(edge)

    graph = VGroup(edge_mobjects, *vertices.values())
    graph.vertices = vertices
    graph.edges = edge_mobjects

    return graph.scale(scale)


def create_hyperedge_region(node_positions, color=BLUE, opacity=0.3, stroke_width=2):
    """
    Create a colored region (convex hull) around a set of nodes for hyperedge visualization.

    Args:
        node_positions: List of (x, y) or (x, y, z) coordinates
        color: Fill and stroke color
        opacity: Fill opacity
        stroke_width: Stroke width for the boundary

    Returns:
        Polygon mobject representing the hyperedge region
    """
    # Convert to 2D for hull calculation
    points_2d = []
    for pos in node_positions:
        if len(pos) == 2:
            points_2d.append(pos)
        else:
            points_2d.append(pos[:2])

    # For 2 points, create an ellipse around them
    if len(points_2d) == 2:
        center = np.array([(points_2d[0][0] + points_2d[1][0]) / 2,
                          (points_2d[0][1] + points_2d[1][1]) / 2, 0])
        width = np.linalg.norm(np.array(points_2d[1]) - np.array(points_2d[0])) + 0.8
        height = 0.8
        angle = np.arctan2(points_2d[1][1] - points_2d[0][1],
                          points_2d[1][0] - points_2d[0][0])
        ellipse = Ellipse(width=width, height=height, color=color,
                         fill_opacity=opacity, stroke_width=stroke_width)
        ellipse.rotate(angle)
        ellipse.move_to(center)
        return ellipse

    # For 3+ points, compute convex hull and expand it
    from scipy.spatial import ConvexHull

    points_array = np.array(points_2d)

    # Handle collinear points
    try:
        hull = ConvexHull(points_array)
        hull_points = points_array[hull.vertices]
    except:
        # Collinear: just use all points sorted by angle from centroid
        centroid = points_array.mean(axis=0)
        angles = np.arctan2(points_array[:, 1] - centroid[1],
                          points_array[:, 0] - centroid[0])
        sorted_idx = np.argsort(angles)
        hull_points = points_array[sorted_idx]

    # Expand hull outward from centroid
    centroid = hull_points.mean(axis=0)
    expanded = []
    for pt in hull_points:
        direction = pt - centroid
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
        expanded.append(pt + direction * 0.4)

    # Create polygon with 3D coordinates
    polygon_points = [np.array([*pt, 0]) for pt in expanded]
    polygon = Polygon(*polygon_points, color=color, fill_opacity=opacity,
                     stroke_width=stroke_width)

    return polygon


def create_bipartite_graph(left_nodes, right_nodes, edges, scale=0.8, left_color=BLUE, right_color=GREEN):
    """
    Create a bipartite graph with left and right node columns.

    Args:
        left_nodes: Number of nodes on left side (or list of labels)
        right_nodes: Number of nodes on right side (or list of labels)
        edges: List of (left_idx, right_idx) tuples
        scale: Scale factor
        left_color: Color for left partition nodes
        right_color: Color for right partition nodes

    Returns:
        VGroup with vertices dict containing 'L0', 'L1', ... and 'R0', 'R1', ...
    """
    # Handle count or list input
    if isinstance(left_nodes, int):
        left_labels = list(range(left_nodes))
        n_left = left_nodes
    else:
        left_labels = left_nodes
        n_left = len(left_nodes)

    if isinstance(right_nodes, int):
        right_labels = list(range(right_nodes))
        n_right = right_nodes
    else:
        right_labels = right_nodes
        n_right = len(right_nodes)

    # Position nodes
    left_x = -2
    right_x = 2
    spacing = 1.2

    vertices = {}

    # Left nodes
    for i, lbl in enumerate(left_labels):
        y = (n_left - 1) / 2 * spacing - i * spacing
        label = MathTex(str(lbl), color=BLACK).scale(0.5)
        dot = LabeledDot(label, radius=0.25, fill_color=left_color, fill_opacity=0.8)
        dot.move_to(np.array([left_x, y, 0]))
        vertices[f'L{i}'] = dot

    # Right nodes
    for i, lbl in enumerate(right_labels):
        y = (n_right - 1) / 2 * spacing - i * spacing
        label = MathTex(str(lbl), color=BLACK).scale(0.5)
        dot = LabeledDot(label, radius=0.25, fill_color=right_color, fill_opacity=0.8)
        dot.move_to(np.array([right_x, y, 0]))
        vertices[f'R{i}'] = dot

    # Create edges
    edge_mobjects = VGroup()
    for li, ri in edges:
        start = vertices[f'L{li}'].get_center()
        end = vertices[f'R{ri}'].get_center()
        edge = Line(start, end, color=GRAY, stroke_width=2)
        edge_mobjects.add(edge)

    graph = VGroup(edge_mobjects, *vertices.values())
    graph.vertices = vertices
    graph.edges = edge_mobjects

    return graph.scale(scale)


def create_undirected_graph(matrix_data, layout="triangle", scale=1, edge_color=BLUE, edge_labels=False):
    """
    Create an undirected graph from a symmetric adjacency matrix.
    Uses double-ended arrows to indicate bidirectional edges.

    Args:
        matrix_data: 2D list representing a symmetric adjacency matrix
        layout: Layout algorithm for graph positioning (default: "triangle")
        scale: Scale factor for the graph (default: 1)
        edge_color: Color for the edges (default: BLUE)
        edge_labels: If True, return (graph, labels_group) with edge weight labels

    Returns:
        VGroup containing vertices and edges, or (VGroup, VGroup) if edge_labels=True
    """
    num_rows = len(matrix_data)

    # Handle custom triangle layout for 6-node graphs
    if layout == "triangle" and num_rows == 6:
        sqrt3 = math.sqrt(3)
        positions = {
            0: np.array([-3, -sqrt3, 0]),      # Base left
            1: np.array([0, -sqrt3, 0]),       # Base center
            2: np.array([3, -sqrt3, 0]),       # Base right
            3: np.array([-1.5, 0, 0]),         # Middle left
            4: np.array([1.5, 0, 0]),          # Middle right
            5: np.array([0, sqrt3, 0])         # Top point
        }
    else:
        # Default circular layout
        positions = {
            i: np.array([
                math.cos(2 * math.pi * i / num_rows),
                math.sin(2 * math.pi * i / num_rows),
                0
            ]) * 2 for i in range(num_rows)
        }

    # Scale positions
    for k in positions:
        positions[k] = positions[k] * scale

    # Create vertices as labeled dots
    vertices = {}
    for i in range(num_rows):
        label = MathTex(str(i), color=BLACK).scale(0.7)
        dot = LabeledDot(label, radius=0.3, fill_color=WHITE, fill_opacity=1)
        dot.move_to(positions[i])
        vertices[i] = dot

    # Find unique edges (only use upper triangle of symmetric matrix)
    edges_data = []
    for i in range(num_rows):
        for j in range(i + 1, num_rows):
            if matrix_data[i][j] != 0:
                edges_data.append((i, j, matrix_data[i][j]))

    # Create double-ended arrows for edges
    edges = VGroup()
    weight_labels = VGroup()
    edge_dict = {}  # Map (i,j) and (j,i) to edge mobject

    for i, j, weight in edges_data:
        start = positions[i]
        end = positions[j]

        # Create double arrow
        double_arrow = DoubleArrow(
            start, end,
            color=edge_color,
            buff=0.35,  # Space for vertex circles
            stroke_width=3,
            tip_length=0.2,
            max_tip_length_to_length_ratio=0.15
        )
        edges.add(double_arrow)
        # Store edge reference for both directions
        edge_dict[(i, j)] = double_arrow
        edge_dict[(j, i)] = double_arrow

        if edge_labels:
            # Add weight label at midpoint
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.3
            label = Text(str(weight), font_size=20, color=YELLOW).move_to(mid + perp)
            weight_labels.add(label)

    # Combine into graph group
    graph = VGroup(edges, *vertices.values())
    # Store vertices dict for easy access
    graph.vertices = vertices
    graph.edges_group = edges
    graph.edge_dict = edge_dict  # Direct edge lookup
    graph.positions = positions

    if edge_labels:
        return graph, weight_labels
    return graph


def get_edge_between_vertices(graph, i, j):
    """
    Find the edge mobject connecting vertices i and j in an undirected graph.

    Args:
        graph: Graph created by create_undirected_graph
        i, j: Vertex indices

    Returns:
        The DoubleArrow edge mobject, or None if not found
    """
    # Use direct lookup if edge_dict is available
    if hasattr(graph, 'edge_dict'):
        return graph.edge_dict.get((i, j))

    # Fallback to position-based search for backwards compatibility
    pos_i = graph.positions[i]
    pos_j = graph.positions[j]
    mid = (pos_i + pos_j) / 2

    for edge in graph.edges_group:
        edge_mid = edge.get_center()
        if np.linalg.norm(edge_mid - mid) < 0.5:
            return edge
    return None


def highlight_triangle(graph, triangle, color=YELLOW, edge_width=6):
    """
    Create highlight copies of edges forming a triangle.

    Args:
        graph: Graph created by create_undirected_graph
        triangle: Tuple of 3 vertex indices (i, j, k)
        color: Highlight color
        edge_width: Stroke width for highlighted edges

    Returns:
        VGroup of highlighted edge copies
    """
    i, j, k = triangle
    highlights = VGroup()

    for a, b in [(i, j), (j, k), (i, k)]:
        edge = get_edge_between_vertices(graph, a, b)
        if edge:
            highlight = edge.copy()
            highlight.set_color(color)
            highlight.set_stroke(width=edge_width)
            highlights.add(highlight)

    return highlights


def color_nodes_by_value(graph, values, low_color=WHITE, high_color=RED):
    """
    Color graph nodes based on numeric values using gradient interpolation.

    Args:
        graph: Graph with vertices dict
        values: List of values for each node (index-aligned), or dict {node: value}
        low_color: Color for minimum value
        high_color: Color for maximum value

    Returns:
        List of (vertex, target_color) tuples for animation
    """
    if isinstance(values, dict):
        values_list = [values.get(i, 0) for i in range(len(graph.vertices))]
    else:
        values_list = values

    min_val = min(values_list)
    max_val = max(values_list)
    val_range = max_val - min_val if max_val > min_val else 1

    result = []
    for i, vertex in graph.vertices.items():
        t = (values_list[i] - min_val) / val_range
        color = interpolate_color(low_color, high_color, t)
        result.append((vertex, color))

    return result


# Karate club graph adjacency data (Zachary 1977)
# 34 nodes, 78 edges
KARATE_EDGES = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 10), (0, 11),
    (0, 12), (0, 13), (0, 17), (0, 19), (0, 21), (0, 31),
    (1, 2), (1, 3), (1, 7), (1, 13), (1, 17), (1, 19), (1, 21), (1, 30),
    (2, 3), (2, 7), (2, 8), (2, 9), (2, 13), (2, 27), (2, 28), (2, 32),
    (3, 7), (3, 12), (3, 13),
    (4, 6), (4, 10),
    (5, 6), (5, 10), (5, 16),
    (6, 16),
    (8, 30), (8, 32), (8, 33),
    (9, 33),
    (13, 33),
    (14, 32), (14, 33),
    (15, 32), (15, 33),
    (18, 32), (18, 33),
    (19, 33),
    (20, 32), (20, 33),
    (22, 32), (22, 33),
    (23, 25), (23, 27), (23, 29), (23, 32), (23, 33),
    (24, 25), (24, 27), (24, 31),
    (25, 31),
    (26, 29), (26, 33),
    (27, 33),
    (28, 31), (28, 33),
    (29, 32), (29, 33),
    (30, 32), (30, 33),
    (31, 32), (31, 33),
    (32, 33),
]

# Per-node triangle counts for karate graph
KARATE_TRIANGLE_COUNTS = [
    18, 12, 11, 10, 2, 3, 3, 6, 5, 1,  # nodes 0-9
    2, 0, 1, 5, 1, 1, 1, 0, 1, 1,      # nodes 10-19
    1, 0, 1, 6, 2, 2, 1, 4, 2, 3,      # nodes 20-29
    3, 5, 11, 15                        # nodes 30-33
]

KARATE_TOTAL_TRIANGLES = 45


def create_karate_graph(scale=0.08, node_radius=0.2):
    """
    Create the 34-node Zachary karate club graph with spring layout.

    Args:
        scale: Scale factor for positions
        node_radius: Radius of node circles

    Returns:
        VGroup with vertices dict and edges_group
    """
    n_nodes = 34

    # Pre-computed spring layout positions (normalized)
    positions = {
        0: np.array([-1.5, 0.5, 0]),
        1: np.array([-1.2, 1.0, 0]),
        2: np.array([-0.8, 0.3, 0]),
        3: np.array([-1.0, 0.8, 0]),
        4: np.array([-2.2, 0.8, 0]),
        5: np.array([-2.5, 0.3, 0]),
        6: np.array([-2.5, 0.6, 0]),
        7: np.array([-1.0, 1.2, 0]),
        8: np.array([-0.5, 0.0, 0]),
        9: np.array([0.2, -0.5, 0]),
        10: np.array([-2.2, 0.5, 0]),
        11: np.array([-2.0, 0.2, 0]),
        12: np.array([-1.8, 0.8, 0]),
        13: np.array([-0.8, 0.8, 0]),
        14: np.array([0.8, -1.0, 0]),
        15: np.array([1.0, -1.2, 0]),
        16: np.array([-2.8, 0.5, 0]),
        17: np.array([-1.5, 1.2, 0]),
        18: np.array([1.2, -1.0, 0]),
        19: np.array([-0.5, 1.0, 0]),
        20: np.array([1.0, -0.8, 0]),
        21: np.array([-1.2, 1.3, 0]),
        22: np.array([1.2, -0.6, 0]),
        23: np.array([1.0, 0.2, 0]),
        24: np.array([1.5, 0.8, 0]),
        25: np.array([1.8, 0.5, 0]),
        26: np.array([1.5, -0.3, 0]),
        27: np.array([0.5, 0.5, 0]),
        28: np.array([0.2, 0.2, 0]),
        29: np.array([1.2, 0.0, 0]),
        30: np.array([0.0, 0.8, 0]),
        31: np.array([0.5, 1.0, 0]),
        32: np.array([0.8, -0.2, 0]),
        33: np.array([1.0, -0.5, 0]),
    }

    # Scale positions
    for k in positions:
        positions[k] = positions[k] * scale * 10

    # Create vertices
    vertices = {}
    for i in range(n_nodes):
        label = MathTex(str(i), color=BLACK).scale(0.35)
        dot = LabeledDot(label, radius=node_radius, fill_color=WHITE, fill_opacity=1)
        dot.move_to(positions[i])
        vertices[i] = dot

    # Create edges
    edges_group = VGroup()
    for src, tgt in KARATE_EDGES:
        start = positions[src]
        end = positions[tgt]
        line = Line(start, end, color=BLUE, stroke_width=1.5)
        # Shorten to avoid overlapping vertices
        direction = end - start
        length = np.linalg.norm(direction)
        if length > 0:
            unit = direction / length
            line = Line(
                start + unit * node_radius,
                end - unit * node_radius,
                color=BLUE,
                stroke_width=1.5
            )
        edges_group.add(line)

    graph = VGroup(edges_group, *vertices.values())
    graph.vertices = vertices
    graph.edges_group = edges_group
    graph.positions = positions

    return graph
