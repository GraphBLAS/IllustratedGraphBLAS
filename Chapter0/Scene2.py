from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class Scene2(VoiceoverScene, Scene):
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
            """The core operation of Linear Algebra is multiplying matrices and
            vectors with each other.  In this first example, a vector
            is the left operand and a matrix is the right.  When
            multiplying a vector on the left, the vector is treated as
            a scaling factor for each of the rows in the matrix."""
        ):
            self.play(Write(expression_group))
            self.wait(0.5)

        with self.voiceover(
            """Now, we multiply the vector by the matrix to get a result. Each row
            in the matrix contributes to the corresponding element in
            the result vector, but notice how most of the operations
            involve multiplying by zero, which wastes time, memory
            space, and energy when there are truely only two actual
            calculations to be done."""
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
            """The GraphBLAS uses sparse data structures that efficiently store
            only elements in the matrix that are present in the data.
            Where there is no value there isn't a zero stored in
            memory to represent it, instead there is simply nothing.
            The GraphBLAS Library uses various compressed formats to
            store the data in memory using many different kinds of
            sparse algorithms.  """
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
            self.play(FadeIn(sparse_matrix), FadeIn(sparse_vector))

        with self.voiceover(
            """ The core concept of graph algebra is that every matrix can be seen
            as a graph, and every graph can be seen as one or more
            matrices.  Matrix multiplication in linear algebra
            translates to edge traversal in graphs, in the graph
            representation on the right the result vector corresponds
            to the outgoing edges for the node labeled 3 in the graph
            that go to nodes 4 and 5."""
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
