import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


class Scene8(VoiceoverScene, Scene):
    """Chapter 6 Conclusion: Summary and teaser for Chapter 7."""

    def construct(self):
        setup_scene(self)

        title = Text("Chapter Summary", font_size=44).to_edge(UP)

        with self.voiceover(
            """This chapter covered element-wise operations. Element-wise add
            computes union, keeping edges from either input. Element-wise multiply
            computes intersection, keeping only shared edges."""
        ):
            self.play(Write(title))

            # Create summary blocks
            blocks = VGroup()

            # eWiseAdd block
            add_block = VGroup(
                Text("eWiseAdd", font_size=28, color=YELLOW),
                Text("Union (A OR B)", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.1)
            add_box = SurroundingRectangle(add_block, color=YELLOW, buff=0.2)
            add_group = VGroup(add_box, add_block)

            # eWiseMult block
            mult_block = VGroup(
                Text("eWiseMult", font_size=28, color=RED_C),
                Text("Intersection (A AND B)", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.1)
            mult_box = SurroundingRectangle(mult_block, color=RED_C, buff=0.2)
            mult_group = VGroup(mult_box, mult_block)

            blocks.add(add_group, mult_group)
            blocks.arrange(RIGHT, buff=1)
            blocks.shift(UP * 0.5)

            self.play(FadeIn(add_group), FadeIn(mult_group))
            self.wait(1)

        with self.voiceover(
            """Select filters elements by condition, useful for thresholding
            weights. Apply transforms values using unary functions like square
            root, or binary functions with scalars for scaling and division.
            Reduce collapses dimensions, summing rows, columns, or the entire matrix."""
        ):
            # Add select, apply, and reduce blocks
            select_block = VGroup(
                Text("Select", font_size=28, color=GREEN),
                Text("Filter by condition", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.1)
            select_box = SurroundingRectangle(select_block, color=GREEN, buff=0.2)
            select_group = VGroup(select_box, select_block)

            apply_block = VGroup(
                Text("Apply", font_size=28, color=ORANGE),
                Text("Transform values", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.1)
            apply_box = SurroundingRectangle(apply_block, color=ORANGE, buff=0.2)
            apply_group = VGroup(apply_box, apply_block)

            reduce_block = VGroup(
                Text("Reduce", font_size=28, color=PURPLE),
                Text("Collapse dimensions", font_size=20, color=GRAY),
            ).arrange(DOWN, buff=0.1)
            reduce_box = SurroundingRectangle(reduce_block, color=PURPLE, buff=0.2)
            reduce_group = VGroup(reduce_box, reduce_block)

            lower_blocks = VGroup(select_group, apply_group, reduce_group)
            lower_blocks.arrange(RIGHT, buff=0.8)
            lower_blocks.next_to(blocks, DOWN, buff=0.8)

            self.play(FadeIn(select_group), FadeIn(apply_group), FadeIn(reduce_group))
            self.wait(1)

        with self.voiceover(
            """In the next chapter, we explore shortest path algorithms. Using the
            min-plus semiring, we will see how repeated matrix operations find the
            shortest distances through a weighted graph."""
        ):
            # Fade out summary blocks
            all_blocks = VGroup(blocks, lower_blocks)
            self.play(all_blocks.animate.shift(UP * 0.5).scale(0.8))

            # Show next chapter teaser
            next_title = Text("Next: Chapter 7 - Shortest Paths", font_size=32, color=BLUE)
            next_title.shift(DOWN * 1)

            teaser = VGroup(
                MathTex(r"\text{min-plus semiring}", font_size=28, color=BLUE_C),
                MathTex(r"(+, \times) \rightarrow (\min, +)", font_size=24, color=GRAY),
            ).arrange(DOWN, buff=0.2)
            teaser.next_to(next_title, DOWN, buff=0.4)

            self.play(Write(next_title))
            self.wait(0.5)
            self.play(FadeIn(teaser))
            self.wait(1)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(all_blocks),
            FadeOut(next_title), FadeOut(teaser),
        )
        self.wait(0.5)
