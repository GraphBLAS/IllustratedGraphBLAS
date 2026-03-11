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
            """The GraphBLAS is a sparse linear algebra API—a powerful
            mathematical framework for graph analysis. In this video
            series, we'll explore the basic concepts of algebraic
            graph theory and how it can be used to write portable
            graph algorithms on many different kinds of hardware,
            including CPUs and GPUs. By the end of this series, you
            will understand how to create new parallel graph
            algorithms using simple mathematical notation. GraphBLAS
            was developed by a consortium of researchers from academia
            and industry, and is now an open standard with multiple
            implementations."""
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
            """In this chapter, we'll cover how sparse matrices represent graphs,
            the duality between graphs and matrices, the basics of matrix-vector
            multiplication, and why algebraic approaches to graph algorithms
            are so powerful."""
        ):
            chapter_title = Text("Chapter 0: Introduction to GraphBLAS", font_size=40).to_edge(UP)

            outline = VGroup(
                Text("Sparse matrices and graph representation", font_size=28),
                Text("Graph-matrix duality", font_size=28),
                Text("Matrix-vector multiplication basics", font_size=28),
                Text("Why algebraic graph algorithms", font_size=28),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            outline.next_to(chapter_title, DOWN, buff=0.8)

            self.play(Write(chapter_title))
            self.play(FadeIn(outline))
            self.wait(1)

        # Fade out summary
        self.play(FadeOut(chapter_title), FadeOut(outline))
        self.wait(0.5)
