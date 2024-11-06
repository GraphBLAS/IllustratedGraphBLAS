from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Shortest Path Algorithms", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Brief overview of Tropical Geometry, and optimization problems.",
            "Single Source Shortest Path Length example in Python.",
            "Single Source Shortest Path Tree example in Python.",
            "Elements are combined with addition and multiplication from a chosen semiring.",
            "Give some examples of more optmization problems.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
