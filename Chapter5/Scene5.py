import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix


class Scene5(VoiceoverScene, Scene):
    """Undirected Graphs and Hypergraphs."""

    def construct(self):
        setup_scene(self)

        title = Text("Undirected Graphs and Hypergraphs", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Part 1: Undirected graphs
        # For undirected edge 0-1, both nodes participate equally
        # S marks both endpoints, D marks both endpoints

        # 3-node undirected triangle: edges 0-1, 1-2, 0-2
        # S: 3×3 (nodes × edges) - both endpoints marked
        S_undirected = [
            [1, 0, 1],  # node 0 in e0, e2
            [1, 1, 0],  # node 1 in e0, e1
            [0, 1, 1],  # node 2 in e1, e2
        ]

        # D: 3×3 (edges × nodes) - both endpoints marked
        D_undirected = [
            [1, 1, 0],  # e0 connects nodes 0, 1
            [0, 1, 1],  # e1 connects nodes 1, 2
            [1, 0, 1],  # e2 connects nodes 0, 2
        ]

        # A = S @ D gives symmetric adjacency (with 2s for self-loops contribution)
        # Actually: A[i,j] = number of edges containing both i and j
        # But since S and D both mark both endpoints, we get double counting on diagonal
        # For off-diagonal: A[0,1] = sum_e S[0,e]*D[e,1] = 1*1 + 0*1 + 1*0 = 1 ✓

        with self.voiceover(
            """For undirected graphs, both S and D mark both endpoints of each
            edge. In a directed graph, S marks only the source and D marks
            only the destination. In an undirected graph, there is no
            direction, so both matrices mark both participating nodes."""
        ):
            subtitle1 = Text("Undirected Graphs", font_size=32, color=YELLOW)
            subtitle1.next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle1))

            # Create undirected graph visualization
            graph = self.create_undirected_triangle()
            graph.to_edge(RIGHT, buff=1.5).shift(UP * 0.5)

            self.play(Create(graph))
            self.wait(1)

        with self.voiceover(
            """Consider this undirected triangle. Edge e0 connects nodes 0 and 1.
            In the S matrix, both row 0 and row 1 have a one in column e0.
            Similarly, in the D matrix, row e0 has ones at both column 0 and
            column 1."""
        ):
            # Show S matrix
            S_mat = create_sparse_matrix(S_undirected, scale=0.55)
            S_label = MathTex("S", font_size=32, color=YELLOW)

            S_row_labels = VGroup(*[
                Text(str(i), font_size=12, color=BLUE).next_to(S_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            S_col_labels = VGroup(*[
                Text(f"e{j}", font_size=12, color=GREEN).next_to(S_mat.get_columns()[j], UP, buff=0.25)
                for j in range(3)
            ])

            S_group = VGroup(S_label, VGroup(S_mat, S_row_labels, S_col_labels)).arrange(DOWN, buff=0.2)
            S_group.to_edge(LEFT, buff=0.6).shift(UP * 1)

            self.play(Write(S_group))

            # Show D matrix
            D_mat = create_sparse_matrix(D_undirected, scale=0.55)
            D_label = MathTex("D", font_size=32, color=YELLOW)

            D_row_labels = VGroup(*[
                Text(f"e{i}", font_size=12, color=GREEN).next_to(D_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            D_col_labels = VGroup(*[
                Text(str(j), font_size=12, color=BLUE).next_to(D_mat.get_columns()[j], UP, buff=0.25)
                for j in range(3)
            ])

            D_group = VGroup(D_label, VGroup(D_mat, D_row_labels, D_col_labels)).arrange(DOWN, buff=0.2)
            D_group.to_edge(LEFT, buff=0.6).shift(DOWN * 1.5)

            self.play(Write(D_group))

            # Highlight e0 column in S and e0 row in D
            S_e0_col = SurroundingRectangle(S_mat.get_columns()[0], color=YELLOW, buff=0.05)
            D_e0_row = SurroundingRectangle(D_mat.get_rows()[0], color=YELLOW, buff=0.05)
            self.play(Create(S_e0_col), Create(D_e0_row))
            self.wait(1)
            self.play(FadeOut(S_e0_col), FadeOut(D_e0_row))

        with self.voiceover(
            """Notice that S and D are now transposes of each other. For
            undirected graphs, S equals D-transpose. The multiplication
            S times D produces a symmetric adjacency matrix, as expected
            for an undirected graph."""
        ):
            transpose_note = MathTex(r"S = D^T", font_size=32, color=GREEN)
            transpose_note.to_edge(DOWN, buff=1)
            self.play(Write(transpose_note))
            self.wait(2)
            self.play(FadeOut(transpose_note))

        # Clear for hypergraphs
        self.play(FadeOut(subtitle1), FadeOut(graph), FadeOut(S_group), FadeOut(D_group))

        # Part 2: Hypergraphs
        # Hyperedge h0 connects nodes {0, 1, 2}
        # S: 4×2 (4 nodes × 2 hyperedges)
        # h0: {0, 1, 2}, h1: {1, 2, 3}
        S_hyper = [
            [1, 0],  # node 0 in h0
            [1, 1],  # node 1 in h0, h1
            [1, 1],  # node 2 in h0, h1
            [0, 1],  # node 3 in h1
        ]

        # D: 2×4 (2 hyperedges × 4 nodes)
        D_hyper = [
            [1, 1, 1, 0],  # h0 reaches nodes 0, 1, 2
            [0, 1, 1, 1],  # h1 reaches nodes 1, 2, 3
        ]

        with self.voiceover(
            """Now let us consider hypergraphs. In a hypergraph, an edge can
            connect more than two nodes. Think of a research paper with
            three co-authors: that single paper connects all three authors
            simultaneously, not in pairs."""
        ):
            subtitle2 = Text("Hypergraphs", font_size=32, color=GREEN)
            subtitle2.next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle2))

            # Create hypergraph visualization
            hypergraph = self.create_hypergraph()
            hypergraph.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)

            self.play(Create(hypergraph))
            self.wait(1)

        with self.voiceover(
            """We have four nodes and two hyperedges. Hyperedge h0 connects
            nodes 0, 1, and 2 simultaneously. Hyperedge h1 connects nodes
            1, 2, and 3. The overlapping nodes 1 and 2 belong to both
            hyperedges."""
        ):
            # Highlight h0 region
            h0_note = Text("h0: {0, 1, 2}", font_size=18, color=RED)
            h0_note.next_to(hypergraph, UP, buff=0.3)
            self.play(Write(h0_note))
            self.wait(1)
            self.play(FadeOut(h0_note))

        with self.voiceover(
            """In the S matrix, each hyperedge is a column. A one at row i,
            column h means node i is in hyperedge h. Column h0 has ones at
            rows 0, 1, and 2, indicating that all three nodes participate
            in this hyperedge."""
        ):
            # Show S matrix
            S_mat_h = create_sparse_matrix(S_hyper, scale=0.6)
            S_label_h = MathTex("S", font_size=32, color=YELLOW)

            S_row_labels_h = VGroup(*[
                Text(str(i), font_size=12, color=BLUE).next_to(S_mat_h.get_rows()[i], LEFT, buff=0.25)
                for i in range(4)
            ])
            S_col_labels_h = VGroup(*[
                Text(f"h{j}", font_size=12, color=RED).next_to(S_mat_h.get_columns()[j], UP, buff=0.25)
                for j in range(2)
            ])

            S_group_h = VGroup(S_label_h, VGroup(S_mat_h, S_row_labels_h, S_col_labels_h)).arrange(DOWN, buff=0.2)
            S_group_h.to_edge(LEFT, buff=0.6).shift(UP * 1)

            self.play(Write(S_group_h))

            # Highlight h0 column (3 entries)
            h0_col = SurroundingRectangle(S_mat_h.get_columns()[0], color=RED, buff=0.05)
            h0_entries = Text("3 nodes in h0", font_size=16, color=RED)
            h0_entries.next_to(h0_col, DOWN, buff=0.2)
            self.play(Create(h0_col), Write(h0_entries))
            self.wait(1)
            self.play(FadeOut(h0_col), FadeOut(h0_entries))

        with self.voiceover(
            """The D matrix is the transpose of S for hypergraphs, just like
            for undirected graphs. Each row is a hyperedge, and ones mark
            which nodes that hyperedge reaches."""
        ):
            # Show D matrix
            D_mat_h = create_sparse_matrix(D_hyper, scale=0.6)
            D_label_h = MathTex("D", font_size=32, color=YELLOW)

            D_row_labels_h = VGroup(*[
                Text(f"h{i}", font_size=12, color=RED).next_to(D_mat_h.get_rows()[i], LEFT, buff=0.25)
                for i in range(2)
            ])
            D_col_labels_h = VGroup(*[
                Text(str(j), font_size=12, color=BLUE).next_to(D_mat_h.get_columns()[j], UP, buff=0.25)
                for j in range(4)
            ])

            D_group_h = VGroup(D_label_h, VGroup(D_mat_h, D_row_labels_h, D_col_labels_h)).arrange(DOWN, buff=0.2)
            D_group_h.to_edge(LEFT, buff=0.6).shift(DOWN * 1.3)

            self.play(Write(D_group_h))
            self.wait(1)

        with self.voiceover(
            """The product S times D gives a co-membership matrix. Entry i, j
            counts how many hyperedges contain both nodes i and j. This
            reveals which nodes frequently appear together, useful for
            community detection and recommendation systems."""
        ):
            # S @ D result explanation
            # A[i,j] = number of hyperedges containing both i and j
            # A[1,2] = 2 (both h0 and h1 contain nodes 1 and 2)
            result_note = VGroup(
                MathTex(r"(S \times D)[i,j]", font_size=28),
                Text("= hyperedges containing both i and j", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            result_note.to_edge(DOWN, buff=0.5)

            self.play(Write(result_note))
            self.wait(2)

        self.play(FadeOut(result_note))

        # Show key difference from regular graphs
        with self.voiceover(
            """The key difference from regular graphs is that a hyperedge
            column in S and hyperedge row in D can have more than two ones.
            This single structural change extends our representation from
            pairwise connections to group connections."""
        ):
            key_diff = VGroup(
                Text("Regular edges: 2 entries per column/row", font_size=20, color=BLUE),
                Text("Hyperedges: any number of entries", font_size=20, color=GREEN),
            ).arrange(DOWN, buff=0.3)
            key_diff.to_edge(DOWN, buff=0.5)

            self.play(Write(key_diff))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(subtitle2), FadeOut(hypergraph),
            FadeOut(S_group_h), FadeOut(D_group_h), FadeOut(key_diff)
        )
        self.wait(0.5)

    def create_undirected_triangle(self):
        """Create an undirected triangle graph."""
        positions = {
            0: np.array([-1, -0.5, 0]),
            1: np.array([1, -0.5, 0]),
            2: np.array([0, 1, 0]),
        }

        # Create vertices
        vertices = {}
        for i, pos in positions.items():
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.3, fill_color=WHITE, fill_opacity=1)
            dot.move_to(pos)
            vertices[i] = dot

        # Undirected edges (double arrows)
        edges = VGroup()
        edge_labels = VGroup()

        edge_defs = [(0, 1, "e0"), (1, 2, "e1"), (0, 2, "e2")]
        for src, dst, name in edge_defs:
            line = DoubleArrow(
                positions[src], positions[dst],
                color=BLUE, buff=0.35, stroke_width=3,
                tip_length=0.12, max_tip_length_to_length_ratio=0.15
            )
            edges.add(line)

            mid = (positions[src] + positions[dst]) / 2
            direction = positions[dst] - positions[src]
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.25
            label = Text(name, font_size=14, color=BLUE).move_to(mid + perp)
            edge_labels.add(label)

        graph = VGroup(edges, edge_labels, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        graph.scale(0.9)
        return graph

    def create_hypergraph(self):
        """Create a 4-node hypergraph with 2 hyperedges."""
        positions = {
            0: np.array([-1.5, 1, 0]),
            1: np.array([0, 1, 0]),
            2: np.array([0, -0.5, 0]),
            3: np.array([1.5, -0.5, 0]),
        }

        # Hyperedge regions
        hyperedges = VGroup()

        # h0: {0, 1, 2} - red region
        h0_points = [positions[0], positions[1], positions[2]]
        h0_region = self.create_hyperedge_polygon(h0_points, RED, 0.25)
        h0_label = Text("h0", font_size=16, color=RED)
        h0_center = np.mean(h0_points, axis=0)
        h0_label.move_to(h0_center + np.array([-0.5, 0, 0]))
        hyperedges.add(h0_region, h0_label)

        # h1: {1, 2, 3} - green region
        h1_points = [positions[1], positions[2], positions[3]]
        h1_region = self.create_hyperedge_polygon(h1_points, GREEN, 0.25)
        h1_label = Text("h1", font_size=16, color=GREEN)
        h1_center = np.mean(h1_points, axis=0)
        h1_label.move_to(h1_center + np.array([0.5, 0, 0]))
        hyperedges.add(h1_region, h1_label)

        # Create vertices on top
        vertices = {}
        for i, pos in positions.items():
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.25, fill_color=WHITE, fill_opacity=1)
            dot.move_to(pos)
            vertices[i] = dot

        graph = VGroup(hyperedges, *vertices.values())
        graph.vertices = vertices
        graph.scale(0.9)
        return graph

    def create_hyperedge_polygon(self, points, color, opacity):
        """Create an expanded polygon for a hyperedge region."""
        centroid = np.mean(points, axis=0)
        expanded = []
        for pt in points:
            direction = pt - centroid
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            expanded.append(pt + direction * 0.5)

        polygon = Polygon(*expanded, color=color, fill_opacity=opacity, stroke_width=2)
        return polygon
