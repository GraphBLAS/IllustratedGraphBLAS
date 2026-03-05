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
    KARATE_TOTAL_TRIANGLES,
)


class Scene4(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Title
        title = Text("Karate Club Network", font_size=42).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Stats panel on the left
        stats_title = Text("Network Stats", font_size=28, color=BLUE).to_edge(LEFT, buff=0.5)
        stats_title.shift(UP * 2)

        stat1 = Text("34 members", font_size=22)
        stat2 = Text("78 friendships", font_size=22)
        stat3 = Text("? triangles", font_size=22)

        stats = VGroup(stat1, stat2, stat3).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        stats.next_to(stats_title, DOWN, buff=0.4, aligned_edge=LEFT)

        # Karate graph on the right (larger scale to avoid node overlap)
        graph = create_karate_graph(scale=0.14, node_radius=0.16)
        graph.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)

        with self.voiceover(
            """Let's apply triangle counting to a real social network.
            Zachary's karate club is a classic dataset from 1977. It
            represents friendships among 34 members of a university
            karate club."""
        ):
            self.play(Write(title))
            self.play(Write(stats_title))
            self.play(Write(stat1), Write(stat2))
            self.play(Create(graph))
            self.wait(1)

        # Show triangle count appearing
        stat3_final = Text(f"{KARATE_TOTAL_TRIANGLES} triangles", font_size=22, color=YELLOW)
        stat3_final.move_to(stat3.get_center(), aligned_edge=LEFT)

        with self.voiceover(
            """Running our A squared algorithm on this network, we find
            exactly 45 triangles. These triangles represent tightly
            connected friend groups where everyone knows everyone."""
        ):
            self.play(Write(stat3))
            self.wait(0.5)
            self.play(ReplacementTransform(stat3, stat3_final))
            self.wait(1)

        # Color nodes by triangle count
        with self.voiceover(
            """Now let's visualize triangle participation per member.
            Lighter nodes participate in fewer triangles, while redder
            nodes are embedded in more triangular structures."""
        ):
            node_colors = color_nodes_by_value(
                graph,
                KARATE_TRIANGLE_COUNTS,
                low_color=WHITE,
                high_color=RED
            )
            # Animate all at once for speed
            animations = [animate_vertex_fill(v, c) for v, c in node_colors]
            self.play(*animations, run_time=1.5)
            self.wait(1)

        # Highlight key nodes
        node0_label = Text("Node 0: 18 triangles", font_size=20, color=YELLOW)
        node33_label = Text("Node 33: 15 triangles", font_size=20, color=YELLOW)
        labels_group = VGroup(node0_label, node33_label).arrange(DOWN, buff=0.2)
        labels_group.next_to(stats, DOWN, buff=0.8)

        with self.voiceover(
            """The most connected members stand out clearly. Node 0, the
            club instructor, participates in 18 triangles. Node 33, the
            club president, is in 15. These two are the natural leaders
            and community hubs."""
        ):
            self.play(Write(node0_label))
            # Pulse node 0
            self.play(
                graph.vertices[0].animate.scale(1.4),
                rate_func=there_and_back,
                run_time=0.8
            )
            self.play(Write(node33_label))
            # Pulse node 33
            self.play(
                graph.vertices[33].animate.scale(1.4),
                rate_func=there_and_back,
                run_time=0.8
            )
            self.wait(1)

        # Final insight
        insight = Text(
            "High triangle counts indicate community hubs",
            font_size=24,
            color=GREEN
        ).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            """Triangle counting reveals social structure. Members with
            high triangle counts are embedded in tight-knit groups where
            mutual friendships reinforce connections. This is why triangle
            counting is fundamental in community detection and social
            network analysis."""
        ):
            self.play(Write(insight))
            self.wait(2)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(stats_title),
            FadeOut(stat1),
            FadeOut(stat2),
            FadeOut(stat3_final),
            FadeOut(graph),
            FadeOut(node0_label),
            FadeOut(node33_label),
            FadeOut(insight),
        )
        self.wait(0.5)
