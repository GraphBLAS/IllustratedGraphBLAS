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
    CHAPTER8_TRIANGLE_DATA,
    CHAPTER8_PER_NODE_TRIANGLES,
)


class Scene6(VoiceoverScene, Scene):
    """Triangle Centrality Computation - breaking down the formula."""

    def construct(self):
        setup_scene(self)

        # Title
        title = Text("Computing Triangle Centrality", font_size=42).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Formula at the top
        formula = MathTex(
            r"TC = \frac{3(A \cdot y) - 2(T \cdot y) + y}{k}",
            font_size=36
        ).next_to(title, DOWN, buff=0.4)

        with self.voiceover(
            """Let's break down the triangle centrality formula.
            TC equals 3 times A dot y, minus 2 times T dot y, plus y,
            all divided by k. We already have all the pieces we need
            from our triangle counting work."""
        ):
            self.play(Write(formula))
            self.wait(1)

        self.play(formula.animate.scale(0.8).to_edge(UP, buff=0.3))
        self.play(FadeOut(title))

        # Show the components in a 3-column layout
        # Left: y vector (per-node triangle counts)
        y_data = [[c * 2] for c in CHAPTER8_PER_NODE_TRIANGLES]  # Raw sums (not divided by 2)
        y_mat = Matrix(y_data, v_buff=0.4, h_buff=0.3).scale(0.35)
        y_label = MathTex("y", font_size=28, color=YELLOW)
        y_desc = Text("row sums of T", font_size=16, color=GRAY)
        y_group = VGroup(y_label, y_mat, y_desc).arrange(DOWN, buff=0.15)
        y_group.to_edge(LEFT, buff=0.8).shift(DOWN * 0.5)

        # Middle: A matrix
        A_mat = create_sparse_matrix(CHAPTER8_MATRIX_DATA, scale=0.35, v_buff=0.4, h_buff=0.4)
        A_label = MathTex("A", font_size=28, color=BLUE)
        A_desc = Text("adjacency", font_size=16, color=GRAY)
        A_group = VGroup(A_label, A_mat, A_desc).arrange(DOWN, buff=0.15)
        A_group.move_to(ORIGIN).shift(DOWN * 0.5)

        # Right: T matrix (binary version)
        T_indicator = [[1 if v > 0 else 0 for v in row] for row in CHAPTER8_TRIANGLE_DATA]
        T_mat = create_sparse_matrix(T_indicator, scale=0.35, v_buff=0.4, h_buff=0.4)
        T_label = MathTex("T", font_size=28, color=ORANGE)
        T_desc = Text("T > 0 (bool)", font_size=16, color=GRAY)
        T_group = VGroup(T_label, T_mat, T_desc).arrange(DOWN, buff=0.15)
        T_group.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.5)

        with self.voiceover(
            """We need three components. First, y: the row sums of our
            triangle matrix T, giving per-node triangle counts before
            dividing by 2. Second, A: our adjacency matrix. Third,
            the triangle matrix T: a boolean matrix showing where triangles exist."""
        ):
            self.play(Write(y_label), Create(y_mat), Write(y_desc))
            self.play(Write(A_label), Create(A_mat), Write(A_desc))
            self.play(Write(T_label), Create(T_mat), Write(T_desc))
            self.wait(1)

        # Fade matrices and show the computation steps
        self.play(
            FadeOut(y_group),
            FadeOut(A_group),
            FadeOut(T_group),
        )

        # Step-by-step breakdown
        step1 = VGroup(
            MathTex(r"A \cdot y", font_size=32, color=BLUE),
            Text("= sum of ALL neighbors' triangle counts", font_size=20),
        ).arrange(RIGHT, buff=0.3)
        step1.next_to(formula, DOWN, buff=0.6)

        step2 = VGroup(
            MathTex(r"T \cdot y", font_size=32, color=ORANGE),
            Text("= sum of TRIANGLE neighbors' counts", font_size=20),
        ).arrange(RIGHT, buff=0.3)
        step2.next_to(step1, DOWN, buff=0.4)

        step3 = VGroup(
            MathTex(r"3(A \cdot y) - 2(T \cdot y)", font_size=32),
            Text("= weighted combination", font_size=20),
        ).arrange(RIGHT, buff=0.3)
        step3.next_to(step2, DOWN, buff=0.4)

        with self.voiceover(
            """A times y computes, for each node, the sum of all its
            neighbors' triangle counts. T times y computes
            the sum of only triangle neighbors' counts. The difference
            with coefficients 3 and 2 means non-triangle neighbors
            contribute more to your centrality score."""
        ):
            self.play(Write(step1))
            self.play(Write(step2))
            self.play(Write(step3))
            self.wait(1)

        # Show the weighting math
        weight_explanation = VGroup(
            Text("Non-triangle neighbors: 3 - 0 = 3", font_size=22, color=GREEN),
            Text("Triangle neighbors: 3 - 2 = 1", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.2)
        weight_explanation.next_to(step3, DOWN, buff=0.5)

        with self.voiceover(
            """Here's why: for non-triangle neighbors, they appear in
            A dot y but not in T dot y, so their coefficient is 3 minus
            0 equals 3. For triangle neighbors, they appear in both,
            so their coefficient is 3 minus 2 equals 1. Non-triangle
            neighbors count three times more."""
        ):
            self.play(Write(weight_explanation))
            self.wait(1)

        # Show code
        self.play(
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(weight_explanation),
        )

        code_lines = """def triangle_centrality(A):
    # y = per-node triangle counts
    T = A.dup(clear=True)
    T(A.S) << A.mxm(A.T)
    y = T.reduce_rowwise(binary.plus).new()

    # k = normalization factor (sum of all triangle counts)
    k = y.reduce(binary.plus).new().value

    # T1 = where triangles exist (binary mask)
    T1 = T.dup(bool)

    tc = (3 * (A @ y) + -2 * (T1 @ y) + y) / k

    return tc.new()"""
        code = Code(
            code_string=code_lines,
            language="python",
            background="window",
        ).scale(0.7)
        code.move_to(ORIGIN).shift(DOWN * 0.3)

        with self.voiceover(
            """In code, the computation is straightforward. We compute y
            as row sums of T. k is the total for normalization. Then
            A times y gives all-neighbor sums, T times y gives
            triangle-neighbor sums, and we combine them with the weights
            3, negative 2, and 1."""
        ):
            self.play(Create(code))
            self.wait(1)

        # Insight at the bottom
        insight = Text(
            "Bridges to other communities contribute more to centrality",
            font_size=22,
            color=GREEN
        ).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            """The key insight: nodes that bridge to other highly-triangulated
            communities score higher. A node connected to many triangles
            outside its own cluster is more central than one embedded
            only in its local group."""
        ):
            self.play(Write(insight))
            self.wait(1)

        # Fade out
        self.play(
            FadeOut(formula),
            FadeOut(code),
            FadeOut(insight),
        )
        self.wait(0.5)
