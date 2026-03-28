import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
import math
from scene_utils import setup_scene, animate_vertex_fill

# Import the matrix data from Scene1
from Scene1 import SCENE1_MATRIX_DATA

# Matrix states at each iteration (None = absent)
D_INIT = [[0 if i == j else None for j in range(6)] for i in range(6)]

D_ITER1 = [
    [0, 1, None, 2, None, None],
    [None, 0, 11, None, None, None],
    [None, None, 0, None, None, None],
    [None, None, None, 0, 4, 1],
    [None, None, 5, None, 0, None],
    [None, None, None, None, 2, 0],
]

D_ITER2 = [
    [0, 1, 12, 2, 6, 3],
    [None, 0, 11, None, None, None],
    [None, None, 0, None, None, None],
    [None, None, 9, 0, 3, 1],  # D[3,4] updated 4->3
    [None, None, 5, None, 0, None],
    [None, None, 7, None, 2, 0],
]

D_ITER3 = [
    [0, 1, 11, 2, 5, 3],  # D[0,4] 6->5, D[0,2] 12->11
    [None, 0, 11, None, None, None],
    [None, None, 0, None, None, None],
    [None, None, 8, 0, 3, 1],  # D[3,2] 9->8
    [None, None, 5, None, 0, None],
    [None, None, 7, None, 2, 0],
]

D_ITER4 = [
    [0, 1, 10, 2, 5, 3],  # D[0,2] 11->10
    [None, 0, 11, None, None, None],
    [None, None, 0, None, None, None],
    [None, None, 8, 0, 3, 1],
    [None, None, 5, None, 0, None],
    [None, None, 7, None, 2, 0],
]


