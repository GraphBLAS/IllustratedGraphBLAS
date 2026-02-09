import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene

class Scene6(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Masking", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """In sparse computations, we often want to exclude certain
            elements. Maybe they're already processed, or don't meet our
            criteria. Computing on every element wastes time and energy.
            Masking solves this by controlling which elements participate."""
        ):
            # Show vector with sparse values
            waste_label = Text("Vector v:", font_size=30).shift(UP * 2)
            v_vec = Matrix([[1], [0], [3], [0], [5], [0]], h_buff=0.8).scale(0.6)
            v_vec.next_to(waste_label, DOWN)

            waste_note = Text("6 positions, only 3 have values", font_size=20, color=YELLOW)
            waste_note.next_to(v_vec, DOWN, buff=0.5)

            self.play(Write(waste_label), Write(v_vec))
            self.play(Write(waste_note))
            self.wait(2)

            self.play(FadeOut(waste_label), FadeOut(v_vec), FadeOut(waste_note))

        with self.voiceover(
            """There are two types of masks. A structural mask includes
            elements that exist in the mask, regardless of their value. A
            value mask includes elements where the mask is True. For boolean
            vectors, they're equivalent. You can complement a mask with the
            tilde operator, meaning operate where the mask is NOT set. This
            is crucial for BFS: we want to explore nodes we haven't visited yet."""
        ):
            # Show three mask types
            mask_types = VGroup()

            # Structural mask
            struct_title = Text("Structural mask:", font_size=28).shift(UP * 2 + LEFT * 3)
            struct_code = Code(
                code_string="mask = [1, _, 1, _, 1, _]  # _ = no value\nw << A.mxv(v)[mask]",
                language="python",
                background="window"
            ).scale(0.5).next_to(struct_title, DOWN)
            struct_label = Text("Only positions 0, 2, 4", font_size=18, color=GREEN)
            struct_label.next_to(struct_code, DOWN)
            struct = VGroup(struct_title, struct_code, struct_label)

            # Value mask
            value_title = Text("Value mask:", font_size=28).shift(UP * 2 + RIGHT * 3)
            value_code = Code(
                code_string="mask = [T, F, T, F, T, F]\nw << A.mxv(v)[mask]",
                language="python",
                background="window"
            ).scale(0.5).next_to(value_title, DOWN)
            value_label = Text("Same result", font_size=18, color=GREEN)
            value_label.next_to(value_code, DOWN)
            value = VGroup(value_title, value_code, value_label)

            # Complement mask
            comp_title = Text("Complement mask:", font_size=28).shift(DOWN * 0.5)
            comp_code = Code(
                code_string="w << A.mxv(v)[~mask]  # Tilde = NOT",
                language="python",
                background="window"
            ).scale(0.5).next_to(comp_title, DOWN)
            comp_label = Text("Positions 1, 3, 5", font_size=18, color=BLUE)
            comp_label.next_to(comp_code, DOWN)
            comp = VGroup(comp_title, comp_code, comp_label)

            mask_types = VGroup(struct, value, comp).arrange(DOWN, buff=0.8)

            self.play(Write(struct))
            self.wait(2)
            self.play(Write(value))
            self.wait(2)
            self.play(Write(comp))
            self.wait(2)

            self.play(FadeOut(mask_types))

        self.play(FadeOut(title))
        self.wait(0.5)
