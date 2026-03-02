import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from scene_utils import (
    CHAPTER3_MATRIX_DATA,
    create_undirected_graph,
    animate_vertex_fill,
    setup_scene,
)


class Scene3(VoiceoverScene, Scene):
    """Masked Vector-Matrix Multiply - combining vxm with masking."""

    def construct(self):
        setup_scene(self)

        title = Text("Masked Vector-Matrix Multiply", font_size=42).to_edge(UP)
        self.play(Write(title))

        matrix_data = CHAPTER3_MATRIX_DATA

        with self.voiceover(
            """Now let's combine vector-matrix multiply with masking. The syntax
            puts the mask on the output: w with mask receives the result of
            v times A. The computation happens, but only masked positions get
            the values."""
        ):
            syntax = Code(
                code_string="w(mask) << v.vxm(A, semiring)",
                language="python",
                background="window"
            ).scale(0.7).next_to(title, DOWN, buff=0.4)
            self.play(Write(syntax))
            self.wait(2)

        # Create the graph (undirected with double arrows)
        graph = create_undirected_graph(matrix_data, layout="triangle", scale=0.9)
        graph.to_edge(LEFT, buff=0.8).shift(DOWN * 0.5)

        with self.voiceover(
            """Consider our undirected graph. We start at node zero and discover
            nodes one and three. Now we want to expand from the new frontier,
            but we don't want to rediscover node zero. With bidirectional edges,
            node one can reach back to node zero. A complement mask prevents this."""
        ):
            self.play(Create(graph))
            # Show iteration 1 result
            self.play(animate_vertex_fill(graph.vertices[0], GREEN))  # visited
            self.play(
                animate_vertex_fill(graph.vertices[1], YELLOW),
                animate_vertex_fill(graph.vertices[3], YELLOW)
            )  # current frontier
            self.wait(1)

        # Create vector displays on the right
        vec_group = VGroup()

        # Frontier vector
        frontier_label = Text("frontier:", font_size=22)
        frontier_cells = self.create_vector_display(["", "T", "", "T", "", ""])
        frontier_row = VGroup(frontier_label, frontier_cells).arrange(RIGHT, buff=0.3)

        # Visited vector (mask)
        visited_label = Text("visited:", font_size=22)
        visited_cells = self.create_vector_display(["T", "", "", "", "", ""])
        visited_row = VGroup(visited_label, visited_cells).arrange(RIGHT, buff=0.3)

        # Complement mask
        complement_label = Text("~visited.S:", font_size=22, color=BLUE)
        complement_cells = self.create_vector_display(
            ["F", "T", "T", "T", "T", "T"],
            colors=[RED, GREEN, GREEN, GREEN, GREEN, GREEN]
        )
        complement_row = VGroup(complement_label, complement_cells).arrange(RIGHT, buff=0.3)

        vec_group = VGroup(frontier_row, visited_row, complement_row)
        vec_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        vec_group.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)

        with self.voiceover(
            """Here's our state. The frontier contains nodes one and three. Node
            zero is already visited. The complement mask shows which positions
            are available: everything except position zero."""
        ):
            self.play(Write(frontier_row))
            self.wait(0.5)
            self.play(Write(visited_row))
            self.wait(0.5)
            self.play(Write(complement_row))
            self.wait(1)

        # Show the expansion
        # With symmetric matrix CHAPTER3_MATRIX_DATA:
        # Row 1: [1, 0, 5, 0, 0, 0] - node 1 connects to nodes 0 and 2
        # Row 3: [2, 0, 0, 0, 2, 9] - node 3 connects to nodes 0, 4, and 5
        # Result without mask: positions 0, 2, 4, 5 could have values
        # But node 0 is masked out!

        with self.voiceover(
            """When we expand the frontier, node one can reach nodes zero and two.
            Node three can reach nodes zero, four, and five. Without masking, we'd
            revisit node zero from both directions! The complement mask filters
            these out, keeping only the truly new nodes: two, four, and five."""
        ):
            # Show expansion arrows on graph
            self.play(
                animate_vertex_fill(graph.vertices[2], ORANGE),
                animate_vertex_fill(graph.vertices[4], ORANGE),
                animate_vertex_fill(graph.vertices[5], ORANGE),
            )
            self.wait(1)

        # Now show what happens with a more interesting mask
        self.play(FadeOut(syntax))

        with self.voiceover(
            """Let's see masking in action at the next iteration. Suppose nodes
            zero, one, and three are all visited. We expand from nodes two, four,
            and five. Each has edges back to visited nodes! Node two connects to
            node one. Nodes four and five connect back through the graph. The
            complement mask filters all of these out."""
        ):
            # Update visited to include 0, 1, 3
            new_visited_cells = self.create_vector_display(["T", "T", "", "T", "", ""])
            new_complement_cells = self.create_vector_display(
                ["F", "F", "T", "F", "T", "T"],
                colors=[RED, RED, GREEN, RED, GREEN, GREEN]
            )

            self.play(
                Transform(visited_cells, new_visited_cells),
                Transform(complement_cells, new_complement_cells)
            )

            # Update graph colors
            self.play(
                animate_vertex_fill(graph.vertices[1], GREEN),
                animate_vertex_fill(graph.vertices[3], GREEN),
            )
            self.wait(1)

        # Show the masked output
        result_label = Text("result (masked):", font_size=22, color=YELLOW)
        result_cells = self.create_vector_display(
            ["", "", "T", "", "T", "T"],
            colors=[DARK_GRAY, DARK_GRAY, GREEN, DARK_GRAY, GREEN, GREEN]
        )
        result_row = VGroup(result_label, result_cells).arrange(RIGHT, buff=0.3)
        result_row.next_to(complement_row, DOWN, buff=0.5)

        with self.voiceover(
            """The result only contains nodes two, four, and five. These are the
            newly discovered nodes, the next frontier. Positions zero, one, and
            three are masked out, even if the computation produced values there.
            The mask ensures we only track new discoveries."""
        ):
            self.play(Write(result_row))
            self.wait(2)

        # Show the power of this
        power_box = VGroup(
            Text("Why this matters:", font_size=24, color=YELLOW),
            Text("• No redundant computation on visited nodes", font_size=20),
            Text("• Output directly usable as next frontier", font_size=20),
            Text("• One operation does expand + filter", font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        power_box.to_edge(DOWN, buff=0.5)

        with self.voiceover(
            """This pattern is incredibly efficient. We expand to all neighbors
            and filter to unvisited in a single operation. No post-processing
            needed. The output is directly our new frontier, ready for the next
            iteration."""
        ):
            self.play(Write(power_box))
            self.wait(3)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(vec_group),
            FadeOut(result_row), FadeOut(power_box)
        )
        self.wait(0.5)

    def create_vector_display(self, values, colors=None):
        """Create a horizontal vector display with cells."""
        cells = VGroup()
        for i, val in enumerate(values):
            if colors:
                color = colors[i]
            else:
                color = GREEN if val else DARK_GRAY
            cell = self.create_cell(val, color)
            cells.add(cell)
        cells.arrange(RIGHT, buff=0.05)

        # Add index labels below
        indices = VGroup(*[
            Text(str(i), font_size=12, color=GRAY).next_to(cells[i], DOWN, buff=0.05)
            for i in range(len(values))
        ])

        return VGroup(cells, indices)

    def create_cell(self, value, color):
        """Create a single cell."""
        rect = Square(side_length=0.4, color=color, fill_opacity=0.3, stroke_width=2)
        if value:
            text = Text(str(value), font_size=16).move_to(rect.get_center())
            return VGroup(rect, text)
        return rect
