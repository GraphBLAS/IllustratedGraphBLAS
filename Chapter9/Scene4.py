import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene, create_sparse_matrix


class Scene4(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # --- Voiceover 1: Core mxm step ---
        with self.voiceover(
            """Forward inference processes each layer in sequence. At each layer,
            we multiply the current activations Y by the weight matrix W, using
            the plus-times semiring from Chapter 4."""
        ):
            equation = MathTex(
                r"Y", r"\leftarrow", r"\text{plus\_times}(", r"Y", r"\times", r"W_{layer}", r")",
                font_size=36,
            ).to_edge(UP, buff=0.8)
            self.play(Write(equation))

            # Small worked example: 2x4 Y times 4x4 sparse W -> 2x4 result
            y_data = [
                [1.0, 0, 0.5, 0],
                [0, 0.8, 0, 0.3],
            ]
            w_data = [
                [0, 0.5, 0, 0],
                [0.3, 0, 0, 0],
                [0, 0, 0.7, 0],
                [0, -0.4, 0, 0.6],
            ]
            # Result: row0 = [0, 0.5, 0.35, 0], row1 = [0.24, -0.12, 0, 0.18]
            result_data = [
                [0, 0.5, 0.35, 0],
                [0.24, -0.12, 0, 0.18],
            ]

            y_mat = create_sparse_matrix(y_data, scale=0.5).shift(LEFT * 4.5)
            y_label = MathTex("Y", font_size=28).next_to(y_mat, UP, buff=0.2)

            times = MathTex(r"\times", font_size=36).next_to(y_mat, RIGHT, buff=0.3)

            w_mat = create_sparse_matrix(w_data, scale=0.5).next_to(times, RIGHT, buff=0.3)
            w_label = MathTex("W", font_size=28).next_to(w_mat, UP, buff=0.2)

            equals = MathTex("=", font_size=36).next_to(w_mat, RIGHT, buff=0.3)

            r_mat = create_sparse_matrix(result_data, scale=0.5).next_to(equals, RIGHT, buff=0.3)
            r_label = MathTex("Y'", font_size=28).next_to(r_mat, UP, buff=0.2)

            self.play(FadeIn(y_mat), Write(y_label))
            self.play(Write(times), FadeIn(w_mat), Write(w_label))
            self.play(Write(equals), FadeIn(r_mat), Write(r_label))
            self.wait(1)

        # --- Voiceover 2: Scale context ---
        with self.voiceover(
            """With 60,000 images and 1024 neurons, this is a large sparse matrix
            multiply. Because the weight matrix is sparse, GraphBLAS only computes
            products where both operands have stored values."""
        ):
            self.play(
                FadeOut(y_mat), FadeOut(y_label), FadeOut(times),
                FadeOut(w_mat), FadeOut(w_label), FadeOut(equals),
                FadeOut(r_mat), FadeOut(r_label), FadeOut(equation),
            )

            # Dimension diagram
            dims = VGroup(
                MathTex(r"[60000 \times 1024]", font_size=32, color=BLUE),
                MathTex(r"\times", font_size=32),
                MathTex(r"[1024 \times 1024]", font_size=32, color=GREEN),
                MathTex(r"=", font_size=32),
                MathTex(r"[60000 \times 1024]", font_size=32, color=YELLOW),
            ).arrange(RIGHT, buff=0.3).shift(UP * 1)
            self.play(Write(dims))

            loop_code = Code(
                code_string="for layer in range(nlayers):\n    Y << plus_times(Y @ W[layer])",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7).next_to(dims, DOWN, buff=0.8)
            self.play(FadeIn(loop_code))
            self.wait(1)

        # --- Voiceover 3: Layer pipeline ---
        with self.voiceover(
            """This repeats for all 120 layers. The output of one layer becomes
            the input to the next. But matrix multiply alone is not enough. We
            also need bias addition and activation functions."""
        ):
            self.play(FadeOut(dims), FadeOut(loop_code))

            # Layer pipeline diagram
            pipeline_items = []
            labels = ["Y", "W[0]", "Y", "W[1]", "Y", "...", "W[119]", "Y"]
            for label_text in labels:
                if label_text == "...":
                    item = MathTex(r"\cdots", font_size=28)
                else:
                    item = MathTex(label_text, font_size=24)
                pipeline_items.append(item)

            pipeline = VGroup()
            for i, item in enumerate(pipeline_items):
                pipeline.add(item)
                if i < len(pipeline_items) - 1:
                    pipeline.add(MathTex(r"\rightarrow", font_size=24))

            pipeline.arrange(RIGHT, buff=0.15)
            self.play(Write(pipeline))
            self.wait(1)

        self.play(FadeOut(pipeline))
        self.wait(0.5)