class Scene2(VoiceoverScene, Scene):
    """All-Pairs Shortest Path (APSP) Algorithm Visualization."""

    # Iteration colors: cool to warm spectrum
    ITER_COLORS = [BLUE, TEAL, YELLOW, ORANGE]

    def construct(self):
        setup_scene(self)

        # Create components
        code = self.create_code_display()
        graph, weight_labels = self.create_graph_display()
        matrix_group = self.create_apsp_matrix(D_INIT)

        # Position layout: code left, graph center-right, matrix center-right
        code.scale(0.55).to_edge(LEFT, buff=0.3).shift(UP * 0.3)
        graph_group = VGroup(graph, weight_labels)
        graph_group.scale(0.5).move_to(ORIGIN).shift(UP * 0.3 + RIGHT * 1.0)
        matrix_group.scale(0.4).to_edge(RIGHT, buff=0.3).shift(UP * 0.3 + LEFT * 1.0)

        # Store references
        self.code = code
        self.graph = graph
        self.weight_labels = weight_labels
        self.matrix_group = matrix_group
        self.graph_group = graph_group

        # Phase A: Introduction
        with self.voiceover(
            """Single-source shortest path finds distances from one starting node.
            All-pairs shortest path computes a complete distance matrix where entry
            i,j contains the shortest path from node i to node j. The algorithm
            uses repeated matrix multiplication with the MIN_PLUS semiring."""
        ):
            self.play(FadeIn(code))
            self.play(Create(graph), FadeIn(weight_labels))
            self.play(FadeIn(matrix_group))
            self.wait(0.5)

        # Phase B: Initialize - show diagonal zeros
        with self.voiceover(
            """We initialize the distance matrix D with zeros on the diagonal
            and the adjacency matrix values for direct edges."""
        ):
            # Highlight diagonal cells
            highlights = self.get_diagonal_highlights()
            self.play(*[Create(h) for h in highlights])
            self.wait(0.5)
            self.play(*[FadeOut(h) for h in highlights])
            self.wait(0.5)

        # Phase C: Iteration 1 - Direct edges
        iter_label = Text("Iteration 1", font_size=24, color=self.ITER_COLORS[0])
        iter_label.to_edge(DOWN, buff=0.5)

        with self.voiceover(
            """The first matrix multiplication D times D discovers all one-hop
            paths, which are the direct edges in our graph."""
        ):
            self.play(FadeIn(iter_label))

            # Update matrix to show direct edges
            new_matrix = self.create_apsp_matrix(D_ITER1)
            new_matrix.scale(0.4).move_to(self.matrix_group)
            self.play(Transform(self.matrix_group, new_matrix))

            # Highlight edges that were added
            edge_pairs = [(0, 1), (0, 3), (1, 2), (3, 4), (3, 5), (4, 2), (5, 4)]
            for src, dst in edge_pairs:
                edge = self.get_edge_mobject(src, dst)
                if edge:
                    self.play(
                        edge.animate.set_color(self.ITER_COLORS[0]).set_stroke(width=4),
                        run_time=0.3
                    )
            self.wait(0.5)

        # Phase D: Iteration 2 - Two-hop paths with MIN update
        with self.voiceover(
            """The second matrix multiplication finds all two-hop paths from every
            source to every destination. The MIN accumulator keeps only the shortest
            distances. Here the path from node three through five to four gives
            distance three, replacing the direct edge of four."""
        ):
            # Update iteration label
            new_iter_label = Text("Iteration 2", font_size=24, color=self.ITER_COLORS[1])
            new_iter_label.to_edge(DOWN, buff=0.5)
            self.play(Transform(iter_label, new_iter_label))

            # Highlight edges that were added
            edge_pairs = [(0, 1), (0, 3), (1, 2), (3, 4), (3, 5), (4, 2), (5, 4)]
            for src, dst in edge_pairs:
                edge = self.get_edge_mobject(src, dst)
                if edge:
                    self.play(
                        edge.animate.set_color(self.ITER_COLORS[1]).set_stroke(width=4),
                        run_time=0.3
                    )
            # Show the MIN update calculation for D[3,4]: 4 -> 3
            min_calc = MathTex(r"1+2=3 < 4", font_size=28, color=self.ITER_COLORS[1])
            min_calc.next_to(self.matrix_group, DOWN, buff=0.3)
            check = MathTex(r"\checkmark", font_size=36, color=self.ITER_COLORS[1])
            check.next_to(min_calc, RIGHT, buff=0.1)

            # Flash the cell that's being updated
            cell_highlight = self.create_cell_highlight(3, 4, self.ITER_COLORS[1])
            self.play(Create(cell_highlight), FadeIn(min_calc))
            self.play(FadeIn(check))

            # Update matrix
            new_matrix = self.create_apsp_matrix(D_ITER2)
            new_matrix.scale(0.4).move_to(self.matrix_group)
            self.play(Transform(self.matrix_group, new_matrix))
            self.play(FadeOut(cell_highlight), FadeOut(min_calc), FadeOut(check))
            self.wait(0.5)

        # Phase E: Iteration 3 - Three-hop paths with multiple MIN updates
        with self.voiceover(
            """Matrix multiplication continues to find three-hop paths. Each iteration
            potentially discovers shorter routes. The path from zero to four through
            three and five now costs five instead of six."""
        ):
            # Update iteration label
            new_iter_label = Text("Iteration 3", font_size=24, color=self.ITER_COLORS[2])
            new_iter_label.to_edge(DOWN, buff=0.5)
            self.play(Transform(iter_label, new_iter_label))

            # Highlight edges that were added
            edge_pairs = [(0, 1), (0, 3), (1, 2), (3, 4), (3, 5), (4, 2), (5, 4)]
            for src, dst in edge_pairs:
                edge = self.get_edge_mobject(src, dst)
                if edge:
                    self.play(
                        edge.animate.set_color(self.ITER_COLORS[2]).set_stroke(width=4),
                        run_time=0.3
                    )

            # Show MIN updates
            updates = [
                (0, 4, "3+2=5 < 6"),
                (0, 2, "6+5=11 < 12"),
                (3, 2, "3+5=8 < 9"),
            ]

            for row, col, formula in updates:
                min_calc = MathTex(formula, font_size=28, color=self.ITER_COLORS[2])
                min_calc.next_to(self.matrix_group, DOWN, buff=0.3)
                check = MathTex(r"\checkmark", font_size=36, color=self.ITER_COLORS[2])
                check.next_to(min_calc, RIGHT, buff=0.1)

                cell_highlight = self.create_cell_highlight(row, col, self.ITER_COLORS[2])
                self.play(Create(cell_highlight), FadeIn(min_calc), run_time=0.5)
                self.play(FadeIn(check), run_time=0.3)
                self.play(FadeOut(cell_highlight), FadeOut(min_calc), FadeOut(check), run_time=0.3)

            # Update matrix
            new_matrix = self.create_apsp_matrix(D_ITER3)
            new_matrix.scale(0.4).move_to(self.matrix_group)
            self.play(Transform(self.matrix_group, new_matrix))
            self.wait(0.5)

        # Phase F: Iteration 4 - One more MIN update
        with self.voiceover(
            """The fourth iteration finds one more improvement. Matrix multiplication
            propagates the improved distance from zero to four, giving us a shorter
            path to node two."""
        ):
            # Update iteration label
            new_iter_label = Text("Iteration 4", font_size=24, color=self.ITER_COLORS[3])
            new_iter_label.to_edge(DOWN, buff=0.5)
            self.play(Transform(iter_label, new_iter_label))

            # Highlight edges that were added
            edge_pairs = [(0, 1), (0, 3), (1, 2), (3, 4), (3, 5), (4, 2), (5, 4)]
            for src, dst in edge_pairs:
                edge = self.get_edge_mobject(src, dst)
                if edge:
                    self.play(
                        edge.animate.set_color(self.ITER_COLORS[3]).set_stroke(width=4),
                        run_time=0.3
                    )
            # Show MIN update for D[0,2]: 11 -> 10
            min_calc = MathTex(r"5+5=10 < 11", font_size=28, color=self.ITER_COLORS[3])
            min_calc.next_to(self.matrix_group, DOWN, buff=0.3)
            check = MathTex(r"\checkmark", font_size=36, color=self.ITER_COLORS[3])
            check.next_to(min_calc, RIGHT, buff=0.1)

            cell_highlight = self.create_cell_highlight(0, 2, self.ITER_COLORS[3])
            self.play(Create(cell_highlight), FadeIn(min_calc))
            self.play(FadeIn(check))

            # Update matrix
            new_matrix = self.create_apsp_matrix(D_ITER4)
            new_matrix.scale(0.4).move_to(self.matrix_group)
            self.play(Transform(self.matrix_group, new_matrix))
            self.play(FadeOut(cell_highlight), FadeOut(min_calc), FadeOut(check))
            self.wait(0.5)

        # Phase G: Convergence
        with self.voiceover(
            """After iteration five, matrix multiplication produces no changes.
            The algorithm has converged to the final shortest path distances."""
        ):
            # Update iteration label
            new_iter_label = Text("Iteration 5 - Converged", font_size=24, color=GREEN)
            new_iter_label.to_edge(DOWN, buff=0.5)
            self.play(Transform(iter_label, new_iter_label))

            # Pulse the matrix
            self.play(self.matrix_group.animate.scale(1.1))
            self.play(self.matrix_group.animate.scale(1/1.1))
            self.wait(0.5)

        # Phase H: Final visualization
        with self.voiceover(
            """The distance matrix now contains all-pairs shortest paths. This is
            equivalent to taking the transitive closure of the weighted graph
            using the MIN_PLUS semiring."""
        ):
            # Create final complete graph showing all shortest paths
            complete_graph = self.create_complete_graph(D_ITER4)
            complete_graph.scale(0.5).move_to(self.graph_group)

            self.play(
                FadeOut(graph),
                FadeOut(weight_labels),
                FadeIn(complete_graph),
            )
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(code),
            FadeOut(complete_graph),
            FadeOut(self.matrix_group),
            FadeOut(iter_label),
        )
        self.wait(0.5)

    def create_code_display(self):
        """Create the Python code display for APSP algorithm."""
        code_string = """def apsp(A):
    n = A.nrows
    D = A.dup()
    D.setdiag(0)

    for _ in range(int(log2(n)) + 1):
        D(accum=min) << D.mxm(D, min_plus)

    return D"""

        code = Code(
            code_string=code_string,
            language="python",
            background="window",
            formatter_style="dracula",
        )
        return code

    def create_graph_display(self):
        """Create the graph with edge weight labels."""
        matrix_data = SCENE1_MATRIX_DATA
        num_rows = len(matrix_data)

        # Triangle layout for 6 nodes
        sqrt3 = math.sqrt(3)
        positions = {
            0: np.array([-3, -sqrt3, 0]),      # Base left
            1: np.array([0, -sqrt3, 0]),       # Base center
            2: np.array([3, -sqrt3, 0]),       # Base right
            3: np.array([-1.5, 0, 0]),         # Middle left
            4: np.array([1.5, 0, 0]),          # Middle right
            5: np.array([0, sqrt3, 0])         # Top point
        }

        # Create vertices as labeled dots
        vertices = {}
        for i in range(num_rows):
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.25, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        # Find edges from matrix
        edges_data = []
        for i in range(num_rows):
            for j in range(num_rows):
                if matrix_data[i][j] != 0:
                    edges_data.append((i, j, matrix_data[i][j]))

        # Create directed arrows for edges
        edges = VGroup()
        edge_dict = {}
        weight_labels = VGroup()

        for i, j, weight in edges_data:
            start = positions[i]
            end = positions[j]

            arrow = Arrow(
                start, end,
                color=BLUE,
                buff=0.3,
                stroke_width=3,
                tip_length=0.15,
                max_tip_length_to_length_ratio=0.2
            )
            edges.add(arrow)
            edge_dict[(i, j)] = arrow

            # Add weight label at midpoint with perpendicular offset
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.25
            label = Text(str(weight), font_size=18, color=YELLOW).move_to(mid + perp)
            weight_labels.add(label)

        # Combine into graph group
        graph = VGroup(edges, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        graph.edge_dict = edge_dict
        graph.positions = positions

        return graph, weight_labels

    def create_apsp_matrix(self, data):
        """Create 6x6 sparse matrix with row/col labels for APSP."""
        # Convert None to empty string for display, keep numbers
        display_data = []
        for row in data:
            display_row = []
            for val in row:
                if val is None:
                    display_row.append("")
                else:
                    display_row.append(str(val))
            display_data.append(display_row)

        matrix = Matrix(display_data, v_buff=0.6, h_buff=0.6)

        # Hide empty entries by setting opacity to 0
        num_cols = len(data[0])
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val is None:
                    matrix.get_entries()[i * num_cols + j].set_opacity(0)

        # Add row labels (0-5) on left
        row_labels = VGroup(*[
            Text(str(i), font_size=16, color=BLUE).next_to(
                matrix.get_rows()[i], LEFT, buff=0.3)
            for i in range(6)
        ])

        # Add col labels (0-5) on top
        col_labels = VGroup(*[
            Text(str(j), font_size=16, color=BLUE).next_to(
                matrix.get_columns()[j], UP, buff=0.2)
            for j in range(6)
        ])

        # Title
        title = Text("D", font_size=24, color=WHITE)
        title.next_to(matrix, UP, buff=0.5)

        group = VGroup(matrix, row_labels, col_labels, title)
        group.matrix = matrix
        return group

    def get_diagonal_highlights(self):
        """Get highlight rectangles for diagonal cells."""
        matrix = self.matrix_group.matrix
        highlights = []
        for i in range(6):
            entry = matrix.get_entries()[i * 6 + i]
            rect = SurroundingRectangle(entry, color=YELLOW, buff=0.1)
            highlights.append(rect)
        return highlights

    def create_cell_highlight(self, row, col, color):
        """Create a highlight rectangle for a specific matrix cell."""
        matrix = self.matrix_group.matrix
        entry = matrix.get_entries()[row * 6 + col]
        return SurroundingRectangle(entry, color=color, buff=0.1)

    def get_edge_mobject(self, i, j):
        """Get the edge arrow mobject for edge (i, j)."""
        return self.graph.edge_dict.get((i, j))

    def create_complete_graph(self, distances):
        """Create final dense graph showing all shortest paths."""
        # Circular layout for 6 nodes - better visibility for dense graphs
        radius = 2.5
        positions = {
            i: np.array([
                radius * math.cos(2 * math.pi * i / 6 - math.pi/2),
                radius * math.sin(2 * math.pi * i / 6 - math.pi/2),
                0
            ])
            for i in range(6)
        }

        # Create vertices
        vertices = {}
        for i in range(6):
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.25, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        # Original edges from SCENE1_MATRIX_DATA
        original_edges = set()
        for i in range(6):
            for j in range(6):
                if SCENE1_MATRIX_DATA[i][j] != 0:
                    original_edges.add((i, j))

        # Create edges for all non-diagonal, non-None entries
        edges = VGroup()
        weight_labels = VGroup()

        for i in range(6):
            for j in range(6):
                if i != j and distances[i][j] is not None:
                    start = positions[i]
                    end = positions[j]

                    # Use blue for original edges, green for discovered paths
                    if (i, j) in original_edges:
                        color = BLUE
                        stroke_width = 3
                    else:
                        color = GREEN
                        stroke_width = 2

                    arrow = Arrow(
                        start, end,
                        color=color,
                        buff=0.3,
                        stroke_width=stroke_width,
                        tip_length=0.12,
                        max_tip_length_to_length_ratio=0.2
                    )
                    edges.add(arrow)

                    # Add weight label
                    mid = (start + end) / 2
                    direction = end - start
                    perp = np.array([-direction[1], direction[0], 0])
                    if np.linalg.norm(perp) > 0:
                        perp = perp / np.linalg.norm(perp) * 0.2
                    label = Text(str(distances[i][j]), font_size=14, color=YELLOW)
                    label.move_to(mid + perp)
                    weight_labels.add(label)

        graph = VGroup(edges, *vertices.values(), weight_labels)
        graph.vertices = vertices
        return graph
