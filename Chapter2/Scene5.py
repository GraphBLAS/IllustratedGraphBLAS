import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    CHAPTER0_MATRIX_DATA,
    create_adjacency_digraph,
    animate_vertex_fill,
    setup_scene,
)


class Scene5(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Single Source Shortest Path", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Use the standard triangular graph from other chapters
        # CHAPTER0_MATRIX_DATA edges with weights:
        # 0→1 (1), 0→3 (2), 1→2 (5), 3→4 (2), 3→5 (9), 4→2 (5), 5→4 (2)
        matrix_data = CHAPTER0_MATRIX_DATA

        graph, weight_labels = create_adjacency_digraph(
            matrix_data, layout="triangle", scale=0.9, edge_labels=True
        )
        graph.to_edge(RIGHT, buff=1.5)
        weight_labels.shift(graph.get_center())  # Align labels with graph position

        with self.voiceover(
            """Let's trace through single source shortest path using our familiar
            weighted graph. The edge labels show the distance for each connection.
            We want to find the shortest distance from node zero to all other nodes,
            using the MIN accumulator."""
        ):
            self.play(Create(graph))
            self.play(Write(weight_labels))

        # Distance vector display
        dist_label = Text("dist =", font_size=28).to_edge(LEFT, buff=0.5).shift(UP * 1)

        with self.voiceover(
            """We initialize the distance vector with zero for the source node.
            All other entries are absent, meaning unreached."""
        ):
            # Initial: dist[0] = 0, rest are absent (sparse)
            dist_vec = Matrix([["0"], [""], [""], [""], [""], [""]], h_buff=0.8).scale(0.55)
            dist_vec.next_to(dist_label, RIGHT, buff=0.3)

            self.play(Write(dist_label), Write(dist_vec))
            self.play(animate_vertex_fill(graph.vertices[0], GREEN))

        # Show the accumulator syntax
        acc_syntax = Code(
            code_string="dist(dist.S, gb.binary.min) << dist.vxm(A, min_plus)",
            language="python",
            background="window"
        ).scale(0.5).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            """Each iteration multiplies the distance vector by the adjacency
            matrix using the min-plus semiring. The MIN accumulator keeps the
            smaller of the existing distance or the newly computed one."""
        ):
            self.play(Write(acc_syntax))

        with self.voiceover(
            """After the first iteration, we discover nodes one and three.
            Node one has distance one, and node three has distance two."""
        ):
            # Iteration 1: dist = [0, 1, _, 2, _, _]
            # Found: 0→1 (weight 1), 0→3 (weight 2)
            new_dist1 = Matrix([["0"], ["1"], [""], ["2"], [""], [""]], h_buff=0.8).scale(0.55)
            new_dist1.move_to(dist_vec)

            self.play(Transform(dist_vec, new_dist1))
            self.play(
                animate_vertex_fill(graph.vertices[1], YELLOW),
                animate_vertex_fill(graph.vertices[3], YELLOW),
            )

        with self.voiceover(
            """In the second iteration, we reach nodes two, four, and five.
            Node two is reached through node one at distance six. Node four
            through node three at distance four. And node five at distance eleven."""
        ):
            # Iteration 2: dist = [0, 1, 6, 2, 4, 11]
            # Found: 0→1→2 (1+5=6), 0→3→4 (2+2=4), 0→3→5 (2+9=11)
            new_dist2 = Matrix([["0"], ["1"], ["6"], ["2"], ["4"], ["11"]], h_buff=0.8).scale(0.55)
            new_dist2.move_to(dist_vec)

            self.play(Transform(dist_vec, new_dist2))
            self.play(
                animate_vertex_fill(graph.vertices[2], YELLOW),
                animate_vertex_fill(graph.vertices[4], YELLOW),
                animate_vertex_fill(graph.vertices[5], YELLOW),
            )

        with self.voiceover(
            """In the third iteration, the algorithm explores paths through nodes
            four and five. It finds path zero-three-four-two with length nine,
            but we already have six for node two. The MIN accumulator compares
            nine to six and keeps the smaller value."""
        ):
            # Show that MIN keeps shorter paths
            comparison = VGroup(
                Text("0→3→4→2 = 9  vs  0→1→2 = 6", font_size=20, color=GREEN),
                Text("MIN keeps 6", font_size=20, color=GREEN),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            comparison.to_edge(LEFT, buff=1).shift(DOWN * 1.5)
            self.play(Write(comparison))

        with self.voiceover(
            """Similarly, path zero-three-five-four has length thirteen, but node
            four already has distance four. No distances change in this iteration,
            so the vector remains the same. This is our final answer."""
        ):
            # Iteration 3: no changes - distances are final
            # 0→3→4→2 = 2+2+5 = 9 > 6, no change
            # 0→3→5→4 = 2+9+2 = 13 > 4, no change
            self.play(FadeOut(comparison))

            # Mark all as done - distances are final
            self.play(
                animate_vertex_fill(graph.vertices[1], GREEN),
                animate_vertex_fill(graph.vertices[2], GREEN),
                animate_vertex_fill(graph.vertices[3], GREEN),
                animate_vertex_fill(graph.vertices[4], GREEN),
                animate_vertex_fill(graph.vertices[5], GREEN),
            )

        with self.voiceover(
            """To confirm convergence, we run a fourth iteration. If no distances
            change, the algorithm is complete. This is the termination condition:
            iterate until the distance vector stops changing."""
        ):
            # Show termination condition
            termination = Text("Termination: no changes after iteration", font_size=20, color=YELLOW)
            termination.move_to(ORIGIN).shift(DOWN * 2)
            self.play(Write(termination))
            self.wait(1)

        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(weight_labels),
            FadeOut(dist_label), FadeOut(dist_vec), FadeOut(acc_syntax),
            FadeOut(termination)
        )
        self.wait(0.5)
