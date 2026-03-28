import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene1(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Tex("Installing Python-GraphBLAS").scale(1.5).to_edge(UP)

        with self.voiceover(
            """Installing Python GraphBLAS is straightforward using pip,
            or conda for those using Anaconda or Miniforge environments.
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
                background="window",
                formatter_style="dracula",
            ).scale(1.2)
            self.play(FadeIn(pip_code))
            self.wait(1)

            # Conda install option
            conda_code = Code(
                code_string="conda install -c conda-forge python-graphblas",
                language="bash",
                background="window",
                formatter_style="dracula",
            ).scale(1.2)
            conda_code.next_to(pip_code, DOWN, buff=0.5)
            self.play(FadeIn(conda_code))
            self.wait(2)

        # Fade out install commands before showing alternatives
        self.play(FadeOut(pip_code), FadeOut(conda_code))

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
                Code(code_string="using GraphBLAS", language="julia", background="window", formatter_style="dracula").scale(0.7),
            ).arrange(RIGHT, buff=0.3)

            postgres_alt = VGroup(
                Tex("PostgreSQL: ").scale(0.8),
                Code(code_string="CREATE EXTENSION onesparse;", language="sql", background="window", formatter_style="dracula").scale(0.7),
            ).arrange(RIGHT, buff=0.3)

            alt_group = VGroup(alternatives, postgres_alt).arrange(DOWN, buff=0.5)

            self.play(FadeIn(alternatives))
            self.wait(1)
            self.play(FadeIn(postgres_alt))
            self.wait(2)

        # Cleanup
        self.play(FadeOut(title), FadeOut(alt_group))
        self.wait(0.5)
