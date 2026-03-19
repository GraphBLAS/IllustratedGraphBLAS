import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    CHAPTER0_MATRIX_DATA,
    create_sparse_matrix,
    create_adjacency_digraph,
    animate_vertex_fill,
    set_vertex_fill_preserve_label,
    setup_scene,
)


class Scene5(VoiceoverScene, Scene):
    """Vector-Matrix Multiply (vxm) — Outgoing Edges with PLUS_TIMES and ANY_PAIR."""

    def construct(self):
        setup_scene(self)

        title = Text("Vector-Matrix Multiply (vxm)", font_size=42).to_edge(UP)
        self.play(Write(title))

        matrix_data = CHAPTER0_MATRIX_DATA

        # Persistent code block — stays on screen, transforms when semiring changes
        code = Code(
            code_string="w << v.vxm(A, plus_times)",
            language="python",
            background="window"
        ).scale(0.6).next_to(title, DOWN, buff=0.3)

        with self.voiceover(
            """GraphBLAS provides two multiplication directions: vxm and mxv.
            The difference determines whether you traverse outgoing or incoming
            edges. Let's start with vxm using the plus_times semiring, which
            places the vector on the left."""
        ):
            self.play(Write(code))
            self.wait(1)

        # Create input vector v (entry at node 3)
        v_data = [[0], [0], [0], [1], [0], [0]]
        v_vec = create_sparse_matrix(v_data, scale=0.45)

        times_sym = MathTex(r"\times").scale(0.8)
        matrix = create_sparse_matrix(matrix_data, scale=0.45)
        equals_sym = MathTex("=").scale(0.8)

        w_entries = [["?"], ["?"], ["?"], ["?"], ["?"], ["?"]]
        w_vec = Matrix(w_entries, v_buff=0.8).scale(0.45)

        graph, weight_labels = create_adjacency_digraph(
            matrix_data, layout="triangle", scale=0.55, edge_labels=True
        )

        # Arrange equation: v × A = w
        equation = VGroup(v_vec, times_sym, matrix, equals_sym, w_vec).arrange(RIGHT, buff=0.3)
        content = VGroup(equation, graph).arrange(RIGHT, buff=0.8)
        content.next_to(code, DOWN, buff=1)
        weight_labels.shift(graph.get_center())

        # Labels
        v_label = MathTex("v").scale(0.7).next_to(v_vec, UP, buff=0.25)
        matrix_label = MathTex("A").scale(0.7).next_to(matrix, UP, buff=0.4)
        w_label = MathTex("w").scale(0.7).next_to(w_vec, UP, buff=0.25)

        v_row_labels = VGroup(*[
            Text(str(i), font_size=12, color=GREEN).next_to(v_vec.get_rows()[i], LEFT, buff=0.25)
            for i in range(6)
        ])
        row_labels = VGroup(*[
            Text(str(i), font_size=12, color=BLUE).next_to(matrix.get_rows()[i], LEFT, buff=0.25)
            for i in range(6)
        ])
        col_labels = VGroup(*[
            Text(str(j), font_size=12, color=BLUE).next_to(matrix.get_columns()[j], UP, buff=0.25)
            for j in range(6)
        ])
        w_row_labels = VGroup(*[
            Text(str(i), font_size=12, color=YELLOW).next_to(w_vec.get_rows()[i], RIGHT, buff=0.25)
            for i in range(6)
        ])

        with self.voiceover(
            """We set up our equation with vector v containing a single entry at
            position three. This is our starting node. We multiply v by the
            adjacency matrix A to get result vector w."""
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
            """Here is our directed graph with edge weights. Node three has two
            outgoing edges: one to node four with weight two, and one to node five
            with weight nine."""
        ):
            self.play(Create(graph))
            self.play(Write(weight_labels))
            self.play(animate_vertex_fill(graph.vertices[3], YELLOW))
            self.wait(1)

        # Highlight row 3 of A and v[3]
        row_3_highlight = SurroundingRectangle(matrix.get_rows()[3], color=YELLOW, buff=0.05)
        v_3_highlight = SurroundingRectangle(v_vec.get_rows()[3], color=YELLOW, buff=0.05)

        with self.voiceover(
            """vxm reads row three of the matrix, the outgoing edges from node three.
            Since v has an entry at position three, we look across row three of A.
            The non-zero entries at columns four and five give us the result."""
        ):
            self.play(Create(row_3_highlight), Create(v_3_highlight))
            self.wait(1)

            new_w_values = ["", "", "", "", "2", "9"]
            for j, val in enumerate(new_w_values):
                old_entry = w_vec.get_entries()[j]
                if val:
                    new_entry = Text(val, font_size=16, color=GREEN).move_to(old_entry.get_center())
                    self.play(Transform(old_entry, new_entry), run_time=0.5)
                    self.play(animate_vertex_fill(graph.vertices[j], GREEN), run_time=0.3)
                else:
                    self.play(old_entry.animate.set_opacity(0), run_time=0.3)

            self.wait(1)

        self.play(FadeOut(row_3_highlight), FadeOut(v_3_highlight))

        with self.voiceover(
            """With plus_times, the result carries the actual edge weights.
            vxm discovered nodes four and five, the outgoing neighbors of node three.
            The vector on the left selects a row, and the row encodes where that
            node's edges point."""
        ):
            summary_text = Text(
                "vxm reads ROWS → discovers OUTGOING edges",
                font_size=24, color=YELLOW
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(summary_text))
            self.wait(2)

        # --- Part 2: ANY_PAIR ---

        # Fade out summary, highlights, reset vertex colors
        self.play(FadeOut(summary_text))

        # Reset discovered vertices back to WHITE (except node 3 stays YELLOW)
        self.play(
            animate_vertex_fill(graph.vertices[4], WHITE),
            animate_vertex_fill(graph.vertices[5], WHITE),
            run_time=0.5
        )

        # Transform code to any_pair
        code2 = Code(
            code_string="w << v.vxm(A, any_pair)",
            language="python",
            background="window"
        ).scale(0.6).next_to(title, DOWN, buff=0.3)

        # Reset w vector to question marks
        w_entries2 = [["?"], ["?"], ["?"], ["?"], ["?"], ["?"]]
        w_vec2 = Matrix(w_entries2, v_buff=0.8).scale(0.45).move_to(w_vec.get_center())
        w_row_labels2 = VGroup(*[
            Text(str(i), font_size=12, color=YELLOW).next_to(w_vec2.get_rows()[i], RIGHT, buff=0.25)
            for i in range(6)
        ])

        with self.voiceover(
            """Now let's switch to the any_pair semiring. any_pair is designed
            for purely structural problems. It only checks whether an edge
            exists, ignoring the weight values entirely. This avoids loading
            weight data from memory, reducing compute cost and cache pressure."""
        ):
            self.play(Transform(code, code2))
            self.play(
                Transform(w_vec, w_vec2),
                Transform(w_row_labels, w_row_labels2),
            )
            self.wait(1)

        # Highlight row 3 again
        row_3_highlight2 = SurroundingRectangle(matrix.get_rows()[3], color=YELLOW, buff=0.05)
        v_3_highlight2 = SurroundingRectangle(v_vec.get_rows()[3], color=YELLOW, buff=0.05)

        with self.voiceover(
            """We read row three again, the same outgoing edges. But this time
            the result contains boolean True values instead of weights."""
        ):
            self.play(Create(row_3_highlight2), Create(v_3_highlight2))
            self.wait(1)

            # Fill result: w[4]="T", w[5]="T"
            new_w_values2 = ["", "", "", "", "T", "T"]
            for j, val in enumerate(new_w_values2):
                old_entry = w_vec.get_entries()[j]
                if val:
                    new_entry = Text(val, font_size=16, color=GREEN).move_to(old_entry.get_center())
                    self.play(Transform(old_entry, new_entry), run_time=0.5)
                    self.play(animate_vertex_fill(graph.vertices[j], GREEN), run_time=0.3)
                else:
                    self.play(old_entry.animate.set_opacity(0), run_time=0.3)

            self.wait(1)

        self.play(FadeOut(row_3_highlight2), FadeOut(v_3_highlight2))

        with self.voiceover(
            """The result shows reachability, not distance. For BFS and other
            structural algorithms, this is all we need. The same structure is
            discovered, but without the cost of loading edge weights."""
        ):
            summary_text2 = Text(
                "ANY_PAIR: structure only, no weight loading",
                font_size=24, color=YELLOW
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(summary_text2))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(code), FadeOut(summary_text2),
            FadeOut(v_vec), FadeOut(v_label), FadeOut(v_row_labels),
            FadeOut(times_sym),
            FadeOut(matrix), FadeOut(matrix_label), FadeOut(row_labels), FadeOut(col_labels),
            FadeOut(equals_sym),
            FadeOut(w_vec), FadeOut(w_label), FadeOut(w_row_labels),
            FadeOut(graph), FadeOut(weight_labels),
        )
        self.wait(0.5)
