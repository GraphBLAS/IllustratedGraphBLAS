from manim import *
import numpy as np
import random

code1 = """
def matrix_multiply(A, B):
  m = len(A)
  n = len(B[0])
  p = len(B)
  C = [[0] * n for _ in range(m)]
  for i in range(m):
    for j in range(n):
      for k in range(p):
        C[i][j] += A[i][k] * B[k][j]
  return result
"""

code2 = """
from operator import add, mul
def op(A, B, C, i, j, k):
    C[i][j] = add(mul(A[i][k],
              B[k][j]),
              C[i][j])

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                op(A, B, C, i, j, k)
    return result
"""

code3 = """
from operator import min, add
def op(A, B, C, i, j, k):
    C[i][j] = min(add(A[i][k],
              B[k][j]),
              C[i][j])

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                op(A, B, C, i, j, k)
    return result
"""

class Scene1(Scene):
    def construct(self):
        # Define the function as code in a box
        for code in (code1, code2, code3):
            code_box = Code(
                code=code,
                language="python",
                font_size=24,
                background="window",
                insert_line_no=False,
                line_spacing=0.6,
            )
            code_box.scale(0.8).to_edge(LEFT, buff=1)

            matrix_A = np.random.randint(0, 10, (3, 3))
            matrix_B = np.random.randint(0, 10, (3, 3))
            matrix_C = np.zeros((3, 3), dtype=int)

            matrix_A_tex = Matrix(matrix_A.tolist(), v_buff=0.8).scale(0.75)
            matrix_B_tex = Matrix(matrix_B.tolist(), v_buff=0.8).scale(0.75)
            matrix_C_tex = Matrix(matrix_C.tolist(), v_buff=0.8).scale(0.75)

            A_label = MathTex("A = ").scale(0.5).next_to(matrix_A_tex, LEFT)
            B_label = MathTex("B = ").scale(0.5).next_to(matrix_B_tex, LEFT)
            C_label = MathTex("C = ").scale(0.5).next_to(matrix_C_tex, LEFT)

            matrix_group = VGroup(
                VGroup(A_label, matrix_A_tex).arrange(RIGHT, buff=0.3),
                VGroup(B_label, matrix_B_tex).arrange(RIGHT, buff=0.3),
                VGroup(C_label, matrix_C_tex).arrange(RIGHT, buff=0.3),
            ).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1)

            # Add the function and matrices to the scene
            self.play(Write(code_box), run_time=2)
            self.play(Write(matrix_group), run_time=2)

            # Pause to display
            self.wait(2)
            self.play(FadeOut(code_box), FadeOut(matrix_group))
