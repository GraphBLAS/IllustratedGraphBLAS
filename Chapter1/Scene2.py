import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import CHAPTER0_MATRIX_DATA, create_labeled_matrix, hide_zero_entries, setup_scene
from scene_utils.graph_utils import create_karate_graph


class Scene2(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Tex("Creating Matrices and Vectors").scale(1.5).to_edge(UP)

        with self.voiceover(
            """GraphBLAS uses coordinate format, or C O O format, to
            create sparse vectors and matrices. For a vector, we provide
            two arrays: the indices where values exist, and the values
            themselves. Here we create a vector of size 6 with a single
            value at position 3."""
        ):
            self.play(Write(title))

            vector_code = Code(
                code_string="""import graphblas as gb

# Vector from COO format
v = gb.Vector.from_coo(
    [3],    # indices
    [2],    # values
    size=6
)""",
                language="python",
                background="window"
            ).scale(0.7)
            vector_code.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
            self.play(FadeIn(vector_code))

            # Visual representation of the vector (same as Chapter 0)
            vector_data = [[0], [0], [0], [2], [0], [0]]
            vector_visual = Matrix(vector_data, v_buff=0.5).scale(1.5)
            vector_visual.to_edge(RIGHT, buff=1.5).shift(DOWN * 0.5)

            vector_labels = [Tex(str(i)) for i in range(6)]
            for i, label in enumerate(vector_labels):
                label.next_to(vector_visual.get_rows()[i], LEFT, buff=1)

            self.play(FadeIn(vector_visual), *[FadeIn(label) for label in vector_labels])

            # Highlight non-zero entry
            nz_highlights = [
                SurroundingRectangle(vector_visual.get_entries()[3], color=YELLOW, buff=0.1),
            ]
            self.play(*[Create(h) for h in nz_highlights])
            self.wait(1)

        self.play(
            FadeOut(vector_code), FadeOut(vector_visual),
            *[FadeOut(label) for label in vector_labels],
            *[FadeOut(h) for h in nz_highlights]
        )

        with self.voiceover(
            """For matrices, we use three arrays: row indices, column
            indices, and values. This creates a sparse 6 by 6 matrix
            with only 7 non-zero elements."""
        ):
            matrix_code = Code(
                code_string="""# Matrix from COO format
A = gb.Matrix.from_coo(
    [0, 0, 1, 3, 3, 4, 5],  # rows
    [1, 3, 2, 4, 5, 2, 4],  # cols
    [1, 2, 5, 2, 9, 5, 2],  # values
    nrows=6, ncols=6
)""",
                language="python",
                background="window"
            ).scale(0.65)
            matrix_code.to_edge(LEFT, buff=0.3).shift(DOWN * 0.5)
            self.play(FadeIn(matrix_code))

            # Visual matrix representation (same as Chapter 0)
            matrix_data = CHAPTER0_MATRIX_DATA

            matrix, row_labels, col_labels = create_labeled_matrix(
                matrix_data, scale=1.5, v_buff=0.5, h_buff=0.5
            )
            matrix_group = VGroup(matrix, *row_labels, *col_labels)
            matrix_group.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

            self.play(FadeIn(matrix_group))
            self.wait(1)

        # Transition: fade out COO code, keep matrix
        self.play(FadeOut(matrix_code))

        # Section 4: from_dicts constructor
        with self.voiceover(
            """For more Pythonic construction, GraphBLAS supports
            dictionary format. Nested dictionaries map row indices to
            column-value pairs. This is intuitive for representing
            adjacency lists where each row describes outgoing edges."""
        ):
            dict_code = Code(
                code_string="""# Matrix from nested dictionaries
A = gb.Matrix.from_dicts({
    0: {1: 1, 3: 2},
    1: {2: 5},
    3: {4: 2, 5: 9},
    4: {2: 5},
    5: {4: 2}
}, nrows=6, ncols=6)""",
                language="python",
                background="window"
            ).scale(0.65)
            dict_code.to_edge(LEFT, buff=0.3).shift(DOWN * 0.5)
            self.play(FadeIn(dict_code))
            self.wait(1)

        # Transition to edgelist
        self.play(FadeOut(dict_code))

        # Section 5: from_edgelist constructor
        with self.voiceover(
            """Edge lists are common in graph data. GraphBLAS can build
            matrices directly from sequences of row-column pairs or
            triples that include values. This mirrors how graph edges
            are often stored in files."""
        ):
            edgelist_code = Code(
                code_string="""# Matrix from edge list
edges = [
    (0, 1, 1), (0, 3, 2),
    (1, 2, 5),
    (3, 4, 2), (3, 5, 9),
    (4, 2, 5),
    (5, 4, 2)
]
A = gb.Matrix.from_edgelist(
    edges, nrows=6, ncols=6
)""",
                language="python",
                background="window"
            ).scale(0.65)
            edgelist_code.to_edge(LEFT, buff=0.3).shift(DOWN * 0.5)
            self.play(FadeIn(edgelist_code))
            self.wait(1)

        # Transition to mmread - clear the small matrix
        self.play(FadeOut(edgelist_code), FadeOut(matrix_group))

        # Section 6: Matrix Market file reading
        with self.voiceover(
            """Real-world graphs are often stored in Matrix Market format.
            GraphBLAS can read these files directly. Here we load the
            Zachary karate club network, a classic 34-node social network
            from 1977."""
        ):
            mmread_code = Code(
                code_string="""# Read Matrix Market file
import graphblas.io as gbio

A = gbio.mmread("karate.mtx")
print(A)  # 34x34 matrix, 78 edges""",
                language="python",
                background="window"
            ).scale(0.7)
            mmread_code.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
            self.play(FadeIn(mmread_code))

            # Show the karate graph
            karate_graph = create_karate_graph(scale=0.08, node_radius=0.2)
            karate_graph.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
            self.play(FadeIn(karate_graph))

            # Add info label
            info_label = Tex("34 nodes, 78 edges").scale(0.7)
            info_label.next_to(karate_graph, DOWN, buff=0.3)
            self.play(FadeIn(info_label))
            self.wait(1)

        # Transition back to sparse philosophy - recreate the 6x6 matrix
        self.play(FadeOut(mmread_code), FadeOut(karate_graph), FadeOut(info_label))

        # Recreate matrix for sparse philosophy section
        matrix2, row_labels2, col_labels2 = create_labeled_matrix(
            matrix_data, scale=1.5, v_buff=0.5, h_buff=0.5
        )
        matrix_group2 = VGroup(matrix2, *row_labels2, *col_labels2)
        matrix_group2.move_to(ORIGIN)
        self.play(FadeIn(matrix_group2))

        with self.voiceover(
            """Notice how most entries in this matrix are zero. In
            GraphBLAS, these zeros are not stored at all - they simply
            don't exist in the sparse representation. This is what makes
            GraphBLAS efficient for large, sparse graphs."""
        ):
            # Hide zero entries to show sparse nature
            hide_anims = hide_zero_entries(matrix2, matrix_data)
            self.play(*hide_anims)

            # Highlight non-zero positions (matching Chapter 0 matrix)
            nz_positions = [(0, 1), (0, 3), (1, 2), (3, 4), (3, 5), (4, 2), (5, 4)]
            nz_highlights2 = [
                SurroundingRectangle(
                    matrix2.get_entries()[i * 6 + j], color=YELLOW, buff=0.1
                )
                for i, j in nz_positions
            ]
            self.play(*[Create(h) for h in nz_highlights2])
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(matrix_group2), *[FadeOut(h) for h in nz_highlights2]
        )
        self.wait(0.5)
