import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import create_logo_grid, setup_scene


class Scene0(VoiceoverScene, Scene):
    """Introduction to Matrix-Matrix Multiplication."""

    def construct(self):
        setup_scene(self)

        logos_group = create_logo_grid()

        # Title text
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """In the previous chapters, we used vector-matrix multiply to discover
            neighbors one hop away. But what if we want to find nodes two or three
            hops away? Matrix-matrix multiplication lets us combine multiple
            adjacency matrices to discover multi-hop paths in a single operation.
            In GraphBLAS, we write this as C equals A dot mxm B with a semiring."""
        ):
            self.play(Write(title))
            for logo in logos_group:
                self.play(FadeIn(logo, run_time=0.1))
            footer = Text(
                "The GraphBLAS Forum"
            ).scale(0.75).to_edge(DOWN)
            self.play(Write(footer))

        # Fade out intro elements
        self.play(FadeOut(title), FadeOut(logos_group), FadeOut(footer))
        self.wait(0.5)
