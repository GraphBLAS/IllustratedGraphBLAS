from manim import *
import scipy.optimize

class Scene0(Scene):
    def construct(self):
        # Title
        title = Text("Breadth First Search", font_size=48).to_edge(UP)

        bullet_points = BulletedList(
            "The primary algorithm for graph analysis is Breadth First Search.",
            "Give an example of how it differs from Depth First Search.",
            "Show how DFS is inherently serial, where BFS can be parallelized",
            "Compare and contrast procedural BFS algorithms to Linear Algebra",
            "Explain problems parallelizing procedural code, including architectural considerations (CUDA, etc)",
            "Explain how Linear Algebra abstracts away the need to consider parallelization.",
            font_size=36
        )
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
        self.wait(2)
