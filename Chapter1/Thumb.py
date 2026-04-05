from manim import *


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Python-GraphBLAS", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        code = Code(
            code_string="""import graphblas as gb
from graphblas import Matrix, Vector, binary

A = Matrix.from_coo(
    [0, 0, 1, 3, 3, 4, 5],
    [1, 3, 2, 4, 5, 2, 4],
    [1, 2, 5, 2, 9, 5, 2],
)""",
            language="python",
            background="window",
        ).scale(0.7)
        code.move_to(ORIGIN)

        concept = Text("Creating and Exploring Sparse Graphs", font_size=28, color=GREEN)
        concept.next_to(code, DOWN, buff=0.6)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(FadeIn(code))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
