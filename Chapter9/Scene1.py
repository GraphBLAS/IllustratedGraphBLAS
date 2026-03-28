import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    setup_scene,
    create_bipartite_graph,
    create_sparse_matrix,
    CHAPTER9_BIPARTITE_EDGES,
)


class Scene1(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # --- Voiceover 1: Neural network layer as bipartite graph ---
        with self.voiceover(
            """A neural network layer takes input values, multiplies by weights,
            and produces outputs. This is the same structure as a bipartite graph
            where input neurons connect to output neurons through weighted edges,
            as we saw in Chapter 1."""
        ):
            graph = create_bipartite_graph(
                4, 3, CHAPTER9_BIPARTITE_EDGES, scale=0.9,
                left_color=BLUE, right_color=GREEN
            )
            input_label = Text("Inputs", font_size=24, color=BLUE).next_to(graph, UP + LEFT, buff=0.3)
            output_label = Text("Outputs", font_size=24, color=GREEN).next_to(graph, UP + RIGHT, buff=0.3)

            self.play(FadeIn(graph), Write(input_label), Write(output_label))
            self.wait(1)

        # --- Voiceover 2: Weight matrix = adjacency matrix ---
        with self.voiceover(
            """Arranging the weights into a matrix gives us the adjacency matrix
            from Chapter 1. Each edge weight becomes a matrix entry. Absent
            connections are simply absent entries in the sparse matrix."""
        ):
            # Shift graph left
            graph_group = VGroup(graph, input_label, output_label)
            self.play(graph_group.animate.scale(0.7).to_edge(LEFT, buff=0.5))

            # Weight matrix corresponding to the bipartite edges
            # 4 inputs x 3 outputs, edges from CHAPTER9_BIPARTITE_EDGES
            w_data = [
                [0.5, 0, 0.3],
                [0, 0.7, 0],
                [0.4, 0, 0.6],
                [0, -0.2, 0],
            ]
            w_matrix = create_sparse_matrix(w_data, scale=0.7)
            w_label = MathTex("W", font_size=36).next_to(w_matrix, UP, buff=0.3)
            w_group = VGroup(w_matrix, w_label).to_edge(RIGHT, buff=1.0)

            self.play(FadeIn(w_group))

            # Highlight one edge and its matrix entry
            edge_highlight = graph.edges[0].copy().set_color(YELLOW).set_stroke(width=4)
            entry = w_matrix.get_entries()[0]  # [0,0] = 0.5
            entry_highlight = SurroundingRectangle(entry, color=YELLOW, buff=0.05)
            self.play(Create(edge_highlight), Create(entry_highlight))
            self.wait(1)

        # --- Voiceover 3: mxm operation ---
        with self.voiceover(
            """Computing a layer's output is matrix-vector multiplication using
            the plus-times semiring, the same mxm operation from Chapter 4."""
        ):
            self.play(FadeOut(edge_highlight), FadeOut(entry_highlight))
            self.play(FadeOut(graph_group), FadeOut(w_group))

            equation = MathTex(r"y = x \times W", font_size=48).shift(UP)
            self.play(Write(equation))

            code = Code(
                code_string="Y << plus_times(Y @ W)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7).next_to(equation, DOWN, buff=0.5)
            self.play(FadeIn(code))
            self.wait(1)

        self.play(FadeOut(equation), FadeOut(code))
        self.wait(0.5)
