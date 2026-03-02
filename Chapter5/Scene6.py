import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import setup_scene, create_sparse_matrix, create_bipartite_graph


class Scene6(VoiceoverScene, Scene):
    """Applications: Path Composition and Bipartite Graphs."""

    def construct(self):
        setup_scene(self)

        title = Text("Applications", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Part 1: Path Composition
        # S @ D = A (adjacency)
        # S @ D @ S @ D = A² (two-hop paths)
        # More interestingly: D @ S = edge-to-edge adjacency

        # 3-node path: 0→1→2
        S_path = [
            [1, 0],  # node 0 sources e0
            [0, 1],  # node 1 sources e1
            [0, 0],  # node 2 sources nothing
        ]

        D_path = [
            [0, 1, 0],  # e0 → node 1
            [0, 0, 1],  # e1 → node 2
        ]

        with self.voiceover(
            """One powerful application of the two-matrix representation is
            path composition. We know that S times D gives the adjacency
            matrix. But we can also compute A squared, which gives two-hop
            paths, by multiplying S times D times S times D."""
        ):
            subtitle1 = Text("Path Composition", font_size=32, color=YELLOW)
            subtitle1.next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle1))

            # Show the equation
            path_eq = MathTex(
                r"A^2 = (S \times D) \times (S \times D) = S \times D \times S \times D",
                font_size=28
            )
            path_eq.next_to(subtitle1, DOWN, buff=0.5)
            self.play(Write(path_eq))
            self.wait(1)

        with self.voiceover(
            """But there is another interesting product: D times S. This
            multiplication gives us edge-to-edge adjacency. Entry e-i, e-j
            in D times S tells us how many nodes edges i and j share. Two
            edges sharing a node are adjacent in this edge graph."""
        ):
            # Show D × S interpretation
            edge_adj_eq = MathTex(
                r"D \times S = \text{edge-to-edge adjacency}",
                font_size=28, color=GREEN
            )
            edge_adj_eq.next_to(path_eq, DOWN, buff=0.5)
            self.play(Write(edge_adj_eq))

            # Show example
            DS_desc = VGroup(
                MathTex(r"(D \times S)[e_i, e_j]", font_size=24),
                Text("= nodes shared by edges i and j", font_size=18, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            DS_desc.next_to(edge_adj_eq, DOWN, buff=0.4)
            self.play(Write(DS_desc))
            self.wait(2)

        self.play(FadeOut(path_eq), FadeOut(edge_adj_eq), FadeOut(DS_desc))

        with self.voiceover(
            """Consider edges e0 going from node 0 to node 1, and edge e1
            going from node 1 to node 2. These edges share node 1. The
            product D times S at position e0, e1 equals one, indicating
            they share one node."""
        ):
            # Show small example
            S_mat = create_sparse_matrix(S_path, scale=0.6)
            S_label = MathTex("S", font_size=28)

            D_mat = create_sparse_matrix(D_path, scale=0.6)
            D_label = MathTex("D", font_size=28)

            # D @ S = [[1, 1], [1, 1]] (both edges share one node with themselves and each other)
            # Actually: D is 2×3, S is 3×2, so D @ S is 2×2
            # DS[0,0] = D[0,:] @ S[:,0] = [0,1,0] @ [1,0,0]^T = 0
            # DS[0,1] = D[0,:] @ S[:,1] = [0,1,0] @ [0,1,0]^T = 1
            # DS[1,0] = D[1,:] @ S[:,0] = [0,0,1] @ [1,0,0]^T = 0
            # DS[1,1] = D[1,:] @ S[:,1] = [0,0,1] @ [0,1,0]^T = 0
            # Hmm, this doesn't give edge adjacency directly...
            # Let me reconsider. For edge adjacency through shared nodes:
            # We want: how many nodes are both destination of e_i AND source of e_j
            # That's exactly D @ S.
            # e0 ends at 1, e1 starts at 1, so DS[0,1] = 1 ✓
            # This means "can traverse from e0 to e1" (sequential edges)

            DS_mat = Matrix([[0, 1], [0, 0]], v_buff=0.7, h_buff=0.7).scale(0.5)
            DS_label = MathTex("D \\times S", font_size=28)

            S_group = VGroup(S_label, S_mat).arrange(DOWN, buff=0.2)
            D_group = VGroup(D_label, D_mat).arrange(DOWN, buff=0.2)
            DS_group = VGroup(DS_label, DS_mat).arrange(DOWN, buff=0.2)

            matrices = VGroup(D_group, S_group, DS_group).arrange(RIGHT, buff=1)
            matrices.move_to(ORIGIN).shift(DOWN * 0.5)

            times1 = MathTex(r"\times", font_size=24).move_to((D_group.get_right() + S_group.get_left()) / 2)
            equals1 = MathTex("=", font_size=24).move_to((S_group.get_right() + DS_group.get_left()) / 2)

            self.play(Write(matrices), Write(times1), Write(equals1))

            # Highlight the shared node entry
            ds_entry = SurroundingRectangle(DS_mat.get_entries()[1], color=YELLOW, buff=0.05)
            ds_note = Text("e0→e1: share node 1", font_size=16, color=YELLOW)
            ds_note.next_to(DS_mat, DOWN, buff=0.3)
            self.play(Create(ds_entry), Write(ds_note))
            self.wait(2)

        self.play(
            FadeOut(matrices), FadeOut(times1), FadeOut(equals1),
            FadeOut(ds_entry), FadeOut(ds_note), FadeOut(subtitle1)
        )

        # Part 2: Bipartite Graphs
        with self.voiceover(
            """Another natural application is bipartite graphs. A bipartite
            graph has two disjoint sets of nodes, with edges only between
            sets, never within a set. Job matching is a classic example:
            workers on one side, tasks on the other."""
        ):
            subtitle2 = Text("Bipartite Graphs", font_size=32, color=GREEN)
            subtitle2.next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle2))

            # Create bipartite visualization
            bipartite = create_bipartite_graph(
                left_nodes=["W0", "W1", "W2"],
                right_nodes=["T0", "T1"],
                edges=[(0, 0), (0, 1), (1, 0), (2, 1)],
                scale=0.7
            )
            bipartite.to_edge(RIGHT, buff=1.5).shift(DOWN * 0.3)

            left_label = Text("Workers", font_size=18, color=BLUE)
            left_label.next_to(bipartite, UP, buff=0.3).shift(LEFT * 1.5)
            right_label = Text("Tasks", font_size=18, color=GREEN)
            right_label.next_to(bipartite, UP, buff=0.3).shift(RIGHT * 1.5)

            self.play(Create(bipartite), Write(left_label), Write(right_label))
            self.wait(1)

        # Bipartite S and D matrices
        # Workers: W0, W1, W2 (sources)
        # Tasks: T0, T1 (destinations)
        # Edges: e0: W0→T0, e1: W0→T1, e2: W1→T0, e3: W2→T1

        # S: 3×4 (workers × edges)
        S_bipartite = [
            [1, 1, 0, 0],  # W0 sources e0, e1
            [0, 0, 1, 0],  # W1 sources e2
            [0, 0, 0, 1],  # W2 sources e3
        ]

        # D: 4×2 (edges × tasks)
        D_bipartite = [
            [1, 0],  # e0 → T0
            [0, 1],  # e1 → T1
            [1, 0],  # e2 → T0
            [0, 1],  # e3 → T1
        ]

        with self.voiceover(
            """The two-matrix representation naturally captures bipartite
            structure. The S matrix has workers as rows and edges as columns.
            The D matrix has edges as rows and tasks as columns. No block
            structure tricks are needed."""
        ):
            # Show S matrix (workers)
            S_mat_b = create_sparse_matrix(S_bipartite, scale=0.5)
            S_label_b = MathTex("S", font_size=28).set_color(BLUE)

            S_row_labels = VGroup(*[
                Text(f"W{i}", font_size=10, color=BLUE).next_to(S_mat_b.get_rows()[i], LEFT, buff=0.2)
                for i in range(3)
            ])
            S_col_labels = VGroup(*[
                Text(f"e{j}", font_size=10, color=GRAY).next_to(S_mat_b.get_columns()[j], UP, buff=0.2)
                for j in range(4)
            ])

            S_group_b = VGroup(S_label_b, VGroup(S_mat_b, S_row_labels, S_col_labels)).arrange(DOWN, buff=0.15)
            S_group_b.to_edge(LEFT, buff=0.5).shift(UP * 0.8)

            self.play(Write(S_group_b))

            # Show D matrix (tasks)
            D_mat_b = create_sparse_matrix(D_bipartite, scale=0.5)
            D_label_b = MathTex("D", font_size=28).set_color(GREEN)

            D_row_labels = VGroup(*[
                Text(f"e{i}", font_size=10, color=GRAY).next_to(D_mat_b.get_rows()[i], LEFT, buff=0.2)
                for i in range(4)
            ])
            D_col_labels = VGroup(*[
                Text(f"T{j}", font_size=10, color=GREEN).next_to(D_mat_b.get_columns()[j], UP, buff=0.2)
                for j in range(2)
            ])

            D_group_b = VGroup(D_label_b, VGroup(D_mat_b, D_row_labels, D_col_labels)).arrange(DOWN, buff=0.15)
            D_group_b.to_edge(LEFT, buff=0.5).shift(DOWN * 1.3)

            self.play(Write(D_group_b))
            self.wait(1)

        with self.voiceover(
            """The product S times D is a 3 by 2 matrix: workers by tasks.
            Entry W-i, T-j counts how many ways worker i can be assigned
            to task j. For a simple bipartite graph, this is zero or one."""
        ):
            # S @ D = workers × tasks
            # [[1,1], [1,0], [0,1]]
            SD_data = [[1, 1], [1, 0], [0, 1]]
            SD_mat = create_sparse_matrix(SD_data, scale=0.55)
            SD_label = MathTex("S \\times D", font_size=24)

            SD_note = Text("Workers → Tasks", font_size=16, color=YELLOW)

            SD_group = VGroup(SD_label, SD_mat, SD_note).arrange(DOWN, buff=0.2)
            SD_group.to_edge(DOWN, buff=0.6)

            self.play(Write(SD_group))
            self.wait(2)

        self.play(FadeOut(SD_group))

        with self.voiceover(
            """For maximum matching problems, we want to select edges such
            that each worker is assigned to at most one task, and each task
            to at most one worker. The incidence structure makes constraint
            formulation natural: select columns of S where each row has at
            most one selected entry."""
        ):
            matching_note = VGroup(
                Text("Maximum Matching:", font_size=22, color=YELLOW),
                Text("Select edges (columns) such that:", font_size=18),
                Text("• Each worker row: at most one '1'", font_size=16, color=BLUE),
                Text("• Each task column: at most one '1'", font_size=16, color=GREEN),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            matching_note.to_edge(DOWN, buff=0.4)

            self.play(Write(matching_note))
            self.wait(3)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(subtitle2), FadeOut(bipartite),
            FadeOut(left_label), FadeOut(right_label),
            FadeOut(S_group_b), FadeOut(D_group_b), FadeOut(matching_note)
        )
        self.wait(0.5)
