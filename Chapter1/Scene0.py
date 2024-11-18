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
            """In this video, you will learn how to install and use the Python
            GraphBLAS library, which will be used throughout the rest
            of the video series for code examples.  It's not necessary
            to install Python or use the library for understanding the
            basic concepts of the GraphBLAS, so you can skip this
            video and move onto the next chapter if you want to get
            straight to the concepts.  """
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
