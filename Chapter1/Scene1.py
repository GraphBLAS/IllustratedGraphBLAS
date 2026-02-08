import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import get_speech_service


class Scene1(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(get_speech_service())

        title = Tex("Installing Python-GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """Installing Python GraphBLAS is straightforward using pip.
            The package automatically includes SuiteSparse GraphBLAS,
            which is a high-performance implementation of the GraphBLAS
            specification developed by Tim Davis at Texas A and M
            University."""
        ):
            self.play(Write(title))

            # Terminal-style code block for pip install
            pip_code = Code(
                code_string="pip install python-graphblas",
                language="bash",
                background="window"
            ).scale(1.2)
            self.play(FadeIn(pip_code))
            self.wait(2)

        with self.voiceover(
            """If Python isn't your preferred language, GraphBLAS
            bindings are also available for other environments. Julia
            has a native GraphBLAS package, and there's even a Postgres
            extension that brings GraphBLAS operations directly into SQL
            queries."""
        ):
            # Show alternatives
            alternatives = VGroup(
                Tex("Julia: ").scale(0.8),
                Code(code_string="using GraphBLAS", language="julia", background="window").scale(0.7),
            ).arrange(RIGHT, buff=0.3)

            postgres_alt = VGroup(
                Tex("PostgreSQL: ").scale(0.8),
                Code(code_string="CREATE EXTENSION pggraphblas;", language="sql", background="window").scale(0.7),
            ).arrange(RIGHT, buff=0.3)

            alt_group = VGroup(alternatives, postgres_alt).arrange(DOWN, buff=0.5)
            alt_group.next_to(pip_code, DOWN, buff=0.8)

            self.play(FadeIn(alternatives))
            self.wait(1)
            self.play(FadeIn(postgres_alt))
            self.wait(2)

        # Cleanup
        self.play(FadeOut(title), FadeOut(pip_code), FadeOut(alt_group))
        self.wait(0.5)
