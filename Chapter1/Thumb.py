from manim import *
import os

class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)
        bullet_points = BulletedList(
            "Install Python library",
            "Also reference Julia and Postgres Library.",
            "Give examples to create matrix from Introduction.",
            "Show how to print, plot and draw basic graphs.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        footer = Text(
            "The GraphBLAS Forum"
        ).scale(0.75).to_edge(DOWN)
        self.play(Write(footer))
        self.wait(1)
