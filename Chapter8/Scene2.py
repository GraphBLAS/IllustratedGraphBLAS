import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    setup_scene,
    create_undirected_graph,
    create_sparse_matrix,
    CHAPTER8_MATRIX_DATA,
    CHAPTER8_A2_DATA,
    CHAPTER8_TRIANGLE_DATA,
    highlight_triangle,
    animate_vertex_fill,
)


class Scene2(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Title
        title = Text("The A² Algorithm", font_size=42).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Three-panel layout: code (left) | matrix (center) | graph (right)

        # Code panel
        code_lines = [
            "# A² counts 2-hop paths",
            "A2 = A @ A",
            "",
            "# Element-wise multiply",
            "T = A2 * A",
            "",
            "# Sum and divide by 6",
            "triangles = T.sum() // 6",
        ]
        code = Code(
            code_string="\n".join(code_lines),
            language="python",
            background="window",
        ).scale(0.7)
        code.to_edge(LEFT, buff=0.3).shift(DOWN * 0.2)

        # Matrix A
        A_label = Text("A", font_size=28, color=BLUE)
        A_mat = create_sparse_matrix(CHAPTER8_MATRIX_DATA, scale=0.4, v_buff=0.5, h_buff=0.5)
        A_group = VGroup(A_label, A_mat).arrange(DOWN, buff=0.2)

        # Graph (circular layout to show all triangles clearly)
        graph = create_undirected_graph(CHAPTER8_MATRIX_DATA, layout="circular", scale=0.6)

        # Position center and right panels
        A_group.move_to(ORIGIN).shift(DOWN * 0.3)
        graph.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)

        with self.voiceover(
            """The key insight for counting triangles algebraically is that
            squaring the adjacency matrix counts two-hop paths. If there's a
            path from node i to j through some intermediate node, A squared
            will capture it."""
        ):
            self.play(Create(code))
            self.play(Write(A_label), Create(A_mat))
            self.play(Create(graph))
            self.wait(1)

        # Show A² computation
        A2_label = Text("A²", font_size=28, color=GREEN)
        A2_mat = create_sparse_matrix(CHAPTER8_A2_DATA, scale=0.4, v_buff=0.5, h_buff=0.5)
        A2_group = VGroup(A2_label, A2_mat).arrange(DOWN, buff=0.2)
        A2_group.move_to(A_group.get_center())

        with self.voiceover(
            """When we compute A squared, each entry tells us how many
            two-hop paths connect those nodes. For example, if A squared
            at position i, j equals 2, there are two different intermediate
            nodes connecting i to j."""
        ):
            self.play(
                ReplacementTransform(A_label, A2_label),
                ReplacementTransform(A_mat, A2_mat),
            )
            self.wait(1)

        # Show element-wise multiply concept
        with self.voiceover(
            """Now here's the key step. If A squared says there's a two-hop
            path between i and j, and the original matrix A says there's
            also a direct edge between i and j, then we have a triangle.
            The two-hop path and the direct edge form a closed loop of
            three nodes."""
        ):
            # Highlight a triangle on the graph
            tri_highlight = highlight_triangle(graph, (0, 1, 2), color=YELLOW)
            self.play(Create(tri_highlight))
            # Highlight the participating vertices
            for node in [0, 1, 2]:
                self.play(animate_vertex_fill(graph.vertices[node], YELLOW), run_time=0.3)
            self.wait(1)

        # Show T = A² ⊙ A
        times_sym = MathTex(r"\odot", font_size=36)
        A_small = Text("A", font_size=28, color=BLUE)
        equals_sym = MathTex("=", font_size=36)
        T_label = Text("T", font_size=28, color=ORANGE)
        T_mat = create_sparse_matrix(CHAPTER8_TRIANGLE_DATA, scale=0.4, v_buff=0.5, h_buff=0.5)

        # Arrange equation: A² ⊙ A = T
        eq_group = VGroup(A2_label.copy(), times_sym, A_small, equals_sym, T_label, T_mat)

        with self.voiceover(
            """The element-wise product of A squared and A gives us matrix
            T. Each non-zero entry in T indicates an edge that participates
            in at least one triangle. The value tells us how many triangles
            that edge belongs to."""
        ):
            # Fade out A² label and matrix before showing T
            self.play(FadeOut(A2_label), FadeOut(A2_mat))

            T_group = VGroup(T_label, T_mat).arrange(DOWN, buff=0.2)
            T_group.move_to(A_group.get_center())
            self.play(Write(T_label), Create(T_mat))

            # Reset graph colors
            self.play(FadeOut(tri_highlight))
            for node in [0, 1, 2]:
                self.play(animate_vertex_fill(graph.vertices[node], WHITE), run_time=0.2)
            self.wait(1)

        # Show final sum
        sum_text = MathTex(r"\text{sum}(T) = 24", font_size=32)
        div_text = MathTex(r"24 \div 6 = 4 \text{ triangles}", font_size=32)
        result_group = VGroup(sum_text, div_text).arrange(DOWN, buff=0.3)
        result_group.next_to(T_group, DOWN, buff=0.5)

        with self.voiceover(
            """Finally, we sum all entries in T and divide by 6. Why 6?
            Each triangle has three edges, and each edge is counted twice
            in the symmetric matrix. Three times two equals six. The result
            is exactly 4 triangles, matching what we counted visually."""
        ):
            self.play(Write(sum_text))
            self.wait(0.5)
            self.play(Write(div_text))
            self.wait(1)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(code),
            FadeOut(T_label),
            FadeOut(T_mat),
            FadeOut(graph),
            FadeOut(result_group),
        )
        self.wait(0.5)
