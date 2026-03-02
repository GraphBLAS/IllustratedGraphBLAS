import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene

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

        # Helper function to create animated accumulator scenario
        def animate_accumulator_scenario(
            self, w_data, r_data, result_data, op_symbol, title_text, label_text, label_color, final_pos
        ):
            """
            Animate w merging with r using the given operator, then move result to final position.
            Returns the final scenario group.
            """
            # Create copies of w and r for this scenario
            w_copy = Matrix([[x] for x in w_data], h_buff=0.8).scale(0.5)
            r_copy = Matrix([[x] for x in r_data], h_buff=0.8).scale(0.5)

            # Create operator symbol
            if op_symbol:
                op_text = Text(op_symbol, font_size=36)
            else:
                op_text = Text("→", font_size=36, color=GREY)

            # Create result matrix
            result_mat = Matrix([[x] for x in result_data], h_buff=0.8).scale(0.5)

            # Position w, op, r at the final position (no center overlap)
            merge_group = VGroup(w_copy, op_text, r_copy).arrange(RIGHT, buff=0.4)
            merge_group.move_to(final_pos)

            # Show w, operator, r
            self.play(FadeIn(w_copy), FadeIn(op_text), FadeIn(r_copy))

            # Animate merge: w slides into r with flash effect
            self.play(
                w_copy.animate.move_to(r_copy.get_center()),
                run_time=0.8
            )

            # Flash effect and transform to result, centering at final_pos
            result_mat.move_to(final_pos)
            self.play(
                Flash(r_copy, color=label_color, flash_radius=0.8),
                FadeOut(w_copy),
                FadeOut(op_text),
                Transform(r_copy, result_mat),
                run_time=0.6
            )

            # Create title and label
            scenario_title = Text(title_text, font_size=24)
            scenario_label = Text(label_text, font_size=18, color=label_color)

            # Assemble final scenario group centered at final_pos
            scenario_title.next_to(r_copy, UP, buff=0.2)
            scenario_label.next_to(r_copy, DOWN, buff=0.2)
            scenario = VGroup(scenario_title, r_copy, scenario_label)

            self.play(FadeIn(scenario_title), FadeIn(scenario_label), run_time=0.3)

            return scenario

        # Data for scenarios
        w_data = [3, 7, 5, 9, 2, 4]
        r_data = [5, 2, 8, 4, 6, 1]

        # Results:
        # No acc: r replaces w -> [5, 2, 8, 4, 6, 1]
        # PLUS: w + r -> [8, 9, 13, 13, 8, 5]
        # MIN: min(w, r) -> [3, 2, 5, 4, 2, 1]

        # Final positions for the three scenarios (equally spaced, center is centered)
        spacing = 4.5
        left_pos = LEFT * spacing + DOWN * 0.5
        center_pos = DOWN * 0.5
        right_pos = RIGHT * spacing + DOWN * 0.5

        # Voiceover 2: Introduce accumulation concept and show no accumulator
        with self.voiceover(
            """This is where accumulation comes in. Without an accumulator,
            new values simply replace old ones."""
        ):
            self.play(FadeOut(vectors_group))
            no_acc = animate_accumulator_scenario(
                self, w_data, r_data,
                [5, 2, 8, 4, 6, 1],  # result: r replaces w
                None, "No accumulator:", "(replace)", GREY, left_pos
            )

        # Voiceover 3: PLUS accumulator
        with self.voiceover(
            """With a PLUS accumulator, new values add to existing ones -
            essential for aggregating results across iterations."""
        ):
            plus_acc = animate_accumulator_scenario(
                self, w_data, r_data,
                [8, 9, 13, 13, 8, 5],  # result: w + r
                "+", "PLUS accumulator:", "(add)", GREEN, center_pos
            )

        # Voiceover 4: MIN accumulator
        with self.voiceover(
            """With a MIN accumulator, we keep whichever value is smaller -
            perfect for maintaining shortest distances in path-finding algorithms."""
        ):
            min_acc = animate_accumulator_scenario(
                self, w_data, r_data,
                [3, 2, 5, 4, 2, 1],  # result: min(w, r)
                "min", "MIN accumulator:", "(minimum)", BLUE, right_pos
            )

        scenarios = VGroup(no_acc, plus_acc, min_acc)

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
