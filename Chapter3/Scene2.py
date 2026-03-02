import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene2(VoiceoverScene, Scene):
    """Masking Basics - structural vs value masks, complement masks."""

    def construct(self):
        setup_scene(self)

        title = Text("Masking", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Now that we understand vector-matrix multiply, let's add masking.
            Masks control which positions in the OUTPUT can receive values. This
            is crucial: we're not filtering the input, we're controlling where
            results land."""
        ):
            # Key insight box
            insight = VGroup(
                Text("Key Insight:", font_size=24, color=YELLOW),
                Text("Mask controls OUTPUT positions", font_size=22),
                Text("not input filtering", font_size=22, color=GRAY)
            ).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.5)
            self.play(Write(insight))
            self.wait(2)
            self.play(FadeOut(insight))

        with self.voiceover(
            """There are two ways to specify a mask. A structural mask selects
            positions where the mask vector has any value stored, regardless of
            what that value is. A value mask selects positions where the mask
            evaluates to True."""
        ):
            # Create side-by-side comparison
            struct_group = VGroup()
            value_group = VGroup()

            # Structural mask example
            struct_title = Text("Structural Mask", font_size=28, color=GREEN).shift(UP * 2)
            struct_vec = self.create_labeled_vector(
                ["3", "", "7", "", "1", ""],
                "mask",
                show_indices=True
            ).scale(0.7).next_to(struct_title, DOWN, buff=0.4)
            struct_syntax = Code(
                code_string="w(mask.S) << ...",
                language="python",
                background="window"
            ).scale(0.5).next_to(struct_vec, DOWN, buff=0.3)
            struct_result = Text(
                "Positions 0, 2, 4 can receive values",
                font_size=18, color=GREEN
            ).next_to(struct_syntax, DOWN, buff=0.2)
            struct_group = VGroup(struct_title, struct_vec, struct_syntax, struct_result)
            struct_group.shift(LEFT * 3)

            # Value mask example
            value_title = Text("Value Mask", font_size=28, color=BLUE).shift(UP * 2)
            value_vec = self.create_labeled_vector(
                ["T", "F", "T", "F", "T", "F"],
                "mask",
                show_indices=True
            ).scale(0.7).next_to(value_title, DOWN, buff=0.4)
            value_syntax = Code(
                code_string="w(mask.V) << ...",
                language="python",
                background="window"
            ).scale(0.5).next_to(value_vec, DOWN, buff=0.3)
            value_result = Text(
                "Positions 0, 2, 4 can receive values",
                font_size=18, color=BLUE
            ).next_to(value_syntax, DOWN, buff=0.2)
            value_group = VGroup(value_title, value_vec, value_syntax, value_result)
            value_group.shift(RIGHT * 3)

            self.play(Write(struct_group))
            self.wait(1)
            self.play(Write(value_group))
            self.wait(2)

            # Highlight that they produce the same result
            same_result = Text(
                "Same effect for boolean vectors!",
                font_size=22, color=YELLOW
            ).to_edge(DOWN, buff=0.8)
            self.play(Write(same_result))
            self.wait(1)

            self.play(FadeOut(struct_group), FadeOut(value_group), FadeOut(same_result))

        with self.voiceover(
            """The complement operator, tilde, inverts the mask. With a complement
            structural mask, we write to positions where the mask has NO value.
            This is exactly what we need for BFS: we want to write to positions
            that haven't been visited yet."""
        ):
            # Show complement mask
            comp_title = Text("Complement Mask", font_size=32, color=YELLOW)
            comp_title.next_to(title, DOWN, buff=0.5)

            # Original mask
            orig_label = Text("visited:", font_size=24).shift(UP * 0.5 + LEFT * 4)
            orig_vec = self.create_labeled_vector(
                ["T", "", "", "", "", ""],
                None, show_indices=True
            ).scale(0.7).next_to(orig_label, RIGHT, buff=0.3)

            # Complement visualization
            comp_label = Text("~visited.S:", font_size=24).shift(DOWN * 1 + LEFT * 4)
            comp_vec = self.create_complement_vector(
                ["T", "", "", "", "", ""]
            ).scale(0.7).next_to(comp_label, RIGHT, buff=0.3)

            self.play(Write(comp_title))
            self.play(Write(orig_label), Write(orig_vec))
            self.wait(1)
            self.play(Write(comp_label), Write(comp_vec))
            self.wait(1)

            # Show syntax
            comp_syntax = Code(
                code_string="# Write only to unvisited positions\nfrontier(~visited.S) << ...",
                language="python",
                background="window"
            ).scale(0.6).to_edge(DOWN, buff=0.8)
            self.play(Write(comp_syntax))
            self.wait(2)

            self.play(
                FadeOut(comp_title), FadeOut(orig_label), FadeOut(orig_vec),
                FadeOut(comp_label), FadeOut(comp_vec), FadeOut(comp_syntax)
            )

        with self.voiceover(
            """Let's see this visually. When we compute a result, the mask
            determines which positions actually get written. Positions where the
            mask is False, or in complement mode where it's True, are simply
            skipped. The computation may happen, but the result is discarded."""
        ):
            # Visual demonstration
            demo_title = Text("Masked Assignment", font_size=28).next_to(title, DOWN, buff=0.4)
            self.play(Write(demo_title))

            # Show: result = [5, 6, 7, 8, 9, 10], mask = [T, F, T, F, T, F]
            result_label = Text("computed result:", font_size=20).shift(UP * 0.8 + LEFT * 2)
            result_vals = VGroup(*[
                self.create_cell(str(5+i), GRAY) for i in range(6)
            ]).arrange(RIGHT, buff=0.1).next_to(result_label, RIGHT, buff=0.3)

            mask_label = Text("mask:", font_size=20).shift(LEFT * 2)
            mask_vals = VGroup(*[
                self.create_cell("T" if i % 2 == 0 else "F", GREEN if i % 2 == 0 else RED)
                for i in range(6)
            ]).arrange(RIGHT, buff=0.1).next_to(mask_label, RIGHT, buff=0.3)
            mask_vals.align_to(result_vals, LEFT)

            output_label = Text("w after assignment:", font_size=20).shift(DOWN * 0.8 + LEFT * 2)
            output_vals = VGroup(*[
                self.create_cell(str(5+i) if i % 2 == 0 else "", GREEN if i % 2 == 0 else DARK_GRAY)
                for i in range(6)
            ]).arrange(RIGHT, buff=0.1).next_to(output_label, RIGHT, buff=0.3)
            output_vals.align_to(result_vals, LEFT)

            self.play(Write(result_label), Write(result_vals))
            self.wait(0.5)
            self.play(Write(mask_label), Write(mask_vals))
            self.wait(0.5)

            # Animate the filtering
            arrows = VGroup()
            for i in range(6):
                if i % 2 == 0:  # Mask is True
                    arrow = Arrow(
                        result_vals[i].get_bottom(),
                        output_vals[i].get_top() + UP * 0.3,
                        color=GREEN, stroke_width=2, buff=0.1
                    )
                    arrows.add(arrow)

            self.play(Write(output_label), *[Create(a) for a in arrows])
            self.play(Write(output_vals))
            self.wait(2)

            self.play(
                FadeOut(demo_title), FadeOut(result_label), FadeOut(result_vals),
                FadeOut(mask_label), FadeOut(mask_vals), FadeOut(output_label),
                FadeOut(output_vals), FadeOut(arrows)
            )

        with self.voiceover(
            """Remember: the mask doesn't change what we compute, it changes where
            we store the results. This distinction becomes important when we combine
            masking with existing values in the output vector, which we'll explore
            next with replacement semantics."""
        ):
            summary = VGroup(
                Text("Masking Summary:", font_size=28, color=YELLOW),
                Text("• Structural (.S) - where values exist", font_size=22),
                Text("• Value (.V) - where values are True", font_size=22),
                Text("• Complement (~) - invert the mask", font_size=22),
                Text("• Controls OUTPUT, not input", font_size=22, color=GREEN),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(ORIGIN)
            self.play(Write(summary))
            self.wait(3)

        self.play(FadeOut(title), FadeOut(summary))
        self.wait(0.5)

    def create_labeled_vector(self, values, label, show_indices=False):
        """Create a horizontal vector with optional label and indices."""
        cells = VGroup()
        for val in values:
            cell = self.create_cell(val, WHITE if val else DARK_GRAY)
            cells.add(cell)
        cells.arrange(RIGHT, buff=0.1)

        result = VGroup(cells)

        if show_indices:
            indices = VGroup(*[
                Text(str(i), font_size=14, color=GRAY).next_to(cells[i], DOWN, buff=0.1)
                for i in range(len(values))
            ])
            result.add(indices)

        if label:
            lbl = Text(label, font_size=20).next_to(cells, LEFT, buff=0.3)
            result.add(lbl)

        return result

    def create_complement_vector(self, values):
        """Create a vector showing complement of structural mask."""
        cells = VGroup()
        for i, val in enumerate(values):
            # Complement: True where original has no value
            is_complement = (val == "" or val is None)
            cell = self.create_cell(
                "T" if is_complement else "F",
                GREEN if is_complement else RED
            )
            cells.add(cell)
        cells.arrange(RIGHT, buff=0.1)

        indices = VGroup(*[
            Text(str(i), font_size=14, color=GRAY).next_to(cells[i], DOWN, buff=0.1)
            for i in range(len(values))
        ])

        return VGroup(cells, indices)

    def create_cell(self, value, color):
        """Create a single cell with value."""
        rect = Square(side_length=0.5, color=color, fill_opacity=0.2, stroke_width=2)
        if value:
            text = Text(str(value), font_size=18).move_to(rect.get_center())
            return VGroup(rect, text)
        return rect
