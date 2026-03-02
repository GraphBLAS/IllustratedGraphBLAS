import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene6(VoiceoverScene, Scene):
    """Summary and Algorithm Connections."""

    def construct(self):
        setup_scene(self)

        title = Text("Summary: Matrix-Matrix Multiply", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Recap table
        table_data = [
            ["Operation", "Meaning"],
            ["v @ A", "1-hop neighbors of v"],
            ["A @ A", "2-hop paths"],
            ["A^k", "k-hop paths"],
            ["Transitive Closure", "All reachable pairs"],
        ]

        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2},
        ).scale(0.55)
        table.next_to(title, DOWN, buff=0.6)

        # Style the header row
        for cell in table.get_rows()[0]:
            cell.set_color(YELLOW)

        with self.voiceover(
            """Let us review what we have learned. Vector-matrix multiply
            finds one-hop neighbors. A times A gives two-hop paths.
            A to the k gives k-hop paths. And transitive closure
            computes all reachable pairs through any path length."""
        ):
            self.play(Create(table))
            self.wait(2)

        self.play(FadeOut(table))

        # Preview triangle counting
        tri_title = Text("Preview: Triangle Counting", font_size=36).next_to(title, DOWN, buff=0.6)

        # Show A^2 ⊙ A (Hadamard product)
        formula = MathTex(
            r"\text{triangles} = A^2 \odot A"
        ).scale(1.0).next_to(tri_title, DOWN, buff=0.5)

        explanation = VGroup(
            Text("A² reveals shared neighbors", font_size=24),
            Text("Hadamard product with A selects triangles", font_size=24),
        ).arrange(DOWN, buff=0.2).next_to(formula, DOWN, buff=0.5)

        # Small triangle diagram
        tri_graph = self.create_triangle()
        tri_graph.scale(0.6).next_to(explanation, DOWN, buff=0.5)

        with self.voiceover(
            """In coming chapters, we will use matrix-matrix multiply for
            triangle counting. A squared reveals shared neighbors between
            nodes. The Hadamard product, element-wise multiplication with
            A, selects only those pairs that form closed triangles."""
        ):
            self.play(Write(tri_title))
            self.play(Write(formula))
            self.play(FadeIn(explanation))
            self.play(Create(tri_graph))
            self.wait(2)

        self.play(FadeOut(tri_title), FadeOut(formula), FadeOut(explanation), FadeOut(tri_graph))

        # Final message
        final_text = VGroup(
            Text("The pattern is always the same:", font_size=28),
            Text("1. Encode the graph as a matrix", font_size=24, color=BLUE),
            Text("2. Choose your semiring", font_size=24, color=GREEN),
            Text("3. Let algebra do the work", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.3)
        final_text.next_to(title, DOWN, buff=1)

        with self.voiceover(
            """The pattern is always the same: encode the graph as a matrix,
            choose your semiring, and let algebra do the work. Matrix
            multiplication handles the traversal logic, while the semiring
            determines what values are combined and how."""
        ):
            self.play(FadeIn(final_text, shift=UP))
            self.wait(2)

        self.play(FadeOut(final_text))

        # GraphBLAS Forum footer
        footer = Text("The GraphBLAS Forum").scale(0.75).to_edge(DOWN)

        with self.voiceover(
            """Thank you for watching. In the next chapter, we will explore
            more advanced operations and build on these foundations."""
        ):
            self.play(Write(footer))
            self.wait(2)

        # Cleanup
        self.play(FadeOut(title), FadeOut(footer))
        self.wait(0.5)

    def create_triangle(self):
        """Create a simple triangle graph."""
        import math
        positions = {
            0: np.array([-1, -0.5, 0]),
            1: np.array([1, -0.5, 0]),
            2: np.array([0, 0.8, 0]),
        }

        vertices = {}
        for i in range(3):
            label = MathTex(str(i), color=BLACK).scale(0.5)
            dot = LabeledDot(label, radius=0.2, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        edges_list = [(0, 1), (1, 2), (0, 2)]
        edges = VGroup()

        for i, j in edges_list:
            edge = Line(
                positions[i], positions[j],
                color=YELLOW, stroke_width=3, buff=0.22
            )
            edges.add(edge)

        graph = VGroup(edges, *vertices.values())
        return graph
