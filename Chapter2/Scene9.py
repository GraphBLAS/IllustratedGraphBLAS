import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene

class Scene9(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Chapter Summary", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """Let's review what we've covered in this chapter. Semirings let
            you customize what multiplication means, from counting paths to
            finding shortest routes. Accumulation defines how results merge
            with existing data. Masking focuses computation on relevant
            elements. Together, they transform GraphBLAS into a flexible
            framework for diverse graph problems."""
        ):
            # Summary bullets
            summary = VGroup(
                Text("• Semirings customize multiplication operations", font_size=28),
                Text("• Accumulation combines new with existing data", font_size=28),
                Text("• Masking controls element participation", font_size=28),
                Text("• Integration enables flexible, efficient algorithms", font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            summary.move_to(ORIGIN)

            for bullet in summary:
                self.play(Write(bullet))
                self.wait(0.5)

            self.wait(2)
            self.play(FadeOut(summary))

        with self.voiceover(
            """In the next chapter, we'll explore additional GraphBLAS
            operations that give you even more control. Element-wise operations
            let you combine matrices position-by-position. Selection operations
            filter elements based on predicates. And apply operations transform
            every element in a matrix. These tools complete your GraphBLAS toolkit."""
        ):
            # Preview next chapter
            self.play(Transform(title, Text("Next: Chapter 3", font_size=48).to_edge(UP)))

            preview = VGroup(
                Text("• Element-wise operations", font_size=28),
                Text("• Select operations", font_size=28),
                Text("• Apply operations", font_size=28),
                Text("• Practical applications", font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            preview.move_to(ORIGIN)

            for bullet in preview:
                self.play(Write(bullet))
                self.wait(0.5)

            self.wait(2)

        self.play(FadeOut(title), FadeOut(preview))
        self.wait(0.5)
