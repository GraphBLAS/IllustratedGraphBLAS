from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Shortest Path Algorithms", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Generalizes matrix multiplication to non-standard operations",
            "Used in graph algorithms like shortest paths and connectivity",
            "Elements are combined with addition and multiplication from a chosen semiring",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
