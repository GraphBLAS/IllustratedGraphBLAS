import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import create_sparse_matrix, create_small_graph_from_matrix, setup_scene


class Scene5(VoiceoverScene, Scene):
    """Transitive Closure."""

    def construct(self):
        setup_scene(self)

        title = Text("Transitive Closure", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Question: Can node i reach node j through ANY path?
        question = Text(
            "Can node i reach node j through any path?",
            font_size=28, color=YELLOW
        ).next_to(title, DOWN, buff=0.5)

        with self.voiceover(
            """Transitive closure answers a fundamental question: can node i
            reach node j through any path? Not just one hop, not just two
            hops, but through any sequence of edges."""
        ):
            self.play(Write(question))
            self.wait(1)

        self.play(FadeOut(question))

        # Example graph with two "clusters" connected by one edge
        # This shows how reachability grows over iterations
        #
        #   0 -- 1      3 -- 4
        #         \    /
        #          2
        #
        A_data = [
            [0, 1, 0, 0, 0],  # 0 -> 1
            [1, 0, 1, 0, 0],  # 1 -> 0, 2
            [0, 1, 0, 1, 0],  # 2 -> 1, 3
            [0, 0, 1, 0, 1],  # 3 -> 2, 4
            [0, 0, 0, 1, 0],  # 4 -> 3
        ]

        # Create graph
        graph = self.create_graph()
        graph.to_edge(RIGHT, buff=1.5)

        with self.voiceover(
            """Consider this graph. Node zero connects to node one. Node one
            connects to node two. And the chain continues to nodes three and
            four. Direct inspection shows zero can reach four, but only through
            multiple hops."""
        ):
            self.play(Create(graph))
            self.wait(1)

        # Show iterative computation
        # R_0 = A (direct connections)
        R0_data = A_data

        R0_mat = create_sparse_matrix(R0_data, scale=0.32, v_buff=0.55, h_buff=0.55)
        R0_label = MathTex("R_0 = A").scale(0.6)
        R0_small_graph = create_small_graph_from_matrix(R0_data, scale=0.22, directed=False, edge_color=BLUE)
        R0_desc = Text("Direct edges", font_size=16, color=GRAY)
        R0_group = VGroup(R0_label, R0_mat, R0_small_graph, R0_desc).arrange(DOWN, buff=0.1).to_edge(LEFT, buff=0.8).shift(UP * 1.5)

        with self.voiceover(
            """We compute transitive closure iteratively. Start with R-zero
            equal to A, the direct connections. Then repeatedly add new
            reachable pairs by multiplying."""
        ):
            self.play(Write(R0_group))
            self.wait(1)

        # R_1 = R_0 | (A @ R_0) - adds 2-hop connections
        # Union of direct and 2-hop paths
        R1_data = [
            [1, 1, 1, 0, 0],  # 0 can reach 0,1,2
            [1, 1, 1, 1, 0],  # 1 can reach 0,1,2,3
            [1, 1, 1, 1, 1],  # 2 can reach all
            [0, 1, 1, 1, 1],  # 3 can reach 1,2,3,4
            [0, 0, 1, 1, 1],  # 4 can reach 2,3,4
        ]

        R1_mat = create_sparse_matrix(R1_data, scale=0.32, v_buff=0.55, h_buff=0.55)
        R1_label = MathTex(r"R_1 = R_0 \cup (A \times R_0)").scale(0.5)
        R1_small_graph = create_small_graph_from_matrix(R1_data, scale=0.22, directed=False, edge_color=GREEN)
        R1_desc = Text("+ 2-hop paths", font_size=16, color=GREEN)
        R1_group = VGroup(R1_label, R1_mat, R1_small_graph, R1_desc).arrange(DOWN, buff=0.1).next_to(R0_group, DOWN, buff=0.3)

        with self.voiceover(
            """R-one equals R-zero union A times R-zero. This adds all
            two-hop paths to our reachability. Notice how the matrix
            fills in as new pairs become connected."""
        ):
            self.play(Write(R1_group))
            # Highlight new entries that appeared
            self.wait(1)

        # R_2 = R_1 | (A @ R_1) - converges (all pairs now reachable)
        R2_data = [
            [1, 1, 1, 1, 1],  # 0 can reach all
            [1, 1, 1, 1, 1],  # 1 can reach all
            [1, 1, 1, 1, 1],  # 2 can reach all
            [1, 1, 1, 1, 1],  # 3 can reach all
            [1, 1, 1, 1, 1],  # 4 can reach all
        ]

        R2_mat = create_sparse_matrix(R2_data, scale=0.32, v_buff=0.55, h_buff=0.55)
        R2_label = MathTex(r"R_2 = R_1 \cup (A \times R_1)").scale(0.5)
        R2_small_graph = create_small_graph_from_matrix(R2_data, scale=0.22, directed=False, edge_color=YELLOW)
        R2_desc = Text("Fixed point", font_size=16, color=YELLOW)
        R2_group = VGroup(R2_label, R2_mat, R2_small_graph, R2_desc).arrange(DOWN, buff=0.1).next_to(R1_group, DOWN, buff=0.3)

        with self.voiceover(
            """After another iteration, R-two fills completely. Every node
            can reach every other node. Further iterations add no new
            entries. We have reached a fixed point, the transitive closure."""
        ):
            self.play(Write(R2_group))
            self.wait(1)

        # Clear matrices, show code pattern
        self.play(FadeOut(R0_group), FadeOut(R1_group), FadeOut(R2_group))

        code = Code(
            code_string="""R = A.dup()
while True:
    old_nvals = R.nvals
    R << R.mxm(A, any_pair) | R
    if R.nvals == old_nvals:
        break  # Fixed point""",
            language="python",
            background="window"
        ).scale(0.7).to_edge(LEFT, buff=0.8)

        with self.voiceover(
            """Here is the GraphBLAS pattern. We start with R as a copy of A.
            Then we loop, multiplying R by A with the ANY_PAIR semiring and
            taking the union with R. When no new entries appear, the number
            of values stops changing, and we have our transitive closure."""
        ):
            self.play(Write(code))
            self.wait(2)

        # Applications
        apps = VGroup(
            Text("Applications:", font_size=24, color=YELLOW),
            Text("• Database query planning", font_size=20),
            Text("• Network analysis", font_size=20),
            Text("• Compiler optimization", font_size=20),
            Text("• Dependency resolution", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        apps.next_to(code, DOWN, buff=0.6)

        with self.voiceover(
            """This pattern appears in database query planning, network
            analysis, compiler optimization, and dependency resolution.
            Any problem asking can X reach Y benefits from transitive
            closure."""
        ):
            self.play(FadeIn(apps, shift=UP))
            self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(code), FadeOut(apps)
        )
        self.wait(0.5)

    def create_graph(self):
        """Create a chain graph: 0-1-2-3-4."""
        positions = {
            0: np.array([-2, 1, 0]),
            1: np.array([-1, 0, 0]),
            2: np.array([0, -0.5, 0]),
            3: np.array([1, 0, 0]),
            4: np.array([2, 1, 0]),
        }

        vertices = {}
        for i in range(5):
            label = MathTex(str(i), color=BLACK).scale(0.6)
            dot = LabeledDot(label, radius=0.25, fill_color=WHITE, fill_opacity=1)
            dot.move_to(positions[i])
            vertices[i] = dot

        edges_list = [(0, 1), (1, 2), (2, 3), (3, 4)]
        edges = VGroup()

        for i, j in edges_list:
            edge = DoubleArrow(
                positions[i], positions[j],
                color=BLUE, buff=0.3, stroke_width=3,
                tip_length=0.12, max_tip_length_to_length_ratio=0.12
            )
            edges.add(edge)

        graph = VGroup(edges, *vertices.values())
        graph.vertices = vertices
        return graph
