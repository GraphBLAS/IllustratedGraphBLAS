import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene

class Scene4(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Accumulation", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Voiceover 1: Introduction and show vectors
        with self.voiceover(
            """In iterative graph algorithms, we often need to combine new
            results with existing data. Should new values overwrite old ones?
            Add to them? Take the minimum or maximum?"""
        ):
            # Show vector setup - arrange side by side
            w_label = Text("Existing vector w:", font_size=28)
            w_vec = Matrix([[3], [7], [5], [9], [2], [4]], h_buff=0.8).scale(0.6)
            w_group = VGroup(w_label, w_vec).arrange(DOWN, buff=0.3)

            r_label = Text("New result r:", font_size=28)
            r_vec = Matrix([[5], [2], [8], [4], [6], [1]], h_buff=0.8).scale(0.6)
            r_group = VGroup(r_label, r_vec).arrange(DOWN, buff=0.3)

            vectors_group = VGroup(w_group, r_group).arrange(RIGHT, buff=2).shift(UP * 0.5)

            self.play(Write(w_group))
            self.play(Write(r_group))

        # Prepare the three scenarios with updated values
        # w = [3, 7, 5, 9, 2, 4], r = [5, 2, 8, 4, 6, 1]

        # No accumulator (replace with r)
        no_acc_title = Text("No accumulator:", font_size=24)
        no_acc_result = Matrix([[5], [2], [8], [4], [6], [1]], h_buff=0.8).scale(0.5)
        no_acc_label = Text("(replace)", font_size=18, color=GREY)

        # PLUS accumulator (w + r)
        plus_acc_title = Text("PLUS accumulator:", font_size=24)
        plus_acc_result = Matrix([[8], [9], [13], [13], [8], [5]], h_buff=0.8).scale(0.5)
        plus_acc_label = Text("(add)", font_size=18, color=GREEN)

        # MIN accumulator (min of w, r)
        min_acc_title = Text("MIN accumulator:", font_size=24)
        min_acc_result = Matrix([[3], [2], [5], [4], [2], [1]], h_buff=0.8).scale(0.5)
        min_acc_label = Text("(minimum)", font_size=18, color=BLUE)

        # Arrange each scenario vertically
        no_acc = VGroup(no_acc_title, no_acc_result, no_acc_label).arrange(DOWN, buff=0.2)
        plus_acc = VGroup(plus_acc_title, plus_acc_result, plus_acc_label).arrange(DOWN, buff=0.2)
        min_acc = VGroup(min_acc_title, min_acc_result, min_acc_label).arrange(DOWN, buff=0.2)

        # Position all scenarios
        scenarios = VGroup(no_acc, plus_acc, min_acc).arrange(RIGHT, buff=1.2).shift(DOWN * 0.5)

        # Voiceover 2: Introduce accumulation concept and show no accumulator
        with self.voiceover(
            """This is where accumulation comes in. Without an accumulator,
            new values simply replace old ones."""
        ):
            self.play(FadeOut(vectors_group))
            self.play(Write(no_acc))

        # Voiceover 3: PLUS accumulator
        with self.voiceover(
            """With a PLUS accumulator, new values add to existing ones -
            essential for aggregating results across iterations."""
        ):
            self.play(Write(plus_acc))

        # Voiceover 4: MIN accumulator
        with self.voiceover(
            """With a MIN accumulator, we keep whichever value is smaller -
            perfect for maintaining shortest distances in path-finding algorithms."""
        ):
            self.play(Write(min_acc))

        # Prepare syntax examples
        syntax_examples = VGroup(
            Code(
                code_string="w << A.mxv(v)             # No accumulator",
                language="python",
                background="window"
            ).scale(0.6),
            Code(
                code_string="w(gb.binary.plus) << A.mxv(v)   # PLUS accumulator",
                language="python",
                background="window"
            ).scale(0.6),
            Code(
                code_string="w(gb.binary.min) << A.mxv(v)    # MIN accumulator",
                language="python",
                background="window"
            ).scale(0.6),
        ).arrange(DOWN, buff=0.5)

        # Voiceover 5: Show syntax
        with self.voiceover(
            """In python-graphblas, specifying an accumulator is straightforward.
            You simply pass the binary operator to the output vector before assignment."""
        ):
            self.play(FadeOut(scenarios))
            self.play(Write(syntax_examples))

        self.play(FadeOut(syntax_examples), FadeOut(title))
        self.wait(0.5)
