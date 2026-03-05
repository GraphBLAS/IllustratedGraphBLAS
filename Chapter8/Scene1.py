import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    setup_scene,
    create_undirected_graph,
    CHAPTER8_MATRIX_DATA,
    CHAPTER8_TRIANGLES,
    highlight_triangle,
    animate_vertex_fill,
)


class Scene1(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Title
        title = Text("What is a Triangle?", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Create the 6-node graph centered (circular layout to show all triangles clearly)
        graph = create_undirected_graph(CHAPTER8_MATRIX_DATA, layout="circular", scale=0.6)
        graph.move_to(ORIGIN).shift(DOWN * 0.3)

        with self.voiceover(
            """A triangle in a graph is a set of three nodes where every pair
            is connected by an edge. In other words, each node in the triangle
            is directly connected to both of the others."""
        ):
            self.play(Create(graph))
            self.wait(1)

        # Highlight each triangle one by one
        triangle_colors = [YELLOW, ORANGE, GREEN, PURPLE]

        with self.voiceover(
            """Let's identify the triangles in this graph. Here we have
            nodes zero, one, and two forming our first triangle."""
        ):
            highlight1 = highlight_triangle(graph, CHAPTER8_TRIANGLES[0], color=triangle_colors[0])
            self.play(Create(highlight1))
            # Also highlight vertices
            for node in CHAPTER8_TRIANGLES[0]:
                self.play(animate_vertex_fill(graph.vertices[node], triangle_colors[0]), run_time=0.3)
            self.wait(0.5)

        with self.voiceover(
            """Nodes zero, two, and three form a second triangle."""
        ):
            highlight2 = highlight_triangle(graph, CHAPTER8_TRIANGLES[1], color=triangle_colors[1])
            self.play(Create(highlight2))
            for node in CHAPTER8_TRIANGLES[1]:
                if node not in CHAPTER8_TRIANGLES[0]:  # Don't re-color shared nodes
                    self.play(animate_vertex_fill(graph.vertices[node], triangle_colors[1]), run_time=0.3)
            self.wait(0.5)

        with self.voiceover(
            """Nodes two, three, and four make a third triangle."""
        ):
            highlight3 = highlight_triangle(graph, CHAPTER8_TRIANGLES[2], color=triangle_colors[2])
            self.play(Create(highlight3))
            for node in CHAPTER8_TRIANGLES[2]:
                if node == 4:  # Only new node
                    self.play(animate_vertex_fill(graph.vertices[node], triangle_colors[2]), run_time=0.3)
            self.wait(0.5)

        with self.voiceover(
            """And finally, nodes three, four, and five complete our fourth triangle."""
        ):
            highlight4 = highlight_triangle(graph, CHAPTER8_TRIANGLES[3], color=triangle_colors[3])
            self.play(Create(highlight4))
            self.play(animate_vertex_fill(graph.vertices[5], triangle_colors[3]), run_time=0.3)
            self.wait(0.5)

        # Show count
        count_text = Text("Total: 4 triangles", font_size=36).next_to(graph, DOWN, buff=0.8)

        with self.voiceover(
            """This graph contains four triangles total. Notice that some
            nodes participate in multiple triangles. Node two, for example,
            is part of three different triangles, making it a hub in this
            structure."""
        ):
            self.play(Write(count_text))
            # Pulse node 2 to show it's a hub
            self.play(
                graph.vertices[2].animate.scale(1.3),
                rate_func=there_and_back,
                run_time=1
            )
            self.wait(1)

        # Reset vertex colors
        with self.voiceover(
            """Counting triangles is useful for understanding graph
            structure. Dense clusters of triangles often indicate tightly
            connected communities."""
        ):
            for node in graph.vertices:
                self.play(animate_vertex_fill(graph.vertices[node], WHITE), run_time=0.15)
            self.wait(1)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(graph),
            FadeOut(highlight1),
            FadeOut(highlight2),
            FadeOut(highlight3),
            FadeOut(highlight4),
            FadeOut(count_text),
        )
        self.wait(0.5)
