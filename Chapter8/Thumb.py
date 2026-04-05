import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import (
    create_undirected_graph, highlight_triangle,
    CHAPTER8_MATRIX_DATA, CHAPTER8_TRIANGLES,
)


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Triangle Counting", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # 6-node undirected graph with triangles highlighted
        graph = create_undirected_graph(CHAPTER8_MATRIX_DATA, scale=0.45)

        triangle_colors = [YELLOW, ORANGE, TEAL, PURPLE]
        highlights = VGroup()
        for tri, color in zip(CHAPTER8_TRIANGLES, triangle_colors):
            h = highlight_triangle(graph, tri, color=color, edge_width=5)
            highlights.add(h)

        graph_group = VGroup(graph, highlights)

        # Formula on the right
        formula = MathTex(r"A^2 \odot A").scale(1.2)
        count_text = Text("= 4 triangles", font_size=24)
        formula_group = VGroup(formula, count_text).arrange(DOWN, buff=0.3)

        illustration = VGroup(graph_group, formula_group).arrange(RIGHT, buff=1.0)
        illustration.move_to(ORIGIN)

        concept = Text("Algebraic Triangle Detection", font_size=28, color=GREEN)
        concept.next_to(illustration, DOWN, buff=0.8)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Create(graph), Create(highlights), Write(formula_group))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
