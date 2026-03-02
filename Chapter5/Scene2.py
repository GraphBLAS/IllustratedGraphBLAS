import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from scene_utils import (
    setup_scene,
    create_sparse_matrix,
    create_incidence_matrices,
    CHAPTER5_EDGES,
)


class Scene2(VoiceoverScene, Scene):
    """S @ D = Adjacency Matrix: Animated Multiplication."""

    def construct(self):
        setup_scene(self)

        title = Text("Multiplication Gives Adjacency", font_size=44).to_edge(UP)
        self.play(Write(title))

        # Generate incidence matrices from shared edge definition
        S_incidence, D_incidence, S_data, D_data = create_incidence_matrices(CHAPTER5_EDGES)
        S_mat = S_incidence.matrix
        D_mat = D_incidence.matrix

        # A = S @ D: 3×3 (nodes × nodes)
        # A[i,j] = sum over edges e of S[i,e] * D[e,j]
        # = 1 if there's an edge from i to j
        n_nodes = len(S_data)
        n_edges = len(D_data)
        A_data = [[sum(S_data[i][e] * D_data[e][j] for e in range(n_edges))
                   for j in range(n_nodes)] for i in range(n_nodes)]

        with self.voiceover(
            """We have built our two incidence matrices S and D. Now let us
            see what happens when we multiply them. S has dimensions
            n by m, nodes by edges. D has dimensions m by n, edges by nodes."""
        ):
            # Create S group with label and dimension
            S_label = MathTex("S", font_size=36, color=YELLOW)
            S_dim = Text("3×3", font_size=16, color=GRAY)

            S_group = VGroup(
                S_label,
                S_dim,
                S_incidence
            ).arrange(DOWN, buff=0.2)
            S_group.to_edge(LEFT, buff=0.5).shift(UP * 0.5)

            self.play(Write(S_group))

            # Create D group with label and dimension
            D_label = MathTex("D", font_size=36, color=YELLOW)
            D_dim = Text("3×3", font_size=16, color=GRAY)

            D_group = VGroup(
                D_label,
                D_dim,
                D_incidence
            ).arrange(DOWN, buff=0.2)
            D_group.move_to(ORIGIN).shift(UP * 0.5)

            self.play(Write(D_group))
            self.wait(1)

        with self.voiceover(
            """When we multiply S times D, the inner dimension, the edges,
            cancels out. We get an n by n matrix: nodes by nodes. This is
            exactly the adjacency matrix."""
        ):
            # Show multiplication equation
            times_sym = MathTex(r"\times", font_size=36)
            equals_sym = MathTex("=", font_size=36)

            # Create result matrix A
            A_mat = create_sparse_matrix(A_data, scale=0.55)
            A_label = MathTex("A", font_size=36, color=YELLOW)
            A_dim = Text("3×3", font_size=16, color=GREEN)

            # Row/col labels for A
            A_row_labels = VGroup(*[
                Text(str(i), font_size=12, color=BLUE).next_to(A_mat.get_rows()[i], LEFT, buff=0.25)
                for i in range(3)
            ])
            A_col_labels = VGroup(*[
                Text(str(j), font_size=12, color=BLUE).next_to(A_mat.get_columns()[j], UP, buff=0.2)
                for j in range(3)
            ])

            A_group = VGroup(
                A_label,
                A_dim,
                VGroup(A_mat, A_row_labels, A_col_labels)
            ).arrange(DOWN, buff=0.2)
            A_group.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)

            # Animate multiplication
            times_sym.move_to((S_group.get_right() + D_group.get_left()) / 2)
            equals_sym.move_to((D_group.get_right() + A_group.get_left()) / 2)

            self.play(Write(times_sym), Write(equals_sym), Write(A_group))
            self.wait(1)

        # Dimension annotation
        with self.voiceover(
            """Let us trace the dimensions. S is n by m, D is m by n. The
            m dimension, representing edges, cancels in the multiplication.
            We are left with n by n: the adjacency matrix dimensions."""
        ):
            dim_eq = MathTex(
                r"(n \times m) \times (m \times n) = (n \times n)",
                font_size=28
            ).set_color(GREEN)
            dim_eq.to_edge(DOWN, buff=1.5)

            # Highlight the canceling dimension
            dim_cancel = Text("edges cancel", font_size=16, color=RED)
            dim_cancel.next_to(dim_eq, DOWN, buff=0.2)

            self.play(Write(dim_eq), Write(dim_cancel))
            self.wait(2)

        self.play(FadeOut(dim_eq), FadeOut(dim_cancel))

        # Show specific computation
        with self.voiceover(
            """Let us verify one entry. To compute A at row 0, column 1, we
            take row 0 of S and column 1 of D. Row 0 of S is one, zero, one.
            Column 1 of D is one, zero, zero. The dot product is one times
            one plus zero plus zero, which equals one. Indeed, there is an
            edge from node 0 to node 1."""
        ):
            # Highlight row 0 of S
            S_row0 = SurroundingRectangle(S_mat.get_rows()[0], color=RED, buff=0.05)
            # Highlight column 1 of D
            D_col1 = SurroundingRectangle(D_mat.get_columns()[1], color=RED, buff=0.05)
            # Highlight result A[0,1]
            A_01 = SurroundingRectangle(A_mat.get_entries()[1], color=RED, buff=0.05)

            self.play(Create(S_row0), Create(D_col1))
            self.wait(0.5)
            self.play(Create(A_01))

            # Show computation
            computation = MathTex(
                r"A[0,1] = (1 \cdot 1) + (0 \cdot 0) + (1 \cdot 0) = 1",
                font_size=24
            ).set_color(RED)
            computation.to_edge(DOWN, buff=1)

            self.play(Write(computation))
            self.wait(2)

            self.play(FadeOut(S_row0), FadeOut(D_col1), FadeOut(A_01), FadeOut(computation))

        # Show interpretation
        with self.voiceover(
            """Each entry A at i, j counts how many edges go from node i to
            node j. For a simple graph with no parallel edges, this is always
            zero or one. For multi-graphs, we will see how the count can be
            larger."""
        ):
            interpretation = VGroup(
                MathTex(r"A[i,j] = \sum_e S[i,e] \cdot D[e,j]", font_size=28),
                Text("= number of edges from i to j", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.3)
            interpretation.to_edge(DOWN, buff=0.8)

            self.play(Write(interpretation))
            self.wait(2)

        self.play(FadeOut(interpretation))

        # Show the key insight
        with self.voiceover(
            """This is the fundamental relationship. The adjacency matrix
            can be factored as the product of two incidence matrices.
            S captures which nodes are sources. D captures which nodes are
            destinations. Their product reconstructs the graph's connectivity."""
        ):
            insight = VGroup(
                MathTex(r"A = S \times D", font_size=40, color=GREEN),
                Text("Adjacency = Source × Destination", font_size=22, color=GRAY),
            ).arrange(DOWN, buff=0.3)
            insight.to_edge(DOWN, buff=0.5)

            self.play(Write(insight))
            self.wait(3)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(S_group), FadeOut(D_group),
            FadeOut(A_group), FadeOut(times_sym), FadeOut(equals_sym),
            FadeOut(insight)
        )
        self.wait(0.5)
