import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import create_sparse_matrix


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Element-wise Operations", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Two sparse matrices combined element-wise
        A_data = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
        B_data = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]
        C_data = [[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2], [1, 0, 0, 0]]

        A_mat = create_sparse_matrix(A_data, scale=0.45)
        oplus = MathTex(r"\oplus").scale(1.2)
        B_mat = create_sparse_matrix(B_data, scale=0.45)
        equals_sym = MathTex("=").scale(1.2)
        C_mat = create_sparse_matrix(C_data, scale=0.45)

        equation = VGroup(A_mat, oplus, B_mat, equals_sym, C_mat).arrange(RIGHT, buff=0.3)
        equation.move_to(ORIGIN)

        # Colored labels positioned after arrange
        A_label = MathTex("A", color=BLUE).next_to(A_mat, DOWN, buff=0.2)
        B_label = MathTex("B", color=GREEN).next_to(B_mat, DOWN, buff=0.2)
        C_label = MathTex("C").next_to(C_mat, DOWN, buff=0.2)
        labels = VGroup(A_label, B_label, C_label)

        concept = Text("Combining and Transforming Graphs", font_size=28, color=GREEN)
        concept.next_to(equation, DOWN, buff=0.8)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(equation), Write(labels))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
