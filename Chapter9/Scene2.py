import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene, create_bipartite_graph


class Scene2(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # --- Voiceover 1: Dense networks are expensive ---
        with self.voiceover(
            """Traditional networks use dense weight matrices. For 1024 neurons,
            that is over one million weights per layer. With 120 layers, storage
            and computation become enormous."""
        ):
            # Fully connected 4x4 bipartite graph
            all_edges = [(i, j) for i in range(4) for j in range(4)]
            dense_graph = create_bipartite_graph(
                4, 4, all_edges, scale=0.6,
                left_color=BLUE, right_color=GREEN
            ).shift(UP * 0.5)
            dense_label = Text("Fully Connected", font_size=24).next_to(dense_graph, UP, buff=0.3)
            self.play(FadeIn(dense_graph), Write(dense_label))

            stats = VGroup(
                Text("1024 x 1024 = 1,048,576 weights/layer", font_size=24),
                Text("x 120 layers = 125 million weights", font_size=24),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(dense_graph, DOWN, buff=0.5)
            self.play(FadeIn(stats))
            self.wait(1)

        # --- Voiceover 2: Sparse networks ---
        with self.voiceover(
            """Sparse networks keep only important connections, reducing memory
            and computation while maintaining accuracy."""
        ):
            self.play(FadeOut(dense_graph), FadeOut(dense_label), FadeOut(stats))

            # Side by side: dense vs sparse
            dense_edges = [(i, j) for i in range(4) for j in range(4)]
            sparse_edges = [(0, 0), (0, 3), (1, 1), (2, 0), (2, 2), (3, 1)]

            dense_g = create_bipartite_graph(
                4, 4, dense_edges, scale=0.5
            ).shift(LEFT * 3)
            sparse_g = create_bipartite_graph(
                4, 4, sparse_edges, scale=0.5
            ).shift(RIGHT * 3)

            dense_t = Text("Dense", font_size=24).next_to(dense_g, UP, buff=0.3)
            sparse_t = Text("Sparse", font_size=24).next_to(sparse_g, UP, buff=0.3)

            self.play(FadeIn(dense_g), Write(dense_t), FadeIn(sparse_g), Write(sparse_t))

            sparsity_text = Text(
                "32 non-zeros per row out of 1024 — 97% sparse",
                font_size=22,
            ).to_edge(DOWN, buff=0.8)
            self.play(Write(sparsity_text))
            self.wait(1)

        # --- Voiceover 3: RadiX-Net ---
        with self.voiceover(
            """RadiX-Net from the MIT GraphChallenge starts sparse from the
            beginning, rather than pruning a dense network. The topology is
            generated deterministically."""
        ):
            self.play(
                FadeOut(dense_g), FadeOut(sparse_g),
                FadeOut(dense_t), FadeOut(sparse_t),
                FadeOut(sparsity_text),
            )

            # Two-path diagram
            prune_path = VGroup(
                Text("Dense", font_size=24),
                MathTex(r"\rightarrow", font_size=36),
                Text("Prune", font_size=24),
                MathTex(r"\rightarrow", font_size=36),
                Text("Sparse", font_size=24),
            ).arrange(RIGHT, buff=0.3).shift(UP * 1)
            cross = Cross(prune_path, stroke_color=RED, stroke_width=4)

            radix_path = VGroup(
                Text("Start Sparse", font_size=28, color=GREEN),
                Text("(RadiX-Net)", font_size=22, color=GREEN),
            ).arrange(RIGHT, buff=0.3).shift(DOWN * 0.5)

            citation = Text(
                "Kepner et al., 2019",
                font_size=18, color=GRAY
            ).to_edge(DOWN, buff=0.5)

            self.play(Write(prune_path))
            self.play(Create(cross))
            self.play(Write(radix_path))
            self.play(FadeIn(citation))
            self.wait(1)

        self.play(FadeOut(prune_path), FadeOut(cross), FadeOut(radix_path), FadeOut(citation))
        self.wait(0.5)
