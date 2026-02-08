import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import get_speech_service


class Scene5(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(get_speech_service())

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
            """In the next chapter, we will explore more advanced
            GraphBLAS concepts that give you fine-grained control over
            computations. Semirings let you customize how values are
            combined during multiplication. Accumulation allows you to
            merge new results with existing data. And masking gives you
            precise control over which elements participate in a
            computation."""
        ):
            title = Tex("Coming Next").scale(1.5).to_edge(UP)
            self.play(Write(title))

            preview_bullets = BulletedList(
                "Semirings for custom operations",
                "Accumulation for combining results",
                "Masking for selective computation",
                font_size=36
            )
            preview_bullets.next_to(title, DOWN, buff=0.5)

            self.play(FadeIn(preview_bullets, shift=UP, lag_ratio=0.2))
            self.wait(3)

        # No cleanup - chapter ends on the preview
