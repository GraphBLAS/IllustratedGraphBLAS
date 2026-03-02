import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene

class Scene6(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Chapter Summary", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Let's review what we've covered in this chapter. Semirings let
            you customize what multiplication means, from calculating total
            costs to finding shortest routes. Accumulation defines how results
            merge with existing data, essential for iterative algorithms like
            shortest path. Together, these features give you fine-grained
            control over graph computations."""
        ):
            # Summary bullets
            summary = VGroup(
                Text("• Semirings customize multiplication operations", font_size=28),
                Text("• PLUS_TIMES for totals, MIN_PLUS for shortest paths", font_size=28),
                Text("• Accumulation combines new with existing data", font_size=28),
                Text("• MIN accumulator enables iterative refinement", font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            summary.move_to(ORIGIN)

            for bullet in summary:
                self.play(Write(bullet))
                self.wait(0.5)

            self.wait(2)
            self.play(FadeOut(summary))

        with self.voiceover(
            """In the next chapter, we'll explore masking and put together
            a complete BFS implementation. Masking controls which elements
            participate in computation, avoiding redundant work. We'll see
            how semirings, accumulation, and masking combine to create
            efficient graph traversal algorithms."""
        ):
            # Preview next chapter
            self.play(Transform(title, Text("Next: Chapter 3", font_size=48).to_edge(UP)))

            preview = VGroup(
                Text("• Masking for selective computation", font_size=28),
                Text("• Complement masks for unvisited nodes", font_size=28),
                Text("• Complete BFS implementation", font_size=28),
                Text("• Combining all three features", font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            preview.move_to(ORIGIN)

            for bullet in preview:
                self.play(Write(bullet))
                self.wait(0.5)

            self.wait(2)

        self.play(FadeOut(title), FadeOut(preview))
        self.wait(0.5)
