import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene6(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        dnn_code_str = (
            "def DNN(W, Bias, Y):\n"
            "    for layer in range(nlayers):\n"
            "        Y << plus_times(Y @ W[layer])\n"
            "        Y << plus_plus(Y @ Bias[layer])\n"
            "        M << gt(Y, 0)\n"
            "        Y(M.V, replace) << identity(Y)\n"
            "        Y << fmin(Y, 32.0)\n"
            "    return Y"
        )

        # --- Voiceover 1: Show full function ---
        with self.voiceover(
            """Here is the complete forward inference function. It takes weight
            matrices, bias matrices, and the input, then loops over all 120
            layers."""
        ):
            code = Code(
                code_string=dnn_code_str,
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.6)
            self.play(FadeIn(code))
            self.wait(1)

        # --- Voiceover 2: Line-by-line highlighting ---
        with self.voiceover(
            """Line by line: matrix multiply propagates activations through the
            weights. The bias shifts all active values. The mask identifies
            positive values. Replace semantics removes negatives, implementing
            ReLU. And clamping caps values at 32."""
        ):
            # Highlight each code line with annotations
            # Lines of the loop body are code lines 2-6 (0-indexed in the rendered code)
            annotations = [
                "matrix multiply",
                "bias addition",
                "build mask",
                "ReLU masking",
                "clamp to 32",
            ]

            code_lines = code.code_lines
            # The loop body lines are indices 2 through 6
            for i, annotation_text in enumerate(annotations):
                line_idx = i + 2  # lines 2,3,4,5,6 in the code object
                line = code_lines[line_idx]
                rect = SurroundingRectangle(line, color=YELLOW, buff=0.05)
                label = Text(annotation_text, font_size=18, color=YELLOW).next_to(code, RIGHT, buff=0.4)
                label.align_to(line, UP)

                if i == 0:
                    self.play(Create(rect), Write(label))
                else:
                    self.play(
                        Transform(rect, SurroundingRectangle(line, color=YELLOW, buff=0.05)),
                        Transform(label, Text(annotation_text, font_size=18, color=YELLOW).next_to(code, RIGHT, buff=0.4).align_to(line, UP)),
                    )
                self.wait(0.5)

            self.play(FadeOut(rect), FadeOut(label))

        # --- Voiceover 3: Classification step ---
        with self.voiceover(
            """After all layers, we classify each image by reducing rows to
            boolean. The result is compared against ground truth."""
        ):
            self.play(code.animate.shift(UP * 1.5).scale(0.8))

            classify_code = Code(
                code_string="categories = Y.reduce_rows().new(dtype=bool)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.6).next_to(code, DOWN, buff=0.5)
            self.play(FadeIn(classify_code))

            # Schematic: Y -> reduce -> categories -> compare -> accuracy
            pipeline = VGroup(
                Text("Y", font_size=22, color=BLUE),
                MathTex(r"\rightarrow", font_size=28),
                Text("reduce_rows", font_size=18),
                MathTex(r"\rightarrow", font_size=28),
                Text("categories", font_size=18, color=GREEN),
                MathTex(r"\rightarrow", font_size=28),
                Text("compare", font_size=18),
                MathTex(r"\rightarrow", font_size=28),
                Text("accuracy", font_size=22, color=YELLOW),
            ).arrange(RIGHT, buff=0.15).next_to(classify_code, DOWN, buff=0.4)
            self.play(Write(pipeline))
            self.wait(1)

        self.play(FadeOut(code), FadeOut(classify_code), FadeOut(pipeline))
        self.wait(0.5)
