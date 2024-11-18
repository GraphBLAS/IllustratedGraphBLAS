from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

class Scene0(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

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
            """Triangles are a graph structure where three nodes are all connected
            to each other.  This is a fundamental building block in
            breaking down graphs for analysis and processing.  In this
            video, we will go over several algebraic approaches to
            triangle counting and show a powerful algorithm for
            determining the centrality ranking of nodes in a graph
            based on the number of triangles around them. """
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
        self.wait(0.5)
