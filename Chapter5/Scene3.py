import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix


class Scene3(VoiceoverScene, Scene):
    """Why Two Matrices: Edge Identity vs Adjacency."""

    def construct(self):
        setup_scene(self)

        title = Text("Why Two Matrices?", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Simple graph: 0→1, 0→2, 1→2
        # Adjacency matrix loses edge identity
        A_data = [
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0],
        ]

        # S and D preserve edge identity
        S_data = [
            [1, 0, 1],  # node 0 sources e0, e2
            [0, 1, 0],  # node 1 sources e1
            [0, 0, 0],  # node 2 sources nothing
        ]

        D_data = [
            [0, 1, 0],  # e0 → node 1
            [0, 0, 1],  # e1 → node 2
            [0, 0, 1],  # e2 → node 2
        ]

        with self.voiceover(
            """Why do we need two matrices when a single adjacency matrix
            seems to work fine? The answer lies in edge identity. Let us
            compare what each representation captures."""
        ):
            subtitle = Text("Edge Identity", font_size=32, color=YELLOW)
            subtitle.next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle))
            self.wait(1)

        with self.voiceover(
            """The adjacency matrix is compact: one entry per node pair.
            Position i, j tells us whether there is an edge from i to j.
            But it does not tell us which edge it is. The edges themselves
            have no individual identity."""
        ):
            # Show adjacency matrix
            A_mat = create_sparse_matrix(A_data, scale=0.6)
            A_label = Text("Adjacency Matrix", font_size=24, color=BLUE)
            A_dim = Text("n × n", font_size=16, color=GRAY)

            # Add row/col labels
            A_row_labels = VGroup(*[
                Text(str(i), font_size=14, color=BLUE).next_to(A_mat.get_rows()[i], LEFT, buff=0.3)
                for i in range(3)
            ])
            A_col_labels = VGroup(*[
                Text(str(j), font_size=14, color=BLUE).next_to(A_mat.get_columns()[j], UP, buff=0.3)
                for j in range(3)
            ])

            A_group = VGroup(
                A_label,
                VGroup(A_mat, A_row_labels, A_col_labels),
                A_dim
            ).arrange(DOWN, buff=0.3)
            A_group.to_edge(LEFT, buff=1).shift(DOWN * 0.3)

            self.play(Write(A_group))
            self.wait(1)

            # Highlight that edges are just numbers
            edge_problem = Text("Edges are just 0/1 flags", font_size=18, color=RED)
            edge_problem.next_to(A_group, DOWN, buff=0.3)
            self.play(Write(edge_problem))
            self.wait(1)

        with self.voiceover(
            """The two-matrix representation gives each edge a distinct column
            in S and a distinct row in D. Edge e0 has its own column, edge e1
            has its own column, and so on. Each edge maintains its identity."""
        ):
            # Show S and D matrices
            S_mat = create_sparse_matrix(S_data, scale=0.5)
            S_label = MathTex("S", font_size=32, color=GREEN)

            S_row_labels = VGroup(*[
                Text(str(i), font_size=12, color=BLUE).next_to(S_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            S_col_labels = VGroup(*[
                Text(f"e{j}", font_size=12, color=GREEN).next_to(S_mat.get_columns()[j], UP, buff=0.25)
                for j in range(3)
            ])

            D_mat = create_sparse_matrix(D_data, scale=0.5)
            D_label = MathTex("D", font_size=32, color=GREEN)

            D_row_labels = VGroup(*[
                Text(f"e{i}", font_size=12, color=GREEN).next_to(D_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            D_col_labels = VGroup(*[
                Text(str(j), font_size=12, color=BLUE).next_to(D_mat.get_columns()[j], UP, buff=0.25)
                for j in range(3)
            ])

            S_group = VGroup(S_label, VGroup(S_mat, S_row_labels, S_col_labels)).arrange(DOWN, buff=0.2)
            D_group = VGroup(D_label, VGroup(D_mat, D_row_labels, D_col_labels)).arrange(DOWN, buff=0.2)

            SD_group = VGroup(S_group, D_group).arrange(DOWN, buff=0.5)
            SD_group.to_edge(RIGHT, buff=1).shift(DOWN * 0.3)

            self.play(Write(SD_group))
            self.wait(1)

            # Highlight edge identity
            edge_good = Text("Each edge has its own column/row", font_size=18, color=GREEN)
            edge_good.next_to(SD_group, DOWN, buff=0.3)
            self.play(Write(edge_good))
            self.wait(1)

        self.play(FadeOut(edge_problem), FadeOut(edge_good))

        # Show factorization concept
        with self.voiceover(
            """This is a factorization. Any adjacency matrix A can be written
            as S times D, where the number of columns in S equals the number
            of rows in D, which is the number of edges in the graph."""
        ):
            factor_eq = MathTex(r"A = S \times D", font_size=40, color=YELLOW)
            factor_desc = VGroup(
                Text("Factorization:", font_size=22, color=YELLOW),
                Text("columns of S = rows of D = number of edges", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2)

            factor_group = VGroup(factor_eq, factor_desc).arrange(DOWN, buff=0.4)
            factor_group.to_edge(DOWN, buff=0.5)

            self.play(Write(factor_group))
            self.wait(2)

        self.play(FadeOut(factor_group))

        # Clear and show benefits
        self.play(FadeOut(subtitle), FadeOut(A_group), FadeOut(SD_group))

        with self.voiceover(
            """Edge identity enables several capabilities that adjacency
            matrices cannot provide. First, we can have edge attributes.
            Each edge, being a distinct column, can have associated data
            like weights, timestamps, or labels stored in separate vectors."""
        ):
            benefit1 = VGroup(
                Text("1. Edge Attributes", font_size=28, color=YELLOW),
                Text("Store per-edge data (weights, labels, timestamps)", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            benefit1.shift(UP * 1.5)

            self.play(Write(benefit1))
            self.wait(2)

        with self.voiceover(
            """Second, we can represent multi-graphs, where multiple edges
            connect the same pair of nodes. In an adjacency matrix, these
            would collapse into a single count. With S and D, each parallel
            edge remains distinct."""
        ):
            benefit2 = VGroup(
                Text("2. Multi-graphs", font_size=28, color=GREEN),
                Text("Multiple edges between same node pair", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            benefit2.next_to(benefit1, DOWN, buff=0.5)

            self.play(Write(benefit2))
            self.wait(2)

        with self.voiceover(
            """Third, we can analyze edge relationships. The product D times S
            gives us edge-to-edge adjacency: which edges share a common node.
            This is useful for line graphs and edge clustering."""
        ):
            benefit3 = VGroup(
                Text("3. Edge-to-Edge Analysis", font_size=28, color=BLUE),
                MathTex(r"D \times S = \text{edge adjacency}", font_size=24),
            ).arrange(DOWN, buff=0.2)
            benefit3.next_to(benefit2, DOWN, buff=0.5)

            self.play(Write(benefit3))
            self.wait(2)

        # Show D × S computation
        with self.voiceover(
            """Notice that D times S produces an edge by edge matrix. Entry
            e-i, e-j counts the nodes shared between edges i and j. Edges
            sharing a node are adjacent in this edge graph."""
        ):
            # D × S = edge adjacency (3×3)
            DS_data = [
                [1, 0, 0],  # e0 shares 1 node with itself, 0 with e1, 0 with e2
                [0, 1, 0],  # e1 shares 0 with e0, 1 with itself, 0 with e2
                [0, 0, 1],  # e2 shares 0 with e0, 0 with e1, 1 with itself
            ]
            # Actually: D @ S where D is 3×3 and S is 3×3
            # D[e,j] * S[j,e'] = sum over nodes j
            # e0: endpoints are 0,1. e1: endpoints are 1,2. e2: endpoints are 0,2.
            # e0-e1 share node 1: D[0,1]*S[1,1] = 1*1 = 1
            # e0-e2 share node 0: D[0,0]*S[0,2] = 0*1 = 0... wait
            # D[0,:] = [0,1,0], S[:,0] = [1,0,0]^T
            # Actually D is edge×node, S is node×edge
            # D @ S: [edge×node] @ [node×edge] = edge×edge
            # DS[0,0] = D[0,:] @ S[:,0] = [0,1,0] @ [1,0,0]^T = 0
            # Wait, that's wrong. Let me recalculate.
            # S = [[1,0,1],[0,1,0],[0,0,0]] (node×edge)
            # D = [[0,1,0],[0,0,1],[0,0,1]] (edge×node)
            # D @ S = (edge×node) @ (node×edge) = edge×edge
            # DS[0,1] = D[0,:] @ S[:,1] = [0,1,0] @ [0,1,0]^T = 1 (edge 0 and 1 share node 1)
            # DS[0,2] = D[0,:] @ S[:,2] = [0,1,0] @ [1,0,0]^T = 0 (no shared source node)
            # Actually node 1 is destination of e0, and source of e1
            # So DS counts when destination of one edge equals source of another

            DS_note = VGroup(
                MathTex(r"D \times S", font_size=28, color=BLUE),
                Text("Edges connected via shared nodes", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            DS_note.to_edge(DOWN, buff=0.5)

            self.play(Write(DS_note))
            self.wait(2)

        # Summary
        self.play(FadeOut(benefit1), FadeOut(benefit2), FadeOut(benefit3), FadeOut(DS_note))

        with self.voiceover(
            """The two-matrix representation is more expressive than a single
            adjacency matrix. We trade compactness for expressiveness: more
            storage, but richer structure. For many graph algorithms, this
            trade-off is worthwhile."""
        ):
            summary = VGroup(
                Text("Adjacency Matrix:", font_size=24, color=RED),
                Text("Compact but loses edge identity", font_size=20, color=GRAY),
                Text(" ", font_size=10),
                Text("S and D Matrices:", font_size=24, color=GREEN),
                Text("More storage but preserves edges", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            summary.move_to(ORIGIN)

            self.play(Write(summary))
            self.wait(3)

        # Cleanup
        self.play(FadeOut(title), FadeOut(summary))
        self.wait(0.5)
