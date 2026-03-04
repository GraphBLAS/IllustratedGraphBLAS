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

# After sqrt: 2, 3, 4, 5, 6
SQRT_DATA = [[0, 2, 3, 0], [0, 0, 4, 0], [0, 0, 0, 5], [6, 0, 0, 0]]


class Scene4(VoiceoverScene, Scene):
    """Apply: Unary transformation with sqrt."""

    def construct(self):
        setup_scene(self)

        title = Text("Apply: Unary Transformation", font_size=44).to_edge(UP)

        with self.voiceover(
            """Apply transforms each matrix element using a function. This matrix
            M contains perfect squares: 4, 9, 16, 25, and 36. We apply the square
            root function."""
        ):
            self.play(Write(title))

            # Create original matrix
            mat_m = create_sparse_matrix(M_DATA, scale=0.6)
            mat_m.shift(LEFT * 3)
            mat_label = MathTex("M", font_size=36).next_to(mat_m, UP, buff=0.3)

            self.play(FadeIn(mat_m), Write(mat_label))
            self.wait(0.5)

            # Show formula
            formula = MathTex(r"\sqrt{M}", font_size=48, color=GREEN)
            formula.move_to(ORIGIN)
            self.play(Write(formula))
            self.wait(0.5)

        with self.voiceover(
            """Apply visits each stored value. 4 becomes 2, 9 becomes 3, 16 becomes
            4, 25 becomes 5, and 36 becomes 6. The sparsity structure is preserved;
            apply only transforms existing values."""
        ):
            # Create result matrix
            mat_result = create_sparse_matrix(SQRT_DATA, scale=0.6)
            mat_result.shift(RIGHT * 3)
            result_label = MathTex(r"\sqrt{M}", font_size=36, color=GREEN)
            result_label.next_to(mat_result, UP, buff=0.3)

            # Animate sqrt transformation for each non-zero entry
            # Positions: (0,1)=4, (0,2)=9, (1,2)=16, (2,3)=25, (3,0)=36
            transformations = [
                ((0, 1), 4, 2),
                ((0, 2), 9, 3),
                ((1, 2), 16, 4),
                ((2, 3), 25, 5),
                ((3, 0), 36, 6),
            ]

            # First show the result matrix structure
            self.play(FadeIn(mat_result), Write(result_label))

            # Animate each transformation with sqrt symbol
            for (row, col), old_val, new_val in transformations:
                idx = row * 4 + col  # 4 columns
                old_entry = mat_m.get_entries()[idx]
                new_entry = mat_result.get_entries()[idx]

                # Create sqrt animation text
                sqrt_text = MathTex(f"\\sqrt{{{old_val}}} = {new_val}", font_size=24, color=GREEN)
                sqrt_text.move_to(ORIGIN + DOWN * 2)

                # Highlight transformation
                highlight_old = SurroundingRectangle(old_entry, color=YELLOW, buff=0.1)
                highlight_new = SurroundingRectangle(new_entry, color=GREEN, buff=0.1)

                self.play(
                    Create(highlight_old),
                    Create(highlight_new),
                    Write(sqrt_text),
                    run_time=0.5
                )
                self.wait(0.3)
                self.play(
                    FadeOut(highlight_old),
                    FadeOut(highlight_new),
                    FadeOut(sqrt_text),
                    run_time=0.3
                )

            # Show "structure preserved" note
            note = Text("Sparsity structure preserved", font_size=20, color=GRAY)
            note.to_edge(DOWN, buff=0.5)
            self.play(Write(note))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(mat_m), FadeOut(mat_label),
            FadeOut(formula), FadeOut(mat_result), FadeOut(result_label),
            FadeOut(note),
        )
        self.wait(0.5)
