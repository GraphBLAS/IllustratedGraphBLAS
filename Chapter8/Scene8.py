import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene8(VoiceoverScene, Scene):
    """Chapter 8 Summary and Chapter 9 Preview."""

    def construct(self):
        setup_scene(self)

        title = Text("Chapter 8 Summary", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Summary points - updated to include triangle centrality
        summary_items = VGroup(
            Text("What we covered:", font_size=32, color=YELLOW),
            Text("1. Triangles: three mutually connected nodes", font_size=24),
            Text("2. A² counts 2-hop paths between nodes", font_size=24),
            Text("3. A² ⊙ A identifies triangle-participating edges", font_size=24),
            Text("4. Sum and divide by 6 for total triangle count", font_size=24),
            Text("5. Row sums give per-node triangle participation", font_size=24),
            Text("6. Triangle centrality weights neighbor contributions", font_size=24),
            Text("7. Different metrics reveal different central nodes", font_size=24),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        summary_items.next_to(title, DOWN, buff=0.4)
        summary_items.to_edge(LEFT, buff=0.8)

        with self.voiceover(
            """Let's review what we covered in this chapter. A triangle is
            three nodes where each pair is connected. Squaring the adjacency
            matrix counts two-hop paths. The element-wise product of A squared
            and A identifies edges in triangles. Summing and dividing by six
            gives the total count. Row sums give per-node participation.
            Triangle centrality weights neighbor contributions differently,
            and we saw how it identifies different central nodes than simple
            triangle counts."""
        ):
            for item in summary_items:
                self.play(Write(item), run_time=0.4)
            self.wait(1)

        # Key formulas box
        formula_box = VGroup(
            Text("Key Formulas:", font_size=24, color=GREEN),
            MathTex(r"\text{triangles} = \frac{\text{sum}(A^2 \odot A)}{6}", font_size=32),
            MathTex(r"TC = \frac{3(Ay) - 2(Ty) + y}{k}", font_size=32),
        ).arrange(DOWN, buff=0.25)
        formula_box.to_edge(RIGHT, buff=1.0).shift(UP * 0.3)

        with self.voiceover(
            """The key formulas: total triangles equals the sum of A squared
            hadamard A, divided by six. Triangle centrality uses a weighted
            combination of neighbor triangle counts, where non-triangle
            neighbors contribute more than triangle neighbors."""
        ):
            self.play(Write(formula_box))
            self.wait(1)

        # Transition to Chapter 9 preview
        self.play(FadeOut(summary_items), FadeOut(formula_box))

        preview_title = Text("Coming in Chapter 9", font_size=36, color=BLUE)
        preview_title.next_to(title, DOWN, buff=0.8)

        preview_items = VGroup(
            Text("Sparse Neural Networks", font_size=28),
            Text("Neural networks as graph operations", font_size=22, color=GRAY),
            Text("Sparse weight matrices for efficiency", font_size=22, color=GRAY),
            Text("GraphBLAS for deep learning inference", font_size=22, color=GRAY),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        preview_items.next_to(preview_title, DOWN, buff=0.5)

        with self.voiceover(
            """In the next chapter, we will explore sparse neural networks.
            Neural network layers can be expressed as matrix operations,
            and when weight matrices are sparse, GraphBLAS provides an
            efficient framework for inference. We will see how the same
            algebraic building blocks we have learned apply to deep learning."""
        ):
            self.play(Write(preview_title))
            for item in preview_items:
                self.play(Write(item), run_time=0.4)
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(preview_title),
            FadeOut(preview_items),
        )
        self.wait(0.5)
