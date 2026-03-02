import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import create_small_graph_from_matrix, setup_scene


class Scene2(VoiceoverScene, Scene):
    """Matrix-Matrix Multiply: Multi-hop Paths."""

    def construct(self):
        setup_scene(self)

        # Adjacency matrix data for graph visualization
        A_adj_data = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ]

        # A^2 result data: 2-hop paths (diagonal + opposite corners)
        A2_adj_data = [
            [2, 0, 0, 2],
            [0, 2, 2, 0],
            [0, 2, 2, 0],
            [2, 0, 0, 2],
        ]

        # Introduce A @ A for 2-hop
        mxm_title = Text("Matrix-Matrix Multiply: Multi-hop Paths", font_size=36).to_edge(UP)

        a_mat_1 = Matrix([
            ["", "1", "1", ""],
            ["1", "", "", "1"],
            ["1", "", "", "1"],
            ["", "1", "1", ""],
        ], v_buff=0.6, h_buff=0.6).scale(0.4)
        a_label_1 = MathTex("A").scale(0.7)
        a_graph_1 = create_small_graph_from_matrix(A_adj_data, scale=0.3, directed=False, edge_color=BLUE)
        a_col_1 = VGroup(a_label_1, a_mat_1, a_graph_1).arrange(DOWN, buff=0.15)

        times_2 = MathTex(r"\times").scale(0.8)

        a_mat_2 = Matrix([
            ["", "1", "1", ""],
            ["1", "", "", "1"],
            ["1", "", "", "1"],
            ["", "1", "1", ""],
        ], v_buff=0.6, h_buff=0.6).scale(0.4)
        a_label_2 = MathTex("A").scale(0.7)
        a_graph_2 = create_small_graph_from_matrix(A_adj_data, scale=0.3, directed=False, edge_color=BLUE)
        a_col_2 = VGroup(a_label_2, a_mat_2, a_graph_2).arrange(DOWN, buff=0.15)

        equals_2 = MathTex("=").scale(0.8)

        # A^2 result: 2-hop paths (diagonal + opposite corners)
        a2_mat = Matrix([
            ["2", "", "", "2"],
            ["", "2", "2", ""],
            ["", "2", "2", ""],
            ["2", "", "", "2"],
        ], v_buff=0.6, h_buff=0.6).scale(0.4)
        a2_label = MathTex("A^2").scale(0.7)
        a2_graph = create_small_graph_from_matrix(A2_adj_data, scale=0.3, directed=False, edge_color=YELLOW)
        a2_col = VGroup(a2_label, a2_mat, a2_graph).arrange(DOWN, buff=0.15)

        mxm_eq = VGroup(
            a_col_1,
            times_2,
            a_col_2,
            equals_2,
            a2_col
        ).arrange(RIGHT, buff=0.3)
        mxm_eq.next_to(mxm_title, DOWN, buff=0.4)

        label_mxm = Text("2-hop paths", font_size=24, color=YELLOW).next_to(mxm_eq, DOWN, buff=0.3)

        with self.voiceover(
            """When we multiply the adjacency matrix by itself, we get A squared.
            Each entry in A squared tells us how many 2-hop paths exist between
            nodes. This is the algebraic way to explore paths of any length."""
        ):
            self.play(Write(mxm_title))
            self.play(Write(mxm_eq))
            self.play(Write(label_mxm))
            self.wait(1)

        self.play(FadeOut(mxm_eq), FadeOut(label_mxm))

        # Show GraphBLAS syntax
        syntax_title = Text("GraphBLAS Syntax", font_size=36).move_to(mxm_title.get_center())

        syntax_code = Code(
            code_string="""# Matrix-matrix multiply with semiring
C << A.mxm(B, semiring)

# Or using Python operator (default semiring)
C = A @ B""",
            language="python",
            background="window"
        ).scale(0.8)
        syntax_code.next_to(syntax_title, DOWN, buff=0.8)

        with self.voiceover(
            """In GraphBLAS, we write matrix-matrix multiply as A dot mxm B,
            specifying a semiring. Python-graphblas also supports the at-sign
            operator for the default plus-times semiring. The semiring determines
            how elements are combined during multiplication."""
        ):
            self.play(Transform(mxm_title, syntax_title))
            self.play(Write(syntax_code))
            self.wait(2)

        # Cleanup
        self.play(FadeOut(mxm_title), FadeOut(syntax_code))
        self.wait(0.5)
