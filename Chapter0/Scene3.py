import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import CHAPTER0_MATRIX_DATA, create_adjacency_digraph, setup_scene


class Scene3(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        matrix_data = CHAPTER0_MATRIX_DATA

        num_rows, num_cols = len(matrix_data), len(matrix_data[0])
        vector_data = [[0], [0], [0], [2], [0], [0]]  # Vertical vector
        initial_result_data = [[0], [0], [0], [0], [4], [18]]  # Example result vector

        # Create vertically oriented input and result vectors
        row_vector = Matrix(vector_data, v_buff=0.5).scale(1.5)
        dense_matrix = Matrix(matrix_data, v_buff=0.5, h_buff=0.5).scale(1.5)
        result_vector = Matrix(initial_result_data, v_buff=0.5).scale(1.5)

        # Create symbols for the equation
        at_symbol = Tex("@").scale(2)
        equal_symbol = Tex("=").scale(2)

        # Arrange the equation with vertical vectors but treat as row vectors
        expression_group = VGroup(
            row_vector, at_symbol, dense_matrix, equal_symbol, result_vector
        ).arrange(buff=0.5)

        for entry in result_vector.get_entries():
            entry.set_opacity(0)

        with self.voiceover(
            """The core operation of linear algebra is multiplying
            matrices and vectors. In this example, a vector is the
            left operand and a matrix is the right. When multiplying a
            vector on the left, each element of the vector acts as a
            scaling factor for the corresponding row in the matrix."""
        ):
            row_labels = [Tex(str(i)) for i in range(num_rows)]
            col_labels = [Tex(str(j)) for j in range(num_cols)]

            for i, label in enumerate(row_labels):
                label.next_to(row_vector.get_rows()[i], LEFT * 3)
            for j, label in enumerate(col_labels):
                label.next_to(dense_matrix.get_columns()[j], UP * 1.5)

            self.play(Write(expression_group), *[Write(label) for label in row_labels + col_labels])
            self.wait(0.5)

        with self.voiceover(
            """Now, we multiply the vector by the matrix to get a result. Each row
            in the matrix contributes to the corresponding element in
            the result vector, but notice how most of the operations
            involve multiplying by zero, which wastes time, memory
            space, and energy when there are truly only two
            calculations needed."""
        ):
            for i in range(6):  # Row-wise operations
                row_highlight = SurroundingRectangle(dense_matrix.get_rows()[i], color=YELLOW, buff=0.1)
                vector_entry = row_vector.get_entries()[i]
                vector_highlight = SurroundingRectangle(vector_entry, color=YELLOW, buff=0.1)

                self.play(Create(row_highlight), Create(vector_highlight))

                for j in range(6):
                    matrix_entry = dense_matrix.get_entries()[i * 6 + j]
                    result_entry = result_vector.get_entries()[j]

                    if i == 3 and matrix_data[i][j] != 0:
                        self.play(TransformFromCopy(matrix_entry, result_entry), run_time=0.5)
                        self.play(result_entry.animate.set_opacity(1), vector_entry.animate.set_opacity(1), run_time=0.5)
                    else:
                        self.play(matrix_entry.animate.set_opacity(0.3), vector_entry.animate.set_opacity(0.3), run_time=0.1)

                self.wait(0.3)
                self.play(FadeOut(row_highlight), FadeOut(vector_highlight), run_time=0.5)

        # Create the graph representation
        graph = create_adjacency_digraph(matrix_data)

        self.play(FadeOut(expression_group), FadeOut(*row_labels), FadeOut(*col_labels))
        with self.voiceover(
            """GraphBLAS uses sparse data structures that efficiently
            store only the non-zero elements in a matrix. Where there
            is no value, there isn't a zero stored in memory—instead,
            there is simply nothing. The GraphBLAS library uses
            various compressed formats to store data compactly,
            enabling efficient sparse algorithms that skip unnecessary
            work."""
        ):
            # Position the sparse matrix and result vector next to the graph
            sparse_matrix = Matrix(matrix_data, v_buff=0.5, h_buff=0.5).scale(1.5)
            for i, row in enumerate(matrix_data):
                for j, value in enumerate(row):
                    if value == 0:
                        sparse_matrix.get_entries()[i * len(row) + j].set_opacity(0)

            sparse_matrix.to_edge(LEFT, buff=0.5)
            sparse_vector = Matrix(initial_result_data, v_buff=0.5).scale(1.5).next_to(sparse_matrix, RIGHT, buff=0.5)

            for j, sparse_entry in enumerate(sparse_vector.get_entries()):
                if j in (4, 5):
                    sparse_entry.set_opacity(1)
                else:
                    sparse_entry.set_opacity(0)

            self.play(Create(graph.to_edge(RIGHT).shift(UP * 0.5)))

            # Recreate labels for the sparse matrix display
            row_labels = [Tex(str(i)) for i in range(num_rows)]
            col_labels = [Tex(str(j)) for j in range(num_cols)]

            for i, label in enumerate(row_labels):
                label.next_to(sparse_matrix.get_rows()[i], LEFT * 3)
            for j, label in enumerate(col_labels):
                label.next_to(sparse_matrix.get_columns()[j], UP * 1.5)
            self.play(FadeIn(sparse_matrix), FadeIn(sparse_vector), FadeIn(*row_labels), FadeIn(*col_labels))

        with self.voiceover(
            """The core concept of graph algebra is that every matrix
            can be seen as a graph, and every graph can be seen as one
            or more matrices. Matrix multiplication in linear algebra
            translates to edge traversal in graphs. In the graph on
            the right, the result vector corresponds to the outgoing
            edges from node 3, which connect to nodes 4 and 5."""
        ):
            vector_highlight = SurroundingRectangle(sparse_vector.get_entries()[4:6], color=YELLOW, buff=0.1)
            self.play(Create(vector_highlight))

            col_highlight = SurroundingRectangle(sparse_matrix.get_rows()[3], color=YELLOW, buff=0.1)
            self.play(Create(col_highlight))

            node_highlight = ApplyMethod(graph.vertices[3].set_fill, YELLOW, 1)
            outgoing_edges = [
                graph.edges[(3, j)].animate.set_stroke(color=YELLOW, width=4)
                for j in range(6) if (3, j) in graph.edges
            ]
            self.play(node_highlight, *outgoing_edges)

        self.wait(1)

        # Cleanup: FadeOut all remaining objects
        self.play(
            FadeOut(sparse_matrix),
            FadeOut(sparse_vector),
            FadeOut(graph),
            FadeOut(*row_labels),
            FadeOut(*col_labels),
            FadeOut(vector_highlight),
            FadeOut(col_highlight),
        )
        self.wait(0.5)
