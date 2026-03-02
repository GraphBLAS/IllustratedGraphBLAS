from manim import *


class Thumb(Scene):
    def construct(self):
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        # Chapter subtitle
        subtitle = Text("Matrix-Matrix Multiply", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Two small matrices with @ symbol
        A_mat = Matrix([
            ["", "1", ""],
            ["1", "", "1"],
            ["", "1", ""],
        ], v_buff=0.5, h_buff=0.5).scale(0.6)

        at_sym = MathTex("@").scale(1.2)

        B_mat = Matrix([
            ["", "1", ""],
            ["1", "", "1"],
            ["", "1", ""],
        ], v_buff=0.5, h_buff=0.5).scale(0.6)

        equals_sym = MathTex("=").scale(1.2)

        # Result (A^2)
        C_mat = Matrix([
            ["2", "", "2"],
            ["", "2", ""],
            ["2", "", "2"],
        ], v_buff=0.5, h_buff=0.5).scale(0.6)

        equation = VGroup(A_mat, at_sym, B_mat, equals_sym, C_mat).arrange(RIGHT, buff=0.3)
        equation.move_to(ORIGIN)

        # Labels
        A_label = MathTex("A").next_to(A_mat, DOWN, buff=0.2)
        B_label = MathTex("A").next_to(B_mat, DOWN, buff=0.2)
        C_label = MathTex("A^2").next_to(C_mat, DOWN, buff=0.2)

        labels = VGroup(A_label, B_label, C_label)

        # Key concept text
        concept = Text("Multi-hop Path Discovery", font_size=28, color=GREEN)
        concept.next_to(equation, DOWN, buff=0.8)

        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(equation), Write(labels))
        self.play(Write(concept))
        self.play(Write(footer))
        self.wait(1)
