import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import math
from scene_utils import create_sparse_matrix, create_small_graph_from_matrix, setup_scene, animate_vertex_fill


class Scene4(VoiceoverScene, Scene):
    """Multi-hop Paths: A², A³."""

    def construct(self):
        setup_scene(self)

        title = Text("Multi-hop Paths", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Create a 5-node graph with clear structure
        # Graph:
        #   0 -- 1 -- 2
        #   |         |
        #   3 ------- 4
        #
        # Adjacency matrix (symmetric):
        A_data = [
            [0, 1, 0, 1, 0],  # 0: connects to 1, 3
            [1, 0, 1, 0, 0],  # 1: connects to 0, 2
            [0, 1, 0, 0, 1],  # 2: connects to 1, 4
            [1, 0, 0, 0, 1],  # 3: connects to 0, 4
            [0, 0, 1, 1, 0],  # 4: connects to 2, 3
        ]

        # Create graph visualization
        graph = self.create_graph()
        graph.scale(0.8).to_edge(RIGHT, buff=1)

        A_mat = create_sparse_matrix(A_data, scale=0.4, v_buff=0.65, h_buff=0.65)
        A_label = MathTex("A").scale(0.9)
        A_small_graph = create_small_graph_from_matrix(A_data, scale=0.25, directed=False, edge_color=BLUE)
        A_group = VGroup(A_label, A_mat, A_small_graph).arrange(DOWN, buff=0.2).to_edge(LEFT, buff=1).shift(UP * 0.5)

        with self.voiceover(
            """Let's trace multi-hop paths in a concrete example. Here we have
            a five-node graph. Node zero connects to nodes one and three.
            Node two connects to nodes one and four. The adjacency matrix A
            encodes these direct connections."""
        ):
            self.play(Create(graph))
            self.play(Write(A_group))
            # Highlight node 0
            self.play(animate_vertex_fill(graph.vertices[0], YELLOW))
            self.wait(1)

        # Compute A^2 step by step
        # A^2[i,j] = number of 2-hop paths from i to j
        A2_data = [
            [2, 0, 1, 0, 1],  # 0: 2-hops to 0(via 1,3), 2(via 1), 4(via 3)
            [0, 2, 0, 1, 1],  # 1: 2-hops to 1(via 0,2), 3(via 0), 4(via 2)
            [1, 0, 2, 1, 0],  # 2: 2-hops to 0(via 1), 2(via 1,4), 3(via 4)
            [0, 1, 1, 2, 0],  # 3: 2-hops to 1(via 0), 2(via 4), 3(via 0,4)
            [1, 1, 0, 0, 2],  # 4: 2-hops to 0(via 3), 1(via 2), 4(via 2,3)
        ]

        # Show A^2 calculation
        A2_mat = create_sparse_matrix(A2_data, scale=0.4, v_buff=0.65, h_buff=0.65)
        A2_label = MathTex("A^2").scale(0.9)
        A2_small_graph = create_small_graph_from_matrix(A2_data, scale=0.25, directed=False, edge_color=YELLOW, show_weights=True)
        A2_group = VGroup(A2_label, A2_mat, A2_small_graph).arrange(DOWN, buff=0.2).next_to(A_group, DOWN, buff=0.5)

        with self.voiceover(
            """When we multiply the adjacency matrix by itself, A squared, we
            get two-hop paths. Each entry at position i,j counts how many
            paths of length two exist from node i to node j."""
        ):
            self.play(Write(A2_group))
            self.wait(1)

        # Highlight a specific path: 0 -> 1 -> 2
        # This contributes to A^2[0,2]
        path_text = Text("Path: 0 → 1 → 2", font_size=28, color=GREEN).to_edge(DOWN, buff=1)

        with self.voiceover(
            """Let's trace a specific path. From node zero, we can reach
            node two in two hops by going through node one. This path
            contributes to the entry A-squared at position zero-two.
            A at zero-one times A at one-two equals one times one equals one."""
        ):
            self.play(Write(path_text))
            # Highlight edges 0-1 and 1-2
            self.play(animate_vertex_fill(graph.vertices[1], GREEN))
            self.play(animate_vertex_fill(graph.vertices[2], GREEN))

            # Highlight A^2[0,2]
            highlight = SurroundingRectangle(A2_mat.get_entries()[2], color=GREEN, buff=0.1)
            self.play(Create(highlight))
            self.wait(1)

        self.play(FadeOut(path_text), FadeOut(highlight))

        # Reset vertex colors
        self.play(
            animate_vertex_fill(graph.vertices[1], WHITE),
            animate_vertex_fill(graph.vertices[2], WHITE),
        )

        # Show diagonal entries (2-hop back to self)
        diag_text = Text("Diagonal: 2-hop cycles back to start", font_size=24, color=BLUE).to_edge(DOWN, buff=1)

        with self.voiceover(
            """Notice the diagonal entries. These count two-hop cycles that
            return to the starting node. Node zero has two such cycles:
            zero to one to zero, and zero to three to zero. The diagonal
            of A-squared counts the degree of each node."""
        ):
            self.play(Write(diag_text))
            # Highlight diagonal of A^2
            diag_highlights = VGroup(*[
                SurroundingRectangle(A2_mat.get_entries()[i * 5 + i], color=BLUE, buff=0.05)
                for i in range(5)
            ])
            self.play(Create(diag_highlights))
            self.wait(2)

        self.play(FadeOut(diag_text), FadeOut(diag_highlights))

        # Briefly show A^3
        # A^3 = A^2 @ A = 3-hop paths
        A3_text = MathTex("A^3 = A^2 \\times A").scale(0.8).to_edge(DOWN, buff=1.5)
        A3_desc = Text("3-hop paths", font_size=24, color=YELLOW).next_to(A3_text, DOWN, buff=0.3)

        with self.voiceover(
            """Cubing the matrix gives three-hop paths. We multiply A-squared
            by A again. This pattern continues: A to the k gives k-hop path
            counts. This is the algebraic foundation of graph analytics:
            distances, influence propagation, and connectivity all emerge
            from matrix powers."""
        ):
            self.play(Write(A3_text), Write(A3_desc))
            self.wait(2)

        # Key insight
        insight_box = VGroup(
            Text("Key Insight:", font_size=24, color=YELLOW),
            MathTex(r"A^k[i,j] = \text{number of } k\text{-hop paths from } i \text{ to } j").scale(0.7)
        ).arrange(DOWN, buff=0.2)
        insight_box.move_to(A3_text.get_center())

        self.play(
            FadeOut(A3_text), FadeOut(A3_desc),
            FadeIn(insight_box)
        )
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(A_group),
            FadeOut(A2_group), FadeOut(insight_box)
        )
        self.wait(0.5)

    def create_graph(self):
        """Create the 5-node example graph."""
        # Layout:
        #   0 -- 1 -- 2
        #   |         |
        #   3 ------- 4
        positions = {
            0: np.array([-2, 1, 0]),
            1: np.array([0, 1, 0]),
            2: np.array([2, 1, 0]),
            3: np.array([-2, -1, 0]),
            4: np.array([2, -1, 0]),
        }

        vertices = {}
        for i in range(5):
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.3, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        edges_list = [(0, 1), (1, 2), (0, 3), (2, 4), (3, 4)]
        edges = VGroup()

        for i, j in edges_list:
            edge = DoubleArrow(
                positions[i], positions[j],
                color=BLUE, buff=0.35, stroke_width=3,
                tip_length=0.15, max_tip_length_to_length_ratio=0.1
            )
            edges.add(edge)

        graph = VGroup(edges, *vertices.values())
        graph.vertices = vertices
        return graph
