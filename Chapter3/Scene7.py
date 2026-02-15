import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene


class Scene7(VoiceoverScene, Scene):
    """Summary - recap of vxm + masking + replacement = BFS."""

    def construct(self):
        setup_scene(self)

        title = Text("Chapter Summary", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Let's recap what we've learned. We started with vector-matrix
            multiply, the core operation for graph traversal. One algebraic
            operation finds all neighbors of our current frontier."""
        ):
            # Building blocks
            block1 = VGroup(
                Text("1. Vector-Matrix Multiply", font_size=28, color=YELLOW),
                Text("Expand frontier to all neighbors", font_size=22, color=GRAY),
                Code(
                    code_string="w << v.vxm(A, any_pair)",
                    language="python",
                    background="window"
                ).scale(0.5),
            ).arrange(DOWN, buff=0.2)
            block1.next_to(title, DOWN, buff=0.6)

            self.play(Write(block1))
            self.wait(1)

        with self.voiceover(
            """We added masking to control where results are written. The
            complement mask on the levels vector filters to unvisited nodes
            only, preventing redundant work."""
        ):
            block2 = VGroup(
                Text("2. Complement Masking", font_size=28, color=BLUE),
                Text("Write only to unvisited positions", font_size=22, color=GRAY),
                Code(
                    code_string="w(~levels.S) << v.vxm(A, any_pair)",
                    language="python",
                    background="window"
                ).scale(0.5),
            ).arrange(DOWN, buff=0.2)
            block2.next_to(block1, DOWN, buff=0.5)

            self.play(Write(block2))
            self.wait(1)

        with self.voiceover(
            """Finally, replacement semantics ensures the frontier contains
            only current-level nodes. Combined together, these three concepts
            give us a complete, efficient BFS implementation."""
        ):
            block3 = VGroup(
                Text("3. Replacement Semantics", font_size=28, color=GREEN),
                Text("Clear old values, keep only new", font_size=22, color=GRAY),
                Code(
                    code_string="frontier(~levels.S, replace=True) << frontier.vxm(A, any_pair)",
                    language="python",
                    background="window"
                ).scale(0.5),
            ).arrange(DOWN, buff=0.2)
            block3.next_to(block2, DOWN, buff=0.5)

            self.play(Write(block3))
            self.wait(2)

        # Fade out blocks
        self.play(FadeOut(block1), FadeOut(block2), FadeOut(block3))

        with self.voiceover(
            """This pattern, vector-matrix multiply with masking and replacement,
            is a template for many graph algorithms. Single-source shortest path
            uses the same structure with a different semiring. Connected components,
            PageRank, and triangle counting all build on these foundations."""
        ):
            future = VGroup(
                Text("This Pattern Powers:", font_size=32, color=YELLOW),
                Text("• Single-Source Shortest Path (SSSP)", font_size=24),
                Text("• Connected Components", font_size=24),
                Text("• PageRank", font_size=24),
                Text("• Triangle Counting", font_size=24),
                Text("• And many more...", font_size=24, color=GRAY),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(ORIGIN)

            self.play(Write(future))
            self.wait(3)

        self.play(FadeOut(future))

        with self.voiceover(
            """The key insight: by expressing graph algorithms as linear algebra,
            we get composable operations that can be optimized independently.
            The library handles parallelism, memory layout, and hardware
            acceleration. We just specify the computation, and GraphBLAS
            makes it fast."""
        ):
            insight = VGroup(
                Text("The GraphBLAS Philosophy:", font_size=32, color=GREEN),
                Text("Specify WHAT to compute", font_size=26),
                Text("Let the library decide HOW", font_size=26),
            ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

            self.play(Write(insight))
            self.wait(3)

        self.play(FadeOut(title), FadeOut(insight))
        self.wait(0.5)
