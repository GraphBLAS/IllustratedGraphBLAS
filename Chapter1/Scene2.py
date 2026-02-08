import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import CHAPTER0_MATRIX_DATA, create_labeled_matrix, hide_zero_entries, get_speech_service


class Scene2(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(get_speech_service())

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

        with self.voiceover(
            """Notice how most entries in this matrix are zero. In
            GraphBLAS, these zeros are not stored at all - they simply
            don't exist in the sparse representation. This is what makes
            GraphBLAS efficient for large, sparse graphs."""
        ):
            # Hide zero entries to show sparse nature
            hide_anims = hide_zero_entries(matrix, matrix_data)
            self.play(*hide_anims)

            # Highlight non-zero positions (matching Chapter 0 matrix)
            nz_positions = [(0, 1), (0, 3), (1, 2), (3, 4), (3, 5), (4, 2), (5, 4)]
            nz_highlights = [
                SurroundingRectangle(
                    matrix.get_entries()[i * 6 + j], color=YELLOW, buff=0.1
                )
                for i, j in nz_positions
            ]
            self.play(*[Create(h) for h in nz_highlights])
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(matrix_code),
            FadeOut(matrix_group), *[FadeOut(h) for h in nz_highlights]
        )
        self.wait(0.5)
