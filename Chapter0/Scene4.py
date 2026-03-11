import sys
sys.path.insert(0, '..')
import math

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import setup_scene


def get_chart_config(values):
    """Return y_range, scale factor, and format function based on max value."""
    max_val = max(values)

    if max_val >= 1.0:  # Billions scale
        # Round up to nice number for y_max
        y_max = math.ceil(max_val * 1.2)  # 20% headroom
        y_step = max(1, y_max // 4)
        scale = 1.0
        suffix = "B"
    else:  # Millions scale (values are in billions, so 0.375 = 375M)
        # Convert to millions for display
        max_millions = max_val * 1000
        y_max_millions = math.ceil(max_millions / 100) * 100  # Round to nearest 100M
        y_max = y_max_millions / 1000  # Back to billions for chart
        y_step = y_max / 4
        scale = 1000  # Multiply by 1000 to get millions
        suffix = "M"

    return y_max, y_step, scale, suffix


def format_value(val, scale, suffix):
    """Format value for bar label."""
    display_val = val * scale if scale > 1 else val
    if display_val >= 10:
        return f"{int(display_val)}{suffix}"
    else:
        return f"{display_val:.1f}{suffix}"

# Graph labels with edge counts
GRAPHS = ["Twitter\n1.5B", "web\n1.9B", "kron\n4.2B", "urand\n4.3B"]

# Placeholder benchmark results (billions of edges/second)
BENCHMARKS = {
    "Breadth First Search": [5.8, 7.1, 7.6, 5.0],
    "PageRank": [0.148, 0.337, 0.217, 0.375],
    "Connected Components": [1.2, 1.1, 1.1, 1.1],
    "Single Source Shortest Path": [0.181, 0.717, 0.257, 0.175],
}

ALGORITHM_SUMMARIES = {
    "Breadth First Search": "BFS explores a graph level by level, traversing all nodes reachable from a starting node.",
    "PageRank": "PageRank computes the importance of each node based on the structure of incoming links.",
    "Connected Components": "Connected components identifies groups of nodes that are reachable from one another.",
    "Single Source Shortest Path": "SSSP finds the minimum cost path from a source node to all other nodes in a weighted graph.",
}

class Scene4(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        title = Text("SuiteSparse GraphBLAS Performance", font_size=36).to_edge(UP)
        y_label = Text("Edges/Second", font_size=20).rotate(PI/2)

        with self.voiceover(
            """SuiteSparse GraphBLAS achieves impressive performance across
            standard graph algorithm benchmarks on four large-scale graphs
            ranging from 1.5 to 4.3 billion edges."""
        ):
            self.play(Write(title))

        for bench_name, values in BENCHMARKS.items():
            subtitle = Text(bench_name, font_size=28).next_to(title, DOWN)

            # Get dynamic y-axis configuration based on data scale
            y_max, y_step, scale, suffix = get_chart_config(values)

            # Create chart with zero values initially
            chart = BarChart(
                values=[0, 0, 0, 0],
                bar_names=GRAPHS,
                y_range=[0, y_max, y_step],
                y_length=4,
                x_length=10,
                bar_colors=[BLUE, GREEN, ORANGE, RED],
            ).scale(0.9)

            y_label_copy = y_label.copy().next_to(chart, LEFT)

            with self.voiceover(f"Results for {bench_name}."):
                self.play(Write(subtitle))
                self.play(Create(chart), FadeIn(y_label_copy))
                # Animate bars growing from zero to actual values
                self.play(chart.animate.change_bar_values(values))

                # Add value labels above each bar
                bar_labels = VGroup()
                for i, (bar, val) in enumerate(zip(chart.bars, values)):
                    label = Text(format_value(val, scale, suffix), font_size=18)
                    label.next_to(bar, UP, buff=0.1)
                    bar_labels.add(label)
                self.play(FadeIn(bar_labels))
                self.wait(1)

            with self.voiceover(ALGORITHM_SUMMARIES[bench_name]):
                self.wait(0.5)  # Chart stays visible during voiceover

            self.play(FadeOut(chart), FadeOut(subtitle), FadeOut(y_label_copy), FadeOut(bar_labels))

        self.play(FadeOut(title))
        self.wait(0.5)
