import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    setup_scene,
    create_undirected_graph,
    create_sparse_matrix,
    CHAPTER8_MATRIX_DATA,
    CHAPTER8_TRIANGLE_DATA,
    CHAPTER8_PER_NODE_TRIANGLES,
    color_nodes_by_value,
    animate_vertex_fill,
)


class Scene3(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Title
        title = Text("Per-Node Triangle Counts", font_size=42).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Three-panel layout: code (left) | matrix/vector (center) | graph (right)

        # Code panel
        code_lines = [
            "# Sum each row for per-node count",
            "row_sums = T.sum(axis=1)",
            "",
            "# Divide by 2",
            "# (each triangle counted twice)",
            "per_node = row_sums // 2",
        ]
        code = Code(
            code_string="\n".join(code_lines),
            language="python",
            background="window",
            formatter_style="dracula",
        ).scale(0.7)
        code.to_edge(LEFT, buff=0.3).shift(DOWN * 0.2)

        # Matrix T
        T_label = Text("T", font_size=28, color=ORANGE)
        T_mat = create_sparse_matrix(CHAPTER8_TRIANGLE_DATA, scale=0.4, v_buff=0.5, h_buff=0.5)
        T_group = VGroup(T_label, T_mat).arrange(DOWN, buff=0.2)
        T_group.move_to(ORIGIN).shift(DOWN * 0.3)

        # Graph (circular layout to show all triangles clearly)
        graph = create_undirected_graph(CHAPTER8_MATRIX_DATA, layout="circular", scale=0.6)
        graph.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)

        with self.voiceover(
            """We can also count how many triangles each node participates
            in. Starting from our triangle matrix T, we sum each row to
            get the total triangle participation for that node."""
        ):
            self.play(Create(code))
            self.play(Write(T_label), Create(T_mat))
            self.play(Create(graph))
            self.wait(1)

        # Create row sums vector
        row_sums = [sum(row) for row in CHAPTER8_TRIANGLE_DATA]  # [3, 2, 5, 5, 3, 2]

        # Show arrow from matrix to vector
        arrow = Arrow(T_mat.get_right(), T_mat.get_right() + RIGHT * 0.8, color=WHITE)

        # Row sums vector
        sums_data = [[s] for s in row_sums]
        sums_mat = Matrix(sums_data, v_buff=0.5, h_buff=0.3).scale(0.4)
        sums_label = Text("row sums", font_size=20)
        sums_group = VGroup(sums_label, sums_mat).arrange(DOWN, buff=0.15)
        sums_group.next_to(arrow, RIGHT, buff=0.2)

        with self.voiceover(
            """Summing each row gives us these values. But we need to
            divide by 2 because in our symmetric matrix, each triangle
            is counted twice per node. Once for each direction of the
            participating edges."""
        ):
            self.play(Create(arrow))
            self.play(Write(sums_label), Create(sums_mat))
            self.wait(1)

        # Show per-node counts
        per_node_data = [[c] for c in CHAPTER8_PER_NODE_TRIANGLES]  # [2, 1, 3, 3, 2, 1]
        per_node_mat = Matrix(per_node_data, v_buff=0.5, h_buff=0.3).scale(0.4)
        per_node_label = Text("per node", font_size=20)
        per_node_group = VGroup(per_node_label, per_node_mat).arrange(DOWN, buff=0.15)
        per_node_group.move_to(sums_group.get_center())

        div_arrow = Arrow(
            sums_group.get_bottom() + DOWN * 0.1,
            sums_group.get_bottom() + DOWN * 0.6,
            color=WHITE
        )
        div_label = MathTex(r"\div 2", font_size=24).next_to(div_arrow, RIGHT, buff=0.1)

        with self.voiceover(
            """After dividing by 2, we get the actual per-node triangle
            counts. Node 0 participates in 2 triangles. Node 1 participates
            in 1. Nodes 2 and 3, our hubs, each participate in 3 triangles."""
        ):
            self.play(
                ReplacementTransform(sums_label, per_node_label),
                ReplacementTransform(sums_mat, per_node_mat),
            )
            self.wait(1)

        # Color graph nodes by triangle count
        with self.voiceover(
            """We can visualize this by coloring nodes according to their
            triangle participation. Nodes with more triangles appear
            redder, while nodes with fewer triangles stay lighter."""
        ):
            node_colors = color_nodes_by_value(
                graph,
                CHAPTER8_PER_NODE_TRIANGLES,
                low_color=WHITE,
                high_color=RED
            )
            for vertex, color in node_colors:
                self.play(animate_vertex_fill(vertex, color), run_time=0.3)
            self.wait(1)

        # Add node labels showing counts
        count_labels = VGroup()
        for i, count in enumerate(CHAPTER8_PER_NODE_TRIANGLES):
            label = Text(f"{count}", font_size=18, color=YELLOW)
            label.next_to(graph.vertices[i], UP, buff=0.15)
            count_labels.add(label)

        with self.voiceover(
            """The numbers above each node show their triangle counts.
            Nodes 2 and 3 are clearly the most central, each belonging
            to 3 triangles. This metric helps identify important nodes
            in tightly connected communities."""
        ):
            self.play(Write(count_labels))
            self.wait(1)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(code),
            FadeOut(T_label),
            FadeOut(T_mat),
            FadeOut(arrow),
            FadeOut(per_node_label),
            FadeOut(per_node_mat),
            FadeOut(graph),
            FadeOut(count_labels),
        )
        self.wait(0.5)
