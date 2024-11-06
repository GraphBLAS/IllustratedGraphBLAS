from manim import *

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Sparse Neural Networks", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "Neural Network introduction and theory.",
            "Network Networks are often dense adjacencies for simplicity and direct mapping to parallel hardware.",
            "Sparse NN has advantages of similar or better results with less memory and resources",
            "Sparse NN can be created *de novo* avoiding being limited by dense boundaries.",
            "Give implementation example in Python of Radix-Net and show algebraic interpretation.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
