import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    setup_scene,
    create_karate_graph,
    color_nodes_by_value,
    animate_vertex_fill,
    KARATE_TRIANGLE_COUNTS,
    KARATE_TRIANGLE_CENTRALITY,
)


class Scene7(VoiceoverScene, Scene):
    """Karate Club Triangle Centrality - comparing metrics."""

    def construct(self):
        setup_scene(self)

        # Title
        title = Text("Triangle Centrality: Karate Club", font_size=42).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Create two graphs side by side
        graph_left = create_karate_graph(scale=0.11, node_radius=0.14)
        graph_right = create_karate_graph(scale=0.11, node_radius=0.14)

        graph_left.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        graph_right.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)

        # Labels
        label_left = Text("Triangle Count", font_size=24, color=RED)
        label_left.next_to(graph_left, UP, buff=0.3)

        label_right = Text("Triangle Centrality", font_size=24, color=BLUE)
        label_right.next_to(graph_right, UP, buff=0.3)

        with self.voiceover(
            """Let's compare triangle count and triangle centrality on
            the karate club network. On the left, nodes are colored by
            their per-node triangle count. On the right, we will show
            triangle centrality scores."""
        ):
            self.play(Write(label_left), Write(label_right))
            self.play(Create(graph_left), Create(graph_right))
            self.wait(1)

        # Color left graph by triangle count
        left_colors = color_nodes_by_value(
            graph_left,
            KARATE_TRIANGLE_COUNTS,
            low_color=WHITE,
            high_color=RED
        )

        # Color right graph by triangle centrality
        tc_list = [KARATE_TRIANGLE_CENTRALITY[i] for i in range(34)]
        right_colors = color_nodes_by_value(
            graph_right,
            tc_list,
            low_color=WHITE,
            high_color=BLUE
        )

        with self.voiceover(
            """Now let's color both graphs. The left uses triangle counts
            where red indicates more triangles. The right uses triangle
            centrality where blue indicates higher centrality."""
        ):
            # Color both simultaneously
            left_anims = [animate_vertex_fill(v, c) for v, c in left_colors]
            right_anims = [animate_vertex_fill(v, c) for v, c in right_colors]
            self.play(*left_anims, *right_anims, run_time=1.5)
            self.wait(1)

        # Highlight key differences
        # Node 0: highest triangle count (18), but not highest centrality
        # Node 13: only 6 triangles, but HIGHEST centrality (0.756)

        diff_title = Text("Key Differences", font_size=28, color=YELLOW)
        diff_title.move_to(ORIGIN).shift(UP * 0.5)

        diff1 = Text("Node 13: 6 triangles, but HIGHEST centrality", font_size=20)
        diff2 = Text("Node 0: 18 triangles, but rank 2 in centrality", font_size=20)
        diff3 = Text("Node 32: 13 triangles, but only 0.47 centrality", font_size=20)
        diffs = VGroup(diff1, diff2, diff3).arrange(DOWN, buff=0.15)
        diffs.next_to(diff_title, DOWN, buff=0.3)

        with self.voiceover(
            """The rankings differ significantly. Node 13 has only 6
            triangles but the highest centrality score. Node 0 has the
            most triangles at 18, but ranks second in centrality. Node
            32 has 13 triangles but a moderate centrality of 0.47."""
        ):
            self.play(Write(diff_title))
            self.play(Write(diff1))
            # Pulse node 13 on both graphs
            self.play(
                graph_left.vertices[13].animate.scale(1.5),
                graph_right.vertices[13].animate.scale(1.5),
                rate_func=there_and_back,
                run_time=0.8
            )
            self.play(Write(diff2))
            # Pulse node 0
            self.play(
                graph_left.vertices[0].animate.scale(1.5),
                graph_right.vertices[0].animate.scale(1.5),
                rate_func=there_and_back,
                run_time=0.8
            )
            self.play(Write(diff3))
            self.wait(1)

        self.play(FadeOut(diff_title), FadeOut(diffs))

        # Explanation panel
        explain_title = Text("Why Node 13?", font_size=28, color=GREEN)
        explain_title.move_to(ORIGIN).shift(UP * 0.5)

        explain_lines = VGroup(
            Text("Node 13 connects groups 0-3 and 33", font_size=20),
            Text("Its non-triangle neighbors are in many triangles", font_size=20),
            Text("It bridges highly-triangulated communities", font_size=20),
        ).arrange(DOWN, buff=0.15)
        explain_lines.next_to(explain_title, DOWN, buff=0.3)

        with self.voiceover(
            """Why does node 13 rank highest? Looking at the network,
            node 13 connects the instructor's group around node 0 with
            other parts of the club. Its non-triangle neighbors participate
            in many triangles. Node 13 acts as a bridge between
            highly-triangulated communities, which the centrality formula
            rewards."""
        ):
            self.play(Write(explain_title))
            for line in explain_lines:
                self.play(Write(line), run_time=0.4)
            # Pulse node 13 again
            self.play(
                graph_left.vertices[13].animate.scale(1.5),
                graph_right.vertices[13].animate.scale(1.5),
                rate_func=there_and_back,
                run_time=0.8
            )
            self.wait(1)

        self.play(FadeOut(explain_title), FadeOut(explain_lines))

        # Top 5 comparison table
        top5_title = Text("Top 5 by Each Metric", font_size=24)
        top5_title.move_to(ORIGIN).shift(UP * 0.3)

        # Triangle count top 5: 0(18), 33(15), 32(13), 1(12), 2(11)
        # TC top 5: 13(0.76), 0(0.67), 31(0.65), 2(0.64), 9(0.58)
        tc_top = VGroup(
            Text("Triangle Count", font_size=18, color=RED),
            Text("0: 18", font_size=16),
            Text("33: 15", font_size=16),
            Text("32: 13", font_size=16),
            Text("1: 12", font_size=16),
            Text("2: 11", font_size=16),
        ).arrange(DOWN, buff=0.1)

        cent_top = VGroup(
            Text("Centrality", font_size=18, color=BLUE),
            Text("13: 0.76", font_size=16),
            Text("0: 0.67", font_size=16),
            Text("31: 0.65", font_size=16),
            Text("2: 0.64", font_size=16),
            Text("9: 0.58", font_size=16),
        ).arrange(DOWN, buff=0.1)

        tables = VGroup(tc_top, cent_top).arrange(RIGHT, buff=1.5)
        tables.next_to(top5_title, DOWN, buff=0.3)

        with self.voiceover(
            """Comparing the top 5 by each metric: by triangle count,
            nodes 0, 33, 32, 1, and 2 lead. By centrality, nodes 13,
            0, 31, 2, and 9 lead. Only nodes 0 and 2 appear in both
            top 5 lists. Triangle centrality identifies different
            important vertices."""
        ):
            self.play(Write(top5_title))
            self.play(Write(tc_top), Write(cent_top))
            self.wait(1)

        # Final insight
        insight = Text(
            "Different metrics reveal different aspects of importance",
            font_size=22,
            color=GREEN
        ).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            """The key takeaway: different metrics reveal different aspects
            of importance. Triangle counts show direct participation.
            Triangle centrality identifies nodes that concentrate or
            bridge triangulated structures. Both are useful depending
            on what you want to measure."""
        ):
            self.play(Write(insight))
            self.wait(1)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(label_left),
            FadeOut(label_right),
            FadeOut(graph_left),
            FadeOut(graph_right),
            FadeOut(top5_title),
            FadeOut(tables),
            FadeOut(insight),
        )
        self.wait(0.5)
