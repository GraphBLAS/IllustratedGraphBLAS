from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Placeholder", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "TBD",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
