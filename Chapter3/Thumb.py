import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import create_small_graph_from_matrix, CHAPTER3_MATRIX_DATA, set_vertex_fill_preserve_label


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Breadth-First Search", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # 6-node undirected graph colored by BFS level from node 0
        graph = create_small_graph_from_matrix(CHAPTER3_MATRIX_DATA, scale=0.6, directed=False)

        # Color nodes by BFS level from source node 0
        # Level 0: node 0 (source)
        set_vertex_fill_preserve_label(graph.vertices[0], YELLOW)
        # Level 1: nodes 1, 3 (direct neighbors of 0)
        set_vertex_fill_preserve_label(graph.vertices[1], ORANGE)
        set_vertex_fill_preserve_label(graph.vertices[3], ORANGE)
        # Level 2: nodes 2, 4, 5
        set_vertex_fill_preserve_label(graph.vertices[2], RED_B)
        set_vertex_fill_preserve_label(graph.vertices[4], RED_B)
        set_vertex_fill_preserve_label(graph.vertices[5], RED_B)

        # Small legend
        legend = VGroup(
            VGroup(Dot(color=YELLOW, radius=0.1), Text("Source", font_size=18)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=ORANGE, radius=0.1), Text("Level 1", font_size=18)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=RED_B, radius=0.1), Text("Level 2", font_size=18)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        illustration = VGroup(graph, legend).arrange(RIGHT, buff=0.8)
        illustration.move_to(ORIGIN)

        concept = Text("Graph Traversal with Linear Algebra", font_size=28, color=GREEN)
        concept.next_to(illustration, DOWN, buff=0.8)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Create(graph), FadeIn(legend))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
