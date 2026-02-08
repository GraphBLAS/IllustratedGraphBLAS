from manim import *
import numpy as np

class Scene2(Scene):
    def construct(self):
        # Define the function as code in a box
        code = """\
def matrix_multiply(A, B):
    m, n, p = len(A), len(B[0]), len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result"""
        code_box = Code(
            code=code,
            language="python",
            font_size=24,
            background="window",
            line_spacing=0.6,
        )
        code_box.scale(0.8).to_edge(LEFT, buff=1)

        # Define matrix dimensions
        m, n, p = 4, 4, 4  # Adjust these for different matrix sizes

        # Generate random matrices A and B
        matrix_A = np.random.randint(0, 10, (m, p))
        matrix_B = np.random.randint(0, 10, (p, n))
        matrix_C = np.zeros((m, n), dtype=int)

        # Format the matrices for display
        matrix_A_tex = Matrix(matrix_A.tolist(), v_buff=0.8).scale(0.5)
        matrix_B_tex = Matrix(matrix_B.tolist(), v_buff=0.8).scale(0.5)
        matrix_C_tex = Matrix(matrix_C.tolist(), v_buff=0.8).scale(0.5)

        # Label the matrices
        A_label = MathTex("A = ").scale(0.5).next_to(matrix_A_tex, LEFT)
        B_label = MathTex("B = ").scale(0.5).next_to(matrix_B_tex, LEFT)
        C_label = MathTex("C = ").scale(0.5).next_to(matrix_C_tex, LEFT)

        # Position the matrices vertically on the right
        matrix_group = VGroup(
            VGroup(A_label, matrix_A_tex).arrange(RIGHT, buff=0.3),
            VGroup(B_label, matrix_B_tex).arrange(RIGHT, buff=0.3),
            VGroup(C_label, matrix_C_tex).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1)

        # Add the function and matrices to the scene
        self.play(Write(code_box), run_time=2)
        self.play(Write(matrix_group), run_time=2)

        operation_text = Text("", font_size=24).next_to(code_box, DOWN)

        # Perform the matrix multiplication with animations
        for i in range(m):  # Rows of A
            for j in range(n):  # Columns of B
                for k in range(p):  # Summation index
                    # Highlight the current elements in A, B, and C
                    a_element = matrix_A_tex.get_entries()[i * p + k]
                    b_element = matrix_B_tex.get_entries()[k * n + j]
                    c_element = matrix_C_tex.get_entries()[i * n + j]

                    self.play(
                        a_element.animate.set_color(YELLOW),
                        b_element.animate.set_color(YELLOW),
                        c_element.animate.set_color(YELLOW),
                    )

                    # Update C[i][j]
                    current_value = matrix_C[i][j]
                    product = matrix_A[i][k] * matrix_B[k][j]
                    matrix_C[i][j] += product
                    result = matrix_C[i][j]

                    self.play(FadeOut(operation_text), run_time=0.1)
                    # Update operation text
                    text = (
                        f"C[{i}][{j}] = {current_value} + "
                        f"A[{i}][{k}] * B[{k}][{j}] = {current_value} + "
                        f"{matrix_A[i][k]} * {matrix_B[k][j]} = {result}"
                    )
                    # Create a text box to display the current operation
                    operation_text = Text(text, font_size=24).next_to(code_box, DOWN)

                    self.play(Write(operation_text), run_time=0.1)

                    new_value = MathTex(result, font_size=24).move_to(c_element)
                    self.play(Transform(c_element, new_value))

                    # Reset colors
                    self.play(
                        a_element.animate.set_color(WHITE),
                        b_element.animate.set_color(WHITE),
                        c_element.animate.set_color(WHITE),
                    )

        # Pause to display
        self.wait(2)
