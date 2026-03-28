import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix


# Weighted graph W: (0→1)=5, (0→2)=2, (1→2)=8, (2→3)=3, (3→0)=1
W_DATA = [[0, 5, 2, 0], [0, 0, 8, 0], [0, 0, 0, 3], [1, 0, 0, 0]]

# After select > 3: only (0→1)=5 and (1→2)=8 remain
FILTERED_DATA = [[0, 5, 0, 0], [0, 0, 8, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


class Scene3(VoiceoverScene, Scene):
    """Select: Filtering elements by threshold."""

    def construct(self):
        setup_scene(self)

        title = Text("Select: Filtering by Threshold", font_size=44).to_edge(UP)

        with self.voiceover(
            """The select operation filters elements based on a condition. Consider
            this weighted graph with edges ranging from weight 1 to 8. We want to
            keep only edges with weight greater than 3."""
        ):
            self.play(Write(title))

            # Create weighted graph
            graph = self.create_weighted_graph(W_DATA)
            graph.scale(1.5).shift(LEFT * 3 + UP * 0.3)
            label = Text("Weighted Graph W", font_size=24).next_to(graph, UP)

            # Create matrix
            mat = create_sparse_matrix(W_DATA, scale=0.55)
            mat.shift(RIGHT * 3 + UP * 1.0)
            mat_label = Text("W", font_size=28).next_to(mat, UP)

            self.play(Create(graph), Write(label), FadeIn(mat), Write(mat_label))
            self.wait(0.5)

            # Show Python code for select
            code = Code(
                code_string='W.select(">", 3)',
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code.next_to(mat, DOWN, buff=0.4)
            self.play(FadeIn(code))
            self.wait(1)

        with self.voiceover(
            """Select tests each edge. Edges with weight 5 and 8 pass the test.
            Edges with weight 1, 2, and 3 are filtered out. The result is a
            sparser graph with only the two strongest connections."""
        ):
            # Test each edge with check/X marks
            # Edge data: (from, to, weight, passes)
            edge_tests = [
                (0, 1, 5, True),   # 5 > 3 ✓
                (0, 2, 2, False),  # 2 > 3 ✗
                (1, 2, 8, True),   # 8 > 3 ✓
                (2, 3, 3, False),  # 3 > 3 ✗
                (3, 0, 1, False),  # 1 > 3 ✗
            ]

            marks = VGroup()
            edges_to_fade = []
            edge_idx = 0

            for edge in graph.edges:
                # Get edge info from our ordered list
                if edge_idx < len(edge_tests):
                    src, dst, weight, passes = edge_tests[edge_idx]

                    # Create mark
                    if passes:
                        mark = Text("✓", font_size=24, color=GREEN)
                    else:
                        mark = Text("✗", font_size=24, color=RED)

                    # Position mark near edge midpoint
                    mid = edge.get_center()
                    mark.move_to(mid + UP * 0.3)

                    self.play(
                        edge.animate.set_color(GREEN if passes else RED),
                        FadeIn(mark),
                        run_time=0.4
                    )
                    marks.add(mark)

                    if not passes:
                        edges_to_fade.append(edge)
                        # Also track the weight label to fade
                        edges_to_fade.append(graph.weight_labels[edge_idx])

                    edge_idx += 1

            self.wait(0.5)

            # Fade out failing edges
            self.play(
                *[obj.animate.set_opacity(0.15) for obj in edges_to_fade],
                *[mark.animate.set_opacity(0) for mark in marks],
            )
            self.wait(0.5)

            # Show result matrix
            result_mat = create_sparse_matrix(FILTERED_DATA, scale=0.55)
            result_mat.next_to(code, DOWN, buff=0.4)
            result_label = Text("Result: 2 edges", font_size=20, color=GREEN)
            result_label.next_to(result_mat, DOWN, buff=0.3)

            self.play(FadeIn(result_mat), Write(result_label))
            self.wait(1)

        with self.voiceover(
            """Comparison operators like greater-than can create boolean masks
            directly. The expression W greater than 3 produces a matrix of true
            and false values indicating which elements pass the test."""
        ):
            # Transform code to show operator syntax
            code2 = Code(
                code_string="(W > 3).new()",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code2.next_to(mat, DOWN, buff=0.4)
            self.play(Transform(code, code2))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(label),
            FadeOut(mat), FadeOut(mat_label), FadeOut(code),
            FadeOut(result_mat), FadeOut(result_label),
        )
        self.wait(0.5)

    def create_weighted_graph(self, matrix_data):
        """Create a directed graph with edge weight labels."""
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

        # Create edges with weight labels
        edges = VGroup()
        weight_labels = VGroup()

        for i in range(n):
            for j in range(n):
                if matrix_data[i][j] != 0:
                    weight = matrix_data[i][j]
                    arrow = Arrow(
                        positions[i], positions[j],
                        color=BLUE, buff=0.25, stroke_width=3,
                        tip_length=0.12, max_tip_length_to_length_ratio=0.25
                    )
                    edges.add(arrow)

                    # Weight label
                    mid = (positions[i] + positions[j]) / 2
                    direction = positions[j] - positions[i]
                    perp = np.array([-direction[1], direction[0], 0])
                    if np.linalg.norm(perp) > 0:
                        perp = perp / np.linalg.norm(perp) * 0.25
                    w_label = Text(str(weight), font_size=16, color=YELLOW)
                    w_label.move_to(mid + perp)
                    w_bg = BackgroundRectangle(w_label, color=BLACK, fill_opacity=0.8, buff=0.1, corner_radius=0.05)
                    weight_labels.add(VGroup(w_bg, w_label))

        graph = VGroup(edges, weight_labels, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        graph.weight_labels = weight_labels
        return graph
