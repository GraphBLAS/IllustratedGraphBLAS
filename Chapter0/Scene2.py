import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    CHAPTER0_MATRIX_DATA,
    create_labeled_matrix,
    hide_zero_entries,
    get_non_zero_positions,
    create_adjacency_digraph,
    animate_vertex_fill,
    setup_scene,
)


class Scene2(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        matrix_data = CHAPTER0_MATRIX_DATA
        num_rows, num_cols = len(matrix_data), len(matrix_data[0])

        dense_matrix, row_labels, col_labels = create_labeled_matrix(matrix_data)

        with self.voiceover(
            """This matrix starts with many values, but most of them
            are zero. This is a common feature of many problems where
            the dataset or the connections between data points are
            sparse. Sparse data is everywhere, and efficiently
            analyzing it presents unique computing challenges."""
        ):
            self.play(Write(dense_matrix), *[Write(label) for label in row_labels + col_labels])

        non_zero_positions = get_non_zero_positions(matrix_data)

        highlights = [
            SurroundingRectangle(dense_matrix.get_entries()[i * num_cols + j], color=BLUE)
            for i, j, _ in non_zero_positions
        ]

        with self.voiceover(
            """Here we highlight the non-zero values, which carry the meaningful
            information in this matrix."""
        ):
            self.play(*[Create(highlight) for highlight in highlights])

        fade_out_animations = hide_zero_entries(dense_matrix, matrix_data)

        with self.voiceover(
            """Let's ignore the zero values, leaving us with only the non-zero
            elements."""
        ):
            self.play(*fade_out_animations)
            self.play(*[FadeOut(highlight) for highlight in highlights])

        matrix_and_labels = VGroup(dense_matrix, *row_labels, *col_labels)
        self.play(matrix_and_labels.animate.to_edge(LEFT))

        # Create the graph, shift it to the right, and raise it by 0.5 units
        nodes = [i for i in range(num_rows)]
        edges = [(i, j) for i, j, _ in non_zero_positions]

        graph = create_adjacency_digraph(matrix_data)

        self.play(Create(graph.to_edge(RIGHT).shift(UP * 0.5)))  # Shift graph to the right and up by 0.5 units

        edge_labels = VGroup()

        with self.voiceover(
                """We can represent this matrix as a graph, where rows
                and columns correspond to nodes, and non-zero elements
                become edges connecting them. As we step through each
                row, you can see how the elements in that row
                correspond to the outgoing edges from that node. The
                value stored in each position represents the weight or
                strength of that connection."""
        ):
            previous_node_highlight = None  # Store the previous node highlight
            for i in range(num_rows):  # Iterate over rows
                row_highlight = SurroundingRectangle(dense_matrix.get_rows()[i], color=YELLOW, buff=0.1)

                # Highlight the current node in the graph
                node_highlight = animate_vertex_fill(graph.vertices[i], YELLOW, 1)

                # Highlight outgoing edges for the current node
                outgoing_edges = [
                    graph.edges[(i, j)].animate.set_stroke(color=YELLOW, width=4)
                    for j in range(num_cols) if (i, j) in graph.edges
                ]

                # Play the row, node, and edge highlights
                self.play(Create(row_highlight), node_highlight, *outgoing_edges)

                for j in range(num_cols):
                    if matrix_data[i][j] != 0:
                        value = matrix_data[i][j]
                        value_text = Tex(str(value)).move_to(dense_matrix.get_entries()[i * num_cols + j].get_center())
                        edge_center = graph.edges[(i, j)].get_center()

                        # Move the value to the graph edge with a slight delay
                        self.play(value_text.animate.move_to(edge_center))
                        edge_labels.add(value_text)
                        self.wait(0.1)  # Small delay for clarity

                # Unhighlight the previous node and edges
                if previous_node_highlight:
                    self.play(animate_vertex_fill(previous_node_highlight, WHITE, 0.5))
                self.play(FadeOut(row_highlight))  # Remove row highlight after processing
                previous_node_highlight = graph.vertices[i]  # Store the current node as previous

        matrix_label = Tex("Adjacency Matrix").next_to(dense_matrix, DOWN)
        graph_label = Tex("Graph").next_to(graph, DOWN)

        with self.voiceover(
                """This type of matrix, where elements describe
                connections in a graph, is called an adjacency matrix.
                Adjacency matrices appear throughout mathematics,
                science, and computing, including machine learning and
                artificial intelligence. They provide a powerful way
                to express graph structures and algorithms using the
                operations of linear algebra, especially matrix
                multiplication."""
        ):
            self.play(FadeIn(matrix_label), FadeIn(graph_label))

        self.wait(1)
        self.play(
            FadeOut(matrix_and_labels),
            FadeOut(graph),
            FadeOut(matrix_label),
            FadeOut(graph_label),
            FadeOut(edge_labels),
            run_time=1  # Smooth fade-out transition
        )
        self.wait(0.5)
