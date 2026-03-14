import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix, create_square_digraph


# Shared data from notebook
# Graph A: edges (0→1), (1→2), (2→3)
A_DATA = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]

# Graph B: edges (1→2), (2→3), (3→0)
B_DATA = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]

# Intersection result: edges (1→2), (2→3) only
INTERSECTION_DATA = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]


class Scene2(VoiceoverScene, Scene):
    """Element-wise Multiply: Intersection of two graphs."""

    def construct(self):
        setup_scene(self)

        title = Text("Element-wise Multiply: Intersection", font_size=44).to_edge(UP)

        with self.voiceover(
            """Element-wise multiply computes the intersection. An edge appears only
            if it exists in both inputs. Using the same graphs A and B, eWiseMult
            keeps only the common edges."""
        ):
            self.play(Write(title))

            # Create Graph A (left, blue)
            graph_a = create_square_digraph(A_DATA, BLUE)
            graph_a.scale(1.2).shift(LEFT * 4 + DOWN * 0.5)
            label_a = Text("Graph A", font_size=24, color=BLUE).next_to(graph_a, UP)

            # Create matrix A below graph
            mat_a = create_sparse_matrix(A_DATA, scale=0.5)
            mat_a.next_to(graph_a, DOWN, buff=0.5)

            # Create Graph B (right, green)
            graph_b = create_square_digraph(B_DATA, GREEN)
            graph_b.scale(1.2).shift(RIGHT * 4 + DOWN * 0.5)
            label_b = Text("Graph B", font_size=24, color=GREEN).next_to(graph_b, UP)

            # Create matrix B below graph
            mat_b = create_sparse_matrix(B_DATA, scale=0.5)
            mat_b.next_to(graph_b, DOWN, buff=0.5)

            self.play(
                Create(graph_a), Write(label_a), FadeIn(mat_a),
                Create(graph_b), Write(label_b), FadeIn(mat_b),
            )
            self.wait(1)

        with self.voiceover(
            """The result contains just two edges: 1 to 2 and 2 to 3, each with
            value 1 times 1 equals 1. Contrast this with union which gave us four
            edges. Intersection keeps only what both graphs share."""
        ):
            # Show Python code below title
            code = Code(
                code_string="A.ewise_mult(B, binary.times)",
                language="python",
                background="window",
            ).scale(0.7)
            code.next_to(title, DOWN, buff=0.3)
            self.play(FadeIn(code))
            self.wait(0.5)

            # Highlight common edges and fade unique ones
            # Track which edges to keep vs fade
            edges_to_fade_a = VGroup()
            edges_to_keep_a = VGroup()
            for edge in graph_a.edges:
                start = edge.get_start()
                end = edge.get_end()
                start_node = self.get_nearest_node(start)
                end_node = self.get_nearest_node(end)
                if (start_node, end_node) in [(1, 2), (2, 3)]:
                    edges_to_keep_a.add(edge)
                else:
                    edges_to_fade_a.add(edge)

            edges_to_fade_b = VGroup()
            edges_to_keep_b = VGroup()
            for edge in graph_b.edges:
                start = edge.get_start()
                end = edge.get_end()
                start_node = self.get_nearest_node(start)
                end_node = self.get_nearest_node(end)
                if (start_node, end_node) in [(1, 2), (2, 3)]:
                    edges_to_keep_b.add(edge)
                else:
                    edges_to_fade_b.add(edge)

            # Highlight common, then fade unique
            self.play(
                *[edge.animate.set_color(YELLOW).set_stroke(width=5) for edge in edges_to_keep_a],
                *[edge.animate.set_color(YELLOW).set_stroke(width=5) for edge in edges_to_keep_b],
            )
            self.wait(0.5)

            self.play(
                *[edge.animate.set_opacity(0.2) for edge in edges_to_fade_a],
                *[edge.animate.set_opacity(0.2) for edge in edges_to_fade_b],
            )
            self.wait(0.5)

            # Create intersection result graph (center, red) with edge weights
            graph_int = create_square_digraph(INTERSECTION_DATA, RED_C, show_weights=True)
            graph_int.scale(1.2).move_to(ORIGIN + DOWN * 0.5)
            label_int = Text("A ∩ B", font_size=24, color=RED_C).next_to(graph_int, UP)

            # Create intersection matrix
            mat_int = create_sparse_matrix(INTERSECTION_DATA, scale=0.5)
            mat_int.next_to(graph_int, DOWN, buff=0.5)

            self.play(
                Write(label_int),
                Create(graph_int),
                FadeIn(mat_int),
            )
            self.wait(0.5)

            # Show comparison
            comparison = VGroup(
                Text("Union: 4 edges", font_size=20, color=YELLOW),
                Text("Intersection: 2 edges", font_size=20, color=RED_C),
            ).arrange(RIGHT, buff=1.5)
            comparison.next_to(mat_int, DOWN, buff=0.4)

            self.play(Write(comparison))
            self.wait(1)

        with self.voiceover(
            """Similarly, Python's AND operator provides a shorthand for intersection.
            A ampersand B creates a lazy intersection, which binary times then
            materializes into the result."""
        ):
            # Transform code to show operator syntax
            code2 = Code(
                code_string="binary.times(A & B).new()",
                language="python",
                background="window",
            ).scale(0.7)
            code2.next_to(title, DOWN, buff=0.3)
            self.play(Transform(code, code2))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(code),
            FadeOut(graph_a), FadeOut(label_a), FadeOut(mat_a),
            FadeOut(graph_b), FadeOut(label_b), FadeOut(mat_b),
            FadeOut(graph_int), FadeOut(label_int), FadeOut(mat_int),
            FadeOut(comparison),
        )
        self.wait(0.5)

    def get_nearest_node(self, pos):
        """Get the nearest node index for a position."""
        positions = {
            0: np.array([-0.7, 0.7, 0]),
            1: np.array([0.7, 0.7, 0]),
            2: np.array([0.7, -0.7, 0]),
            3: np.array([-0.7, -0.7, 0]),
        }
        min_dist = float('inf')
        nearest = 0
        for i, p in positions.items():
            dist = np.linalg.norm(pos[:2] - p[:2])
            if dist < min_dist:
                min_dist = dist
                nearest = i
        return nearest
