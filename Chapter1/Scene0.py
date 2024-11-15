from manim import *

class Scene0(Scene):
    def construct(self):
        num_pairs = 5  # Adjust this to the total number of pairs you have

        for i in range(num_pairs):
            matrix_image = ImageMobject(f"gallery/matrix{i}.jpg").scale(1.5).to_edge(LEFT)
            graph_image = ImageMobject(f"gallery/graph{i}.jpg").scale(1.5).to_edge(RIGHT)

            self.play(FadeIn(matrix_image), FadeIn(graph_image))
            self.wait(1)
            self.play(FadeOut(matrix_image), FadeOut(graph_image))
