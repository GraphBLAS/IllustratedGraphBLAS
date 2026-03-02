import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene

class Scene3(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("Common Semirings", font_size=48).to_edge(UP)
        self.play(Write(title))

        with self.voiceover(
            """PLUS_TIMES is standard arithmetic, used for calculating total
            costs and weighted sums. MIN_PLUS finds shortest paths by minimizing
            total distance. MAX_PLUS finds longest or widest paths, critical in
            network capacity problems. ANY_PAIR checks reachability, perfect
            for BFS since we only care if a path exists. PLUS_PAIR counts
            unweighted paths, useful when edge weights don't matter. You can
            even define custom semirings with your own operations. This
            flexibility makes GraphBLAS a universal framework for graph algorithms."""
        ):
            # Create table data
            table_data = [
                ["Semiring", "Operations", "Use Case"],
                ["PLUS_TIMES", "× and +", "Total costs"],
                ["MIN_PLUS", "+ and min", "Shortest paths"],
                ["MAX_PLUS", "+ and max", "Longest paths"],
                ["ANY_PAIR", "any and any", "Reachability, BFS"],
                ["PLUS_PAIR", "1 and +", "Unweighted paths"],
            ]

            # Create table
            table = Table(
                table_data,
                include_outer_lines=True,
                line_config={"stroke_width": 1, "color": WHITE}
            ).scale(0.5)
            table.move_to(ORIGIN)

            # Color header row
            for i in range(3):
                table.get_entries((1, i+1)).set_color(YELLOW)

            # Highlight different semirings with different colors
            colors = [BLUE, GREEN, RED, ORANGE, PURPLE]
            for row_idx, color in enumerate(colors, start=2):
                table.get_entries((row_idx, 1)).set_color(color)

            self.play(Create(table))
            self.wait(5)

        self.play(FadeOut(table), FadeOut(title))
        self.wait(0.5)
