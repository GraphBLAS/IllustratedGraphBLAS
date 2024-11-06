from manim import *
import os

class Thumb(Scene):
    def construct(self):

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

        logos = [
            ImageMobject(os.path.join(img_dir, filename)).scale(0.5)
            for filename in logo_filenames
        ]

        logos_group = Group(*logos).arrange_in_grid(rows=4, cols=6, buff=0.5)

        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        self.play(Write(title), FadeIn(logos_group))
        self.wait(1)
        footer = Text(
            "The GraphBLAS Forum"
        ).scale(0.75).to_edge(DOWN)
        self.play(Write(footer))
        self.wait(1)
