from manim import *


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        subtitle = Text("Semirings", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Generic semiring formula
        formula = MathTex(
            r"c_{ij} = \bigoplus_k a_{ik} \otimes b_{kj}"
        ).scale(1.1)
        formula.move_to(ORIGIN).shift(UP * 0.3)

        # Three example semiring names
        semirings = VGroup(
            Text("PLUS_TIMES", font_size=24, color=BLUE),
            Text("MIN_PLUS", font_size=24, color=RED),
            Text("ANY_PAIR", font_size=24, color=PURPLE),
        ).arrange(RIGHT, buff=0.8)
        semirings.next_to(formula, DOWN, buff=0.6)

        concept = Text("Customizing Matrix Multiplication", font_size=28, color=GREEN)
        concept.next_to(semirings, DOWN, buff=0.6)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(formula))
        self.play(Write(semirings))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
