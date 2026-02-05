import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from dotenv import load_dotenv
load_dotenv()

from Parts import create_logo_grid


class Scene0(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(voice_name="michelp", transcription_model=None))

        logos_group = create_logo_grid()

        # Title text
        title = Tex("The Illustrated GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """The GraphBLAS is a sparse linear algebra API—a powerful
            mathematical framework for graph analysis. In this video
            series, we'll explore the basic concepts of algebraic
            graph theory and how it can be used to write portable
            graph algorithms on many different kinds of hardware,
            including CPUs and GPUs. By the end of this series, you
            will understand how to create new parallel graph
            algorithms using simple mathematical notation. GraphBLAS
            was developed by a consortium of researchers from academia
            and industry, and is now an open standard with multiple
            implementations."""
        ):
            self.play(Write(title))
            for logo in logos_group:
                self.play(FadeIn(logo, run_time=0.1))
            footer = Text(
                "The GraphBLAS Forum"
            ).scale(0.75).to_edge(DOWN)
            self.play(Write(footer))

        # Fade out title and logos at the end
        self.play(FadeOut(title), FadeOut(logos_group), FadeOut(footer))
        self.wait(0.5)
