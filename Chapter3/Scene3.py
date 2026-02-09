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

class Scene3(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Integration: All Three Together", font_size=42).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Let's put it all together: a complete BFS implementation that
            uses semirings, accumulation, and masking. This version not only
            finds reachable nodes but also computes their distance from the source."""
        ):
            # Show complete BFS code with annotations
            bfs_code = Code(
                code_string="""def complete_bfs(A, start):
    q = gb.Vector(bool, A.nrows)
    q[start] = True
    visited = gb.Vector(bool, A.nrows)
    level = gb.Vector(int, A.nrows)
    level[start] = 0
    current_level = 0

    while q.nvals > 0:
        visited << q | visited  # ACCUMULATION
        q_next << A.mxv(q, gb.semiring.any_pair)[~visited]  # SEMIRING + MASKING

        current_level += 1
        level[q_next] = current_level  # ACCUMULATION
        q = q_next

    return visited, level""",
                language="python",
                background="window"
            ).scale(0.55)
            bfs_code.to_edge(LEFT, buff=0.5)

            self.play(Write(bfs_code))
            self.wait(2)

            # Add annotations
            semiring_arrow = Arrow(
                start=bfs_code.get_right() + LEFT * 3 + UP * 0.3,
                end=bfs_code.get_right() + RIGHT * 0.5 + UP * 0.3,
                color=YELLOW,
                stroke_width=3
            )
            semiring_label = Text("SEMIRING", font_size=18, color=YELLOW)
            semiring_label.next_to(semiring_arrow, RIGHT)

            acc1_arrow = Arrow(
                start=bfs_code.get_right() + LEFT * 3 + UP * 0.7,
                end=bfs_code.get_right() + RIGHT * 0.5 + UP * 0.7,
                color=GREEN,
                stroke_width=3
            )
            acc1_label = Text("ACCUMULATION", font_size=18, color=GREEN)
            acc1_label.next_to(acc1_arrow, RIGHT)

            mask_arrow = Arrow(
                start=bfs_code.get_right() + LEFT * 3 + UP * 0.3,
                end=bfs_code.get_right() + RIGHT * 0.5 + UP * 0.3,
                color=BLUE,
                stroke_width=3
            )
            mask_label = Text("MASKING", font_size=18, color=BLUE)
            mask_label.next_to(mask_arrow, RIGHT)

            acc2_arrow = Arrow(
                start=bfs_code.get_right() + LEFT * 3 + DOWN * 0.3,
                end=bfs_code.get_right() + RIGHT * 0.5 + DOWN * 0.3,
                color=GREEN,
                stroke_width=3
            )
            acc2_label = Text("ACCUMULATION", font_size=18, color=GREEN)
            acc2_label.next_to(acc2_arrow, RIGHT)

            self.play(
                Create(semiring_arrow), Write(semiring_label),
                Create(acc1_arrow), Write(acc1_label),
                Create(mask_arrow), Write(mask_label),
                Create(acc2_arrow), Write(acc2_label)
            )
            self.wait(3)

            self.play(
                FadeOut(semiring_arrow), FadeOut(semiring_label),
                FadeOut(acc1_arrow), FadeOut(acc1_label),
                FadeOut(mask_arrow), FadeOut(mask_label),
                FadeOut(acc2_arrow), FadeOut(acc2_label),
                bfs_code.animate.scale(0.7).to_edge(LEFT, buff=0.3).shift(UP * 0.5)
            )

        # Create graph and vector displays
        matrix_data = CHAPTER0_MATRIX_DATA
        graph = create_adjacency_digraph(matrix_data, layout="triangle", scale=0.9)
        graph.to_edge(RIGHT, buff=0.5).shift(UP * 1)

        with self.voiceover(
            """We use the ANY_PAIR semiring for reachability testing.
            Accumulation with OR tracks all visited nodes. Complement masking
            ensures we only explore unvisited neighbors. A second accumulation
            updates the level vector, recording each node's distance."""
        ):
            self.play(Create(graph))

            # Display vectors below graph
            vec_display = VGroup(
                Text("Level:", font_size=20),
                Text("0: ", font_size=18, color=RED),
                Text("1: ", font_size=18, color=ORANGE),
                Text("2: ", font_size=18, color=YELLOW),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            vec_display.to_edge(RIGHT, buff=0.5).shift(DOWN * 1.5)
            self.play(Write(vec_display))

        with self.voiceover(
            """Starting from node 0 at level 0, we discover nodes 1 and 3 at
            level 1. The ANY_PAIR semiring finds neighbors, complement masking
            excludes visited nodes, and accumulation records their levels."""
        ):
            # Iteration 0: Start at node 0
            self.play(animate_vertex_fill(graph.vertices[0], RED))
            level_0_nodes = Text("0", font_size=18).next_to(vec_display[1], RIGHT)
            self.play(Write(level_0_nodes))
            self.wait(1)

            # Iteration 1: Discover nodes 1, 3
            self.play(
                animate_vertex_fill(graph.vertices[1], ORANGE),
                animate_vertex_fill(graph.vertices[3], ORANGE)
            )
            level_1_nodes = Text("1, 3", font_size=18).next_to(vec_display[2], RIGHT)
            self.play(Write(level_1_nodes))
            self.wait(1)

        with self.voiceover(
            """Finally, nodes 2, 4, and 5 are discovered at level 2. This
            compact implementation demonstrates the power of GraphBLAS: complex
            algorithms become simple combinations of semirings, accumulators,
            and masks. The same structure applies to countless graph algorithms
            - you just swap the semiring and accumulation operator."""
        ):
            # Iteration 2: Discover nodes 2, 4, 5
            self.play(
                animate_vertex_fill(graph.vertices[2], YELLOW),
                animate_vertex_fill(graph.vertices[4], YELLOW),
                animate_vertex_fill(graph.vertices[5], YELLOW)
            )
            level_2_nodes = Text("2, 4, 5", font_size=18).next_to(vec_display[3], RIGHT)
            self.play(Write(level_2_nodes))
            self.wait(2)

        self.play(
            FadeOut(title), FadeOut(bfs_code), FadeOut(graph),
            FadeOut(vec_display), FadeOut(level_0_nodes),
            FadeOut(level_1_nodes), FadeOut(level_2_nodes)
        )
        self.wait(0.5)
