from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class Scene1(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        matrix_data = [
            [0, 1, 0, 2, 0, 0],
            [0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 9],
            [0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 2, 0]
        ]
        num_rows, num_cols = len(matrix_data), len(matrix_data[0])

        dense_matrix = Matrix(matrix_data, v_buff=0.5, h_buff=0.5).scale(1.5)
        row_labels = [Tex(str(i)) for i in range(num_rows)]
        col_labels = [Tex(str(j)) for j in range(num_cols)]

        for i, label in enumerate(row_labels):
            label.next_to(dense_matrix.get_rows()[i], LEFT * 3)
        for j, label in enumerate(col_labels):
            label.next_to(dense_matrix.get_columns()[j], UP * 1.5)

        with self.voiceover(
            """This matrix starts with many values, but most of them are zero.
            This is a sparse matrix. Sparse data is everywhere and it
            presents unique computing challenges when using Linear
            Algebra"""
        ):
            self.play(Write(dense_matrix), *[Write(label) for label in row_labels + col_labels])

        non_zero_positions = [
            (i, j, matrix_data[i][j])
            for i in range(num_rows) for j in range(num_cols) if matrix_data[i][j] != 0
        ]

        zero_positions = [(i, j) for i in range(num_rows) for j in range(num_cols) if matrix_data[i][j] == 0]

        highlights = [
            SurroundingRectangle(dense_matrix.get_entries()[i * num_cols + j], color=BLUE)
            for i, j, _ in non_zero_positions
        ]

        with self.voiceover(
            """Here we highlight the non-zero values, which carry the meaningful
            information in this matrix."""
        ):
            self.play(*[Create(highlight) for highlight in highlights])

        fade_out_animations = [
            dense_matrix.get_entries()[i * num_cols + j].animate.set_opacity(0)
            for i, j in zero_positions
        ]

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

        graph = DiGraph(
            vertices=nodes,
            edges=edges,
            layout="kamada_kawai",
            labels=True,
            edge_config={"stroke_color": BLUE}
        ).scale(1.3)

        self.play(graph.animate.to_edge(RIGHT).shift(UP * 0.5))  # Shift graph to the right and up by 0.5 units

        edge_labels = VGroup()

        with self.voiceover(
                """We can represent this matrix as a graph, where there is a row and
                column for each node, and elements become an edge
                connecting two nodes. The elements of each row vector
                in the matrix corresponds to the outgoing edges for
                the graph node associated with that row."""
        ):
            previous_node_highlight = None  # Store the previous node highlight
            for i in range(num_rows):  # Iterate over rows
                row_highlight = SurroundingRectangle(dense_matrix.get_rows()[i], color=YELLOW, buff=0.1)

                # Highlight the current node in the graph
                node_highlight = ApplyMethod(graph.vertices[i].set_fill, YELLOW, 1)

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
                    self.play(ApplyMethod(previous_node_highlight.set_fill, WHITE, 0.5))
                self.play(FadeOut(row_highlight))  # Remove row highlight after processing
                previous_node_highlight = graph.vertices[i]  # Store the current node as previous

        matrix_label = Tex("Adjacency Matrix").next_to(dense_matrix, DOWN)
        graph_label = Tex("Graph").next_to(graph, DOWN)

        with self.voiceover(
                """This type of matrix, where elements describe connections in a
                graph, is called an adjacency matrix.  It occurs all
                through math, science and computing, including machine
                learning and artificial intelligence.  It's a powerful
                way to express graph structures and algorithms using
                the operations of linear algebra like matrix
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
