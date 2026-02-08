import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import (
    CHAPTER0_MATRIX_DATA,
    create_adjacency_digraph,
    create_labeled_matrix,
    animate_vertex_fill,
    get_speech_service
)


class Scene4(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(get_speech_service())

        title = Tex("BFS with Matrix-Vector Multiplication").scale(1.3).to_edge(UP)

        # Use the same matrix as Chapter 0
        matrix_data = CHAPTER0_MATRIX_DATA
        num_nodes = len(matrix_data)

        with self.voiceover(
            """Breadth-first search is one of the most fundamental graph
            algorithms, and it can be elegantly expressed using
            matrix-vector multiplication. Let's see how this works with
            our 6-node graph."""
        ):
            self.play(Write(title))

            # Create graph and matrix side by side
            graph = create_adjacency_digraph(matrix_data, layout="triangle", scale=1)
            graph.to_edge(RIGHT, buff=1.0)

            # Create adjacency matrix visualization with labels
            matrix, row_labels, col_labels = create_labeled_matrix(
                matrix_data, scale=1, v_buff=0.5, h_buff=0.5
            )
            matrix.to_edge(LEFT, buff=1)

            # Reposition labels after moving the matrix
            for i, label in enumerate(row_labels):
                label.next_to(matrix.get_rows()[i], LEFT * 4)
            for j, label in enumerate(col_labels):
                label.next_to(matrix.get_columns()[j], UP * 2)

            # Hide zeros
            for i, row in enumerate(matrix_data):
                for j, val in enumerate(row):
                    if val == 0:
                        matrix.get_entries()[i * num_nodes + j].set_opacity(0)

            self.play(
                Create(graph),
                FadeIn(matrix),
                *[FadeIn(label) for label in row_labels + col_labels]
            )
            self.wait(1)

        with self.voiceover(
            """Here's the BFS algorithm in GraphBLAS. We start with a
            frontier vector q that marks our starting node. In each
            iteration, we multiply the adjacency matrix by the frontier
            to find all neighbors, then remove nodes we've already
            visited."""
        ):
            bfs_code = Code(
                code_string="""def bfs(A, start):
    n = A.nrows
    q = gb.Vector(bool, n)
    q[start] = True
    visited = gb.Vector(bool, n)

    while q.nvals > 0:
        visited << q | visited
        q_next = gb.Vector(bool, n)
        q_next << A.mxv(q, gb.semiring.any_pair)
        q_next[visited] = gb.NULL
        q = q_next

    return visited""",
                language="python",
                background="window"
            ).scale(0.55)
            bfs_code.move_to(ORIGIN).shift(DOWN * 0.5)
            self.play(FadeIn(bfs_code))
            self.wait(3)

        self.play(FadeOut(bfs_code))

        # # Move matrix up a bit for the animation
        # self.play(
        #     matrix.animate.shift(UP * 0.5),
        #     *[label.animate.shift(UP * 0.5) for label in row_labels + col_labels]
        # )

        with self.voiceover(
            """Let's trace through BFS starting from node 0. The yellow
            nodes represent our current frontier - the nodes we're
            exploring in this iteration."""
        ):
            # Initial state: node 0 is the frontier
            self.play(animate_vertex_fill(graph.vertices[0], YELLOW))

            # Highlight row 0 in matrix
            row_highlight = SurroundingRectangle(
                matrix.get_rows()[0], color=YELLOW, buff=0.1
            )
            self.play(Create(row_highlight))
            self.wait(1)

        with self.voiceover(
            """Multiplying the matrix by our frontier vector finds all
            neighbors of node 0. The matrix shows that node 0 connects
            to nodes 1 and 3, so they become our new frontier."""
        ):
            # Mark node 0 as visited (grey)
            self.play(animate_vertex_fill(graph.vertices[0], GREY))
            self.play(FadeOut(row_highlight))

            # Nodes 1 and 3 become the new frontier (from Chapter 0 matrix)
            self.play(
                animate_vertex_fill(graph.vertices[1], YELLOW),
                animate_vertex_fill(graph.vertices[3], YELLOW),
            )

            # Highlight edges from 0
            edges_from_0 = [(0, 1), (0, 3)]
            edge_anims = [
                graph.edges[e].animate.set_stroke(color=YELLOW, width=4)
                for e in edges_from_0 if e in graph.edges
            ]
            self.play(*edge_anims)
            self.wait(1)

        with self.voiceover(
            """In iteration 2, we explore from nodes 1 and 3. Node 1
            connects to node 2, and node 3 connects to nodes 4 and 5."""
        ):
            # Highlight rows 1 and 3
            row_highlights = [
                SurroundingRectangle(matrix.get_rows()[1], color=YELLOW, buff=0.1),
                SurroundingRectangle(matrix.get_rows()[3], color=YELLOW, buff=0.1),
            ]
            self.play(*[Create(h) for h in row_highlights])
            self.wait(0.5)

            # Mark 1 and 3 as visited
            self.play(
                animate_vertex_fill(graph.vertices[1], GREY),
                animate_vertex_fill(graph.vertices[3], GREY),
            )
            self.play(*[FadeOut(h) for h in row_highlights])

            # Nodes 2, 4, 5 become the new frontier
            self.play(
                animate_vertex_fill(graph.vertices[2], YELLOW),
                animate_vertex_fill(graph.vertices[4], YELLOW),
                animate_vertex_fill(graph.vertices[5], YELLOW),
            )

            # Highlight edges
            edges_iter2 = [(1, 2), (3, 4), (3, 5)]
            edge_anims = [
                graph.edges[e].animate.set_stroke(color=YELLOW, width=4)
                for e in edges_iter2 if e in graph.edges
            ]
            self.play(*edge_anims)
            self.wait(1)

        with self.voiceover(
            """The remaining nodes have edges, but they only point to
            nodes we've already visited. The frontier becomes empty and
            BFS terminates. We have visited all 6 nodes using just
            matrix-vector multiplication."""
        ):
            # Mark 2, 4, 5 as visited
            self.play(
                animate_vertex_fill(graph.vertices[2], GREY),
                animate_vertex_fill(graph.vertices[4], GREY),
                animate_vertex_fill(graph.vertices[5], GREY),
            )

            # Final state - all nodes grey (visited)
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(matrix),
            *[FadeOut(label) for label in row_labels + col_labels]
        )
        self.wait(0.5)
