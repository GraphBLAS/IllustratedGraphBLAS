from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from dotenv import load_dotenv
load_dotenv()

matrices = [
    ('pct20stif', 'Structural Analysis', 1, 2),
    ('rw5151', 'Statistics and Mathematics', 1, 5),
    ('lpl1', 'Resource Optimization', 2, 4),
    ('poli_large', 'Economic Planning', 1, 5),
    ('conf5_0-4x4-10', 'Theoretical Quantum Chemistry', 1, 5),
]

class Scene4(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(voice_name="michelp", transcription_model=None))

        with self.voiceover(
                """Sparse graphs and linear algebra play an important
                role in many scientific and engineering disciplines,
                including:"""
        ):
            title = Tex("Graphs are Everywhere").scale(1.5).to_edge(UP)
            self.play(Write(title))
            self.wait(3)

        for subdir, description, ai, gi in matrices:
            matrix_image = ImageMobject(f"../scraped_images/{subdir}/image_{ai}_inv.jpg").scale(1.5).to_edge(LEFT)
            graph_image = ImageMobject(f"../scraped_images/{subdir}/image_{gi}.jpg").scale(1.5).to_edge(RIGHT)

            self.play(FadeIn(matrix_image), FadeIn(graph_image))
            with self.voiceover(description):
                self.wait(2)
                self.play(FadeOut(matrix_image), FadeOut(graph_image))

        self.play(FadeOut(title))

        with self.voiceover(
                """In our next video, we will introduce the Python
                bindings for GraphBLAS and explore the duality between
                matrix multiplication and graph traversal in more
                depth. We will also introduce fundamental GraphBLAS
                concepts including semirings, accumulation, and
                masking."""
        ):
            title = Tex("Coming Next").scale(1.5).to_edge(UP)

            bullet_points = BulletedList(
                "Install Python library",
                "Matrix Multiplication as Breadth First Search.",
                "Using Semirings to perform combining operations.",
                "Accumulating results as you go.",
                "Masking or including only certain values.",
                font_size=36
            )
            bullet_points.next_to(title, DOWN, buff=0.5)

            self.play(Write(title))
            self.play(FadeIn(bullet_points, shift=UP, lag_ratio=0.1))
            self.wait(3)
