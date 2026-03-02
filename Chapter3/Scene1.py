import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    CHAPTER3_MATRIX_DATA,
    create_sparse_matrix,
    create_undirected_graph,
    animate_vertex_fill,
    setup_scene,
)


class Scene1(VoiceoverScene, Scene):
    """Vector-Matrix Multiply Deep Dive."""

    def construct(self):
        setup_scene(self)

        title = Text("Vector-Matrix Multiply", font_size=48).to_edge(UP)
        self.play(Write(title))

        matrix_data = CHAPTER3_MATRIX_DATA

        with self.voiceover(
            """Before we dive into masking, let's understand vector-matrix multiply
            in GraphBLAS. This operation is the core of graph traversal. When we
            multiply a vector by an adjacency matrix, we're asking: which nodes
            can I reach from my current set of nodes?"""
        ):
            syntax = Code(
                code_string="w << v.vxm(A, semiring)",
                language="python",
                background="window"
            ).scale(0.7).next_to(title, DOWN, buff=0.5)
            self.play(Write(syntax))
            self.wait(2)
            self.play(FadeOut(syntax))

        # Create input vector v (frontier at node 0) - vertical column vector
        v_data = [[1], [0], [0], [0], [0], [0]]
        v_vec = create_sparse_matrix(v_data, scale=0.45)

        # Times symbol
        times_sym = MathTex(r"\times").scale(0.8)

        # Create matrix display
        matrix = create_sparse_matrix(matrix_data, scale=0.45)

        # Equals symbol
        equals_sym = MathTex("=").scale(0.8)

        # Create output vector w (initially question marks) - vertical column vector
        w_entries = [["?"], ["?"], ["?"], ["?"], ["?"], ["?"]]
        w_vec = Matrix(w_entries, v_buff=0.8).scale(0.45)

        # Create graph
        graph = create_undirected_graph(matrix_data, layout="triangle", scale=0.55)

        # Arrange everything horizontally: v × A = w [graph]
        equation = VGroup(v_vec, times_sym, matrix, equals_sym, w_vec).arrange(RIGHT, buff=0.3)

        # Position equation and graph side by side
        content = VGroup(equation, graph).arrange(RIGHT, buff=0.8)
        content.next_to(title, DOWN, buff=1)

        # NOW position all labels after arrangement is complete
        v_label = MathTex("v").scale(0.7).next_to(v_vec, UP, buff=0.25)
        matrix_label = MathTex("A").scale(0.7).next_to(matrix, UP, buff=0.4)
        w_label = MathTex("w").scale(0.7).next_to(w_vec, UP, buff=0.25)

        # Row labels for v (on the left of v)
        v_row_labels = VGroup(*[
            Text(str(i), font_size=12, color=GREEN).next_to(v_vec.get_rows()[i], LEFT, buff=0.25)
            for i in range(6)
        ])

        # Row and column labels for matrix A
        row_labels = VGroup(*[
            Text(str(i), font_size=12, color=BLUE).next_to(matrix.get_rows()[i], LEFT, buff=0.25)
            for i in range(6)
        ])
        col_labels = VGroup(*[
            Text(str(j), font_size=12, color=BLUE).next_to(matrix.get_columns()[j], UP, buff=0.25)
            for j in range(6)
        ])

        # Row labels for w (on the right of w)
        w_row_labels = VGroup(*[
            Text(str(i), font_size=12, color=YELLOW).next_to(w_vec.get_rows()[i], RIGHT, buff=0.25)
            for i in range(6)
        ])

        with self.voiceover(
            """Let's trace through the operation. Vector v represents our frontier,
            with a single entry at position zero, our starting node. Matrix A is
            the adjacency matrix. The result w will show which nodes we can reach."""
        ):
            self.play(
                Write(v_vec), Write(v_label), Write(v_row_labels),
                Write(times_sym),
                Write(matrix), Write(matrix_label), Write(row_labels), Write(col_labels),
                Write(equals_sym),
                Write(w_vec), Write(w_label), Write(w_row_labels),
            )
            self.wait(1)

        with self.voiceover(
            """Here's the graph. Node zero connects to nodes one and three.
            These are the neighbors we should discover through multiplication."""
        ):
            self.play(Create(graph))
            self.play(animate_vertex_fill(graph.vertices[0], YELLOW))
            self.wait(1)

        # For vxm: result[j] = sum over i of v[i] * A[i,j]
        # With v[0]=1: result[j] = A[0,j] (row 0 values)
        # Row 0: [0,1,0,2,0,0] - nodes 1 and 3 are reachable

        # Highlight row 0 of A (the row corresponding to v[0]=1)
        row_0_highlight = SurroundingRectangle(matrix.get_rows()[0], color=YELLOW, buff=0.05)
        v_0_highlight = SurroundingRectangle(v_vec.get_rows()[0], color=YELLOW, buff=0.05)

        with self.voiceover(
            """Since only position zero has a value in v, we look at row zero of
            the matrix. Node zero connects to node one with weight one, and to
            node three with weight two. These values flow into the result."""
        ):
            self.play(Create(row_0_highlight), Create(v_0_highlight))
            self.wait(1)

            # Update w vector entries one by one
            new_w_entries = ["", "1", "", "2", "", ""]
            for j, val in enumerate(new_w_entries):
                old_entry = w_vec.get_entries()[j]
                if val:
                    new_entry = Text(val, font_size=16, color=GREEN).move_to(old_entry.get_center())
                    self.play(Transform(old_entry, new_entry), run_time=0.5)
                    self.play(animate_vertex_fill(graph.vertices[j], GREEN), run_time=0.3)
                else:
                    self.play(old_entry.animate.set_opacity(0), run_time=0.3)

            self.wait(1)

        self.play(FadeOut(row_0_highlight), FadeOut(v_0_highlight))

        with self.voiceover(
            """The result w shows nodes one and three are reachable from node zero.
            The values are edge weights, but for BFS we use the ANY_PAIR semiring
            which just checks reachability, returning True for any connection."""
        ):
            any_pair_note = Text(
                "ANY_PAIR: just 'True' for any connection",
                font_size=22, color=BLUE
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(any_pair_note))
            self.wait(2)

        with self.voiceover(
            """This single operation replaces explicit neighbor iteration. Instead
            of looping through edges, we express frontier expansion as one algebraic
            operation. The matrix encodes the graph, and multiplication discovers
            all neighbors at once."""
        ):
            power_text = Text(
                "One operation → All neighbors discovered",
                font_size=24, color=YELLOW
            ).next_to(any_pair_note, UP, buff=0.3)
            self.play(Write(power_text))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(any_pair_note), FadeOut(power_text),
            FadeOut(v_vec), FadeOut(v_label), FadeOut(v_row_labels),
            FadeOut(times_sym),
            FadeOut(matrix), FadeOut(matrix_label), FadeOut(row_labels), FadeOut(col_labels),
            FadeOut(equals_sym),
            FadeOut(w_vec), FadeOut(w_label), FadeOut(w_row_labels),
            FadeOut(graph)
        )
        self.wait(0.5)
