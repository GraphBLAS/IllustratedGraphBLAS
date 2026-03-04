import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix, create_small_graph_from_matrix


# Shared data from notebook
# Graph A: edges (0→1), (1→2), (2→3)
A_DATA = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]

# Graph B: edges (1→2), (2→3), (3→0)
B_DATA = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]

# Union result: edges (0→1), (1→2), (2→3), (3→0)
UNION_DATA = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]

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
            graph_a = self.create_graph(A_DATA, BLUE)
            graph_a.scale(1.2).shift(LEFT * 4 + DOWN * 0.5)
            label_a = Text("Graph A", font_size=24, color=BLUE).next_to(graph_a, UP)

            # Create matrix A below graph
            mat_a = create_sparse_matrix(A_DATA, scale=0.5)
            mat_a.next_to(graph_a, DOWN, buff=0.5)

            # Create Graph B (right, green)
            graph_b = self.create_graph(B_DATA, GREEN)
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
            """When we compute eWiseAdd, we get all edges from both: 0 to 1 from A,
            1 to 2 and 2 to 3 from both, and 3 to 0 from B. The result has four
            distinct edge positions representing the union."""
        ):
            # Show formula
            formula = MathTex(r"A \cup B", font_size=48, color=YELLOW)
            formula.move_to(ORIGIN + UP * 0.5)
            self.play(Write(formula))
            self.wait(0.5)

            # Fade out highlights and prepare for result
            self.play(FadeOut(common_highlight_a), FadeOut(common_highlight_b))

            # Create union result graph (center, yellow)
            graph_union = self.create_graph(UNION_DATA, YELLOW)
            graph_union.scale(1.2).move_to(ORIGIN + DOWN * 0.5)
            label_union = Text("A ∪ B", font_size=24, color=YELLOW).next_to(graph_union, UP)

            # Create union matrix
            mat_union = create_sparse_matrix(UNION_DATA, scale=0.5)
            mat_union.next_to(graph_union, DOWN, buff=0.5)

            # Animate combining: fade formula, bring in result
            self.play(
                ReplacementTransform(formula, label_union),
                Create(graph_union),
                FadeIn(mat_union),
            )
            self.wait(1)

            # Show edge count
            edge_count = Text("4 edges total", font_size=20, color=YELLOW)
            edge_count.next_to(mat_union, DOWN, buff=0.3)
            self.play(Write(edge_count))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph_a), FadeOut(label_a), FadeOut(mat_a),
            FadeOut(graph_b), FadeOut(label_b), FadeOut(mat_b),
            FadeOut(graph_union), FadeOut(label_union), FadeOut(mat_union),
            FadeOut(edge_count),
        )
        self.wait(0.5)

    def create_graph(self, matrix_data, color):
        """Create a directed graph from adjacency matrix with square layout."""
        n = len(matrix_data)
        positions = {
            0: np.array([-0.7, 0.7, 0]),
            1: np.array([0.7, 0.7, 0]),
            2: np.array([0.7, -0.7, 0]),
            3: np.array([-0.7, -0.7, 0]),
        }

        # Create vertices
        vertices = {}
        for i in range(n):
            label = MathTex(str(i), color=BLACK).scale(0.5)
            dot = LabeledDot(label, radius=0.2, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        # Create edges
        edges = VGroup()
        for i in range(n):
            for j in range(n):
                if matrix_data[i][j] != 0:
                    arrow = Arrow(
                        positions[i], positions[j],
                        color=color, buff=0.25, stroke_width=3,
                        tip_length=0.15, max_tip_length_to_length_ratio=0.25
                    )
                    edges.add(arrow)

        graph = VGroup(edges, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        return graph

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
