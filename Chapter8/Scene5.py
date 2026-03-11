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
    CHAPTER8_PER_NODE_TRIANGLES,
    color_nodes_by_value,
    animate_vertex_fill,
)


class Scene5(VoiceoverScene, Scene):
    """Triangle Centrality Introduction - motivating the concept."""

    def construct(self):
        setup_scene(self)

        # Title
        title = Text("Triangle Centrality", font_size=42).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Start with the question
        question = Text(
            "Per-node counts show participation...",
            font_size=28
        ).next_to(title, DOWN, buff=0.5)

        question2 = Text(
            "but which nodes are truly central?",
            font_size=28,
            color=YELLOW
        ).next_to(question, DOWN, buff=0.2)

        with self.voiceover(
            """Per-node triangle counts tell us how many triangles each node
            participates in. But participation is not the same as importance.
            Which nodes are truly central to the triangle structure of a graph?"""
        ):
            self.play(Write(question))
            self.play(Write(question2))
            self.wait(1)

        self.play(FadeOut(question), FadeOut(question2))

        # Show graph with triangle counts
        graph = create_undirected_graph(CHAPTER8_MATRIX_DATA, layout="circular", scale=0.7)
        graph.move_to(LEFT * 3 + DOWN * 0.3)

        # Color by triangle count
        node_colors = color_nodes_by_value(
            graph,
            CHAPTER8_PER_NODE_TRIANGLES,
            low_color=WHITE,
            high_color=RED
        )
        for vertex, color in node_colors:
            vertex.set_fill(color, opacity=1)
            if vertex.submobjects:
                vertex.submobjects[0].set_color(BLACK)

        # Labels showing counts
        count_labels = VGroup()
        for i, count in enumerate(CHAPTER8_PER_NODE_TRIANGLES):
            label = Text(f"{count}", font_size=16, color=YELLOW)
            label.next_to(graph.vertices[i], UP, buff=0.12)
            count_labels.add(label)

        count_title = Text("Triangle Counts", font_size=24, color=RED)
        count_title.next_to(graph, UP, buff=0.5)

        with self.voiceover(
            """Here is our example graph colored by per-node triangle counts.
            Nodes 2 and 3 have the highest counts with 3 triangles each.
            But is raw participation the best measure of centrality?"""
        ):
            self.play(Create(graph))
            self.play(Write(count_title), Write(count_labels))
            self.wait(1)

        # Key insight panel on right
        insight_title = Text("Key Insight", font_size=28, color=GREEN)
        insight_title.to_edge(RIGHT, buff=2.5).shift(UP * 2)

        insight_lines = VGroup(
            Text("A node is central if it", font_size=22),
            Text("concentrates triangles:", font_size=22),
            Text("By being in many itself", font_size=20, color=BLUE),
            Text("OR", font_size=18, color=GRAY),
            Text("By connecting to neighbors", font_size=20, color=BLUE),
            Text("who are in many", font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        insight_lines.next_to(insight_title, DOWN, buff=0.3, aligned_edge=LEFT)

        with self.voiceover(
            """The key insight behind triangle centrality: a node is central
            if it concentrates triangles. This can happen in two ways.
            The node itself participates in many triangles. Or the node
            connects to neighbors who participate in many triangles."""
        ):
            self.play(Write(insight_title))
            for line in insight_lines:
                self.play(Write(line), run_time=0.3)
            self.wait(1)

        # Show the weighting concept
        weight_box = VGroup(
            Text("Neighbor Weighting:", font_size=22, color=ORANGE),
            Text("Triangle neighbors: weight 1", font_size=18),
            Text("Non-triangle neighbors: weight 3", font_size=18, color=YELLOW),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        weight_box.next_to(insight_lines, DOWN, buff=0.5, aligned_edge=LEFT)

        with self.voiceover(
            """Triangle centrality weights neighbors differently.
            Neighbors you share a triangle with count less than neighbors
            you do not share a triangle with. Why? Non-triangle neighbors
            represent bridges to other communities. Their triangle
            participation signals connections beyond your local cluster."""
        ):
            self.play(Write(weight_box))
            self.wait(1)

        # Show formula preview
        formula = MathTex(
            r"TC = \frac{3(A \cdot y) - 2(T \cdot y) + y}{k}",
            font_size=32
        ).to_edge(DOWN, buff=0.8)

        formula_label = Text("(we'll break this down next)", font_size=18, color=GRAY)
        formula_label.next_to(formula, DOWN, buff=0.15)

        with self.voiceover(
            """The triangle centrality formula captures this weighting.
            A times y sums all neighbors' triangle counts. T times y
            sums only triangle neighbors' counts. The coefficients
            3 and 2 create the differential weighting. We will break
            down this computation in the next scene."""
        ):
            self.play(Write(formula), Write(formula_label))
            self.wait(1)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(graph),
            FadeOut(count_title),
            FadeOut(count_labels),
            FadeOut(insight_title),
            FadeOut(insight_lines),
            FadeOut(weight_box),
            FadeOut(formula),
            FadeOut(formula_label),
        )
        self.wait(0.5)
