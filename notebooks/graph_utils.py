"""Graph drawing utilities for Jupyter notebooks.

Provides consistent styling for graph visualizations across all notebooks.
"""

import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, pos=None, ax=None, title=None,
               node_color='lightblue', directed=True,
               edge_labels=None, node_size=500, font_size=16,
               cmap=None, show=True):
    """Draw a graph with consistent styling.

    Args:
        G: NetworkX graph
        pos: Node positions dict. If None, uses spring_layout with seed=42
        ax: Matplotlib axes. If None, uses current figure
        title: Optional title string
        node_color: Color or list of colors for nodes
        directed: Whether to draw arrows (for DiGraph)
        edge_labels: Dict of (u,v) -> label for edge labels
        node_size: Size of nodes
        font_size: Font size for labels
        cmap: Colormap for node colors (when node_color is numeric)
        show: Whether to call plt.show() (only when ax is None)

    Returns:
        pos: The node positions used (useful for subsequent draws)
    """
    if pos is None:
        pos = nx.spring_layout(G, seed=42)

    draw_kwargs = dict(
        with_labels=True,
        node_color=node_color,
        node_size=node_size,
        font_size=font_size,
        arrows=directed,
    )
    if cmap is not None:
        draw_kwargs['cmap'] = cmap

    nx.draw(G, pos, ax=ax, **draw_kwargs)

    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    if title:
        if ax:
            ax.set_title(title)
        else:
            plt.title(title)

    if ax is None and show:
        plt.show()

    return pos


def draw_weighted_graph(G, pos=None, ax=None, title=None,
                        node_color='lightblue', node_size=500,
                        font_size=16, weight_attr='weight', show=True):
    """Draw graph with edge weight labels.

    Args:
        G: NetworkX graph with edge weights
        pos: Node positions dict. If None, uses spring_layout with seed=42
        ax: Matplotlib axes
        title: Optional title string
        node_color: Color for nodes
        node_size: Size of nodes
        font_size: Font size for labels
        weight_attr: Edge attribute name for weights
        show: Whether to call plt.show()

    Returns:
        pos: The node positions used
    """
    edge_labels = nx.get_edge_attributes(G, weight_attr)
    directed = isinstance(G, nx.DiGraph)
    return draw_graph(G, pos=pos, ax=ax, title=title,
                      node_color=node_color, directed=directed,
                      edge_labels=edge_labels, node_size=node_size,
                      font_size=font_size, show=show)


def draw_comparison(graphs, titles, pos=None, figsize=(12, 5),
                    colors=None, directed=True, show=True):
    """Draw multiple graphs side-by-side for comparison.

    Args:
        graphs: List of NetworkX graphs
        titles: List of title strings
        pos: Shared node positions. If None, computed from first graph
        figsize: Figure size tuple
        colors: List of node colors (one per graph). Defaults to 'lightblue'
        directed: Whether to draw arrows
        show: Whether to call plt.show()

    Returns:
        pos: The node positions used
    """
    n = len(graphs)
    if colors is None:
        colors = ['lightblue'] * n

    fig, axes = plt.subplots(1, n, figsize=figsize)
    if n == 1:
        axes = [axes]

    # Compute positions from first graph if not provided
    if pos is None:
        pos = nx.spring_layout(graphs[0], seed=42)

    for i, (G, title, color) in enumerate(zip(graphs, titles, colors)):
        draw_graph(G, pos=pos, ax=axes[i], title=title,
                   node_color=color, directed=directed, show=False)

    if show:
        plt.show()

    return pos


def matrix_to_graph(M, directed=True, weighted=False):
    """Convert GraphBLAS matrix to NetworkX graph.

    Args:
        M: GraphBLAS Matrix
        directed: If True, creates DiGraph; otherwise Graph
        weighted: If True, includes edge values as 'weight' attribute

    Returns:
        NetworkX Graph or DiGraph
    """
    rows, cols, vals = M.to_coo()
    G = nx.DiGraph() if directed else nx.Graph()

    if weighted:
        for r, c, v in zip(rows, cols, vals):
            G.add_edge(int(r), int(c), weight=v)
    else:
        for r, c in zip(rows, cols):
            G.add_edge(int(r), int(c))

    return G


def draw_vector(v, ax=None, title=None, show=True, box_size=1.0,
                fill_color='lightblue', empty_color='white',
                font_size=14, show_indices=True):
    """Draw a sparse vector as a row of boxes.

    Args:
        v: GraphBLAS Vector
        ax: Matplotlib axes. If None, creates new figure
        title: Optional title string
        show: Whether to call plt.show()
        box_size: Size of each box
        fill_color: Background color for boxes with values
        empty_color: Background color for empty boxes
        font_size: Font size for values
        show_indices: Whether to show index labels below boxes

    Returns:
        ax: The matplotlib axes used
    """
    import matplotlib.patches as patches

    size = v.size
    indices, values = v.to_coo()

    # Convert to dict for easy lookup
    val_dict = {int(i): val for i, val in zip(indices, values)}

    if ax is None:
        fig, ax = plt.subplots(figsize=(max(size * 0.8, 4), 1.5))

    # Draw boxes
    for i in range(size):
        x = i * box_size
        y = 0

        if i in val_dict:
            color = fill_color
            val = val_dict[i]
            # Format value nicely
            if isinstance(val, bool):
                text = 'T' if val else 'F'
            elif isinstance(val, float):
                text = f'{val:.3g}'
            else:
                text = str(int(val))
        else:
            color = empty_color
            text = ''

        rect = patches.FancyBboxPatch(
            (x, y), box_size, box_size,
            boxstyle='round,pad=0.02,rounding_size=0.1',
            facecolor=color, edgecolor='black', linewidth=1.5
        )
        ax.add_patch(rect)

        # Add value text
        if text:
            ax.text(x + box_size/2, y + box_size/2, text,
                    ha='center', va='center', fontsize=font_size,
                    fontweight='bold')

        # Add index label
        if show_indices:
            ax.text(x + box_size/2, y - 0.2, str(i),
                    ha='center', va='top', fontsize=font_size-2,
                    color='gray')

    ax.set_xlim(-0.2, size * box_size + 0.2)
    ax.set_ylim(-0.5 if show_indices else -0.1, box_size + 0.3)
    ax.set_aspect('equal')
    ax.axis('off')

    if title:
        ax.set_title(title, fontsize=font_size)

    if show:
        plt.tight_layout()
        plt.show()

    return ax


