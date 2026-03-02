import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import (
    create_sparse_matrix,
    setup_scene,
    animate_vertex_fill,
    CHAPTER5_EDGES,
)


class Scene1(VoiceoverScene, Scene):
    """The Two-Matrix Representation: S (source) and D (destination)."""

    def construct(self):
        setup_scene(self)

        title = Text("The Two-Matrix Representation", font_size=44).to_edge(UP)
        self.play(Write(title))

        # 3-node graph with 3 edges defined in CHAPTER5_EDGES: [(0,1), (1,2), (0,2)]
        #
        # S (source matrix): n×m = 3×3 (nodes × edges)
        # S[i,e] = 1 if node i is the SOURCE of edge e
        #
        # D (destination matrix): m×n = 3×3 (edges × nodes)
        # D[e,j] = 1 if node j is the DESTINATION of edge e

        # Node positions for graph (triangle)
        positions = {
            0: np.array([-1.5, 1, 0]),
            1: np.array([1.5, 1, 0]),
            2: np.array([0, -1, 0]),
        }

        with self.voiceover(
            """For directed graphs, we represent incidence using two separate
            matrices: S for sources, and D for destinations. Consider this
            simple graph with three nodes and three directed edges."""
        ):
            # Create graph
            graph = self.create_directed_graph(positions)
            graph.scale(0.8).to_edge(RIGHT, buff=1.5).shift(UP * 0.5)

            self.play(Create(graph))
            self.wait(1)

        with self.voiceover(
            """The S matrix has nodes as rows and edges as columns. Each entry
            S at position i, e equals one if node i is the source of edge e.
            Let us build it edge by edge."""
        ):
            # Create empty S matrix display
            S_matrix = self.create_labeled_matrix(
                rows=3, cols=3,
                row_labels=["0", "1", "2"],
                col_labels=["e0", "e1", "e2"],
                row_title="nodes",
                col_title="edges",
                row_color=BLUE,
                col_color=GREEN
            )
            S_label = MathTex("S", font_size=40, color=YELLOW).next_to(S_matrix, UP, buff=0.3)
            S_dim = Text("n × m", font_size=16, color=GRAY).next_to(S_label, RIGHT, buff=0.3)

            S_group = VGroup(S_label, S_dim, S_matrix)
            S_group.to_edge(LEFT, buff=0.6).shift(UP * 1.2)

            self.play(Write(S_group))
            self.wait(0.5)

        # Animate filling S matrix - derive from shared edge definition
        edges = [(src, dst, f"e{i}") for i, (src, dst) in enumerate(CHAPTER5_EDGES)]

        with self.voiceover(
            """Edge e0 goes from node 0 to node 1. So in the S matrix, we put
            a one at row 0, column e0, because node 0 is the source."""
        ):
            # Highlight edge e0 and source node 0
            e0_highlight = graph.edges[0].copy().set_color(YELLOW).set_stroke(width=5)
            self.play(Create(e0_highlight))
            self.play(animate_vertex_fill(graph.vertices[0], RED))

            # Fill S[0, 0] = 1
            self.fill_entry(S_matrix.matrix, 0, 0, "1", RED)
            self.wait(0.5)

            self.play(
                FadeOut(e0_highlight),
                animate_vertex_fill(graph.vertices[0], WHITE),
            )

        with self.voiceover(
            """Edge e1 goes from node 1 to node 2. Node 1 is the source, so
            S at row 1, column e1 is one."""
        ):
            e1_highlight = graph.edges[1].copy().set_color(YELLOW).set_stroke(width=5)
            self.play(Create(e1_highlight))
            self.play(animate_vertex_fill(graph.vertices[1], RED))

            self.fill_entry(S_matrix.matrix, 1, 1, "1", RED)
            self.wait(0.5)

            self.play(
                FadeOut(e1_highlight),
                animate_vertex_fill(graph.vertices[1], WHITE),
            )

        with self.voiceover(
            """Edge e2 goes from node 0 to node 2. Node 0 is the source again,
            so S at row 0, column e2 is one. The S matrix is now complete."""
        ):
            e2_highlight = graph.edges[2].copy().set_color(YELLOW).set_stroke(width=5)
            self.play(Create(e2_highlight))
            self.play(animate_vertex_fill(graph.vertices[0], RED))

            self.fill_entry(S_matrix.matrix, 0, 2, "1", RED)
            self.wait(0.5)

            self.play(
                FadeOut(e2_highlight),
                animate_vertex_fill(graph.vertices[0], WHITE),
            )

        with self.voiceover(
            """Now we build the D matrix. This matrix has edges as rows and nodes
            as columns. D at position e, j equals one if node j is the
            destination of edge e. Notice the dimensions are flipped: D is
            m by n, while S is n by m."""
        ):
            # Create D matrix display
            D_matrix = self.create_labeled_matrix(
                rows=3, cols=3,
                row_labels=["e0", "e1", "e2"],
                col_labels=["0", "1", "2"],
                row_title="edges",
                col_title="nodes",
                row_color=GREEN,
                col_color=BLUE
            )
            D_label = MathTex("D", font_size=40, color=YELLOW).next_to(D_matrix, UP, buff=0.3)
            D_dim = Text("m × n", font_size=16, color=GRAY).next_to(D_label, RIGHT, buff=0.3)

            D_group = VGroup(D_label, D_dim, D_matrix)
            D_group.to_edge(LEFT, buff=0.6).shift(DOWN * 1.5)

            self.play(Write(D_group))
            self.wait(0.5)

        with self.voiceover(
            """Edge e0 goes to node 1. So D at row e0, column 1 is one.
            Edge e1 goes to node 2. D at row e1, column 2 is one.
            Edge e2 also goes to node 2. D at row e2, column 2 is one."""
        ):
            # Fill D matrix entries for destinations
            # e0 → node 1
            e0_highlight = graph.edges[0].copy().set_color(YELLOW).set_stroke(width=5)
            self.play(Create(e0_highlight))
            self.play(animate_vertex_fill(graph.vertices[1], GREEN))
            self.fill_entry(D_matrix.matrix, 0, 1, "1", GREEN)
            self.play(FadeOut(e0_highlight), animate_vertex_fill(graph.vertices[1], WHITE))

            # e1 → node 2
            e1_highlight = graph.edges[1].copy().set_color(YELLOW).set_stroke(width=5)
            self.play(Create(e1_highlight))
            self.play(animate_vertex_fill(graph.vertices[2], GREEN))
            self.fill_entry(D_matrix.matrix, 1, 2, "1", GREEN)
            self.play(FadeOut(e1_highlight), animate_vertex_fill(graph.vertices[2], WHITE))

            # e2 → node 2
            e2_highlight = graph.edges[2].copy().set_color(YELLOW).set_stroke(width=5)
            self.play(Create(e2_highlight))
            self.play(animate_vertex_fill(graph.vertices[2], GREEN))
            self.fill_entry(D_matrix.matrix, 2, 2, "1", GREEN)
            self.play(FadeOut(e2_highlight), animate_vertex_fill(graph.vertices[2], WHITE))

            self.wait(1)

        with self.voiceover(
            """Notice that S and D are not transposes of each other. They encode
            different information: S tells us which node starts each edge,
            D tells us which node ends each edge. Together they fully describe
            the directed graph."""
        ):
            # Highlight that they're different
            not_transpose = Text("S and D are NOT transposes", font_size=24, color=YELLOW)
            not_transpose.to_edge(DOWN, buff=0.5)

            self.play(Write(not_transpose))
            self.wait(2)

        with self.voiceover(
            """The key insight is that these two matrices, when multiplied
            together as S times D, produce the adjacency matrix. We will
            see this in the next scene."""
        ):
            insight = VGroup(
                MathTex(r"S \times D = A", font_size=36, color=GREEN),
                Text("Adjacency matrix from incidence", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            insight.next_to(not_transpose, UP, buff=0.5)

            self.play(FadeOut(not_transpose), Write(insight))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(S_group),
            FadeOut(D_group), FadeOut(insight)
        )
        self.wait(0.5)

    def create_directed_graph(self, positions):
        """Create a directed graph with arrows."""
        vertices = {}
        for i, pos in positions.items():
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.3, fill_color=WHITE, fill_opacity=1)
            dot.move_to(pos)
            vertices[i] = dot

        edges = VGroup()
        edge_labels = VGroup()

        for idx, (src, dst) in enumerate(CHAPTER5_EDGES):
            arrow = Arrow(
                positions[src], positions[dst],
                color=BLUE, buff=0.35, stroke_width=3,
                tip_length=0.2, max_tip_length_to_length_ratio=0.2
            )
            edges.add(arrow)

            # Edge label
            mid = (positions[src] + positions[dst]) / 2
            direction = positions[dst] - positions[src]
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.3
            label = Text(f"e{idx}", font_size=16, color=BLUE).move_to(mid + perp)
            edge_labels.add(label)

        graph = VGroup(edges, edge_labels, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        return graph

    def create_labeled_matrix(self, rows, cols, row_labels, col_labels,
                              row_title, col_title, row_color, col_color):
        """Create an empty matrix with row/column labels."""
        # Create matrix with empty entries
        entries = [["" for _ in range(cols)] for _ in range(rows)]
        matrix = Matrix(entries, v_buff=0.7, h_buff=0.7).scale(0.55)

        # Row labels
        row_label_group = VGroup(*[
            Text(lbl, font_size=14, color=row_color).next_to(matrix.get_rows()[i], LEFT, buff=0.3)
            for i, lbl in enumerate(row_labels)
        ])

        # Column labels
        col_label_group = VGroup(*[
            Text(lbl, font_size=14, color=col_color).next_to(matrix.get_columns()[j], UP, buff=0.3)
            for j, lbl in enumerate(col_labels)
        ])

        # Title labels
        row_title_text = Text(row_title, font_size=12, color=row_color).rotate(PI/2)
        row_title_text.next_to(row_label_group, LEFT, buff=0.2)
        col_title_text = Text(col_title, font_size=12, color=col_color)
        col_title_text.next_to(col_label_group, UP, buff=0.1)

        group = VGroup(matrix, row_label_group, col_label_group, row_title_text, col_title_text)
        group.matrix = matrix
        return group

    def fill_entry(self, matrix, row, col, value, color, run_time=0.3):
        """Fill a matrix entry with a value."""
        num_cols = 3  # We know we have 3 columns
        entry = matrix.get_entries()[row * num_cols + col]
        new_text = Text(value, font_size=18, color=color)
        new_text.move_to(entry.get_center())
        self.play(Transform(entry, new_text), run_time=run_time)
