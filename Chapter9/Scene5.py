import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene, create_sparse_matrix


class Scene5(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # --- Voiceover 1: Bias addition ---
        with self.voiceover(
            """After matrix multiply, three operations complete each layer.
            First, bias addition. Multiplying Y by the diagonal bias matrix
            using plus-plus adds negative 0.3 to every active element. Absent
            entries remain absent."""
        ):
            # Before bias: sparse row with string values
            before_data = [[2.5, 0, 1.0, 0.8]]
            before_mat = create_sparse_matrix(before_data, scale=0.7).shift(UP * 1.5)
            before_label = Text("Before bias", font_size=20, color=GRAY).next_to(before_mat, LEFT, buff=0.5)

            arrow1 = MathTex(r"\downarrow", font_size=36).next_to(before_mat, DOWN, buff=0.3)
            bias_text = Text("+(-0.3)", font_size=20, color=YELLOW).next_to(arrow1, RIGHT, buff=0.2)

            after_data = [[2.2, 0, 0.7, 0.5]]
            after_mat = create_sparse_matrix(after_data, scale=0.7).next_to(arrow1, DOWN, buff=0.3)
            after_label = Text("After bias", font_size=20, color=GRAY).next_to(after_mat, LEFT, buff=0.5)

            self.play(FadeIn(before_mat), Write(before_label))
            self.play(Write(arrow1), Write(bias_text))
            self.play(FadeIn(after_mat), Write(after_label))

            code1 = Code(
                code_string="Y << plus_plus(Y @ Bias[layer])",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.65).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(code1))
            self.wait(1)

        self.play(
            FadeOut(before_mat), FadeOut(before_label),
            FadeOut(arrow1), FadeOut(bias_text),
            FadeOut(after_mat), FadeOut(after_label),
            FadeOut(code1),
        )

        # --- Voiceover 2: ReLU via masking ---
        with self.voiceover(
            """Next, ReLU activation. ReLU removes all negative values. In
            GraphBLAS, we build a boolean mask where Y is greater than zero,
            then apply it with replace semantics from Chapter 5. Entries not
            selected by the mask are removed."""
        ):
            # Y after bias with a negative value
            y_data = [[2.2, 0, -0.1, 0.5]]
            y_mat = create_sparse_matrix(y_data, scale=0.7).shift(UP * 2)
            y_label = Text("Y after bias", font_size=20, color=GRAY).next_to(y_mat, LEFT, buff=0.5)
            self.play(FadeIn(y_mat), Write(y_label))

            # Mask
            arrow_m = MathTex(r"\downarrow", font_size=36).next_to(y_mat, DOWN, buff=0.2)
            mask_label = Text("M = (Y > 0)", font_size=20, color=YELLOW).next_to(arrow_m, RIGHT, buff=0.2)

            # Show mask as T/F - use string-based matrix
            mask_entries = VGroup()
            mask_vals = ["T", "", "F", "T"]
            mask_colors = [GREEN, WHITE, RED, GREEN]
            for i, (val, col) in enumerate(zip(mask_vals, mask_colors)):
                if val:
                    t = Text(val, font_size=24, color=col)
                else:
                    t = Text("", font_size=24)
                mask_entries.add(t)
            mask_row = VGroup(*mask_entries).arrange(RIGHT, buff=0.6).next_to(arrow_m, DOWN, buff=0.2)
            mask_brackets = VGroup(
                MathTex("[", font_size=36).next_to(mask_row, LEFT, buff=0.1),
                MathTex("]", font_size=36).next_to(mask_row, RIGHT, buff=0.1),
            )

            self.play(Write(arrow_m), Write(mask_label))
            self.play(FadeIn(mask_row), FadeIn(mask_brackets))

            # Result after masking
            arrow_r = MathTex(r"\downarrow", font_size=36).next_to(mask_row, DOWN, buff=0.3)
            result_data = [[2.2, 0, 0, 0.5]]
            result_mat = create_sparse_matrix(result_data, scale=0.7).next_to(arrow_r, DOWN, buff=0.2)
            result_label = Text("After ReLU", font_size=20, color=GRAY).next_to(result_mat, LEFT, buff=0.5)

            self.play(Write(arrow_r))
            self.play(FadeIn(result_mat), Write(result_label))

            code2 = Code(
                code_string="M << gt(Y, 0)\nY(M.V, replace) << identity(Y)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.6).to_edge(DOWN, buff=0.3)
            self.play(FadeIn(code2))
            self.wait(1)

        self.play(
            FadeOut(y_mat), FadeOut(y_label),
            FadeOut(arrow_m), FadeOut(mask_label),
            FadeOut(mask_row), FadeOut(mask_brackets),
            FadeOut(arrow_r), FadeOut(result_mat), FadeOut(result_label),
            FadeOut(code2),
        )

        # --- Voiceover 3: Clamping ---
        with self.voiceover(
            """Finally, clamping. Any value exceeding 32 is capped at 32,
            preventing numerical overflow across 120 layers. This is the
            element-wise minimum operation."""
        ):
            clamp_before = [[2.2, 0, 35.0, 0.5]]
            clamp_before_mat = create_sparse_matrix(clamp_before, scale=0.7).shift(UP * 1)
            clamp_label = Text("Before clamp", font_size=20, color=GRAY).next_to(clamp_before_mat, LEFT, buff=0.5)

            arrow_c = MathTex(r"\downarrow", font_size=36).next_to(clamp_before_mat, DOWN, buff=0.3)
            clamp_text = Text("min(Y, 32)", font_size=20, color=YELLOW).next_to(arrow_c, RIGHT, buff=0.2)

            clamp_after = [[2.2, 0, 32.0, 0.5]]
            clamp_after_mat = create_sparse_matrix(clamp_after, scale=0.7).next_to(arrow_c, DOWN, buff=0.3)
            clamp_after_label = Text("After clamp", font_size=20, color=GRAY).next_to(clamp_after_mat, LEFT, buff=0.5)

            # Highlight the clamped entry
            self.play(FadeIn(clamp_before_mat), Write(clamp_label))
            self.play(Write(arrow_c), Write(clamp_text))
            self.play(FadeIn(clamp_after_mat), Write(clamp_after_label))

            # Highlight the changed entry (35.0 -> 32.0)
            highlight = SurroundingRectangle(
                clamp_after_mat.get_entries()[2], color=YELLOW, buff=0.05
            )
            self.play(Create(highlight))

            code3 = Code(
                code_string="Y << fmin(Y, 32.0)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.65).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(code3))
            self.wait(1)

        self.play(
            FadeOut(clamp_before_mat), FadeOut(clamp_label),
            FadeOut(arrow_c), FadeOut(clamp_text),
            FadeOut(clamp_after_mat), FadeOut(clamp_after_label),
            FadeOut(highlight), FadeOut(code3),
        )
        self.wait(0.5)
