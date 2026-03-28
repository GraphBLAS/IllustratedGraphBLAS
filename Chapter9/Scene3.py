import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene, create_sparse_matrix


class Scene3(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # --- Voiceover 1: Weight TSV files ---
        with self.voiceover(
            """The GraphChallenge DNN benchmark provides weight matrices as
            tab-separated files. Each row has a row index, column index, and
            weight value. Indices are one-based, so we subtract one when loading
            into zero-based GraphBLAS matrices."""
        ):
            tsv_code = Code(
                code_string="1\t3\t0.5\n2\t1\t0.3\n3\t3\t0.7\n4\t2\t-0.4",
                language="text",
                background="window",
                formatter_style="dracula",
            ).scale(0.7).shift(LEFT * 3 + UP * 0.5)
            tsv_label = Text("weights.tsv", font_size=20, color=GRAY).next_to(tsv_code, UP, buff=0.2)

            arrow = Arrow(tsv_code.get_right(), tsv_code.get_right() + RIGHT * 1.5, buff=0.2)

            # Small sparse matrix from the TSV data
            w_data = [
                [0, 0, 0.5, 0],
                [0.3, 0, 0, 0],
                [0, 0, 0.7, 0],
                [0, -0.4, 0, 0],
            ]
            w_matrix = create_sparse_matrix(w_data, scale=0.55).next_to(arrow, RIGHT, buff=0.3)
            w_label = MathTex("W", font_size=32).next_to(w_matrix, UP, buff=0.2)

            self.play(FadeIn(tsv_code), Write(tsv_label))
            self.play(GrowArrow(arrow))
            self.play(FadeIn(w_matrix), Write(w_label))

            load_code = Code(
                code_string="W = Matrix.from_tsv(f, nrows=1024, ncols=1024)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.6).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(load_code))
            self.wait(1)

        self.play(
            FadeOut(tsv_code), FadeOut(tsv_label), FadeOut(arrow),
            FadeOut(w_matrix), FadeOut(w_label), FadeOut(load_code),
        )

        # --- Voiceover 2: Bias matrices ---
        with self.voiceover(
            """There are 120 weight matrices, each 1024 by 1024. The bias for
            each layer is a diagonal matrix with negative 0.3 on every diagonal
            entry. Multiplying by a diagonal matrix using plus-plus adds the bias
            to every active element."""
        ):
            # Small diagonal bias matrix
            bias_data = [
                [-0.3, 0, 0, 0],
                [0, -0.3, 0, 0],
                [0, 0, -0.3, 0],
                [0, 0, 0, -0.3],
            ]
            bias_matrix = create_sparse_matrix(bias_data, scale=0.6).shift(UP * 0.5)
            bias_label = Text("Bias (diagonal)", font_size=24).next_to(bias_matrix, UP, buff=0.3)

            self.play(FadeIn(bias_matrix), Write(bias_label))

            equation = MathTex(
                r"Y \times \text{Diag}(-0.3)", r"=", r"Y + (-0.3)",
                font_size=32,
            ).next_to(bias_matrix, DOWN, buff=0.5)
            self.play(Write(equation))
            self.wait(1)

        self.play(FadeOut(bias_matrix), FadeOut(bias_label), FadeOut(equation))

        # --- Voiceover 3: Input images and truth ---
        with self.voiceover(
            """The input is a sparse matrix of 60,000 images with 1024 features
            each. The ground truth is a boolean vector of correct categories."""
        ):
            # Schematic rectangles
            input_rect = Rectangle(width=5, height=2.5, color=BLUE).shift(LEFT * 1.5 + UP * 0.3)
            # Scattered dots inside
            dots = VGroup()
            import random
            random.seed(42)
            for _ in range(30):
                x = random.uniform(-2.3, 2.3) + input_rect.get_center()[0]
                y = random.uniform(-1.0, 1.0) + input_rect.get_center()[1]
                dots.add(Dot(point=[x, y, 0], radius=0.03, color=BLUE_C))

            input_label_top = Text("60,000 images", font_size=20).next_to(input_rect, UP, buff=0.15)
            input_label_side = Text("1024 features", font_size=16).rotate(PI / 2).next_to(input_rect, LEFT, buff=0.15)

            truth_rect = Rectangle(width=0.4, height=2.5, color=GREEN).next_to(input_rect, RIGHT, buff=1.0)
            truth_label = Text("Truth", font_size=20).next_to(truth_rect, UP, buff=0.15)

            self.play(
                Create(input_rect), FadeIn(dots),
                Write(input_label_top), Write(input_label_side),
            )
            self.play(Create(truth_rect), Write(truth_label))
            self.wait(1)

        self.play(
            FadeOut(input_rect), FadeOut(dots),
            FadeOut(input_label_top), FadeOut(input_label_side),
            FadeOut(truth_rect), FadeOut(truth_label),
        )
        self.wait(0.5)
