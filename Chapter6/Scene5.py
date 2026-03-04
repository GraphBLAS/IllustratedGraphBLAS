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

# After 2 × M: 8, 18, 32, 50, 72
DOUBLED_DATA = [[0, 8, 18, 0], [0, 0, 32, 0], [0, 0, 0, 50], [72, 0, 0, 0]]


class Scene5(VoiceoverScene, Scene):
    """Apply with left scalar: 2 × M."""

    def construct(self):
        setup_scene(self)

        title = Text("Apply: Scalar on Left", font_size=44).to_edge(UP)

        with self.voiceover(
            """Apply can use binary operators with a scalar. Apply with a left
            scalar places it on the left side of the operation. We compute 2 times
            M, doubling every value."""
        ):
            self.play(Write(title))

            # Create original matrix
            mat_m = create_sparse_matrix(M_DATA, scale=0.6)
            mat_m.shift(LEFT * 3)
            mat_label = MathTex("M", font_size=36).next_to(mat_m, UP, buff=0.3)

            self.play(FadeIn(mat_m), Write(mat_label))
            self.wait(0.5)

            # Show formula with highlighted scalar
            formula = MathTex(r"2", r"\times", r"M", font_size=48)
            formula[0].set_color(ORANGE)
            formula.move_to(ORIGIN)

            self.play(Write(formula))
            self.wait(0.5)

            # Emphasize scalar on left
            scalar_note = Text("scalar on left", font_size=18, color=ORANGE)
            scalar_note.next_to(formula[0], DOWN, buff=0.2)
            self.play(Write(scalar_note))
            self.wait(0.5)

        with self.voiceover(
            """Each value is multiplied by 2. 4 becomes 8, 9 becomes 18, 16 becomes
            32, 25 becomes 50, and 36 becomes 72. This scales all edge weights
            uniformly."""
        ):
            # Create result matrix
            mat_result = create_sparse_matrix(DOUBLED_DATA, scale=0.6)
            mat_result.shift(RIGHT * 3)
            result_label = MathTex(r"2 \times M", font_size=36, color=ORANGE)
            result_label.next_to(mat_result, UP, buff=0.3)

            self.play(FadeIn(mat_result), Write(result_label))

            # Animate scalar distributing to each element
            # Show each transformation
            transformations = [
                ((0, 1), 4, 8),
                ((0, 2), 9, 18),
                ((1, 2), 16, 32),
                ((2, 3), 25, 50),
                ((3, 0), 36, 72),
            ]

            # Create a "2 ×" that floats to each entry
            scalar_2 = MathTex("2 \\times", font_size=20, color=ORANGE)

            for (row, col), old_val, new_val in transformations:
                idx = row * 4 + col
                old_entry = mat_m.get_entries()[idx]
                new_entry = mat_result.get_entries()[idx]

                # Animation text
                mult_text = MathTex(f"2 \\times {old_val} = {new_val}", font_size=24, color=ORANGE)
                mult_text.move_to(ORIGIN + DOWN * 2)

                # Highlights
                highlight_old = SurroundingRectangle(old_entry, color=YELLOW, buff=0.1)
                highlight_new = SurroundingRectangle(new_entry, color=ORANGE, buff=0.1)

                self.play(
                    Create(highlight_old),
                    Create(highlight_new),
                    Write(mult_text),
                    run_time=0.4
                )
                self.wait(0.2)
                self.play(
                    FadeOut(highlight_old),
                    FadeOut(highlight_new),
                    FadeOut(mult_text),
                    run_time=0.3
                )

            self.wait(0.5)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(mat_m), FadeOut(mat_label),
            FadeOut(formula), FadeOut(scalar_note),
            FadeOut(mat_result), FadeOut(result_label),
        )
        self.wait(0.5)
