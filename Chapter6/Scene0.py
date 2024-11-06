from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Page Rank", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Give brief overview of Page Rank.",
            "Show linear algebraic formulation and tie back to fundamentals of design.",
            "Show dense implementation in Python, give disadvantages for large graphs",
            "Show sparse implementation in Python that resolves the issues.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
