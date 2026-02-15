import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene


class Scene4(VoiceoverScene, Scene):
    """Replacement Semantics - merge vs replace behavior."""

    def construct(self):
        setup_scene(self)

        title = Text("Replacement Semantics", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """There's one more crucial concept for BFS: replacement semantics.
            When we write to a masked output, what happens to existing values
            in positions where the mask is False? By default, they're preserved.
            But with replace equals True, they're cleared."""
        ):
            subtitle = Text(
                "What happens to existing values?",
                font_size=28, color=YELLOW
            ).next_to(title, DOWN, buff=0.4)
            self.play(Write(subtitle))
            self.wait(2)

        # Setup the example
        # w = [1, 2, 3, _, _, _] (existing values)
        # mask = [F, F, F, T, T, T]
        # computed result = [_, _, _, 5, 6, 7]

        with self.voiceover(
            """Let's trace through an example. Our output vector w has existing
            values one, two, three in the first three positions. The mask allows
            writing only to positions three, four, and five. Our computation
            produces values five, six, seven for those positions."""
        ):
            # Existing w
            existing_label = Text("existing w:", font_size=24)
            existing_cells = self.create_vector([1, 2, 3, "", "", ""], colors=[
                BLUE, BLUE, BLUE, DARK_GRAY, DARK_GRAY, DARK_GRAY
            ])
            existing_row = VGroup(existing_label, existing_cells).arrange(RIGHT, buff=0.5)
            existing_row.shift(UP * 1.5)

            # Mask
            mask_label = Text("mask:", font_size=24)
            mask_cells = self.create_vector(["F", "F", "F", "T", "T", "T"], colors=[
                RED, RED, RED, GREEN, GREEN, GREEN
            ])
            mask_row = VGroup(mask_label, mask_cells).arrange(RIGHT, buff=0.5)
            mask_row.next_to(existing_row, DOWN, buff=0.4)

            # Computed result (what would be written)
            result_label = Text("computed:", font_size=24)
            result_cells = self.create_vector(["", "", "", 5, 6, 7], colors=[
                DARK_GRAY, DARK_GRAY, DARK_GRAY, YELLOW, YELLOW, YELLOW
            ])
            result_row = VGroup(result_label, result_cells).arrange(RIGHT, buff=0.5)
            result_row.next_to(mask_row, DOWN, buff=0.4)

            self.play(Write(existing_row))
            self.wait(0.5)
            self.play(Write(mask_row))
            self.wait(0.5)
            self.play(Write(result_row))
            self.wait(1)

        # Show the two outcomes side by side
        self.play(FadeOut(subtitle))

        merge_title = Text("Default (Merge)", font_size=28, color=ORANGE).shift(LEFT * 3 + DOWN * 0.5)
        replace_title = Text("replace=True", font_size=28, color=PURPLE).shift(RIGHT * 3 + DOWN * 0.5)

        with self.voiceover(
            """Here's where the two behaviors differ. With default merge behavior,
            existing values are preserved where the mask is False. The output
            combines old and new: one, two, three from before, plus five, six,
            seven from the computation."""
        ):
            self.play(Write(merge_title))

            # Merge result
            merge_result = self.create_vector([1, 2, 3, 5, 6, 7], colors=[
                BLUE, BLUE, BLUE, YELLOW, YELLOW, YELLOW
            ])
            merge_result.next_to(merge_title, DOWN, buff=0.3)

            # Annotations
            merge_old = Text("preserved", font_size=16, color=BLUE)
            merge_new = Text("new", font_size=16, color=YELLOW)
            merge_old.next_to(merge_result[0][:3], DOWN, buff=0.3)
            merge_new.next_to(merge_result[0][3:], DOWN, buff=0.3)

            self.play(Write(merge_result), Write(merge_old), Write(merge_new))
            self.wait(2)

        with self.voiceover(
            """With replace equals True, the output is cleared first. Only
            positions where the mask is True receive values. Positions zero,
            one, two are now empty, even though they had values before. This
            is exactly what the BFS frontier needs."""
        ):
            self.play(Write(replace_title))

            # Replace result
            replace_result = self.create_vector(["", "", "", 5, 6, 7], colors=[
                DARK_GRAY, DARK_GRAY, DARK_GRAY, YELLOW, YELLOW, YELLOW
            ])
            replace_result.next_to(replace_title, DOWN, buff=0.3)

            # Annotations
            replace_cleared = Text("cleared", font_size=16, color=RED)
            replace_new = Text("new", font_size=16, color=YELLOW)
            replace_cleared.next_to(replace_result[0][:3], DOWN, buff=0.3)
            replace_new.next_to(replace_result[0][3:], DOWN, buff=0.3)

            self.play(Write(replace_result), Write(replace_cleared), Write(replace_new))
            self.wait(2)

        # Clean up the comparison
        self.play(
            FadeOut(existing_row), FadeOut(mask_row), FadeOut(result_row),
            FadeOut(merge_title), FadeOut(merge_result), FadeOut(merge_old), FadeOut(merge_new),
            FadeOut(replace_title), FadeOut(replace_result), FadeOut(replace_cleared), FadeOut(replace_new)
        )

        # Show the BFS application
        with self.voiceover(
            """For BFS, the frontier must contain only the current level's nodes.
            If we used merge, old frontier nodes would accumulate, and we'd
            reprocess them forever. With replace, each iteration gives us a
            clean frontier containing only newly discovered nodes."""
        ):
            bfs_title = Text("Why BFS needs replace=True", font_size=32, color=YELLOW)
            bfs_title.next_to(title, DOWN, buff=0.5)
            self.play(Write(bfs_title))

            # Show iteration progression
            iter_labels = VGroup(
                Text("After iter 1:", font_size=22),
                Text("After iter 2:", font_size=22),
                Text("After iter 3:", font_size=22),
            ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(LEFT * 4)

            # With merge (wrong)
            merge_header = Text("Merge (wrong)", font_size=20, color=RED).shift(RIGHT * 0.5 + UP * 1)
            merge_iters = VGroup(
                self.create_small_vector(["", "T", "", "T", "", ""], "frontier at 1,3"),
                self.create_small_vector(["", "T", "T", "T", "T", "T"], "still has 1,3!"),
                self.create_small_vector(["", "T", "T", "T", "T", "T"], "infinite loop"),
            ).arrange(DOWN, buff=0.4).next_to(merge_header, DOWN, buff=0.3)

            # With replace (correct)
            replace_header = Text("Replace (correct)", font_size=20, color=GREEN).shift(RIGHT * 4 + UP * 1)
            replace_iters = VGroup(
                self.create_small_vector(["", "T", "", "T", "", ""], "frontier at 1,3"),
                self.create_small_vector(["", "", "T", "", "T", "T"], "frontier at 2,4,5"),
                self.create_small_vector(["", "", "", "", "", ""], "empty = done!"),
            ).arrange(DOWN, buff=0.4).next_to(replace_header, DOWN, buff=0.3)

            self.play(Write(iter_labels))
            self.play(Write(merge_header), Write(replace_header))
            self.wait(0.5)

            for i in range(3):
                self.play(Write(merge_iters[i]), Write(replace_iters[i]))
                self.wait(1)

            self.wait(1)

        # Show the syntax
        self.play(
            FadeOut(iter_labels), FadeOut(merge_header), FadeOut(merge_iters),
            FadeOut(replace_header), FadeOut(replace_iters), FadeOut(bfs_title)
        )

        with self.voiceover(
            """The syntax is simple: add replace equals True to the output
            specification. This single parameter makes the difference between
            a working BFS and an infinite loop. Combined with complement masking,
            we get exactly the behavior we need."""
        ):
            syntax = Code(
                code_string="# The crucial BFS line\nfrontier(~levels.S, replace=True) << frontier.vxm(A, any_pair)",
                language="python",
                background="window"
            ).scale(0.7).move_to(ORIGIN)
            self.play(Write(syntax))
            self.wait(2)

            # Breakdown
            breakdown = VGroup(
                Text("~levels.S: only unvisited positions", font_size=22, color=BLUE),
                Text("replace=True: clear old frontier", font_size=22, color=GREEN),
                Text("vxm: expand to neighbors", font_size=22, color=YELLOW),
            ).arrange(DOWN, buff=0.3).next_to(syntax, DOWN, buff=0.5)
            self.play(Write(breakdown))
            self.wait(3)

        self.play(FadeOut(title), FadeOut(syntax), FadeOut(breakdown))
        self.wait(0.5)

    def create_vector(self, values, colors):
        """Create a vector display with colored cells."""
        cells = VGroup()
        for i, (val, color) in enumerate(zip(values, colors)):
            cell = self.create_cell(str(val) if val != "" else "", color)
            cells.add(cell)
        cells.arrange(RIGHT, buff=0.05)

        indices = VGroup(*[
            Text(str(i), font_size=14, color=GRAY).next_to(cells[i], DOWN, buff=0.1)
            for i in range(len(values))
        ])

        return VGroup(cells, indices)

    def create_small_vector(self, values, annotation):
        """Create a small vector with annotation."""
        cells = VGroup()
        for val in values:
            color = GREEN if val else DARK_GRAY
            rect = Square(side_length=0.3, color=color, fill_opacity=0.3, stroke_width=1)
            if val:
                text = Text(str(val), font_size=12).move_to(rect.get_center())
                cells.add(VGroup(rect, text))
            else:
                cells.add(rect)
        cells.arrange(RIGHT, buff=0.02)

        annot = Text(annotation, font_size=14, color=GRAY)
        annot.next_to(cells, RIGHT, buff=0.2)

        return VGroup(cells, annot)

    def create_cell(self, value, color):
        """Create a single cell."""
        rect = Square(side_length=0.5, color=color, fill_opacity=0.3, stroke_width=2)
        if value:
            text = Text(str(value), font_size=20).move_to(rect.get_center())
            return VGroup(rect, text)
        return rect
