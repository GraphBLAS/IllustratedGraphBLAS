import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import create_sparse_matrix, create_small_graph_from_matrix, CHAPTER0_MATRIX_DATA


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Introduction to GraphBLAS", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Sparse matrix on the left
        matrix = create_sparse_matrix(CHAPTER0_MATRIX_DATA, scale=0.45)

        # Bidirectional arrow in the center
        arrow = MathTex(r"\Leftrightarrow").scale(1.2)

        # Directed graph on the right
        graph = create_small_graph_from_matrix(CHAPTER0_MATRIX_DATA, scale=0.5, directed=True)

        illustration = VGroup(matrix, arrow, graph).arrange(RIGHT, buff=0.5)
        illustration.move_to(ORIGIN)

        # Labels below matrix and graph
        mat_label = MathTex("A").next_to(matrix, DOWN, buff=0.2)
        graph_label = MathTex("G").next_to(graph, DOWN, buff=0.2)
        labels = VGroup(mat_label, graph_label)

        concept = Text("Graphs as Sparse Matrices", font_size=28, color=GREEN)
        concept.next_to(illustration, DOWN, buff=0.8)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(matrix), Create(graph), Write(labels))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
