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
            """This chapter covers triangle counting and triangle centrality,
            two metrics that reveal structural patterns in graphs."""
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

        # Chapter summary slide
        with self.voiceover(
            """We'll explore what triangles are in graph theory, the A squared
            hadamard A formula for detecting them, how to compute global and
            per-node triangle counts, and triangle centrality for identifying
            important vertices based on triangle concentration."""
        ):
            chapter_title = Text("Chapter 8: Triangle Counting", font_size=40).to_edge(UP)

            outline = VGroup(
                Text("What is a triangle in graphs", font_size=28),
                Text("A squared hadamard A formula", font_size=28),
                Text("Global triangle count", font_size=28),
                Text("Per-node triangle counts", font_size=28),
                Text("Triangle centrality", font_size=28),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            outline.next_to(chapter_title, DOWN, buff=0.8)

            self.play(Write(chapter_title))
            self.play(FadeIn(outline))
            self.wait(1)

        # Fade out summary
        self.play(FadeOut(chapter_title), FadeOut(outline))
        self.wait(0.5)
