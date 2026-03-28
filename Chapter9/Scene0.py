import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import create_logo_grid, setup_scene


class Scene0(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        logos_group = create_logo_grid()

        # Title text
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """This chapter explores how sparse neural networks can be computed
            using GraphBLAS. The same matrix operations we have used for graph
            algorithms turn out to be the building blocks for deep learning
            inference."""
        ):
            self.play(Write(title))
            for logo in logos_group:
                self.play(FadeIn(logo, run_time=0.1))
            footer = Text(
                "The GraphBLAS Forum"
            ).scale(0.75).to_edge(DOWN)
            self.play(Write(footer))

        # Fade out title and logos at the end
        self.play(FadeOut(title), FadeOut(logos_group), FadeOut(footer))

        # Chapter outline slide
        with self.voiceover(
            """We will see how neural network layers map to bipartite graphs
            and weight matrices, why sparse networks overcome the memory limits
            of dense models, how the GraphChallenge benchmark structures its data,
            and how the forward inference function works as a sequence of
            GraphBLAS operations."""
        ):
            chapter_title = Text("Chapter 9: Sparse Deep Neural Network Inference", font_size=36).to_edge(UP)

            outline = VGroup(
                Text("Neural networks as bipartite graphs", font_size=28),
                Text("Dense vs sparse weight matrices", font_size=28),
                Text("GraphChallenge data structure", font_size=28),
                Text("Forward inference with GraphBLAS", font_size=28),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            outline.next_to(chapter_title, DOWN, buff=0.8)

            self.play(Write(chapter_title))
            self.play(FadeIn(outline))
            self.wait(1)

        # Fade out summary
        self.play(FadeOut(chapter_title), FadeOut(outline))
        self.wait(0.5)
