from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class Scene3(VoiceoverScene, Scene):
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

        vector_data = [[0], [0], [2], [0], [0], [0]]
        initial_result_data = [[0], [10], [0], [0], [10], [0]]

        dense_matrix = Matrix(matrix_data, v_buff=0.5, h_buff=0.5).scale(1.5)
        column_vector = Matrix(vector_data, v_buff=0.5).scale(1.5)
        result_vector = Matrix(initial_result_data, v_buff=0.5).scale(1.5)

        at_symbol = Tex("@").scale(2)
        equal_symbol = Tex("=").scale(2)

        expression_group = VGroup(
            dense_matrix, at_symbol, column_vector, equal_symbol, result_vector
        ).arrange(buff=0.5)

        for entry in result_vector.get_entries():
            entry.set_opacity(0)

        with self.voiceover(
            "Here, we see the dense representation of the same matrix on the left, alongside a column vector on the right. This column vector contains only one non-zero element, with a value of two in the third position, while all other values are zero."
        ):
            self.play(Write(expression_group))
            self.wait(1)

        with self.voiceover(
            "Now, we multiply the matrix by the vector to get a result. Notice that each element in the column vector scales the corresponding column of the matrix. Sparse matrices and vectors typically contain many zeros, meaning that most operations are multiplying by zero and result in zero. This ends up being a waste of space, time, and energy for many sparse problems that have no dense representations, like graphs."
        ):
            for j in range(6):
                col_highlight = SurroundingRectangle(dense_matrix.get_columns()[j], color=YELLOW, buff=0.1)
                vector_entry = column_vector.get_entries()[j]
                vector_highlight = SurroundingRectangle(vector_entry, color=YELLOW, buff=0.1)

                self.play(Create(col_highlight), Create(vector_highlight))

                for i in range(6):
                    matrix_entry = dense_matrix.get_entries()[i * 6 + j]
                    result_entry = result_vector.get_entries()[i]

                    if j == 2 and matrix_data[i][j] != 0:
                        self.play(result_entry.animate.set_opacity(1))
                        self.play(TransformFromCopy(matrix_entry, result_entry))
                    else:
                        self.play(matrix_entry.animate.set_opacity(0.3), run_time=0.25)

                self.wait(0.3)
                self.play(FadeOut(col_highlight), FadeOut(vector_highlight))

        # Create the graph representation
        nodes = [i for i in range(6)]
        edges = [(i, j) for i in range(6) for j in range(6) if matrix_data[i][j] != 0]

        graph = DiGraph(
            vertices=nodes,
            edges=edges,
            layout="kamada_kawai",
            labels=True,
            edge_config={"stroke_color": BLUE}
        ).scale(1.3)

        self.play(FadeOut(expression_group))
        with self.voiceover(
            "Here is the sparse matrix and graph representation. Each element in the matrix corresponds to an edge in the graph, highlighting the connection between matrix algebra and graph theory."
        ):
            # Final Animation with Matrix, Vector, and Graph
            sparse_matrix = Matrix(matrix_data, v_buff=0.5, h_buff=0.5).scale(1.5)
            for i, row in enumerate(matrix_data):
                for j, value in enumerate(row):
                    if value == 0:
                        sparse_matrix.get_entries()[i * len(row) + j].set_opacity(0)

            # Position the matrix and vector on the left side of the screen
            sparse_matrix.to_edge(LEFT, buff=0.5)
            sparse_vector = Matrix(vector_data, v_buff=0.5).scale(1.5).next_to(sparse_matrix, RIGHT, buff=0.5)
            self.play(Create(graph.to_edge(RIGHT)))

        with self.voiceover(
            "We now see the sparse matrix and the corresponding input vector. The non-zero element in the vector corresponds to the highlighted column in the matrix and the associated node and edges in the graph."
        ):
            self.play(FadeIn(sparse_matrix), FadeIn(sparse_vector))

            vector_highlight = SurroundingRectangle(sparse_vector.get_entries()[2], color=YELLOW, buff=0.1)
            self.play(Create(vector_highlight))

            col_highlight = SurroundingRectangle(sparse_matrix.get_columns()[2], color=YELLOW, buff=0.1)
            self.play(Create(col_highlight))

            node_highlight = ApplyMethod(graph.vertices[2].set_fill, YELLOW, 1)
            incoming_edges = [
                graph.edges[(j, 2)].animate.set_stroke(color=YELLOW, width=4)
                for j in range(6) if (j, 2) in graph.edges
            ]
            self.play(node_highlight, *incoming_edges)

        self.wait(2)
