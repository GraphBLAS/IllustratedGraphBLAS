from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Matrix Multiplication over Semirings", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Describe matrix multiplication operations in common terms, plus times.",
            "Describe how plus\_times is one of infinite semirings, many useful for graphs.",
            "Explain how structural graph problems don't need values at all, so more efficient semirings can be used.",
            "Give teaser for several algorithms in upcoming videos.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
