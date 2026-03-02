import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix


class Scene4(VoiceoverScene, Scene):
    """Multi-graphs: Parallel Edges as Separate Columns."""

    def construct(self):
        setup_scene(self)

        title = Text("Multi-graphs", font_size=48).to_edge(UP)
        self.play(Write(title))

        # 3 nodes, 4 edges with parallel edges
        # e0: 0→1, e1: 0→1 (parallel), e2: 1→2, e3: 0→2
        #
        # S: 3×4 (nodes × edges)
        S_data = [
            [1, 1, 0, 1],  # node 0 sources e0, e1, e3
            [0, 0, 1, 0],  # node 1 sources e2
            [0, 0, 0, 0],  # node 2 sources nothing
        ]

        # D: 4×3 (edges × nodes)
        D_data = [
            [0, 1, 0],  # e0 → node 1
            [0, 1, 0],  # e1 → node 1 (parallel to e0)
            [0, 0, 1],  # e2 → node 2
            [0, 0, 1],  # e3 → node 2
        ]

        # A = S @ D: 3×3 (nodes × nodes) - WEIGHTED adjacency
        # A[0,1] = 2 (two edges from 0 to 1)
        A_data = [
            [0, 2, 1],  # node 0 → node 1 (count=2), node 2 (count=1)
            [0, 0, 1],  # node 1 → node 2
            [0, 0, 0],  # node 2 → nothing
        ]

        with self.voiceover(
            """A multi-graph allows multiple edges between the same pair of
            nodes. Consider a transportation network where two different
            routes, perhaps a highway and a rail line, both connect the same
            two cities. These are distinct edges, each with its own identity."""
        ):
            subtitle = Text("Multiple Edges, Same Endpoints", font_size=28, color=YELLOW)
            subtitle.next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle))

            # Create multi-graph visualization
            graph = self.create_multigraph()
            graph.to_edge(RIGHT, buff=1).shift(UP * 0.3)

            self.play(Create(graph))
            self.wait(1)

        with self.voiceover(
            """In our example, we have three nodes and four edges. Edges e0
            and e1 are parallel: both go from node 0 to node 1. Edge e2 goes
            from node 1 to node 2. Edge e3 goes from node 0 to node 2."""
        ):
            # Highlight parallel edges
            parallel_highlight = VGroup(
                graph.edges[0].copy().set_color(YELLOW).set_stroke(width=5),
                graph.edges[1].copy().set_color(YELLOW).set_stroke(width=5),
            )
            self.play(Create(parallel_highlight))

            parallel_note = Text("e0 and e1: parallel edges", font_size=18, color=YELLOW)
            parallel_note.next_to(graph, DOWN, buff=0.3)
            self.play(Write(parallel_note))
            self.wait(1)

            self.play(FadeOut(parallel_highlight), FadeOut(parallel_note))

        with self.voiceover(
            """In the S matrix, we see that node 0 is the source of three
            edges: e0, e1, and e3. The parallel edges e0 and e1 appear as
            separate columns, each with a one at row 0."""
        ):
            # Show S matrix
            S_mat = create_sparse_matrix(S_data, scale=0.55)
            S_label = MathTex("S", font_size=36, color=YELLOW)
            S_dim = Text("3×4", font_size=16, color=GRAY)

            S_row_labels = VGroup(*[
                Text(str(i), font_size=12, color=BLUE).next_to(S_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            S_col_labels = VGroup(*[
                Text(f"e{j}", font_size=12, color=GREEN).next_to(S_mat.get_columns()[j], UP, buff=0.25)
                for j in range(4)
            ])

            S_group = VGroup(
                S_label, S_dim,
                VGroup(S_mat, S_row_labels, S_col_labels)
            ).arrange(DOWN, buff=0.2)
            S_group.to_edge(LEFT, buff=0.5).shift(UP * 1)

            self.play(Write(S_group))

            # Highlight parallel edge columns
            e0_col = SurroundingRectangle(S_mat.get_columns()[0], color=YELLOW, buff=0.05)
            e1_col = SurroundingRectangle(S_mat.get_columns()[1], color=YELLOW, buff=0.05)
            self.play(Create(e0_col), Create(e1_col))
            self.wait(1)
            self.play(FadeOut(e0_col), FadeOut(e1_col))

        with self.voiceover(
            """The D matrix has four rows, one per edge. Notice that rows
            e0 and e1 are identical: both have a one at column 1, indicating
            that both edges go to node 1. This is expected for parallel edges."""
        ):
            # Show D matrix
            D_mat = create_sparse_matrix(D_data, scale=0.55)
            D_label = MathTex("D", font_size=36, color=YELLOW)
            D_dim = Text("4×3", font_size=16, color=GRAY)

            D_row_labels = VGroup(*[
                Text(f"e{i}", font_size=12, color=GREEN).next_to(D_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(4)
            ])
            D_col_labels = VGroup(*[
                Text(str(j), font_size=12, color=BLUE).next_to(D_mat.get_columns()[j], UP, buff=0.25)
                for j in range(3)
            ])

            D_group = VGroup(
                D_label, D_dim,
                VGroup(D_mat, D_row_labels, D_col_labels)
            ).arrange(DOWN, buff=0.2)
            D_group.to_edge(LEFT, buff=0.5).shift(DOWN * 1.5)

            self.play(Write(D_group))

            # Highlight identical rows
            e0_row = SurroundingRectangle(D_mat.get_rows()[0], color=YELLOW, buff=0.05)
            e1_row = SurroundingRectangle(D_mat.get_rows()[1], color=YELLOW, buff=0.05)
            self.play(Create(e0_row), Create(e1_row))

            identical_note = Text("Identical rows for parallel edges", font_size=16, color=YELLOW)
            identical_note.next_to(D_group, DOWN, buff=0.3)
            self.play(Write(identical_note))
            self.wait(1)
            self.play(FadeOut(e0_row), FadeOut(e1_row), FadeOut(identical_note))

        with self.voiceover(
            """When we multiply S times D, we get the weighted adjacency
            matrix. Position 0,1 now contains 2, counting the two parallel
            edges from node 0 to node 1. The multiplication naturally counts
            edge multiplicity."""
        ):
            # Show multiplication result
            times_sym = MathTex(r"S \times D =", font_size=28)
            A_mat = create_sparse_matrix(A_data, scale=0.55)
            A_label = Text("Weighted Adjacency", font_size=20, color=GREEN)

            A_row_labels = VGroup(*[
                Text(str(i), font_size=12, color=BLUE).next_to(A_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            A_col_labels = VGroup(*[
                Text(str(j), font_size=12, color=BLUE).next_to(A_mat.get_columns()[j], UP, buff=0.25)
                for j in range(3)
            ])

            mult_group = VGroup(
                times_sym,
                VGroup(A_mat, A_row_labels, A_col_labels),
                A_label
            ).arrange(DOWN, buff=0.2)
            mult_group.to_edge(DOWN, buff=0.5)

            self.play(Write(mult_group))

            # Highlight the count entry
            count_entry = A_mat.get_entries()[1]  # Position [0,1]
            count_highlight = SurroundingRectangle(count_entry, color=RED, buff=0.05)
            count_note = Text("Count = 2", font_size=18, color=RED)
            count_note.next_to(count_highlight, RIGHT, buff=0.3)

            self.play(Create(count_highlight), Write(count_note))
            self.wait(2)

            self.play(FadeOut(count_highlight), FadeOut(count_note))

        self.play(FadeOut(subtitle), FadeOut(mult_group))

        # Show the key advantage
        with self.voiceover(
            """The key advantage is that each edge retains its identity.
            We can attach different weights, labels, or attributes to e0
            and e1 separately. An edge weight vector with four entries
            multiplies naturally with our representation."""
        ):
            # Show edge attribute example
            weight_vec = MathTex(r"w = [w_0, w_1, w_2, w_3]", font_size=28)
            weight_desc = Text("Different weights for parallel edges", font_size=18, color=GRAY)

            example = VGroup(
                Text("e0: Highway (fast, expensive)", font_size=18, color=BLUE),
                Text("e1: Railway (slow, cheap)", font_size=18, color=GREEN),
            ).arrange(DOWN, buff=0.2)

            weight_group = VGroup(weight_vec, weight_desc, example).arrange(DOWN, buff=0.3)
            weight_group.to_edge(DOWN, buff=0.4)

            self.play(Write(weight_group))
            self.wait(3)

        self.play(FadeOut(weight_group))

        # Comparison with adjacency
        with self.voiceover(
            """If we had used only an adjacency matrix, the two parallel edges
            would collapse into a single entry with value 2. We would know
            there are two edges, but we could not distinguish them or assign
            different properties to each."""
        ):
            comparison = VGroup(
                Text("Adjacency Matrix:", font_size=22, color=RED),
                Text("A[0,1] = 2 (edges collapsed)", font_size=18, color=GRAY),
                Text(" ", font_size=10),
                Text("S and D Matrices:", font_size=22, color=GREEN),
                Text("e0 and e1 remain separate", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            comparison.to_edge(DOWN, buff=0.5)

            self.play(Write(comparison))
            self.wait(3)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(S_group),
            FadeOut(D_group), FadeOut(comparison)
        )
        self.wait(0.5)

    def create_multigraph(self):
        """Create a 3-node multi-graph with curved parallel edges."""
        positions = {
            0: np.array([-1.5, 1, 0]),
            1: np.array([1.5, 1, 0]),
            2: np.array([0, -1, 0]),
        }

        # Create vertices
        vertices = {}
        for i, pos in positions.items():
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.3, fill_color=WHITE, fill_opacity=1)
            dot.move_to(pos)
            vertices[i] = dot

        # Edges: e0: 0→1, e1: 0→1 (parallel), e2: 1→2, e3: 0→2
        edges = VGroup()
        edge_labels = VGroup()

        # e0: 0→1 (curved up)
        e0 = CurvedArrow(
            positions[0], positions[1],
            angle=-0.4, color=BLUE, stroke_width=3, tip_length=0.15
        )
        e0_label = Text("e0", font_size=14, color=BLUE).move_to(
            e0.point_from_proportion(0.5) + np.array([0, 0.25, 0])
        )
        edges.add(e0)
        edge_labels.add(e0_label)

        # e1: 0→1 (curved down) - parallel to e0
        e1 = CurvedArrow(
            positions[0], positions[1],
            angle=0.4, color=BLUE, stroke_width=3, tip_length=0.15
        )
        e1_label = Text("e1", font_size=14, color=BLUE).move_to(
            e1.point_from_proportion(0.5) + np.array([0, -0.25, 0])
        )
        edges.add(e1)
        edge_labels.add(e1_label)

        # e2: 1→2 (straight)
        e2 = Arrow(
            positions[1], positions[2],
            color=BLUE, buff=0.35, stroke_width=3, tip_length=0.15
        )
        e2_label = Text("e2", font_size=14, color=BLUE).next_to(e2.get_center(), RIGHT, buff=0.1)
        edges.add(e2)
        edge_labels.add(e2_label)

        # e3: 0→2 (straight)
        e3 = Arrow(
            positions[0], positions[2],
            color=BLUE, buff=0.35, stroke_width=3, tip_length=0.15
        )
        e3_label = Text("e3", font_size=14, color=BLUE).next_to(e3.get_center(), LEFT, buff=0.1)
        edges.add(e3)
        edge_labels.add(e3_label)

        graph = VGroup(edges, edge_labels, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        graph.scale(0.9)
        return graph
