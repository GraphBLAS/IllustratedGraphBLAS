import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import (
    CHAPTER3_MATRIX_DATA,
    create_undirected_graph,
    animate_vertex_fill,
    setup_scene,
)


class Scene6(VoiceoverScene, Scene):
    """Complete BFS Animation - full algorithm trace on a graph."""

    def construct(self):
        setup_scene(self)

        title = Text("BFS in Action", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Create the graph (undirected with double arrows)
        matrix_data = CHAPTER3_MATRIX_DATA
        graph = create_undirected_graph(matrix_data, layout="triangle", scale=1.0)
        graph.to_edge(LEFT, buff=1).shift(DOWN * 0.3)

        # Color legend
        legend = VGroup(
            VGroup(
                Square(side_length=0.3, color=WHITE, fill_opacity=0.3),
                Text("Unvisited", font_size=16)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Square(side_length=0.3, color=YELLOW, fill_opacity=0.5),
                Text("Frontier", font_size=16)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Square(side_length=0.3, color=GREEN, fill_opacity=0.5),
                Text("Visited", font_size=16)
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        legend.to_corner(UP + RIGHT, buff=0.5)

        with self.voiceover(
            """Let's trace BFS on our six-node graph, starting from node zero.
            We'll watch both the graph coloring and the vector states update
            at each iteration. White nodes are unvisited, yellow is the current
            frontier, and green means visited with a level number."""
        ):
            self.play(Create(graph))
            self.play(Write(legend))
            self.wait(1)

        # Vector displays
        vec_area = VGroup()

        frontier_label = Text("frontier:", font_size=22, color=YELLOW)
        levels_label = Text("levels:", font_size=22, color=GREEN)
        level_label = Text("level:", font_size=22, color=BLUE)

        # Initial state
        frontier_cells = self.create_vector_row(["", "", "", "", "", ""])
        levels_cells = self.create_vector_row(["", "", "", "", "", ""])
        level_val = Text("1", font_size=24, color=BLUE)

        frontier_row = VGroup(frontier_label, frontier_cells).arrange(RIGHT, buff=0.3)
        levels_row = VGroup(levels_label, levels_cells).arrange(RIGHT, buff=0.3)
        level_row = VGroup(level_label, level_val).arrange(RIGHT, buff=0.3)

        vec_area = VGroup(level_row, frontier_row, levels_row)
        vec_area.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        vec_area.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)

        with self.voiceover(
            """We start by setting the source node. Node zero gets level one
            in the levels vector and is added to the frontier. This is our
            initial state before the main loop begins."""
        ):
            self.play(Write(vec_area))

            # Initialize: levels[0] = 1, frontier[0] = True
            self.play(animate_vertex_fill(graph.vertices[0], YELLOW))

            new_frontier = self.create_vector_row(["T", "", "", "", "", ""])
            new_levels = self.create_vector_row(["1", "", "", "", "", ""])
            self.play(
                Transform(frontier_cells, new_frontier),
                Transform(levels_cells, new_levels),
            )
            self.wait(1)

        # Iteration 1: level = 2
        with self.voiceover(
            """Iteration one: level equals two. We expand the frontier by
            multiplying with the adjacency matrix. From node zero, we can
            reach nodes one and three. The complement mask on levels ensures
            we only keep unvisited nodes. Both are new, so both stay."""
        ):
            # Update level
            new_level_val = Text("2", font_size=24, color=BLUE)
            self.play(Transform(level_val, new_level_val))

            # Show expansion: nodes 1 and 3 become frontier
            self.play(
                animate_vertex_fill(graph.vertices[0], GREEN),  # now visited
                animate_vertex_fill(graph.vertices[1], YELLOW),
                animate_vertex_fill(graph.vertices[3], YELLOW),
            )

            # Update vectors
            new_frontier = self.create_vector_row(["", "T", "", "T", "", ""])
            new_levels = self.create_vector_row(["1", "2", "", "2", "", ""])
            self.play(
                Transform(frontier_cells, new_frontier),
                Transform(levels_cells, new_levels),
            )
            self.wait(1)

        # Iteration 2: level = 3
        with self.voiceover(
            """Iteration two: level equals three. From nodes one and three, we
            can reach nodes zero, two, four, and five. But node zero is already
            visited! The complement mask filters it out. Only the unvisited nodes
            two, four, and five become the new frontier. This is masking in action."""
        ):
            # Update level
            new_level_val = Text("3", font_size=24, color=BLUE)
            self.play(Transform(level_val, new_level_val))

            # Show expansion: nodes 2, 4, 5 become frontier
            self.play(
                animate_vertex_fill(graph.vertices[1], GREEN),  # now visited
                animate_vertex_fill(graph.vertices[3], GREEN),  # now visited
                animate_vertex_fill(graph.vertices[2], YELLOW),
                animate_vertex_fill(graph.vertices[4], YELLOW),
                animate_vertex_fill(graph.vertices[5], YELLOW),
            )

            # Update vectors
            new_frontier = self.create_vector_row(["", "", "T", "", "T", "T"])
            new_levels = self.create_vector_row(["1", "2", "3", "2", "3", "3"])
            self.play(
                Transform(frontier_cells, new_frontier),
                Transform(levels_cells, new_levels),
            )
            self.wait(1)

        # Iteration 3: level = 4 (but frontier becomes empty)
        with self.voiceover(
            """Iteration three: level would be four. We expand from nodes two,
            four, and five. Node two connects to one and four. Node four connects
            to two, three, and five. Node five connects to three and four. But
            every single neighbor is already visited! After masking, the frontier
            is completely empty."""
        ):
            # Update level
            new_level_val = Text("4", font_size=24, color=BLUE)
            self.play(Transform(level_val, new_level_val))

            # All frontier nodes become visited, no new frontier
            self.play(
                animate_vertex_fill(graph.vertices[2], GREEN),
                animate_vertex_fill(graph.vertices[4], GREEN),
                animate_vertex_fill(graph.vertices[5], GREEN),
            )

            # Update frontier to empty
            new_frontier = self.create_vector_row(["", "", "", "", "", ""])
            self.play(Transform(frontier_cells, new_frontier))
            self.wait(1)

        with self.voiceover(
            """The frontier is empty, so we exit the loop. The levels vector
            contains the final result: node zero is at level one, nodes one
            and three at level two, and nodes two, four, five at level three.
            Every node's distance from the source is recorded."""
        ):
            # Highlight the final result
            done_label = Text("BFS Complete!", font_size=28, color=GREEN).to_edge(DOWN, buff=0.5)
            self.play(Write(done_label))

            # Highlight levels vector
            result_box = SurroundingRectangle(levels_cells, color=GREEN, buff=0.1)
            self.play(Create(result_box))
            self.wait(2)

        # Show the efficiency
        self.play(FadeOut(done_label), FadeOut(result_box))

        with self.voiceover(
            """Notice what happened: three iterations to process six nodes, with
            no wasted work. Each node was discovered exactly once, processed
            exactly once, and never revisited. The combination of masking and
            replacement made this automatic. No explicit tracking, no visited
            set management, just clean algebraic operations."""
        ):
            efficiency = VGroup(
                Text("Efficiency:", font_size=28, color=YELLOW),
                Text("• 3 iterations for 6 nodes", font_size=22),
                Text("• Each node discovered once", font_size=22),
                Text("• Each node processed once", font_size=22),
                Text("• No explicit visited tracking", font_size=22),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            efficiency.to_edge(DOWN, buff=0.4)

            self.play(Write(efficiency))
            self.wait(3)

        self.play(
            FadeOut(title), FadeOut(graph), FadeOut(legend),
            FadeOut(vec_area), FadeOut(efficiency)
        )
        self.wait(0.5)

    def create_vector_row(self, values):
        """Create a row of cells for vector display."""
        cells = VGroup()
        for i, val in enumerate(values):
            cell = self.create_cell(val)
            cells.add(cell)
        cells.arrange(RIGHT, buff=0.05)

        # Add indices
        indices = VGroup(*[
            Text(str(i), font_size=12, color=GRAY).next_to(cells[i], DOWN, buff=0.08)
            for i in range(len(values))
        ])

        return VGroup(cells, indices)

    def create_cell(self, value):
        """Create a single cell with value."""
        color = GREEN if value else DARK_GRAY
        rect = Square(side_length=0.4, color=color, fill_opacity=0.3 if value else 0.1, stroke_width=2)
        if value:
            text = Text(str(value), font_size=16).move_to(rect.get_center())
            return VGroup(rect, text)
        return rect
