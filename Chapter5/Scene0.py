from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Triangle Counting and Centrality", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Triangle are an important structure in graphs.",
            "Show various examples of counting triangles in Python, give explanation.",
            "Show how Triangle Centrality with example in Python.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
