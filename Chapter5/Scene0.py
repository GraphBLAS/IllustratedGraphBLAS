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
            """This chapter introduces incidence matrices, an alternative
            graph representation using source and destination matrices."""
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
            """We'll learn how source and destination matrices decompose a
            graph's structure, how multiplying S times D recovers the
            adjacency matrix, how this representation naturally handles
            multigraphs with parallel edges, and how hypergraphs model
            complex relationships beyond pairwise connections."""
        ):
            chapter_title = Text("Chapter 5: Incidence Matrices", font_size=40).to_edge(UP)

            outline = VGroup(
                Text("Source and destination matrices", font_size=28),
                Text("S x D = Adjacency", font_size=28),
                Text("Multigraphs (parallel edges)", font_size=28),
                Text("Hypergraphs", font_size=28),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            outline.next_to(chapter_title, DOWN, buff=0.8)

            self.play(Write(chapter_title))
            self.play(FadeIn(outline))
            self.wait(1)

        # Fade out summary
        self.play(FadeOut(chapter_title), FadeOut(outline))
        self.wait(0.5)
