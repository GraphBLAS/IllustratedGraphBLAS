import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

import numpy as np
import math
from scene_utils import setup_scene, animate_vertex_fill, set_vertex_fill_preserve_label

# New edge weights for better MIN demonstration
# Edges: (0→1)=1, (0→3)=2, (1→2)=11, (3→4)=4, (3→5)=1, (4→2)=5, (5→4)=2
# This creates paths where MIN accumulator actually updates values:
# - Node 2: 12 → 11 → 10 (three updates!)
# - Node 4: 6 → 5 (one update)
SCENE1_MATRIX_DATA = [
    [0, 1, 0, 2, 0, 0],   # 0→1=1, 0→3=2
    [0, 0, 11, 0, 0, 0],  # 1→2=11
    [0, 0, 0, 0, 0, 0],   # node 2 has no outgoing
    [0, 0, 0, 0, 4, 1],   # 3→4=4, 3→5=1
    [0, 0, 5, 0, 0, 0],   # 4→2=5
    [0, 0, 0, 0, 2, 0]    # 5→4=2
]


class Scene1(VoiceoverScene, Scene):
    """SSSP Algorithm Visualization using MIN_PLUS semiring."""

    def construct(self):
        setup_scene(self)

        # Create components
        code = self.create_code_display()
        graph, weight_labels = self.create_graph_display()
        dist_group = self.create_dist_vector([None] * 6)

        # Position layout: code left, graph right, vector bottom
        code.scale(0.55).to_edge(LEFT, buff=0.3).shift(UP * 0.5)
        graph_group = VGroup(graph, weight_labels)
        graph_group.scale(0.7).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        dist_group.to_edge(DOWN, buff=0.8)

        # Store references for later use
        self.graph = graph
        self.weight_labels = weight_labels
        self.code = code

        # Phase A: Introduction
        with self.voiceover(
            """Here is a simple implementation of single-source shortest path using
            the MIN_PLUS semiring. The algorithm takes an adjacency matrix A and a
            source node. We initialize a distance vector where only the source has
            a value of zero, representing zero distance to itself."""
        ):
            self.play(FadeIn(code))
            self.play(Create(graph), FadeIn(weight_labels))
            self.play(FadeIn(dist_group))
            self.wait(0.5)

        # Phase B: Initialization - highlight source
        with self.voiceover(
            """We set the source node's distance to zero. All other nodes have no
            distance value yet, they are unreachable until we discover paths to them."""
        ):
            self.play(animate_vertex_fill(graph.vertices[0], YELLOW, 1))

            # Update dist[0] = 0
            new_dist = self.create_dist_vector([0, None, None, None, None, None])
            new_dist.move_to(dist_group)
            self.play(Transform(dist_group, new_dist))
            self.wait(0.5)

        # Phase C: Iteration 1 - relax from node 0
        with self.voiceover(
            """In the first iteration, we perform a vector-matrix multiply using the
            MIN_PLUS semiring. From node zero, we can reach node one with distance one,
            and node three with distance two. These values are written to the distance vector."""
        ):

            # Highlight outgoing edges from node 0: 0->1 and 0->3
            edge_01 = self.get_edge_mobject(0, 1)
            edge_03 = self.get_edge_mobject(0, 3)

            self.play(
                edge_01.animate.set_color(YELLOW).set_stroke(width=5),
                edge_03.animate.set_color(YELLOW).set_stroke(width=5),
            )

            # Show math labels
            math_01 = MathTex("0+1=1", font_size=24, color=GREEN).next_to(edge_01, UP, buff=0.1)
            math_03 = MathTex("0+2=2", font_size=24, color=GREEN).next_to(edge_03, LEFT, buff=0.1)
            self.play(FadeIn(math_01), FadeIn(math_03))

            # Update distance vector
            new_dist = self.create_dist_vector([0, 1, None, 2, None, None])
            new_dist.move_to(dist_group)
            self.play(Transform(dist_group, new_dist))

            # Mark nodes 1 and 3 as reached (green)
            self.play(
                animate_vertex_fill(graph.vertices[1], GREEN, 1),
                animate_vertex_fill(graph.vertices[3], GREEN, 1),
            )

            # Reset edge colors to indicate processed
            self.play(
                edge_01.animate.set_color(GREEN).set_stroke(width=3),
                edge_03.animate.set_color(GREEN).set_stroke(width=3),
                FadeOut(math_01), FadeOut(math_03),
            )
            self.wait(0.5)

        # Phase D: Iteration 2 - relax from nodes 1 and 3
        with self.voiceover(
            """The second iteration explores from the newly reached nodes. From node one
            we reach node two with distance twelve. From node three we reach node four
            with distance six, and node five with distance three. All nodes are now
            reachable, but these may not be the shortest paths."""
        ):
            # Mark frontier nodes (1 and 3) as orange
            self.play(
                animate_vertex_fill(graph.vertices[1], ORANGE, 1),
                animate_vertex_fill(graph.vertices[3], ORANGE, 1),
            )

            # Highlight edges from frontier: 1->2, 3->4, 3->5
            edge_12 = self.get_edge_mobject(1, 2)
            edge_34 = self.get_edge_mobject(3, 4)
            edge_35 = self.get_edge_mobject(3, 5)

            self.play(
                edge_12.animate.set_color(YELLOW).set_stroke(width=5),
                edge_34.animate.set_color(YELLOW).set_stroke(width=5),
                edge_35.animate.set_color(YELLOW).set_stroke(width=5),
            )

            # Show math labels
            math_12 = MathTex("1+11=12", font_size=24, color=GREEN).next_to(edge_12, DOWN, buff=0.1)
            math_34 = MathTex("2+4=6", font_size=24, color=GREEN).next_to(edge_34, UP, buff=0.1)
            math_35 = MathTex("2+1=3", font_size=24, color=GREEN).next_to(edge_35, LEFT, buff=0.1)
            self.play(FadeIn(math_12), FadeIn(math_34), FadeIn(math_35))

            # Update distance vector
            new_dist = self.create_dist_vector([0, 1, 12, 2, 6, 3])
            new_dist.move_to(dist_group)
            self.play(Transform(dist_group, new_dist))

            # Mark nodes 2, 4, 5 as reached (green), and settle 1 and 3
            self.play(
                animate_vertex_fill(graph.vertices[1], GREEN, 1),
                animate_vertex_fill(graph.vertices[3], GREEN, 1),
                animate_vertex_fill(graph.vertices[2], GREEN, 1),
                animate_vertex_fill(graph.vertices[4], GREEN, 1),
                animate_vertex_fill(graph.vertices[5], GREEN, 1),
            )

            # Reset edge colors
            self.play(
                edge_12.animate.set_color(GREEN).set_stroke(width=3),
                edge_34.animate.set_color(GREEN).set_stroke(width=3),
                edge_35.animate.set_color(GREEN).set_stroke(width=3),
                FadeOut(math_12), FadeOut(math_34), FadeOut(math_35),
            )
            self.wait(0.5)

        # Phase E: Iteration 3 - MIN APPLIES!
        with self.voiceover(
            """In iteration three, the min accumulator finds shorter paths. Through node
            five, we can reach node four with distance five, better than six. Through
            node four, we reach node two with distance eleven, better than twelve. The
            existing values are replaced with the shorter distances."""
        ):
            # Highlight edges 5->4 and 4->2
            edge_54 = self.get_edge_mobject(5, 4)
            edge_42 = self.get_edge_mobject(4, 2)

            self.play(
                edge_54.animate.set_color(YELLOW).set_stroke(width=5),
                edge_42.animate.set_color(YELLOW).set_stroke(width=5),
            )

            # Show math labels indicating improvement
            math_54 = MathTex(r"3+2=5 < 6", font_size=24, color=GREEN).next_to(edge_54, RIGHT, buff=0.1)
            math_42 = MathTex(r"6+5=11 < 12", font_size=24, color=GREEN).next_to(edge_42, DOWN, buff=0.1)
            self.play(FadeIn(math_54), FadeIn(math_42))

            # Show checkmarks for successful updates
            check_54 = MathTex(r"\checkmark", font_size=36, color=GREEN).next_to(math_54, RIGHT, buff=0.1)
            check_42 = MathTex(r"\checkmark", font_size=36, color=GREEN).next_to(math_42, RIGHT, buff=0.1)
            self.play(FadeIn(check_54), FadeIn(check_42))

            # Update distance vector with flash effect on changed cells
            new_dist = self.create_dist_vector([0, 1, 11, 2, 5, 3])
            new_dist.move_to(dist_group)
            self.play(Transform(dist_group, new_dist))

            # Reset edges to green (processed)
            self.play(
                edge_54.animate.set_color(GREEN).set_stroke(width=3),
                edge_42.animate.set_color(GREEN).set_stroke(width=3),
                FadeOut(math_54), FadeOut(math_42),
                FadeOut(check_54), FadeOut(check_42),
            )
            self.wait(0.5)

        # Phase F: Iteration 4 - MIN APPLIES AGAIN!
        with self.voiceover(
            """In iteration four, node four's improved distance of five propagates
            further. Now the path to node two through node four is only ten, replacing
            eleven. This demonstrates how the algorithm iteratively relaxes distances
            until convergence."""
        ):
            # Highlight edge 4->2
            edge_42 = self.get_edge_mobject(4, 2)

            self.play(
                edge_42.animate.set_color(YELLOW).set_stroke(width=5),
            )

            # Show math label indicating improvement
            math_42 = MathTex(r"5+5=10 < 11", font_size=24, color=GREEN).next_to(edge_42, DOWN, buff=0.1)
            self.play(FadeIn(math_42))

            # Show checkmark for successful update
            check_42 = MathTex(r"\checkmark", font_size=36, color=GREEN).next_to(math_42, RIGHT, buff=0.1)
            self.play(FadeIn(check_42))

            # Update distance vector
            new_dist = self.create_dist_vector([0, 1, 10, 2, 5, 3])
            new_dist.move_to(dist_group)
            self.play(Transform(dist_group, new_dist))

            # Reset edge
            self.play(
                edge_42.animate.set_color(GREEN).set_stroke(width=3),
                FadeOut(math_42), FadeOut(check_42),
            )
            self.wait(0.5)

        # Phase G: Convergence check
        with self.voiceover(
            """In iteration five, no shorter paths are found. The algorithm has
            converged with optimal distances to all nodes."""
        ):
            # Highlight edges that could provide shorter paths: 5->4, 4->2
            edge_54 = self.get_edge_mobject(5, 4)
            edge_42 = self.get_edge_mobject(4, 2)

            self.play(
                edge_54.animate.set_color(YELLOW).set_stroke(width=5),
                edge_42.animate.set_color(YELLOW).set_stroke(width=5),
            )

            # Show math labels indicating no improvement
            math_54 = MathTex(r"3+2=5 = 5", font_size=24, color=GRAY).next_to(edge_54, RIGHT, buff=0.1)
            math_42 = MathTex(r"5+5=10 = 10", font_size=24, color=GRAY).next_to(edge_42, DOWN, buff=0.1)
            self.play(FadeIn(math_54), FadeIn(math_42))

            self.wait(0.5)

            # Show no update with X marks
            x_54 = MathTex(r"\times", font_size=36, color=RED).next_to(math_54, RIGHT, buff=0.1)
            x_42 = MathTex(r"\times", font_size=36, color=RED).next_to(math_42, RIGHT, buff=0.1)
            self.play(FadeIn(x_54), FadeIn(x_42))

            # Reset edges
            self.play(
                edge_54.animate.set_color(GREEN).set_stroke(width=3),
                edge_42.animate.set_color(GREEN).set_stroke(width=3),
                FadeOut(math_54), FadeOut(math_42),
                FadeOut(x_54), FadeOut(x_42),
            )
            self.wait(0.5)

        # Phase H: Conclusion
        with self.voiceover(
            """The final vector contains the shortest distance from the source to every
            reachable node. Notice how node two was updated three times as the algorithm
            discovered progressively shorter paths."""
        ):
            # Pulse the final distance vector
            self.play(dist_group.animate.scale(1.1))
            self.play(dist_group.animate.scale(1/1.1))

            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(code), FadeOut(graph), FadeOut(weight_labels),
            FadeOut(dist_group),
        )
        self.wait(0.5)

    def create_code_display(self):
        """Create the Python code display."""
        code_string = """def sssp(A, source):
    n = A.nrows
    dist = Vector(float, size=n)
    dist[source] = 0.0

    for iteration in range(n - 1):
        new_dist = dist.dup()
        new_dist(accum=min) << dist.vxm(A, min_plus)

        if new_dist.isequal(dist):
            break
        dist = new_dist

    return dist"""

        code = Code(
            code_string=code_string,
            language="python",
            background="window",
        )
        return code

    def create_graph_display(self):
        """Create the graph with edge weight labels."""
        matrix_data = SCENE1_MATRIX_DATA
        num_rows = len(matrix_data)

        # Triangle layout for 6 nodes
        sqrt3 = math.sqrt(3)
        positions = {
            0: np.array([-3, -sqrt3, 0]),      # Base left
            1: np.array([0, -sqrt3, 0]),       # Base center
            2: np.array([3, -sqrt3, 0]),       # Base right
            3: np.array([-1.5, 0, 0]),         # Middle left
            4: np.array([1.5, 0, 0]),          # Middle right
            5: np.array([0, sqrt3, 0])         # Top point
        }

        # Create vertices as labeled dots
        vertices = {}
        for i in range(num_rows):
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.25, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        # Find edges from matrix
        edges_data = []
        for i in range(num_rows):
            for j in range(num_rows):
                if matrix_data[i][j] != 0:
                    edges_data.append((i, j, matrix_data[i][j]))

        # Create directed arrows for edges
        edges = VGroup()
        edge_dict = {}
        weight_labels = VGroup()

        for i, j, weight in edges_data:
            start = positions[i]
            end = positions[j]

            arrow = Arrow(
                start, end,
                color=BLUE,
                buff=0.3,
                stroke_width=3,
                tip_length=0.15,
                max_tip_length_to_length_ratio=0.2
            )
            edges.add(arrow)
            edge_dict[(i, j)] = arrow

            # Add weight label at midpoint with perpendicular offset
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.25
            label = Text(str(weight), font_size=18, color=YELLOW).move_to(mid + perp)
            weight_labels.add(label)

        # Combine into graph group
        graph = VGroup(edges, *vertices.values())
        graph.vertices = vertices
        graph.edges = edges
        graph.edge_dict = edge_dict

        return graph, weight_labels

    def create_dist_vector(self, values):
        """Create a distance vector display."""
        cells = VGroup()
        cell_width = 0.6

        for i, val in enumerate(values):
            rect = Square(side_length=cell_width, stroke_width=2, stroke_color=WHITE)
            if val is not None:
                text = Text(str(val), font_size=20).move_to(rect)
                cell = VGroup(rect, text)
            else:
                cell = rect
            cells.add(cell)

        cells.arrange(RIGHT, buff=0.05)

        # Index labels below
        indices = VGroup(*[
            Text(str(i), font_size=14, color=GRAY).next_to(cells[i], DOWN, buff=0.1)
            for i in range(len(values))
        ])

        label = Text("dist:", font_size=20).next_to(cells, LEFT, buff=0.3)
        return VGroup(label, cells, indices)

    def get_edge_mobject(self, i, j):
        """Get the edge arrow mobject for edge (i, j)."""
        return self.graph.edge_dict.get((i, j))
