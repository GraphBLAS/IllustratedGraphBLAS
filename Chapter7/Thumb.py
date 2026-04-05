from manim import *


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Shortest Paths", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Bellman-Ford relaxation equation
        formula = MathTex(
            r"d_j = \min_k \left( d_k + w_{kj} \right)"
        ).scale(1.0)
        formula.move_to(ORIGIN).shift(UP * 0.3)

        # Semiring name
        semiring_label = Text("MIN_PLUS Semiring", font_size=26, color=ORANGE)
        semiring_label.next_to(formula, DOWN, buff=0.4)

        # Distance vector evolution example
        before = MathTex(r"d = [0, \cdot, \cdot, 2, \cdot, \cdot]").scale(0.7)
        arrow = MathTex(r"\rightarrow").scale(0.8)
        after = MathTex(r"d = [0, 1, \cdot, 2, 4, 3]").scale(0.7)
        iteration = VGroup(before, arrow, after).arrange(RIGHT, buff=0.3)
        iteration.next_to(semiring_label, DOWN, buff=0.4)

        concept = Text("Tropical Semiring for Optimization", font_size=28, color=GREEN)
        concept.next_to(iteration, DOWN, buff=0.6)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(formula))
        self.play(Write(semiring_label))
        self.play(Write(iteration))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
