import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import create_sparse_matrix


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Incidence Matrices", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # S: source matrix (3 nodes x 4 edges)
        # Edges: e0: 0->1, e1: 1->2, e2: 0->2, e3: 2->0
        S_data = [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
        S_mat = create_sparse_matrix(S_data, scale=0.5)

        at_sym = MathTex("@").scale(1.2)

        # D: destination matrix (4 edges x 3 nodes)
        D_data = [[0, 1, 0], [0, 0, 1], [0, 0, 1], [1, 0, 0]]
        D_mat = create_sparse_matrix(D_data, scale=0.5)

        equals_sym = MathTex("=").scale(1.2)

        # A: adjacency matrix (3x3)
        A_data = [[0, 1, 1], [0, 0, 1], [1, 0, 0]]
        A_mat = create_sparse_matrix(A_data, scale=0.5)

        equation = VGroup(S_mat, at_sym, D_mat, equals_sym, A_mat).arrange(RIGHT, buff=0.3)
        equation.move_to(ORIGIN)

        # Labels positioned after arrange
        S_label = MathTex("S").next_to(S_mat, DOWN, buff=0.2)
        D_label = MathTex("D").next_to(D_mat, DOWN, buff=0.2)
        A_label = MathTex("A").next_to(A_mat, DOWN, buff=0.2)
        labels = VGroup(S_label, D_label, A_label)

        concept = Text("Decomposing Graph Structure", font_size=28, color=GREEN)
        concept.next_to(equation, DOWN, buff=0.8)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(equation), Write(labels))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