def draw_matrix(M, ax=None, title=None, show=True, box_size=1.0,
                fill_color='lightblue', empty_color='white',
                font_size=12, show_indices=True):
    """Draw a sparse matrix as a grid of boxes.

    Args:
        M: GraphBLAS Matrix
        ax: Matplotlib axes. If None, creates new figure
        title: Optional title string
        show: Whether to call plt.show()
        box_size: Size of each box
        fill_color: Background color for boxes with values
        empty_color: Background color for empty boxes
        font_size: Font size for values
        show_indices: Whether to show row/column index labels

    Returns:
        ax: The matplotlib axes used
    """
    import matplotlib.patches as patches

    nrows, ncols = M.nrows, M.ncols
    rows, cols, values = M.to_coo()

    # Convert to dict for easy lookup
    val_dict = {(int(r), int(c)): val for r, c, val in zip(rows, cols, values)}

    if ax is None:
        # Size figure to fit matrix plus labels
        fig_width = max(ncols * 0.7 + 1, 4)
        fig_height = max(nrows * 0.7 + 1, 3)
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Draw boxes (row 0 at top)
    for r in range(nrows):
        for c in range(ncols):
            x = c * box_size
            y = (nrows - 1 - r) * box_size  # Flip so row 0 is at top

            if (r, c) in val_dict:
                color = fill_color
                val = val_dict[(r, c)]
                # Format value nicely
                if isinstance(val, bool):
                    text = 'T' if val else 'F'
                elif isinstance(val, float):
                    text = f'{val:.3g}'
                else:
                    text = str(int(val))
            else:
                color = empty_color
                text = ''

            rect = patches.FancyBboxPatch(
                (x, y), box_size, box_size,
                boxstyle='round,pad=0.02,rounding_size=0.1',
                facecolor=color, edgecolor='black', linewidth=1.5
            )
            ax.add_patch(rect)

            # Add value text
            if text:
                ax.text(x + box_size/2, y + box_size/2, text,
                        ha='center', va='center', fontsize=font_size,
                        fontweight='bold')

    # Add index labels
    if show_indices:
        # Column labels (top)
        for c in range(ncols):
            ax.text(c * box_size + box_size/2, nrows * box_size + 0.15,
                    str(c), ha='center', va='bottom', fontsize=font_size-1,
                    color='gray')
        # Row labels (left)
        for r in range(nrows):
            ax.text(-0.15, (nrows - 1 - r) * box_size + box_size/2,
                    str(r), ha='right', va='center', fontsize=font_size-1,
                    color='gray')

    margin = 0.3 if show_indices else 0.1
    ax.set_xlim(-margin, ncols * box_size + margin)
    ax.set_ylim(-margin, nrows * box_size + margin + (0.3 if show_indices else 0))
    ax.set_aspect('equal')
    ax.axis('off')

    if title:
        ax.set_title(title, fontsize=font_size + 2)

    if show:
        plt.tight_layout()
        plt.show()

    return ax


def draw_matrices_side_by_side(matrices, titles, figsize=None, box_size=1.0,
                                fill_color='lightblue', empty_color='white',
                                font_size=12, show_indices=True, show=True):
    """Draw multiple sparse matrices side by side.

    Args:
        matrices: List of GraphBLAS Matrices
        titles: List of title strings for each matrix
        figsize: Optional figure size tuple. If None, computed automatically
        box_size: Size of each box
        fill_color: Background color for boxes with values
        empty_color: Background color for empty boxes
        font_size: Font size for values
        show_indices: Whether to show row/column index labels
        show: Whether to call plt.show()

    Returns:
        fig, axes: The matplotlib figure and axes used
    """
    n = len(matrices)

    if figsize is None:
        # Compute figure size based on matrix dimensions
        total_width = sum(M.ncols for M in matrices) * 0.7 + n * 1.5
        max_height = max(M.nrows for M in matrices) * 0.7 + 1.5
        figsize = (max(total_width, 6), max(max_height, 3))

    fig, axes = plt.subplots(1, n, figsize=figsize)
    if n == 1:
        axes = [axes]

    for ax, M, title in zip(axes, matrices, titles):
        draw_matrix(M, ax=ax, title=title, show=False, box_size=box_size,
                    fill_color=fill_color, empty_color=empty_color,
                    font_size=font_size, show_indices=show_indices)

    if show:
        plt.tight_layout()
        plt.show()

    return fig, axes
