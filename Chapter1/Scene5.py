import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene


class Scene5(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        with self.voiceover(
            """Let's review what we covered in this chapter."""
        ):
            title = Tex("What We Learned").scale(1.5).to_edge(UP)
            self.play(Write(title))

            summary_bullets = BulletedList(
                "Installing python-graphblas with pip",
                "Creating sparse matrices and vectors with COO format",
                "Matrix-vector multiplication using mxv",
                "Breadth-first search as linear algebra",
                font_size=36
            )
            summary_bullets.next_to(title, DOWN, buff=0.5)

            self.play(FadeIn(summary_bullets, shift=UP, lag_ratio=0.2))
            self.wait(2)

        self.play(FadeOut(title), FadeOut(summary_bullets))

        with self.voiceover(
            """In the next chapter, we'll explore semirings, which let you
            customize how values are combined during matrix multiplication.
            We'll see how the same operation can compute total costs,
            shortest paths, or simple reachability, just by changing the
            semiring."""
        ):
            title = Tex("Coming Next").scale(1.5).to_edge(UP)
            self.play(Write(title))

            preview_bullets = BulletedList(
                "Semirings for custom operations",
                "PLUS\\_TIMES, MIN\\_PLUS, and ANY\\_PAIR",
                "Same structure, different meanings",
                font_size=36
            )
            preview_bullets.next_to(title, DOWN, buff=0.5)

            self.play(FadeIn(preview_bullets, shift=UP, lag_ratio=0.2))
            self.wait(3)

        # No cleanup - chapter ends on the preview
