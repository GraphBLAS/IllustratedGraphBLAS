import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import create_sparse_matrix, create_small_graph_from_matrix, setup_scene


class Scene1(VoiceoverScene, Scene):
    """Recall: Vector-Matrix Multiply."""

    def construct(self):
        setup_scene(self)

        # Show recall of v @ A
        recall_title = Text("Recall: Vector-Matrix Multiply", font_size=36).to_edge(UP)

        # Simple visual: v @ A = neighbors
        # Adjacency matrix data for graph visualization
        A_adj_data = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ]

        v_vec = create_sparse_matrix([[1], [0], [0], [0]], scale=0.5)
        times_1 = MathTex(r"\times").scale(0.8)
        a_mat = Matrix([
            ["", "1", "1", ""],
            ["1", "", "", "1"],
            ["1", "", "", "1"],
            ["", "1", "1", ""],
        ], v_buff=0.6, h_buff=0.6).scale(0.5)

        # Small graph below the adjacency matrix
        a_graph = create_small_graph_from_matrix(A_adj_data, scale=0.35, directed=False, edge_color=BLUE)
        a_col = VGroup(a_mat, a_graph).arrange(DOWN, buff=0.2)

        equals_1 = MathTex("=").scale(0.8)
        result_1 = create_sparse_matrix([[0], [1], [1], [0]], scale=0.5)

        vxm_eq = VGroup(v_vec, times_1, a_col, equals_1, result_1).arrange(RIGHT, buff=0.3)
        vxm_eq.next_to(recall_title, DOWN, buff=0.6)

        label_vxm = Text("1-hop neighbors", font_size=24, color=GREEN).next_to(vxm_eq, DOWN, buff=0.3)

        with self.voiceover(
            """Vector-matrix multiply takes a frontier vector and finds all
            nodes one hop away. The vector marks our starting position, and
            multiplication against the adjacency matrix reveals direct neighbors."""
        ):
            self.play(Write(recall_title))
            self.play(Write(vxm_eq))
            self.play(Write(label_vxm))
            self.wait(1)

        self.play(FadeOut(vxm_eq), FadeOut(label_vxm), FadeOut(recall_title))
        self.wait(0.5)
