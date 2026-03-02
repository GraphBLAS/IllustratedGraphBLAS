import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import math
from scene_utils import create_sparse_matrix, create_small_graph_from_matrix, setup_scene


class Scene3(VoiceoverScene, Scene):
    """Matrix-Matrix Multiply Mechanics."""

    def construct(self):
        setup_scene(self)

        title = Text("Matrix-Matrix Multiply Mechanics", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Define two sparse 4x4 matrices
        # A: adjacency-like structure (directed chain: 0→1→2→3)
        A_data = [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ]
        # B: same as A (computing A^2)
        B_data = A_data

        # Result matrix C (A @ B = A^2)
        # Non-zero entries: C[0,2]=1 (path 0→1→2), C[1,3]=1 (path 1→2→3)
        C_data = [
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        A_mat = create_sparse_matrix(A_data, scale=0.5)
        B_mat = create_sparse_matrix(B_data, scale=0.5)

        # Create small graphs below matrices
        A_graph = create_small_graph_from_matrix(A_data, scale=0.28, directed=True, edge_color=BLUE)
        B_graph = create_small_graph_from_matrix(B_data, scale=0.28, directed=True, edge_color=BLUE)

        A_label = MathTex("A").scale(0.8)
        B_label = MathTex("B").scale(0.8)

        times_sym = MathTex(r"\times").scale(0.9)
        equals_sym = MathTex("=").scale(0.9)

        C_label = MathTex("C").scale(0.8)

        # Initially show C as empty matrix
        C_initial = create_sparse_matrix([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ], scale=0.5)

        # Create empty graph for C (just vertices, no edges)
        C_graph_group = self.create_empty_graph(scale=0.28)

        # Arrange with graphs below matrices
        A_col = VGroup(A_label, A_mat, A_graph).arrange(DOWN, buff=0.15)
        B_col = VGroup(B_label, B_mat, B_graph).arrange(DOWN, buff=0.15)
        C_col = VGroup(C_label.copy(), C_initial, C_graph_group).arrange(DOWN, buff=0.15)

        # Arrange equation
        equation = VGroup(
            A_col,
            times_sym,
            B_col,
            equals_sym,
            C_col
        ).arrange(RIGHT, buff=0.4)
        equation.next_to(title, DOWN, buff=0.4)

        # Add row/column labels
        row_labels_A = VGroup(*[
            Text(str(i), font_size=14, color=BLUE).next_to(A_mat.get_rows()[i], LEFT, buff=0.2)
            for i in range(4)
        ])
        col_labels_B = VGroup(*[
            Text(str(j), font_size=14, color=GREEN).next_to(B_mat.get_columns()[j], UP, buff=0.2)
            for j in range(4)
        ])

        with self.voiceover(
            """Matrix-matrix multiply follows the same pattern as vector-matrix
            multiply, but operates row by row. For each entry in the result at
            position i,j, we combine row i of the first matrix with column j
            of the second using our semiring."""
        ):
            self.play(Write(equation))
            self.play(Write(row_labels_A), Write(col_labels_B))
            self.wait(1)

        # Store references for adding edges later
        c_graph_vertices = C_graph_group.vertices
        c_graph_edges = C_graph_group.edges

        # Compute all non-zero entries of C with animation
        # Entry 1: C[0,2] = A[0,1] × B[1,2] = 1
        with self.voiceover(
            """Let's compute the full multiplication. For C at position zero-two,
            we take row zero of A and column two of B. The only matching position
            is at index one, where A has one and B has one. One times one equals one.
            This represents the two-hop path from node zero to node two via node one."""
        ):
            row_highlight = SurroundingRectangle(A_mat.get_rows()[0], color=YELLOW, buff=0.08)
            col_highlight = SurroundingRectangle(B_mat.get_columns()[2], color=YELLOW, buff=0.08)
            self.play(Create(row_highlight), Create(col_highlight))

            computation_text = MathTex(
                r"C[0,2] = A[0,1] \times B[1,2] = 1",
                font_size=28
            ).to_edge(DOWN, buff=1.2)
            self.play(Write(computation_text))

            # Show result at C[0,2]
            entry_pos = C_initial.get_entries()[2].get_center()  # Position [0,2]
            new_entry = Text("1", font_size=18, color=YELLOW).move_to(entry_pos)
            self.play(FadeIn(new_entry, scale=1.5))

            # Add edge 0→2 to the result graph
            edge_0_2 = self.create_directed_edge(c_graph_vertices[0], c_graph_vertices[2], YELLOW)
            c_graph_edges.add(edge_0_2)
            self.play(Create(edge_0_2))
            self.wait(0.5)

            self.play(FadeOut(row_highlight), FadeOut(col_highlight), FadeOut(computation_text))

        # Entry 2: C[1,3] = A[1,2] × B[2,3] = 1
        with self.voiceover(
            """Next, C at position one-three. Row one of A has a value at column two.
            Column three of B has a value at row two. These match, so we get one times
            one equals one. This is the path from node one to node three via node two."""
        ):
            row_highlight = SurroundingRectangle(A_mat.get_rows()[1], color=YELLOW, buff=0.08)
            col_highlight = SurroundingRectangle(B_mat.get_columns()[3], color=YELLOW, buff=0.08)
            self.play(Create(row_highlight), Create(col_highlight))

            computation_text = MathTex(
                r"C[1,3] = A[1,2] \times B[2,3] = 1",
                font_size=28
            ).to_edge(DOWN, buff=1.2)
            self.play(Write(computation_text))

            # Show result at C[1,3]
            entry_pos = C_initial.get_entries()[7].get_center()  # Position [1,3]
            new_entry_2 = Text("1", font_size=18, color=YELLOW).move_to(entry_pos)
            self.play(FadeIn(new_entry_2, scale=1.5))

            # Add edge 1→3 to the result graph
            edge_1_3 = self.create_directed_edge(c_graph_vertices[1], c_graph_vertices[3], YELLOW)
            c_graph_edges.add(edge_1_3)
            self.play(Create(edge_1_3))
            self.wait(0.5)

            self.play(FadeOut(row_highlight), FadeOut(col_highlight), FadeOut(computation_text))

        # Show that other entries are zero (no matching paths)
        with self.voiceover(
            """All other entries remain empty. For example, C at zero-three would
            need a matching value in row zero of A and column three of B, but row
            zero only has a value at column one, and column three only has a value
            at row two. No overlap means no path, no computation needed."""
        ):
            # Briefly highlight row 0 and col 3 to show no match
            row_highlight = SurroundingRectangle(A_mat.get_rows()[0], color=RED, buff=0.08)
            col_highlight = SurroundingRectangle(B_mat.get_columns()[3], color=RED, buff=0.08)
            self.play(Create(row_highlight), Create(col_highlight))

            no_match_text = Text("No matching positions → empty entry", font_size=24, color=RED).to_edge(DOWN, buff=1.2)
            self.play(Write(no_match_text))
            self.wait(1.5)

            self.play(FadeOut(row_highlight), FadeOut(col_highlight), FadeOut(no_match_text))

        # Show sparsity advantage
        sparse_title = Text("Sparse Optimization", font_size=32, color=YELLOW).to_edge(DOWN, buff=1.5)

        empty_positions_text = Text(
            "Empty entries = no computation needed",
            font_size=24, color=GRAY
        ).next_to(sparse_title, DOWN, buff=0.3)

        with self.voiceover(
            """The sparse optimization is powerful. We only compute products
            where both matrices have values. Empty entries mean no work at all.
            For sparse graphs, this reduces complexity from O of n-cubed for
            dense matrices to O of the number of non-zero entries."""
        ):
            self.play(Write(sparse_title))
            self.play(Write(empty_positions_text))

            # Gray out zero positions visually
            for i in range(4):
                for j in range(4):
                    if A_data[i][j] == 0:
                        entry = A_mat.get_entries()[i * 4 + j]
                        entry.set_opacity(0.2)
                    if B_data[i][j] == 0:
                        entry = B_mat.get_entries()[i * 4 + j]
                        entry.set_opacity(0.2)
            self.wait(2)

        self.play(FadeOut(sparse_title), FadeOut(empty_positions_text))

        # Graph interpretation
        interp_title = Text("Graph Interpretation", font_size=32).to_edge(DOWN, buff=1.5)
        interp_text = VGroup(
            Text("A represents edges: 'from → to'", font_size=22),
            Text("A × A represents 2-hop paths: 'from → via → to'", font_size=22),
        ).arrange(DOWN, buff=0.2).next_to(interp_title, DOWN, buff=0.3)

        with self.voiceover(
            """In graph terms, A represents direct edges from one node to another.
            When we multiply A by itself, we get two-hop paths. The result graph
            now shows edges zero to two and one to three, the two-hop connections
            discovered through matrix multiplication."""
        ):
            self.play(Write(interp_title))
            self.play(Write(interp_text))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(equation),
            FadeOut(row_labels_A), FadeOut(col_labels_B),
            FadeOut(interp_title), FadeOut(interp_text),
            FadeOut(new_entry), FadeOut(new_entry_2)
        )
        self.wait(0.5)

    def create_empty_graph(self, scale=0.3):
        """Create a graph with just vertices (no edges) for 4 nodes."""
        num_nodes = 4

        # Create circular layout
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

        # Empty edges group (will be populated during animation)
        edges = VGroup()

        # Combine into graph group
        graph = VGroup(edges, *vertices.values())
        graph.vertices = vertices
        graph.positions = positions
        graph.edges = edges

        return graph.scale(scale)

    def create_directed_edge(self, start_vertex, end_vertex, color):
        """Create a directed arrow between two vertices."""
        start = start_vertex.get_center()
        end = end_vertex.get_center()

        arrow = Arrow(
            start, end,
            color=color,
            buff=0.06,  # Small buffer for scaled vertices
            stroke_width=2,
            tip_length=0.08,
            max_tip_length_to_length_ratio=0.3
        )
        return arrow
