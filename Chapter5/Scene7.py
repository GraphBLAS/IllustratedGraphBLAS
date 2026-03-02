import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene7(VoiceoverScene, Scene):
    """Summary and Chapter 6 Teaser."""

    def construct(self):
        setup_scene(self)

        title = Text("Chapter Summary", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Let us recap what we have covered in this chapter. We introduced
            a new way to represent graphs using two incidence matrices: S for
            sources and D for destinations. Unlike adjacency matrices that
            are square, these matrices are rectangular, with edges as one
            dimension."""
        ):
            block1 = VGroup(
                Text("1. Two-Matrix Representation", font_size=26, color=YELLOW),
                MathTex(r"S: n \times m \text{ (nodes × edges)}", font_size=22),
                MathTex(r"D: m \times n \text{ (edges × nodes)}", font_size=22),
            ).arrange(DOWN, buff=0.2)
            block1.next_to(title, DOWN, buff=0.6)

            self.play(Write(block1))
            self.wait(1)

        with self.voiceover(
            """The fundamental relationship is that S times D equals the
            adjacency matrix. The intermediate dimension, representing edges,
            disappears in the multiplication, leaving us with the familiar
            node-to-node connectivity."""
        ):
            block2 = VGroup(
                Text("2. Multiplication Gives Adjacency", font_size=26, color=GREEN),
                MathTex(r"S \times D = A", font_size=28, color=GREEN),
                Text("Edges cancel, nodes remain", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            block2.next_to(block1, DOWN, buff=0.4)

            self.play(Write(block2))
            self.wait(1)

        with self.voiceover(
            """The key advantage of this representation is that each edge
            maintains its own identity as a column in S and a row in D.
            This enables multi-graphs where parallel edges remain distinct,
            and hypergraphs where edges can connect more than two nodes."""
        ):
            block3 = VGroup(
                Text("3. Edge Identity Preserved", font_size=26, color=BLUE),
                Text("Multi-graphs: parallel edges stay separate", font_size=18, color=GRAY),
                Text("Hypergraphs: edges connect >2 nodes", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            block3.next_to(block2, DOWN, buff=0.4)

            self.play(Write(block3))
            self.wait(2)

        # Fade out blocks
        self.play(FadeOut(block1), FadeOut(block2), FadeOut(block3))

        with self.voiceover(
            """We also explored applications. Path composition through repeated
            multiplication. Edge-to-edge adjacency via D times S, revealing
            which edges share nodes. And bipartite graphs, where the source
            and destination node sets are disjoint."""
        ):
            applications = VGroup(
                Text("Applications:", font_size=28, color=YELLOW),
                VGroup(
                    MathTex(r"A^2 = S \times D \times S \times D", font_size=22),
                    Text("Two-hop paths", font_size=16, color=GRAY),
                ).arrange(RIGHT, buff=0.5),
                VGroup(
                    MathTex(r"D \times S", font_size=22),
                    Text("Edge-to-edge adjacency", font_size=16, color=GRAY),
                ).arrange(RIGHT, buff=0.5),
                Text("Bipartite graphs: natural S/D structure", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            applications.move_to(ORIGIN)

            self.play(Write(applications))
            self.wait(3)

        self.play(FadeOut(applications))

        # Key insight
        with self.voiceover(
            """The key insight is that the two-matrix factorization gives edges
            first-class status. Instead of edges being implicit connections
            between nodes, they become explicit entities with their own
            dimension in the algebra. This expands what GraphBLAS can represent
            while using the same matrix operations."""
        ):
            insight = VGroup(
                Text("Key Insight:", font_size=32, color=YELLOW),
                Text("Edges as first-class entities", font_size=24),
                Text("Same operations, richer structures", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.3)
            insight.move_to(ORIGIN)

            self.play(Write(insight))
            self.wait(3)

        self.play(FadeOut(insight))

        # Chapter 6 teaser
        with self.voiceover(
            """In the next chapter, we turn to element-wise operations. While
            matrix multiplication combines entire rows and columns,
            element-wise operations work position by position. We will see
            how to compute graph unions, intersections, and apply masks to
            filter edges based on conditions."""
        ):
            teaser = VGroup(
                Text("Next: Element-wise Operations", font_size=32, color=GREEN),
                Text("Union and intersection of graphs", font_size=20, color=GRAY),
                Text("Element-wise multiply (eWiseMult)", font_size=20, color=GRAY),
                Text("Masking and filtering edges", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.3)
            teaser.move_to(ORIGIN)

            self.play(Write(teaser))
            self.wait(3)

        with self.voiceover(
            """Where matrix multiplication asks which nodes connect through
            intermediate nodes, element-wise operations ask which edges exist
            in both graphs, or in either graph. These complement each other
            in the GraphBLAS toolkit."""
        ):
            comparison = VGroup(
                Text("Matrix multiply: path connectivity", font_size=20, color=BLUE),
                Text("Element-wise: edge-by-edge operations", font_size=20, color=GREEN),
            ).arrange(DOWN, buff=0.3)
            comparison.to_edge(DOWN, buff=0.8)

            self.play(Write(comparison))
            self.wait(3)

        # Final summary equation
        with self.voiceover(
            """Remember the core equation: A equals S times D. This simple
            factorization opens up multi-graphs, hypergraphs, and edge-centric
            analysis, all within the linear algebraic framework we have been
            building throughout this series."""
        ):
            self.play(FadeOut(teaser), FadeOut(comparison))

            final_eq = MathTex(r"A = S \times D", font_size=48, color=YELLOW)
            final_eq.move_to(ORIGIN)

            self.play(Write(final_eq))
            self.wait(2)

        self.play(FadeOut(title), FadeOut(final_eq))
        self.wait(0.5)
