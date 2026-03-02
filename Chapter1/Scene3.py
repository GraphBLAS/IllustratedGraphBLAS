import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import CHAPTER0_MATRIX_DATA, create_labeled_matrix, hide_zero_entries, setup_scene


class Scene3(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Tex("Matrix-Vector Multiplication").scale(1.5).to_edge(UP)

        # Matrix and vector data (same as Chapter 0)
        matrix_data = CHAPTER0_MATRIX_DATA
        num_cols = len(matrix_data[0])
        vector_data = [[0], [0], [0], [2], [0], [0]]  # value 2 at position 3
        # A @ v: row 0 col 3 has value 2, v[3]=2, so result[0] = 2*2 = 4
        result_data = [[4], [0], [0], [0], [0], [0]]

        with self.voiceover(
            """Now let's perform matrix-vector multiplication, the core
            operation of GraphBLAS. We have our matrix A and vector v
            from before."""
        ):
            self.play(Write(title))

            # Create matrix with labels (same size as Chapter 0)
            matrix, row_labels, col_labels = create_labeled_matrix(
                matrix_data, scale=1, v_buff=0.5, h_buff=0.5
            )

            # Create vector
            vector = Matrix(vector_data, v_buff=0.5).scale(1)
            vector_label = Tex("v").scale(0.8)

            # Create result vector (initially hidden)
            result = Matrix(result_data, v_buff=0.5).scale(1)
            result_label = Tex("w").scale(0.8)

            # Symbols
            at_symbol = Tex("@").scale(1.5)
            equals_symbol = Tex("=").scale(1.5)

            # Arrange: A @ v = w
            matrix_label = Tex("A").scale(0.8)

            equation = VGroup(
                matrix, at_symbol, vector, equals_symbol, result
            ).arrange(RIGHT, buff=0.4)
            equation.shift(DOWN * 0.3)

            # Position labels
            matrix_label.next_to(matrix, UP, buff=0.5)
            vector_label.next_to(vector, UP, buff=0.5)
            result_label.next_to(result, UP, buff=0.5)

            # Update row/col labels to matrix position
            for i, label in enumerate(row_labels):
                label.next_to(matrix.get_rows()[i], LEFT * 2)
            for j, label in enumerate(col_labels):
                label.next_to(matrix.get_columns()[j], UP * 1.2)

            # Hide zeros and result initially
            for i, row in enumerate(matrix_data):
                for j, val in enumerate(row):
                    if val == 0:
                        matrix.get_entries()[i * num_cols + j].set_opacity(0)

            for i, row in enumerate(vector_data):
                if row[0] == 0:
                    vector.get_entries()[i].set_opacity(0)

            for entry in result.get_entries():
                entry.set_opacity(0)

            self.play(
                FadeIn(matrix), FadeIn(vector), FadeIn(result),
                FadeIn(at_symbol), FadeIn(equals_symbol),
                FadeIn(matrix_label), FadeIn(vector_label), FadeIn(result_label),
                *[FadeIn(label) for label in row_labels + col_labels]
            )
            self.wait(1)

        with self.voiceover(
            """In GraphBLAS, we use the m x v method for matrix-vector
            multiplication. The double less-than operator is the
            GraphBLAS assignment operator, which stores the result into
            the output vector w."""
        ):
            code = Code(
                code_string="""# Create output vector
w = gb.Vector(float, A.nrows)

# Matrix-vector multiply
w << A.mxv(v)""",
                language="python",
                background="window"
            ).scale(0.7)
            code.to_edge(DOWN, buff=0.3)
            self.play(FadeIn(code))
            self.wait(2)

        self.play(FadeOut(code))

        with self.voiceover(
            """Let's walk through the computation row by row. For each
            row in the matrix, we multiply the corresponding elements
            with the vector and sum the results. Because both the matrix
            and vector are sparse, most multiplications can be skipped."""
        ):
            # Animate row-by-row multiplication
            num_rows = len(matrix_data)
            for i in range(num_rows):
                row_highlight = SurroundingRectangle(
                    matrix.get_rows()[i], color=YELLOW, buff=0.1
                )
                result_entry = result.get_entries()[i]
                result_highlight = SurroundingRectangle(
                    result_entry, color=GREEN, buff=0.1
                )

                self.play(Create(row_highlight), run_time=0.2)

                # Show which vector elements contribute
                contributing = []
                for j in range(num_cols):
                    if matrix_data[i][j] != 0 and vector_data[j][0] != 0:
                        mat_entry = matrix.get_entries()[i * num_cols + j]
                        vec_entry = vector.get_entries()[j]
                        contributing.append(
                            SurroundingRectangle(
                                VGroup(mat_entry, vec_entry), color=BLUE, buff=0.05
                            )
                        )

                if contributing:
                    self.play(*[Create(c) for c in contributing], run_time=0.2)
                    self.play(
                        result_entry.animate.set_opacity(1),
                        Create(result_highlight),
                        run_time=0.3
                    )
                    self.play(
                        *[FadeOut(c) for c in contributing],
                        FadeOut(result_highlight),
                        run_time=0.2
                    )
                else:
                    self.wait(0.2)

                self.play(FadeOut(row_highlight), run_time=0.2)

        with self.voiceover(
            """Python also supports the at-sign operator as shorthand for
            matrix-vector multiplication, making the code even more
            concise and readable."""
        ):
            shorthand_code = Code(
                code_string="# Shorthand syntax\nw << A @ v",
                language="python",
                background="window"
            ).scale(0.8)
            shorthand_code.to_edge(DOWN, buff=0.5)
            self.play(FadeIn(shorthand_code))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(equation),
            FadeOut(matrix_label), FadeOut(vector_label), FadeOut(result_label),
            *[FadeOut(label) for label in row_labels + col_labels],
            FadeOut(shorthand_code)
        )
        self.wait(0.5)
