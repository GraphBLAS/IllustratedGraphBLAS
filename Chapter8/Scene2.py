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
    CHAPTER8_L_DATA,
    CHAPTER8_L_MASKED_DATA,
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
            formatter_style="dracula",
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

        # Fade out classical method
        self.play(
            FadeOut(title),
            FadeOut(code),
            FadeOut(T_label),
            FadeOut(T_mat),
            FadeOut(graph),
            FadeOut(result_group),
        )
        self.wait(0.5)

        # ===== SANDIA METHOD SECTION =====

        # Title for Sandia method
        sandia_title = Text("The Sandia Method", font_size=42, color=GREEN)
        sandia_title.to_edge(UP, buff=0.3)

        with self.voiceover(
            """This approach works, but we can make it more efficient.
            The classical method has two issues. First, our symmetric
            matrix counts every edge twice, forward and backward.
            Second, we perform two separate operations: matrix multiply,
            then element-wise multiply."""
        ):
            self.play(Write(sandia_title))

            # Show issues with classical method
            issues = VGroup(
                Text("Issues with A² ⊙ A:", font_size=28, color=YELLOW),
                Text("• Symmetric matrix = counting edges twice", font_size=24),
                Text("• Two operations: mxm then ewise_mult", font_size=24),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            issues.move_to(ORIGIN)
            self.play(Write(issues))
            self.wait(1)

        # Introduce solution
        with self.voiceover(
            """The Sandia method addresses both issues. We start by
            selecting only the lower triangular portion of A. This
            gives us matrix L with half the edges."""
        ):
            self.play(FadeOut(issues))

            # Show A and L side by side
            A_label2 = Text("A", font_size=28, color=BLUE)
            A_mat2 = create_sparse_matrix(CHAPTER8_MATRIX_DATA, scale=0.35, v_buff=0.45, h_buff=0.45)
            A_group2 = VGroup(A_label2, A_mat2).arrange(DOWN, buff=0.2)

            arrow = MathTex(r"\xrightarrow{\text{tril}}", font_size=36)

            L_label = Text("L", font_size=28, color=GREEN)
            L_mat = create_sparse_matrix(CHAPTER8_L_DATA, scale=0.35, v_buff=0.45, h_buff=0.45)
            L_group = VGroup(L_label, L_mat).arrange(DOWN, buff=0.2)

            tril_group = VGroup(A_group2, arrow, L_group).arrange(RIGHT, buff=0.5)
            tril_group.move_to(ORIGIN).shift(UP * 0.5)

            self.play(Write(A_label2), Create(A_mat2))
            self.play(Write(arrow))
            self.play(Write(L_label), Create(L_mat))
            self.wait(1)

        # Show the masked multiply
        with self.voiceover(
            """Then we use L as its own mask during the matrix multiply.
            The notation L, open paren, L dot S, close paren, means:
            only compute entries where L already has values. This
            combines the multiply and mask into one operation."""
        ):
            self.play(FadeOut(A_group2), FadeOut(arrow))

            # Move L to the left
            self.play(L_group.animate.to_edge(LEFT, buff=0.8))

            # Show the masked operation code
            sandia_code = Code(
                code_string="L(L.S) << L.mxm(L)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.8)
            sandia_code.move_to(ORIGIN).shift(UP * 0.3)
            self.play(Create(sandia_code))
            self.wait(1)

        # Show result matrix
        with self.voiceover(
            """The result shows exactly one entry per triangle.
            Position 2,0 captures the triangle between nodes 0, 1, and 2.
            Position 3,0 captures nodes 0, 2, and 3. And so on.
            Each triangle appears exactly once in the lower triangular
            portion."""
        ):
            # Show the result matrix
            result_label = Text("Result", font_size=28, color=ORANGE)
            result_mat = create_sparse_matrix(CHAPTER8_L_MASKED_DATA, scale=0.35, v_buff=0.45, h_buff=0.45)
            result_group2 = VGroup(result_label, result_mat).arrange(DOWN, buff=0.2)
            result_group2.to_edge(RIGHT, buff=0.8)

            self.play(Write(result_label), Create(result_mat))
            self.wait(1)

        # Show final count
        with self.voiceover(
            """The sum is simply 4. No division by 6 needed because
            each triangle is counted exactly once. Same answer,
            computed more efficiently."""
        ):
            self.play(FadeOut(sandia_code))

            # Show sum
            sum_text2 = MathTex(r"\text{sum} = 4 \text{ triangles}", font_size=32, color=GREEN)
            sum_text2.move_to(ORIGIN)
            self.play(Write(sum_text2))
            self.wait(1)

        # Code comparison
        with self.voiceover(
            """Here's the complete Sandia method. Select the lower
            triangular portion, perform the masked matrix multiply,
            and sum the result. Three lines of code, half the edges
            to process, and no post-processing division."""
        ):
            self.play(FadeOut(L_group), FadeOut(result_group2), FadeOut(sum_text2))

            # Show full Sandia code
            full_code = Code(
                code_string="""# Sandia method
L = A.select('tril')
L(L.S) << L.mxm(L)
triangles = L.reduce_scalar()""",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.8)
            full_code.move_to(ORIGIN)
            self.play(Create(full_code))
            self.wait(1)

        # Final fade out
        self.play(
            FadeOut(sandia_title),
            FadeOut(full_code),
        )
        self.wait(0.5)
