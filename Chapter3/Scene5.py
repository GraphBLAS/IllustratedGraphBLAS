import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene5(VoiceoverScene, Scene):
    """Building BFS Step by Step - incremental construction of the algorithm."""

    def construct(self):
        setup_scene(self)

        title = Text("Building BFS Step by Step", font_size=42).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Now let's build a complete BFS implementation piece by piece.
            We'll start with the goal: find the level or distance of every
            node from a starting source. We need two vectors: one for the
            current frontier, one for recording levels."""
        ):
            # Problem statement
            problem = VGroup(
                Text("Goal: Find distance from source to all nodes", font_size=26, color=YELLOW),
                Text("Output: levels vector where levels[i] = distance to node i", font_size=22),
            ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.5)
            self.play(Write(problem))
            self.wait(2)

        # Show the two vectors concept
        with self.voiceover(
            """The frontier vector tracks the current wave of exploration. It
            changes completely each iteration, replacing old nodes with new
            discoveries. The levels vector is permanent, accumulating the
            distance for each node as we find it."""
        ):
            self.play(FadeOut(problem))

            two_vecs = VGroup(
                VGroup(
                    Text("frontier", font_size=28, color=YELLOW),
                    Text("Current exploration wave", font_size=20, color=GRAY),
                    Text("REPLACES each iteration", font_size=20, color=RED),
                ).arrange(DOWN, buff=0.2),
                VGroup(
                    Text("levels", font_size=28, color=GREEN),
                    Text("Permanent distance record", font_size=20, color=GRAY),
                    Text("ACCUMULATES over iterations", font_size=20, color=BLUE),
                ).arrange(DOWN, buff=0.2),
            ).arrange(RIGHT, buff=1.5).next_to(title, DOWN, buff=0.6)

            self.play(Write(two_vecs))
            self.wait(2)
            self.play(FadeOut(two_vecs))

        # Build the key line incrementally
        with self.voiceover(
            """Let's build the frontier update line step by step. We start with
            basic expansion: frontier gets the result of frontier times A using
            the any_pair semiring. This finds all neighbors of the current
            frontier."""
        ):
            # Step 1: Basic expansion
            step1_label = Text("Step 1: Basic expansion", font_size=24, color=YELLOW).shift(UP * 2)
            step1_code = Code(
                code_string="frontier << frontier.vxm(A, any_pair)",
                language="python",
                background="window"
            ).scale(0.7).next_to(step1_label, DOWN, buff=0.3)
            step1_problem = Text(
                "Problem: includes already-visited nodes",
                font_size=20, color=RED
            ).next_to(step1_code, DOWN, buff=0.3)

            self.play(Write(step1_label), Write(step1_code))
            self.wait(1)
            self.play(Write(step1_problem))
            self.wait(2)

        with self.voiceover(
            """We fix this by adding a complement mask on the levels vector.
            The mask uses levels dot S for structural presence: only write to
            positions where levels has no value yet. These are the unvisited
            nodes."""
        ):
            # Step 2: Add masking
            step2_label = Text("Step 2: Mask to unvisited", font_size=24, color=YELLOW).shift(UP * 2)
            step2_code = Code(
                code_string="frontier(~levels.S) << frontier.vxm(A, any_pair)",
                language="python",
                background="window"
            ).scale(0.7).next_to(step2_label, DOWN, buff=0.3)
            step2_problem = Text(
                "Problem: old frontier nodes still in vector",
                font_size=20, color=RED
            ).next_to(step2_code, DOWN, buff=0.3)

            self.play(
                Transform(step1_label, step2_label),
                Transform(step1_code, step2_code),
                Transform(step1_problem, step2_problem)
            )
            self.wait(2)

        with self.voiceover(
            """The final piece is replace equals True. This clears the frontier
            before writing, so old nodes don't accumulate. Now the frontier
            contains only the newly discovered nodes, exactly what we need
            for the next iteration."""
        ):
            # Step 3: Add replace
            step3_label = Text("Step 3: Clear old frontier", font_size=24, color=YELLOW).shift(UP * 2)
            step3_code = Code(
                code_string="frontier(~levels.S, replace=True) << frontier.vxm(A, any_pair)",
                language="python",
                background="window"
            ).scale(0.7).next_to(step3_label, DOWN, buff=0.3)
            step3_success = Text(
                "Complete: expands, filters, and replaces in one line!",
                font_size=20, color=GREEN
            ).next_to(step3_code, DOWN, buff=0.3)

            self.play(
                Transform(step1_label, step3_label),
                Transform(step1_code, step3_code),
                Transform(step1_problem, step3_success)
            )
            self.wait(2)

        self.play(FadeOut(step1_label), FadeOut(step1_code), FadeOut(step1_problem))

        # Show the complete algorithm
        with self.voiceover(
            """Here's the complete BFS algorithm. We initialize the frontier
            with the source node and set its level to one. Each iteration
            expands the frontier with masking and replacement, then records
            the current level for all newly discovered nodes. We stop when
            the frontier is empty."""
        ):
            full_code = Code(
                code_string="""def bfs(A: Matrix, source: int) -> Vector:
    n = A.nrows
    levels = Vector(INT64, n)
    levels[source] = 1

    frontier = Vector(BOOL, n)
    frontier[source] = True

    for level in range(2, n + 1):
        # Expand frontier, keep only unvisited
        frontier(~levels.S, replace=True) << frontier.vxm(A, any_pair)

        if frontier.nvals == 0:
            break

        # Record level for newly discovered nodes
        levels(frontier.S) << level

    return levels""",
                language="python",
                background="window"
            ).scale(0.55).move_to(ORIGIN)
            self.play(Write(full_code))
            self.wait(3)

        # Highlight key lines
        with self.voiceover(
            """Notice the symmetry: the frontier update uses complement mask
            with replace, targeting unvisited nodes. The levels update uses
            a regular structural mask, writing only where the frontier is
            present. Two masked assignments, two different purposes."""
        ):
            # Add annotations
            frontier_annot = Text(
                "complement + replace",
                font_size=18, color=YELLOW
            ).next_to(full_code, RIGHT, buff=0.3).shift(UP * 0.5)

            levels_annot = Text(
                "structural mask",
                font_size=18, color=GREEN
            ).next_to(full_code, RIGHT, buff=0.3).shift(DOWN * 0.8)

            self.play(Write(frontier_annot))
            self.wait(1)
            self.play(Write(levels_annot))
            self.wait(2)

        self.play(FadeOut(full_code), FadeOut(frontier_annot), FadeOut(levels_annot))

        # Summary of what each part does
        with self.voiceover(
            """Each component serves a specific purpose. The any_pair semiring
            checks reachability without caring about edge weights. The complement
            mask prevents revisiting. Replace ensures a clean frontier. And
            the structural mask on frontier targets only new discoveries for
            level recording."""
        ):
            summary = VGroup(
                Text("Component Breakdown:", font_size=28, color=YELLOW),
                Text("• any_pair semiring → reachability testing", font_size=22),
                Text("• ~levels.S mask → only unvisited nodes", font_size=22),
                Text("• replace=True → clean frontier each step", font_size=22),
                Text("• frontier.S mask → record new discoveries", font_size=22),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(ORIGIN)

            self.play(Write(summary))
            self.wait(4)

        self.play(FadeOut(title), FadeOut(summary))
        self.wait(0.5)
