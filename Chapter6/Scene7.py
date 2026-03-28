import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene, create_sparse_matrix


# Matrix M for reduce operations demonstration
# Non-zero values: 3, 2, 4, 1, 5
M_DATA = [
    [0, 3, 2, 0],
    [0, 0, 4, 0],
    [0, 0, 0, 1],
    [5, 0, 0, 0],
]

# Row sums: row 0: 3+2=5, row 1: 4, row 2: 1, row 3: 5
ROW_SUMS = [[5], [4], [1], [5]]

# Column sums: col 0: 5, col 1: 3, col 2: 2+4=6, col 3: 1
COL_SUMS = [[5, 3, 6, 1]]

# Total sum: 3 + 2 + 4 + 1 + 5 = 15
SCALAR_SUM = 15


def create_sparse_vector(data, scale=0.6, horizontal=False):
    """
    Create a sparse vector (column or row) with zero entries hidden.

    Args:
        data: List of values for the vector (1D list)
        scale: Scale factor for the vector
        horizontal: If True, create a row vector; if False, create a column vector

    Returns:
        Matrix object representing the vector with zeros hidden
    """
    if horizontal:
        vector_data = [data]
    else:
        vector_data = [[val] for val in data]

    vector = Matrix(vector_data, v_buff=0.8, h_buff=1.0).scale(scale)

    # Hide zero entries
    for i, val in enumerate(data):
        if val == 0:
            vector.get_entries()[i].set_opacity(0)

    return vector


