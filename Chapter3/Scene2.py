import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import (
    CHAPTER0_MATRIX_DATA,
    create_adjacency_digraph,
    animate_vertex_fill,
    setup_scene,
)

class Scene2(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Masking in BFS", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Let's compare BFS with and without masking. Both algorithms
            produce the same result, but masking makes computation far more efficient."""
        ):
            # Show code comparison side-by-side
            code_without = Code(
                code_string="""# WITHOUT masking (inefficient)
def bfs_unmasked(A, start):
    q[start] = True
    while q.nvals > 0:
        visited << q | visited
        q = A.mxv(q, gb.semiring.any_pair)
        # Must manually filter visited nodes""",
                language="python",
                background="window"
            ).scale(0.55).to_edge(LEFT, buff=0.5)

            code_with = Code(
                code_string="""# WITH masking (efficient)
def bfs_masked(A, start):
    q[start] = True
    while q.nvals > 0:
        visited << q | visited
        q << A.mxv(q, gb.semiring.any_pair)[~visited]""",
                language="python",
                background="window"
            ).scale(0.55).to_edge(RIGHT, buff=0.5)

            self.play(Write(code_without), Write(code_with))
            self.wait(3)
            self.play(FadeOut(code_without), FadeOut(code_with))

        # Create graph for visualization
        matrix_data = CHAPTER0_MATRIX_DATA
        graph = create_adjacency_digraph(matrix_data, layout="triangle", scale=1.2)
        graph.shift(UP * 0.5)
        self.play(Create(graph))

        with self.voiceover(
            """Without masking, we recompute nodes we've already visited.
            Node 0's neighbors include previously visited nodes. We must
            manually filter these out after computation - wasteful."""
        ):
            # Show iteration 2 - without masking
            no_mask_label = Text("WITHOUT masking:", font_size=28, color=RED).to_edge(DOWN, buff=2)
            self.play(Write(no_mask_label))

            # Node 0 already visited (green)
            self.play(animate_vertex_fill(graph.vertices[0], GREEN))
            self.wait(0.5)

            # Compute from nodes 1, 3 (current frontier)
            self.play(
                animate_vertex_fill(graph.vertices[1], YELLOW),
                animate_vertex_fill(graph.vertices[3], YELLOW)
            )
            self.wait(1)

            # Result includes node 0 again (wasted - show in RED)
            waste_arrow = Arrow(
                start=graph.vertices[1].get_center(),
                end=graph.vertices[0].get_center(),
                color=RED,
                stroke_width=6
            )
            self.play(Create(waste_arrow))
            waste_label = Text("Redundant!", font_size=20, color=RED)
            waste_label.next_to(waste_arrow, LEFT)
            self.play(Write(waste_label))
            self.wait(2)

            self.play(
                FadeOut(waste_arrow),
                FadeOut(waste_label),
                FadeOut(no_mask_label)
            )

        with self.voiceover(
            """With complement masking, we compute only on unvisited nodes.
            The mask filters at the operation level, not after. This prevents
            redundant work and is dramatically faster on large sparse graphs.
            On a graph with millions of nodes, masking can reduce computation
            by orders of magnitude. It's not just a convenience - it's
            essential for scalable graph algorithms."""
        ):
            # Reset graph
            for i in range(len(graph.vertices)):
                self.play(animate_vertex_fill(graph.vertices[i], WHITE), run_time=0.2)

            # Show iteration 2 - with masking
            mask_label = Text("WITH masking:", font_size=28, color=GREEN).to_edge(DOWN, buff=2)
            self.play(Write(mask_label))

            # Node 0 already visited (green)
            self.play(animate_vertex_fill(graph.vertices[0], GREEN))

            # Show mask visualization
            mask_text = Text("visited = [T, F, F, F, F, F]", font_size=20)
            mask_text.to_edge(LEFT, buff=0.5).shift(DOWN * 2)
            complement_text = Text("~visited = [F, T, T, T, T, T]", font_size=20, color=BLUE)
            complement_text.next_to(mask_text, DOWN)

            self.play(Write(mask_text))
            self.play(Write(complement_text))
            self.wait(1)

            # Compute from nodes 1, 3 with mask
            self.play(
                animate_vertex_fill(graph.vertices[1], YELLOW),
                animate_vertex_fill(graph.vertices[3], YELLOW)
            )
            self.wait(1)

            # Show that node 0 is never considered (stays green)
            check_mark = Text("✓", font_size=40, color=GREEN).next_to(graph.vertices[0], UP)
            check_label = Text("Never recomputed!", font_size=18, color=GREEN)
            check_label.next_to(check_mark, RIGHT)
            self.play(Write(check_mark), Write(check_label))
            self.wait(2)

            self.play(
                FadeOut(mask_text),
                FadeOut(complement_text),
                FadeOut(check_mark),
                FadeOut(check_label),
                FadeOut(mask_label)
            )

        self.play(FadeOut(title), FadeOut(graph))
        self.wait(0.5)
