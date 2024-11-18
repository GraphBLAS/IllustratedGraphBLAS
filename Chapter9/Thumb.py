from manim import *
import os

class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)
        bullet_points = BulletedList(
            "Sparse Neural Networks.",
            "Introduce sparse vs dense tradeoffs.",
            "Introduce Radix-Net concepts.",
            "Radix-Net construction algorithms.",
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
