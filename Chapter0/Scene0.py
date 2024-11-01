from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

class Scene0(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        # Load all logo images from the imgs/ directory
        img_dir = "imgs"
        logo_filenames = [
            "aristotle.png", "anaconda.png", "berkeley.png",
            "cmu.png", "cwi.png", "du.png",
            "graphegon.png", "humboldt.png", "intel.png",
            "imbr.png", "lucata.png", "mit.png",
            "njit.png", "nvidia.png", "pnnl.png",
            "redis.png", "romatre.png", "tamu.png",
            "ucdavis.png", "ucsb.png", "unibz.png",
            "JuliaComputing.jpg"
        ]

        # Create ImageMobject for each logo and scale them uniformly
        logos = [
            ImageMobject(os.path.join(img_dir, filename)).scale(0.5)
            for filename in logo_filenames
        ]

        # Arrange logos in a 4x6 grid using Group
        logos_group = Group(*logos).arrange_in_grid(rows=4, cols=6, buff=0.5)

        # Title text
        title = Tex("Introduction to the GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """Welcome to this introduction to the GraphBLAS Sparse Linear Algebra
            API. In this video series, we’ll explore the basic concepts of
            algebraic graph theory. By the end of this series, you will understand
            how to create new sparse graph algorithms using algebraic operations
            expressed with simple mathematical notation."""
        ):
            self.play(Write(title), FadeIn(logos_group))
            self.wait(2)

        # Footer text
        footer = Text(
            "The GraphBLAS Forum"
        ).scale(0.5).to_edge(DOWN)

        # Display the footer text
        self.play(Write(footer))
        self.wait(2)

        # Fade out title and logos at the end
        self.play(FadeOut(title), FadeOut(logos_group), FadeOut(footer))
        self.wait(0.5)