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


class Scene6(VoiceoverScene, Scene):
    """Matrix-Vector Multiply (mxv) — Incoming Edges with PLUS_TIMES and ANY_PAIR."""

    def construct(self):
        setup_scene(self)

        title = Text("Matrix-Vector Multiply (mxv)", font_size=42).to_edge(UP)
        self.play(Write(title))

        matrix_data = CHAPTER0_MATRIX_DATA

        # Persistent code block
        code = Code(
            code_string="w << A.mxv(v, plus_times)",
            language="python",
            background="window",
            formatter_style="dracula",
        ).scale(0.6).next_to(title, DOWN, buff=0.3)

        with self.voiceover(
            """Now let's look at mxv, where the matrix comes first and the vector
            is on the right. This reverses the traversal direction. We start
            with the plus_times semiring."""
        ):
            self.play(Write(code))
            self.wait(1)

        # Create matrix display
        matrix = create_sparse_matrix(matrix_data, scale=0.45)
        times_sym = MathTex(r"\times").scale(0.8)

        # Create input vector v (entry at node 3)
        v_data = [[0], [0], [0], [1], [0], [0]]
        v_vec = create_sparse_matrix(v_data, scale=0.45)

        equals_sym = MathTex("=").scale(0.8)

        w_entries = [["?"], ["?"], ["?"], ["?"], ["?"], ["?"]]
        w_vec = Matrix(w_entries, v_buff=0.8).scale(0.45)

        graph, weight_labels = create_adjacency_digraph(
            matrix_data, layout="triangle", scale=0.55, edge_labels=True
        )

        # Arrange equation: A × v = w (matrix first)
        equation = VGroup(matrix, times_sym, v_vec, equals_sym, w_vec).arrange(RIGHT, buff=0.3)
        content = VGroup(equation, graph).arrange(RIGHT, buff=0.8)
        content.next_to(code, DOWN, buff=1)
        weight_labels.shift(graph.get_center())

        # Labels
        matrix_label = MathTex("A").scale(0.7).next_to(matrix, UP, buff=0.4)
        v_label = MathTex("v").scale(0.7).next_to(v_vec, UP, buff=0.25)
        w_label = MathTex("w").scale(0.7).next_to(w_vec, UP, buff=0.25)

        row_labels = VGroup(*[
            Text(str(i), font_size=12, color=BLUE).next_to(matrix.get_rows()[i], LEFT, buff=0.25)
            for i in range(6)
        ])
        col_labels = VGroup(*[
            Text(str(j), font_size=12, color=BLUE).next_to(matrix.get_columns()[j], UP, buff=0.25)
            for j in range(6)
        ])
        v_row_labels = VGroup(*[
            Text(str(i), font_size=12, color=GREEN).next_to(v_vec.get_rows()[i], LEFT, buff=0.25)
            for i in range(6)
        ])
        w_row_labels = VGroup(*[
            Text(str(i), font_size=12, color=YELLOW).next_to(w_vec.get_rows()[i], RIGHT, buff=0.25)
            for i in range(6)
        ])

        with self.voiceover(
            """This time the matrix A is on the left and vector v is on the right.
            Again, v has a single entry at position three. Let's see how the result
            differs from vxm."""
        ):
            self.play(
                Write(matrix), Write(matrix_label), Write(row_labels), Write(col_labels),
                Write(times_sym),
                Write(v_vec), Write(v_label), Write(v_row_labels),
                Write(equals_sym),
                Write(w_vec), Write(w_label), Write(w_row_labels),
            )
            self.wait(1)

        with self.voiceover(
            """The same directed graph. Node three has outgoing edges to nodes four
            and five, but only one incoming edge, from node zero."""
        ):
            self.play(Create(graph))
            self.play(Write(weight_labels))
            self.play(animate_vertex_fill(graph.vertices[3], YELLOW))
            self.wait(1)

        # Highlight column 3 of A and v[3]
        col_3_highlight = SurroundingRectangle(matrix.get_columns()[3], color=ORANGE, buff=0.05)
        v_3_highlight = SurroundingRectangle(v_vec.get_rows()[3], color=ORANGE, buff=0.05)

        with self.voiceover(
            """mxv reads column three of the matrix, the incoming edges to node three.
            Looking down column three, only row zero has a value: two. That means
            only node zero has an edge pointing to node three."""
        ):
            self.play(Create(col_3_highlight), Create(v_3_highlight))
            self.wait(1)

            # Update w vector: position 0→"2", rest fade
            new_w_values = ["2", "", "", "", "", ""]
            for j, val in enumerate(new_w_values):
                old_entry = w_vec.get_entries()[j]
                if val:
                    new_entry = Text(val, font_size=16, color=ORANGE).move_to(old_entry.get_center())
                    self.play(Transform(old_entry, new_entry), run_time=0.5)
                    self.play(animate_vertex_fill(graph.vertices[j], ORANGE), run_time=0.3)
                else:
                    self.play(old_entry.animate.set_opacity(0), run_time=0.3)

            self.wait(1)

        self.play(FadeOut(col_3_highlight), FadeOut(v_3_highlight))

        with self.voiceover(
            """With plus_times, we get the edge weight from node zero to node three.
            mxv reads columns, which encode incoming connections."""
        ):
            summary_text = Text(
                "mxv reads COLUMNS → discovers INCOMING edges",
                font_size=24, color=ORANGE
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(summary_text))
            self.wait(2)

        # --- Part 2: ANY_PAIR ---

        self.play(FadeOut(summary_text))

        # Reset discovered vertex back to WHITE (except node 3 stays YELLOW)
        self.play(
            animate_vertex_fill(graph.vertices[0], WHITE),
            run_time=0.5
        )

        # Transform code to any_pair
        code2 = Code(
            code_string="w << A.mxv(v, any_pair)",
            language="python",
            background="window",
            formatter_style="dracula",
        ).scale(0.6).next_to(title, DOWN, buff=0.3)

        # Reset w vector to question marks
        w_entries2 = [["?"], ["?"], ["?"], ["?"], ["?"], ["?"]]
        w_vec2 = Matrix(w_entries2, v_buff=0.8).scale(0.45).move_to(w_vec.get_center())
        w_row_labels2 = VGroup(*[
            Text(str(i), font_size=12, color=YELLOW).next_to(w_vec2.get_rows()[i], RIGHT, buff=0.25)
            for i in range(6)
        ])

        with self.voiceover(
            """Now we switch to the any_pair semiring. Same operation, but
            ignoring weights. The hardware never touches the weight array,
            saving memory bandwidth."""
        ):
            self.play(Transform(code, code2))
            self.play(
                Transform(w_vec, w_vec2),
                Transform(w_row_labels, w_row_labels2),
            )
            self.wait(1)

        # Highlight column 3 again
        col_3_highlight2 = SurroundingRectangle(matrix.get_columns()[3], color=ORANGE, buff=0.05)
        v_3_highlight2 = SurroundingRectangle(v_vec.get_rows()[3], color=ORANGE, buff=0.05)

        with self.voiceover(
            """We read column three again, the same incoming edges. But the
            result is a boolean True instead of the weight value."""
        ):
            self.play(Create(col_3_highlight2), Create(v_3_highlight2))
            self.wait(1)

            # Fill result: w[0]="T"
            new_w_values2 = ["T", "", "", "", "", ""]
            for j, val in enumerate(new_w_values2):
                old_entry = w_vec.get_entries()[j]
                if val:
                    new_entry = Text(val, font_size=16, color=ORANGE).move_to(old_entry.get_center())
                    self.play(Transform(old_entry, new_entry), run_time=0.5)
                    self.play(animate_vertex_fill(graph.vertices[j], ORANGE), run_time=0.3)
                else:
                    self.play(old_entry.animate.set_opacity(0), run_time=0.3)

            self.wait(1)

        self.play(FadeOut(col_3_highlight2), FadeOut(v_3_highlight2))

        with self.voiceover(
            """Same structure discovered, but without the cost of loading weights.
            For algorithms like BFS that only care about connectivity, any_pair
            is the right choice."""
        ):
            summary_text2 = Text(
                "ANY_PAIR: structure only, no weight loading",
                font_size=24, color=ORANGE
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(summary_text2))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(code), FadeOut(summary_text2),
            FadeOut(matrix), FadeOut(matrix_label), FadeOut(row_labels), FadeOut(col_labels),
            FadeOut(times_sym),
            FadeOut(v_vec), FadeOut(v_label), FadeOut(v_row_labels),
            FadeOut(equals_sym),
            FadeOut(w_vec), FadeOut(w_label), FadeOut(w_row_labels),
            FadeOut(graph), FadeOut(weight_labels),
        )
        self.wait(0.5)
