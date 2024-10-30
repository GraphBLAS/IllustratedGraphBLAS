from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

class Scene3(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        # Title text
        title = Tex("Coming Next").scale(1.5).to_edge(UP)

        with self.voiceover(
            """In the next video in this series, we'll explore more ways to use
            matrix multiplication to work with graphs, and explain the
            notion of a semiring which can be used to compute many
            different functions across the values of GraphBLAS
            objects."""
        ):
            self.play(Write(title))
            self.wait(2)

            # Display the first bullet point
            bullet1 = Tex("- Matrix Multiplication: Using matrix operations to work with graphs").scale(0.8)
            bullet1.next_to(title, DOWN * 2, aligned_edge=LEFT).to_edge(LEFT)
            self.play(Write(bullet1))
            self.wait(2)

            # Display the second bullet point
            bullet2 = Tex("- Semirings: A mathematical structure to compute functions").scale(0.8)
            bullet2.next_to(bullet1, DOWN * 2, aligned_edge=LEFT).to_edge(LEFT)
            self.play(Write(bullet2))
            self.wait(2)

        # Footer text
        footer = Text(
            "This video is brought to you by The GraphBLAS Forum and funded by NumFOCUS"
        ).scale(0.5).to_edge(DOWN)

        # Display the footer text
        self.play(Write(footer))
        self.wait(2)

        # Fade out all elements at the end
        self.play(FadeOut(title), FadeOut(bullet1), FadeOut(bullet2), FadeOut(footer))
        self.wait(0.5)
