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
            """This chapter builds a complete breadth-first search
            implementation using GraphBLAS operations."""
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
            """We'll explore vector-matrix and matrix-vector multiply for
            graph traversal, masking to control which outputs are written,
            complement masks for selecting unvisited nodes, and replacement
            semantics for managing the frontier between iterations. By the
            end, these concepts combine into an efficient BFS algorithm."""
        ):
            chapter_title = Text("Chapter 3: BFS Implementation", font_size=40).to_edge(UP)

            outline = VGroup(
                Text("Matrix-vector multiply (vxm)", font_size=28),
                Text("Vector-matrix multiply (vxm)", font_size=28),
                Text("Masking to control output", font_size=28),
                Text("Complement masks", font_size=28),
                Text("Replacement semantics", font_size=28),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            outline.next_to(chapter_title, DOWN, buff=0.8)

            self.play(Write(chapter_title))
            self.play(FadeIn(outline))
            self.wait(1)

        # Fade out summary
        self.play(FadeOut(chapter_title), FadeOut(outline))
        self.wait(0.5)
