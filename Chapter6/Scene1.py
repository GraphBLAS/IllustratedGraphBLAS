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

# Union result with binary.plus: edges sum where both exist
# (0→1)=1, (1→2)=2, (2→3)=2, (3→0)=1
UNION_DATA = [[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2], [1, 0, 0, 0]]

# Node positions (square layout)
POS = {0: np.array([0, 1, 0]), 1: np.array([1, 1, 0]), 2: np.array([1, 0, 0]), 3: np.array([0, 0, 0])}


class Scene1(VoiceoverScene, Scene):
    """Element-wise Add: Union of two graphs."""

    def construct(self):
        setup_scene(self)

        title = Text("Element-wise Add: Union", font_size=44).to_edge(UP)

        with self.voiceover(
            """Element-wise add computes the union of two graphs. An edge appears
            in the result if it exists in either input. Graph A has edges 0 to 1,
            1 to 2, and 2 to 3. Graph B has edges 1 to 2, 2 to 3, and 3 to 0.
            Edges 1 to 2 and 2 to 3 appear in both graphs."""
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

            # Highlight common edges (1→2, 2→3) in yellow
            # Edge indices: A has (0,1)=0, (1,2)=1, (2,3)=2; B has (1,2)=0, (2,3)=1, (3,0)=2
            common_highlight_a = VGroup()
            common_highlight_b = VGroup()

            # Find and highlight edge 1→2 and 2→3 in both graphs
            for edge in graph_a.edges:
                start = edge.get_start()
                end = edge.get_end()
                # Check if this is edge 1→2 or 2→3
                start_node = self.get_nearest_node(start)
                end_node = self.get_nearest_node(end)
                if (start_node, end_node) in [(1, 2), (2, 3)]:
                    highlight = edge.copy().set_color(YELLOW).set_stroke(width=6)
                    common_highlight_a.add(highlight)

            for edge in graph_b.edges:
                start = edge.get_start()
                end = edge.get_end()
                start_node = self.get_nearest_node(start)
                end_node = self.get_nearest_node(end)
                if (start_node, end_node) in [(1, 2), (2, 3)]:
                    highlight = edge.copy().set_color(YELLOW).set_stroke(width=6)
                    common_highlight_b.add(highlight)

            self.play(Create(common_highlight_a), Create(common_highlight_b))
            self.wait(1)

        with self.voiceover(
            """When we compute eWiseAdd with binary plus, we get all edges from both
            graphs. Edge 0 to 1 comes from A, edge 3 to 0 comes from B. The shared
            edges 1 to 2 and 2 to 3 sum to 2 in the result."""
        ):
            # Show Python code below title
            code = Code(
                code_string="A.ewise_add(B, binary.plus)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code.next_to(title, DOWN, buff=0.3)
            self.play(FadeIn(code))
            self.wait(0.5)

            # Fade out highlights and prepare for result
            self.play(FadeOut(common_highlight_a), FadeOut(common_highlight_b))

            # Create union result graph (center, yellow) with edge weights
            graph_union = create_square_digraph(UNION_DATA, YELLOW, show_weights=True)
            graph_union.scale(1.2).move_to(ORIGIN + DOWN * 0.5)
            label_union = Text("A ∪ B", font_size=24, color=YELLOW).next_to(graph_union, UP)

            # Create union matrix
            mat_union = create_sparse_matrix(UNION_DATA, scale=0.5)
            mat_union.next_to(graph_union, DOWN, buff=0.5)

            # Animate bringing in result
            self.play(
                Write(label_union),
                Create(graph_union),
                FadeIn(mat_union),
            )
            self.wait(1)

            # Show edge count
            edge_count = Text("4 edges total", font_size=20, color=YELLOW)
            edge_count.next_to(mat_union, DOWN, buff=0.3)
            self.play(Write(edge_count))
            self.wait(1)

        with self.voiceover(
            """The same operation can be written more concisely using Python's OR
            operator. The expression A pipe B creates a lazy union, which is then
            passed to binary plus to produce the result."""
        ):
            # Transform code to show operator syntax
            code2 = Code(
                code_string="binary.plus(A | B).new()",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code2.next_to(title, DOWN, buff=0.3)
            self.play(Transform(code, code2))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(code),
            FadeOut(graph_a), FadeOut(label_a), FadeOut(mat_a),
            FadeOut(graph_b), FadeOut(label_b), FadeOut(mat_b),
            FadeOut(graph_union), FadeOut(label_union), FadeOut(mat_union),
            FadeOut(edge_count),
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
