from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Applying Operators and Selecting Values", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Apply a function to all elements in a graph, transforming it.",
            "Show how selection can choose elements that match a criteria.",
            "Give an example of apply in an algorithm in Python.",
            "Give an example of select in an algorithm in Python.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
