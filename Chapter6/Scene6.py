import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix


# Matrix M with perfect squares: 4, 9, 16, 25, 36
M_DATA = [[0, 4, 9, 0], [0, 0, 16, 0], [0, 0, 0, 25], [36, 0, 0, 0]]

# After M ÷ 2: 2, 4.5, 8, 12.5, 18
HALVED_DATA = [[0, 2, 4.5, 0], [0, 0, 8, 0], [0, 0, 0, 12.5], [18, 0, 0, 0]]


class Scene6(VoiceoverScene, Scene):
    """Apply with right scalar: M ÷ 2."""

    def construct(self):
        setup_scene(self)

        title = Text("Apply: Scalar on Right", font_size=44).to_edge(UP)

        with self.voiceover(
            """Apply with a right scalar places it on the right. We compute M
            divided by 2, halving every value. The scalar 2 is the right operand."""
        ):
            self.play(Write(title))

            # Create original matrix
            mat_m = create_sparse_matrix(M_DATA, scale=0.6)
            mat_m.shift(LEFT * 4.5)
            mat_label = MathTex("M", font_size=36).next_to(mat_m, UP, buff=0.3)

            self.play(FadeIn(mat_m), Write(mat_label))
            self.wait(0.5)

            # Show Python code
            code = Code(
                code_string="M.apply(binary.div, right=2)",
                language="python",
                background="window",
            ).scale(0.7)
            code.move_to(ORIGIN + UP * 0.5)
            self.play(FadeIn(code))
            self.wait(0.5)

        with self.voiceover(
            """Each value is divided: 4 becomes 2, 9 becomes 4.5, 16 becomes 8,
            25 becomes 12.5, and 36 becomes 18. The distinction between left and
            right matters for non-commutative operations. 2 divided by M is very
            different from M divided by 2."""
        ):
            # Create result matrix
            mat_result = create_sparse_matrix(HALVED_DATA, scale=0.6)
            mat_result.shift(RIGHT * 4.5)
            result_label = Text("Result", font_size=24, color=ORANGE)
            result_label.next_to(mat_result, UP, buff=0.3)

            self.play(FadeIn(mat_result), Write(result_label))

            # Animate division for each element
            transformations = [
                ((0, 1), 4, 2),
                ((0, 2), 9, 4.5),
                ((1, 2), 16, 8),
                ((2, 3), 25, 12.5),
                ((3, 0), 36, 18),
            ]

            for (row, col), old_val, new_val in transformations:
                idx = row * 4 + col
                old_entry = mat_m.get_entries()[idx]
                new_entry = mat_result.get_entries()[idx]

                # Animation text
                div_text = MathTex(f"{old_val} \\div 2 = {new_val}", font_size=24, color=ORANGE)
                div_text.move_to(ORIGIN + DOWN * 2)

                # Highlights
                highlight_old = SurroundingRectangle(old_entry, color=YELLOW, buff=0.1)
                highlight_new = SurroundingRectangle(new_entry, color=ORANGE, buff=0.1)

                self.play(
                    Create(highlight_old),
                    Create(highlight_new),
                    Write(div_text),
                    run_time=0.4
                )
                self.wait(0.2)
                self.play(
                    FadeOut(highlight_old),
                    FadeOut(highlight_new),
                    FadeOut(div_text),
                    run_time=0.3
                )

            self.wait(0.5)

            # Show contrast note
            contrast = VGroup(
                MathTex(r"2 \div M", font_size=28, color=RED_C),
                MathTex(r"\neq", font_size=28),
                MathTex(r"M \div 2", font_size=28, color=GREEN),
            ).arrange(RIGHT, buff=0.3)
            contrast.to_edge(DOWN, buff=0.6)

            contrast_note = Text("Order matters for non-commutative ops", font_size=18, color=GRAY)
            contrast_note.next_to(contrast, DOWN, buff=0.2)

            self.play(Write(contrast), Write(contrast_note))
            self.wait(1)

        with self.voiceover(
            """Division also uses Python's natural syntax. M divided by 2 applies
            the scalar on the right, matching the mathematical notation. All common
            Python mathematical operators are supported, making very natural looking
            code possible."""
        ):
            # Transform code to show operator syntax
            code2 = Code(
                code_string="M / 2",
                language="python",
                background="window",
            ).scale(0.7)
            code2.move_to(ORIGIN + UP * 0.5)
            self.play(Transform(code, code2))
            self.wait(0.5)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(mat_m), FadeOut(mat_label),
            FadeOut(code), FadeOut(mat_result), FadeOut(result_label),
            FadeOut(contrast), FadeOut(contrast_note),
        )
        self.wait(0.5)
