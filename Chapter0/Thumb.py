import sys
sys.path.insert(0, '..')

from manim import *
from scene_utils import create_logo_grid


class Thumb(Scene):
    def construct(self):
        logos_group = create_logo_grid()

        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        self.play(Write(title), FadeIn(logos_group))
        self.wait(1)
        footer = Text(
            "The GraphBLAS Forum"
        ).scale(0.75).to_edge(DOWN)
        self.play(Write(footer))
        self.wait(1)
