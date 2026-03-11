import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()
import os

from scene_utils import setup_scene


class Scene0(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Load all logo images from the imgs/ directory
        img_dir = "../imgs"
        logo_filenames = [
            "aristotle.png", "anaconda.png", "berkeley.png",
            "cmu.png", "cwi.png", "du.png",
            "graphegon.png", "humboldt.png", "intel.png",
            "imbr.png", "lucata.png", "mit.png",
            "njit.png", "nvidia.png", "pnnl.png",
            "redis.png", "romatre.png", "tamu.png",
            "ucdavis.png", "ucsb.png", "unibz.png",
            "JuliaComputing.jpg", "falkor.png", "supabase3.png",
        ]

        # Create ImageMobject for each logo and scale them uniformly
        logos = [
            ImageMobject(os.path.join(img_dir, filename)).scale(0.5)
            for filename in logo_filenames
        ]

        # Arrange logos in a 4x6 grid using Group
        logos_group = Group(*logos).arrange_in_grid(rows=4, cols=6, buff=0.5)

        # Title text
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """Neural Networks are the fundamental building blocks of many machine
            learning and artificial intelligence systems.  Sparse
            neural networks offer a powerful approach to building
            neural networks without being constrained by the memory
            limits imposed by dense neural networks.  In this video we
            will show a simple and powerful mathematical technique for
            building sparse neural networks and performing inference
            computations with them."""
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
            """This chapter covers neural networks as graphs, sparse weight
            matrices, forward propagation through layers, and activation
            functions."""
        ):
            chapter_title = Text("Chapter 9: Sparse Neural Networks", font_size=40).to_edge(UP)

            outline = VGroup(
                Text("Neural networks as graphs", font_size=28),
                Text("Sparse weight matrices", font_size=28),
                Text("Forward propagation", font_size=28),
                Text("Activation functions", font_size=28),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            outline.next_to(chapter_title, DOWN, buff=0.8)

            self.play(Write(chapter_title))
            self.play(FadeIn(outline))
            self.wait(1)

        # Fade out summary
        self.play(FadeOut(chapter_title), FadeOut(outline))
        self.wait(0.5)
