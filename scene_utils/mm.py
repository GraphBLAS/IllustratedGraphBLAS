from manim import *
import numpy as np
import random


def matrix_multiply(A, B):
    m, n, p = len(A), len(B[0]), len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]


class MatrixMultiplicationScene(Scene):
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

        # Generate two random 3x3 matrices
        matrix_A = np.random.randint(0, 10, (3, 3))
        matrix_B = np.random.randint(0, 10, (3, 3))

        # Format the matrices for display
        matrix_A_tex = Matrix(matrix_A.tolist(), v_buff=0.8)
        matrix_B_tex = Matrix(matrix_B.tolist(), v_buff=0.8)

        # Label the matrices
        A_label = MathTex("A = ").next_to(matrix_A_tex, LEFT)
        B_label = MathTex("B = ").next_to(matrix_B_tex, LEFT)

        # Position the matrices on the right side
        matrix_group = VGroup(
            VGroup(A_label, matrix_A_tex).arrange(RIGHT, buff=0.3),
            VGroup(B_label, matrix_B_tex).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1)

        # Add the function and matrices to the scene
        self.play(Write(code_box), run_time=2)
        self.play(Write(matrix_group), run_time=2)

        # Pause to display
        self.wait(2)
