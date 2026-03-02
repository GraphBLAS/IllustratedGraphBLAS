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

    if edge_labels:
        return graph, weight_labels
    return graph