class Scene7(VoiceoverScene, Scene):
    """Reduce Operations: reduce_scalar, reduce_rowwise, reduce_columnwise."""

    def construct(self):
        setup_scene(self)

        title = Text("Reduce Operations", font_size=44).to_edge(UP)

        with self.voiceover(
            """Reduce operations collapse matrix dimensions using a monoid.
            We can reduce an entire matrix to a single scalar, or reduce
            along rows or columns to produce vectors."""
        ):
            self.play(Write(title))

            # Create and show the source matrix
            mat_m = create_sparse_matrix(M_DATA, scale=0.6)
            mat_m.move_to(ORIGIN)
            mat_label = MathTex("M", font_size=36).next_to(mat_m, UP, buff=0.3)

            self.play(FadeIn(mat_m), Write(mat_label))
            self.wait(1)

        # --- Part 1: reduce_scalar ---
        with self.voiceover(
            """First, reduce to scalar. This sums all values in the matrix
            to produce a single number. Our matrix contains 3, 2, 4, 1, and 5.
            Adding them gives 15."""
        ):
            # Move matrix to left side
            self.play(
                mat_m.animate.shift(LEFT * 4.5),
                mat_label.animate.shift(LEFT * 4.5),
            )

            # Show Python code
            code = Code(
                code_string="M.reduce_scalar(monoid.plus)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code.move_to(ORIGIN + UP * 0.5)
            self.play(FadeIn(code))

            # Show the calculation
            calc = MathTex(r"3 + 2 + 4 + 1 + 5 = 15", font_size=28, color=BLUE_C)
            calc.next_to(code, DOWN, buff=0.4)
            self.play(Write(calc))

            # Show result scalar
            result_scalar = MathTex("15", font_size=48, color=BLUE)
            result_scalar.shift(RIGHT * 4.5)
            result_box = SurroundingRectangle(result_scalar, color=BLUE, buff=0.2)

            self.play(FadeIn(result_scalar), Create(result_box))
            self.wait(1)

        # Cleanup for next part (after voiceover finishes)
        self.play(
            FadeOut(code), FadeOut(calc),
            FadeOut(result_scalar), FadeOut(result_box),
        )

        # --- Part 2: reduce_rowwise ---
        with self.voiceover(
            """Next, reduce rowwise. This sums each row independently,
            producing a column vector. Row 0 has 3 plus 2 equals 5.
            Row 1 has just 4. Row 2 has just 1. Row 3 has just 5.
            The result is the vector 5, 4, 1, 5."""
        ):
            # Show Python code
            code = Code(
                code_string="M.reduce_rowwise(monoid.plus)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code.move_to(ORIGIN + UP * 0.5)
            self.play(FadeIn(code))

            # Create result vector (column)
            row_result_vec = Matrix(ROW_SUMS, v_buff=0.8).scale(0.6)
            row_result_vec.shift(RIGHT * 4.5)
            row_result_label = Text("row sums", font_size=20, color=GREEN)
            row_result_label.next_to(row_result_vec, UP, buff=0.3)

            self.play(FadeIn(row_result_vec), Write(row_result_label))

            # Highlight each row and corresponding result
            for row_idx in range(4):
                # Get the row from matrix
                row_rect = SurroundingRectangle(
                    mat_m.get_rows()[row_idx], color=YELLOW, buff=0.1
                )
                # Get corresponding result entry
                result_entry = row_result_vec.get_entries()[row_idx]
                result_rect = SurroundingRectangle(result_entry, color=GREEN, buff=0.1)

                self.play(Create(row_rect), Create(result_rect), run_time=0.4)
                self.wait(0.3)
                self.play(FadeOut(row_rect), FadeOut(result_rect), run_time=0.3)

            self.wait(0.5)

        # Cleanup for next part (after voiceover finishes)
        self.play(
            FadeOut(code), FadeOut(row_result_vec), FadeOut(row_result_label),
        )

        # --- Part 3: reduce_columnwise ---
        with self.voiceover(
            """Finally, reduce columnwise. This sums each column, producing
            a row vector. Column 0 has just 5. Column 1 has just 3.
            Column 2 has 2 plus 4 equals 6. Column 3 has just 1.
            The result is the vector 5, 3, 6, 1."""
        ):
            # Show Python code
            code = Code(
                code_string="M.reduce_columnwise(monoid.plus)",
                language="python",
                background="window",
                formatter_style="dracula",
            ).scale(0.7)
            code.move_to(ORIGIN + UP * 0.5)
            self.play(FadeIn(code))

            # Create result vector (row)
            col_result_vec = Matrix(COL_SUMS, h_buff=1.0).scale(0.6)
            col_result_vec.shift(RIGHT * 4.5)
            col_result_label = Text("column sums", font_size=20, color=PURPLE)
            col_result_label.next_to(col_result_vec, UP, buff=0.3)

            self.play(FadeIn(col_result_vec), Write(col_result_label))

            # Highlight each column and corresponding result
            for col_idx in range(4):
                # Get the column from matrix
                col_rect = SurroundingRectangle(
                    mat_m.get_columns()[col_idx], color=YELLOW, buff=0.1
                )
                # Get corresponding result entry
                result_entry = col_result_vec.get_entries()[col_idx]
                result_rect = SurroundingRectangle(result_entry, color=PURPLE, buff=0.1)

                self.play(Create(col_rect), Create(result_rect), run_time=0.4)
                self.wait(0.3)
                self.play(FadeOut(col_rect), FadeOut(result_rect), run_time=0.3)

            self.wait(0.5)

        with self.voiceover(
            """Reduce operations work with any monoid, not just addition.
            Using min finds the minimum value along each dimension.
            Using max finds the maximum. The choice of monoid depends
            on the problem being solved."""
        ):
            # Show monoid examples
            monoid_text = VGroup(
                MathTex(r"\text{plus: } 3 + 2 + 4 + 1 + 5 = 15", font_size=24),
                MathTex(r"\text{min: } \min(3, 2, 4, 1, 5) = 1", font_size=24),
                MathTex(r"\text{max: } \max(3, 2, 4, 1, 5) = 5", font_size=24),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            monoid_text.to_edge(DOWN, buff=0.8)

            self.play(Write(monoid_text))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(mat_m), FadeOut(mat_label),
            FadeOut(code), FadeOut(col_result_vec), FadeOut(col_result_label),
            FadeOut(monoid_text),
        )
        self.wait(0.5)
