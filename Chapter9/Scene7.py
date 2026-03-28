import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene7(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Chapter 9 Summary", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Neural network layers are bipartite graphs with sparse weight
            matrices. RadiX-Net generates sparse topologies deterministically.
            Each layer of inference is a sequence of GraphBLAS operations:
            matrix multiply with plus-times, bias addition with plus-plus, ReLU
            masking with replace semantics, and value clamping. Five lines of
            GraphBLAS code implement the entire inference loop."""
        ):
            summary_items = VGroup(
                Text("What we covered:", font_size=32, color=YELLOW),
                Text("1. Neural network layers as bipartite graphs", font_size=24),
                Text("2. Sparse weight matrices vs dense (97% sparse)", font_size=24),
                Text("3. RadiX-Net: deterministic sparse topology", font_size=24),
                Text("4. GraphChallenge benchmark data structure", font_size=24),
                Text("5. Forward inference as GraphBLAS operations", font_size=24),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            summary_items.next_to(title, DOWN, buff=0.4)
            summary_items.to_edge(LEFT, buff=0.8)

            for item in summary_items:
                self.play(Write(item), run_time=0.4)
            self.wait(1)

        # Key operations box
        with self.voiceover(
            """The five core lines map directly to neural network operations:
            plus-times for forward propagation, plus-plus for bias, greater-than
            for mask construction, replace semantics for ReLU, and fmin for
            clamping."""
        ):
            ops_box = VGroup(
                Text("Inference Loop:", font_size=24, color=GREEN),
                Text("Y << plus_times(Y @ W)    # propagate", font_size=18),
                Text("Y << plus_plus(Y @ Bias)  # bias", font_size=18),
                Text("M << gt(Y, 0)             # mask", font_size=18),
                Text("Y(M.V, replace) << id(Y)  # ReLU", font_size=18),
                Text("Y << fmin(Y, 32.0)        # clamp", font_size=18),
            ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            ops_box.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)

            self.play(Write(ops_box))
            self.wait(1)

        self.play(FadeOut(title), FadeOut(summary_items), FadeOut(ops_box))
        self.wait(0.5)
