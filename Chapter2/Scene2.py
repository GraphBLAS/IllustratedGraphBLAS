import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene2(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Title
        title = Text("Semiring Comparison", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)

        # Define small sparse matrices
        matrix_A_data = [
            [2, 0],
            [0, 3]
        ]

        matrix_B_data = [
            [1, 3],
            [2, 0]
        ]

        # Create input matrices
        matrix_A = Matrix(matrix_A_data, v_buff=0.8, h_buff=0.8).scale(0.7)
        matrix_B = Matrix(matrix_B_data, v_buff=0.8, h_buff=0.8).scale(0.7)

        # Hide zeros in A and B
        num_cols_A = len(matrix_A_data[0])
        for i, row in enumerate(matrix_A_data):
            for j, val in enumerate(row):
                if val == 0:
                    entry = matrix_A.get_entries()[i * num_cols_A + j]
                    entry.set_opacity(0)

        num_cols_B = len(matrix_B_data[0])
        for i, row in enumerate(matrix_B_data):
            for j, val in enumerate(row):
                if val == 0:
                    entry = matrix_B.get_entries()[i * num_cols_B + j]
                    entry.set_opacity(0)

        # Labels
        A_label = MathTex("A = ").scale(0.8)
        B_label = MathTex("B = ").scale(0.8)

        # Position input matrices at top
        A_group = VGroup(A_label, matrix_A).arrange(RIGHT, buff=0.3)
        B_group = VGroup(B_label, matrix_B).arrange(RIGHT, buff=0.3)
        input_group = VGroup(A_group, B_group).arrange(RIGHT, buff=1.5).next_to(title, DOWN, buff=0.8)

        # Voiceover block 1: Intro and input matrices
        with self.voiceover(
            """Let's see this in action with the same pair of input matrices."""
        ):
            self.play(Write(title), run_time=0.5)
            self.play(Write(input_group), run_time=1.5)

        # Get reference x-position from matrix A for alignment
        matrix_A_x = matrix_A.get_center()[0]

        # PLUS_TIMES result
        plus_times_label = Text("PLUS_TIMES:", font_size=30, color=GREEN)
        plus_times_label.to_edge(LEFT, buff=0.5)

        result1_data = [[4, 6], [6, 9]]
        matrix_C1 = Matrix(result1_data, v_buff=0.8, h_buff=0.8).scale(0.7)
        C1_label = MathTex("C = ").scale(0.8)
        c1_group = VGroup(C1_label, matrix_C1).arrange(RIGHT, buff=0.3)

        # Position PLUS_TIMES row below input with buffer, align matrix with A
        plus_times_y = input_group.get_bottom()[1] - 1.2
        plus_times_label.set_y(plus_times_y)
        c1_group.set_y(plus_times_y)
        c1_group.set_x(matrix_A_x, direction=ORIGIN)  # Center matrix_C1 on matrix_A x-position

        plus_times_annotation = Text("← total cost", font_size=24, color=BLUE)
        plus_times_annotation.next_to(c1_group, RIGHT, buff=0.5)

        # Voiceover block 2: PLUS_TIMES explanation
        with self.voiceover(
            """Using PLUS_TIMES, we multiply units by cost per unit and sum across products, giving us total production costs."""
        ):
            self.play(Write(plus_times_label), run_time=0.5)
            self.play(Write(c1_group), run_time=1)
            self.play(Write(plus_times_annotation), run_time=0.5)

        # MIN_PLUS result
        min_plus_label = Text("MIN_PLUS:", font_size=30, color=GREEN)
        min_plus_label.to_edge(LEFT, buff=0.5)

        result2_data = [[3, 5], [5, 3]]
        matrix_C2 = Matrix(result2_data, v_buff=0.8, h_buff=0.8).scale(0.7)
        C2_label = MathTex("C = ").scale(0.8)
        c2_group = VGroup(C2_label, matrix_C2).arrange(RIGHT, buff=0.3)

        # Position MIN_PLUS row below PLUS_TIMES with buffer, align matrix with A
        min_plus_y = plus_times_y - 1.5
        min_plus_label.set_y(min_plus_y)
        c2_group.set_y(min_plus_y)
        c2_group.set_x(matrix_A_x, direction=ORIGIN)  # Center matrix_C2 on matrix_A x-position

        min_plus_annotation = Text("← fastest route", font_size=24, color=BLUE)
        min_plus_annotation.next_to(c2_group, RIGHT, buff=0.5)

        # Voiceover block 3: MIN_PLUS explanation
        with self.voiceover(
            """Using MIN_PLUS, we add travel times along each route and keep the minimum, giving us the fastest path."""
        ):
            self.play(Write(min_plus_label), run_time=0.5)
            self.play(Write(c2_group), run_time=1)
            self.play(Write(min_plus_annotation), run_time=0.5)

        # Highlight comparison
        comparison_box1 = SurroundingRectangle(c1_group, color=YELLOW, buff=0.15)
        comparison_box2 = SurroundingRectangle(c2_group, color=YELLOW, buff=0.15)

        # Voiceover block 4: Conclusion
        with self.voiceover(
            """Notice how the operation structure is identical - we're just changing what 'multiply'
            and 'add' mean. This flexibility lets GraphBLAS solve diverse problems with a single, unified interface."""
        ):
            self.play(Create(comparison_box1), Create(comparison_box2), run_time=0.8)
            self.wait(8)

            # Fade out
            self.play(
                FadeOut(title),
                FadeOut(input_group),
                FadeOut(plus_times_label),
                FadeOut(plus_times_annotation),
                FadeOut(c1_group),
                FadeOut(min_plus_label),
                FadeOut(min_plus_annotation),
                FadeOut(c2_group),
                FadeOut(comparison_box1),
                FadeOut(comparison_box2),
                run_time=1
            )

        self.wait(0.5)
