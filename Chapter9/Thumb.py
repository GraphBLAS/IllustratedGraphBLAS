import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import create_bipartite_graph, CHAPTER9_BIPARTITE_EDGES


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Sparse Neural Networks", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Bipartite graph representing a neural network layer
        graph = create_bipartite_graph(
            4, 3, CHAPTER9_BIPARTITE_EDGES, scale=0.7,
            left_color=BLUE, right_color=GREEN
        )
        graph.move_to(ORIGIN)

        # Column labels
        input_label = Text("Inputs", font_size=22, color=BLUE)
        input_label.next_to(graph, LEFT, buff=0.3)
        output_label = Text("Outputs", font_size=22, color=GREEN)
        output_label.next_to(graph, RIGHT, buff=0.3)

        # Weight matrix equation
        w_label = MathTex(r"Y = Y \cdot W").scale(0.8)
        w_label.next_to(graph, DOWN, buff=0.3)

        illustration = VGroup(graph, input_label, output_label, w_label)
        illustration.move_to(ORIGIN)

        concept = Text("DNN Inference with GraphBLAS", font_size=28, color=GREEN)
        concept.next_to(illustration, DOWN, buff=0.6)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(FadeIn(graph), Write(input_label), Write(output_label), Write(w_label))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
