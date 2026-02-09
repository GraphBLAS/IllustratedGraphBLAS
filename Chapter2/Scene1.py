import sys
sys.path.insert(0, '..')

from manim import *
from manim_voiceover import VoiceoverScene
from dotenv import load_dotenv
load_dotenv()

from Parts import setup_scene


class Scene1(VoiceoverScene, Scene):
    def construct(self):
        setup_scene(self)

        # Title for all examples
        title = Text("Semirings: Same Operation, Different Meanings", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1)

        # ========== PLUS_TIMES Semiring ==========
        # Production Cost Example:
        # A = Factory → Product (units produced per day)
        # B = Product → Material (cost per unit in dollars)
        # C = Factory → Material Cost (total dollars per day)

        with self.voiceover(
            """Let's start with PLUS_TIMES using a manufacturing example.
            Matrix A shows how many units of each product a factory makes per day.
            Matrix B shows the material cost per unit for each product.
            When we multiply, units times dollars per unit gives us total dollars."""
        ):
            semiring_title = Text("PLUS_TIMES: Total Production Cost", font_size=32, color=GREEN)
            semiring_title.next_to(title, DOWN, buff=0.3)
            self.play(Write(semiring_title), run_time=0.8)

            # A: Factory → Product (units/day)
            # F0 makes 50 of P0, 30 of P1, 0 of P2
            # F1 makes 0 of P0, 20 of P1, 40 of P2
            prod_A_data = [[50, 30, 0], [0, 20, 40]]

            # B: Product → Material Cost ($/unit)
            # P0 costs $10/unit, P1 costs $8/unit, P2 costs $5/unit
            # Showing cost breakdown by material type (steel, plastic)
            prod_B_data = [[10, 2], [8, 3], [5, 6]]

            matrix_A_small = self.create_sparse_matrix(prod_A_data, scale=0.55)
            matrix_B_small = self.create_sparse_matrix(prod_B_data, scale=0.55)

            # Result: C[factory, material] = sum over products of (units * cost_per_unit)
            # C[F0, Steel] = 50*10 + 30*8 + 0*5 = 500 + 240 = 740
            # C[F0, Plastic] = 50*2 + 30*3 + 0*6 = 100 + 90 = 190
            # C[F1, Steel] = 0*10 + 20*8 + 40*5 = 160 + 200 = 360
            # C[F1, Plastic] = 0*2 + 20*3 + 40*6 = 60 + 240 = 300
            result_data = [[740, 190], [360, 300]]
            matrix_C_small = self.create_result_matrix(result_data, scale=0.55)

            # Labels for context
            a_label = Text("units/day", font_size=16, color=GRAY)
            b_label = Text("$/unit", font_size=16, color=GRAY)
            c_label = Text("$/day", font_size=16, color=GRAY)

            times_sym = MathTex("\\times").scale(0.8)
            equals_sym = MathTex("=").scale(0.8)

            # Create bipartite graphs for each matrix
            graph_A = self.create_bipartite_graph(
                prod_A_data,
                ["F0", "F1"], ["P0", "P1", "P2"],
                show_weights=True, scale=0.55
            )
            graph_B = self.create_bipartite_graph(
                prod_B_data,
                ["P0", "P1", "P2"], ["St", "Pl"],
                show_weights=True, scale=0.55
            )
            graph_C = self.create_bipartite_graph(
                result_data,
                ["F0", "F1"], ["St", "Pl"],
                show_weights=True, scale=0.55
            )

            # Build matrix columns with graphs below
            a_col = VGroup(MathTex("A").scale(0.7), a_label, matrix_A_small, graph_A).arrange(DOWN, buff=0.25)
            b_col = VGroup(MathTex("B").scale(0.7), b_label, matrix_B_small, graph_B).arrange(DOWN, buff=0.25)
            c_col = VGroup(MathTex("C").scale(0.7), c_label, matrix_C_small, graph_C).arrange(DOWN, buff=0.25)

            equation = VGroup(
                a_col, times_sym, b_col, equals_sym, c_col,
            ).arrange(RIGHT, buff=0.4).move_to(ORIGIN).shift(UP * 0.3)

            self.play(Write(equation), run_time=1.5)

        with self.voiceover(
            """Factory zero produces fifty units of product zero at ten dollars each,
            plus thirty units of product one at eight dollars each. That's five hundred
            plus two forty, giving seven forty dollars per day in steel costs. The units
            cancel out, leaving us with meaningful dollar amounts."""
        ):
            # Show calculation example
            calc_text = MathTex(
                r"\text{Steel cost} = 50 \times \$10 + 30 \times \$8 = \$740\text{/day}",
                font_size=26
            ).next_to(equation, DOWN, buff=0.5)
            self.play(Write(calc_text), run_time=1)

            # Reveal result entries
            self.play(*[entry.animate.set_opacity(1) for entry in matrix_C_small.get_entries()], run_time=1.5)
            self.wait(1)

        # Cleanup PLUS_TIMES
        self.play(FadeOut(semiring_title), FadeOut(equation), FadeOut(calc_text), run_time=0.5)

        # ========== MIN_PLUS Semiring ==========
        # Shortest Path Example:
        # A = City → Hub (travel time in hours)
        # B = Hub → Destination (travel time in hours)
        # C = City → Destination (minimum total travel time)

        with self.voiceover(
            """Now let's see MIN_PLUS with a routing example. Matrix A shows travel
            times from cities to regional hubs. Matrix B shows times from hubs to
            destinations. We want the fastest route, so we add times along each path
            and keep the minimum."""
        ):
            semiring_title = Text("MIN_PLUS: Shortest Travel Time", font_size=32, color=GREEN)
            semiring_title.next_to(title, DOWN, buff=0.3)
            self.play(Write(semiring_title), run_time=0.8)

            # A: City → Hub (hours)
            # NYC can reach Hub0 in 2h, Hub1 in 3h
            # LA can reach Hub1 in 4h, Hub2 in 2h
            cost_A_data = [[2, 3, 0], [0, 4, 2]]

            # B: Hub → Destination (hours)
            # Hub0 to Miami: 3h, Hub1 to Miami: 2h, Hub2 to Miami: 5h
            # Hub0 to Seattle: 5h, Hub1 to Seattle: 3h, Hub2 to Seattle: 2h
            cost_B_data = [[3, 5], [2, 3], [5, 2]]

            matrix_A_small = self.create_sparse_matrix(cost_A_data, scale=0.55)
            matrix_B_small = self.create_sparse_matrix(cost_B_data, scale=0.55)

            # MIN_PLUS result: C[i,j] = min over k of (A[i,k] + B[k,j])
            # C[NYC,Miami] = min(2+3, 3+2) = min(5, 5) = 5
            # C[NYC,Seattle] = min(2+5, 3+3) = min(7, 6) = 6
            # C[LA,Miami] = min(4+2, 2+5) = min(6, 7) = 6
            # C[LA,Seattle] = min(4+3, 2+2) = min(7, 4) = 4
            result_data = [[5, 6], [6, 4]]
            matrix_C_small = self.create_result_matrix(result_data, scale=0.55)

            # Labels for context
            a_label = Text("hours", font_size=16, color=GRAY)
            b_label = Text("hours", font_size=16, color=GRAY)
            c_label = Text("hours", font_size=16, color=GRAY)

            times_sym = MathTex("\\times").scale(0.8)
            equals_sym = MathTex("=").scale(0.8)

            # Create bipartite graphs for each matrix
            graph_A = self.create_bipartite_graph(
                cost_A_data,
                ["NYC", "LA"], ["H0", "H1", "H2"],
                show_weights=True, scale=0.55
            )
            graph_B = self.create_bipartite_graph(
                cost_B_data,
                ["H0", "H1", "H2"], ["Mi", "Se"],
                show_weights=True, scale=0.55
            )
            graph_C = self.create_bipartite_graph(
                result_data,
                ["NYC", "LA"], ["Mi", "Se"],
                show_weights=True, scale=0.55
            )

            # Build matrix columns with graphs below
            a_col = VGroup(MathTex("A").scale(0.7), a_label, matrix_A_small, graph_A).arrange(DOWN, buff=0.25)
            b_col = VGroup(MathTex("B").scale(0.7), b_label, matrix_B_small, graph_B).arrange(DOWN, buff=0.25)
            c_col = VGroup(MathTex("C").scale(0.7), c_label, matrix_C_small, graph_C).arrange(DOWN, buff=0.25)

            equation = VGroup(
                a_col, times_sym, b_col, equals_sym, c_col,
            ).arrange(RIGHT, buff=0.4).move_to(ORIGIN).shift(UP * 0.3)

            self.play(Write(equation), run_time=1.5)

        with self.voiceover(
            """From LA to Seattle, we can go through Hub one in four plus three
            equals seven hours, or through Hub two in two plus two equals four hours.
            The minimum wins: four hours via Hub two. This is exactly how GPS
            navigation finds the fastest route."""
        ):
            calc_text = MathTex(
                r"\text{LA} \to \text{Seattle} = \min(4+3, 2+2) = 4\text{ hours}",
                font_size=26
            ).next_to(equation, DOWN, buff=0.5)
            self.play(Write(calc_text), run_time=1)

            # Reveal result entries
            self.play(*[entry.animate.set_opacity(1) for entry in matrix_C_small.get_entries()], run_time=1.5)
            self.wait(1)

        # Cleanup MIN_PLUS
        self.play(FadeOut(semiring_title), FadeOut(equation), FadeOut(calc_text), run_time=0.5)

        # ========== ANY_PAIR Semiring ==========
        # Reachability Example:
        # A = Person → Skill (1 = has skill)
        # B = Skill → Project (1 = project needs skill)
        # C = Person → Project (1 = person can contribute)

        with self.voiceover(
            """Finally, ANY_PAIR answers yes-or-no questions. Matrix A shows which
            skills each person has. Matrix B shows which skills each project needs.
            We just want to know: can this person contribute to this project at all?"""
        ):
            semiring_title = Text("ANY_PAIR: Reachability", font_size=32, color=GREEN)
            semiring_title.next_to(title, DOWN, buff=0.3)
            self.play(Write(semiring_title), run_time=0.8)

            # A: Person → Skill (boolean)
            # Alice has Python, SQL
            # Bob has SQL, React
            conn_A_data = [[1, 1, 0], [0, 1, 1]]

            # B: Skill → Project (boolean)
            # Backend needs Python, SQL
            # Frontend needs SQL, React
            conn_B_data = [[1, 0], [1, 1], [0, 1]]

            matrix_A_small = self.create_sparse_matrix(conn_A_data, scale=0.55)
            matrix_B_small = self.create_sparse_matrix(conn_B_data, scale=0.55)

            # ANY_PAIR result: C[i,j] = OR over k of (A[i,k] AND B[k,j])
            # C[Alice,Backend] = (1&1) | (1&1) | (0&0) = 1 (Python or SQL)
            # C[Alice,Frontend] = (1&0) | (1&1) | (0&1) = 1 (SQL)
            # C[Bob,Backend] = (0&1) | (1&1) | (1&0) = 1 (SQL)
            # C[Bob,Frontend] = (0&0) | (1&1) | (1&1) = 1 (SQL or React)
            result_data = [[1, 1], [1, 1]]
            matrix_C_small = self.create_result_matrix(result_data, scale=0.55)

            # Labels for context
            a_label = Text("has skill?", font_size=16, color=GRAY)
            b_label = Text("needs skill?", font_size=16, color=GRAY)
            c_label = Text("can help?", font_size=16, color=GRAY)

            times_sym = MathTex("\\times").scale(0.8)
            equals_sym = MathTex("=").scale(0.8)

            # Create bipartite graphs for each matrix (no weights for boolean)
            graph_A = self.create_bipartite_graph(
                conn_A_data,
                ["Ali", "Bob"], ["Py", "SQL", "Re"],
                show_weights=False, scale=0.55
            )
            graph_B = self.create_bipartite_graph(
                conn_B_data,
                ["Py", "SQL", "Re"], ["BE", "FE"],
                show_weights=False, scale=0.55
            )
            graph_C = self.create_bipartite_graph(
                result_data,
                ["Ali", "Bob"], ["BE", "FE"],
                show_weights=False, scale=0.55
            )

            # Build matrix columns with graphs below
            a_col = VGroup(MathTex("A").scale(0.7), a_label, matrix_A_small, graph_A).arrange(DOWN, buff=0.25)
            b_col = VGroup(MathTex("B").scale(0.7), b_label, matrix_B_small, graph_B).arrange(DOWN, buff=0.25)
            c_col = VGroup(MathTex("C").scale(0.7), c_label, matrix_C_small, graph_C).arrange(DOWN, buff=0.25)

            equation = VGroup(
                a_col, times_sym, b_col, equals_sym, c_col,
            ).arrange(RIGHT, buff=0.4).move_to(ORIGIN).shift(UP * 0.3)

            self.play(Write(equation), run_time=1.5)

        with self.voiceover(
            """Both people can contribute to both projects because they each have
            at least one relevant skill. We don't care how many skills match, just
            whether any path exists. This is the key advantage of ANY_PAIR: by ignoring
            actual values, it avoids unnecessary computation. The algorithm can stop
            as soon as it finds any connection, making connectivity queries much faster
            than counting or summing paths."""
        ):
            # Reveal result entries
            self.play(*[entry.animate.set_opacity(1) for entry in matrix_C_small.get_entries()], run_time=1.5)
            self.wait(1)

        # Cleanup ANY_PAIR
        self.play(FadeOut(semiring_title), FadeOut(equation), run_time=0.5)

        # ========== Conclusion ==========
        with self.voiceover(
            """Same matrix multiplication structure, three different questions answered.
            Total production costs, shortest travel times, or simple reachability.
            By choosing the right semiring, GraphBLAS adapts one operation to solve
            many different problems. That's the power of algebraic abstraction."""
        ):
            conclusion = Text(
                "Same operation, different semirings, different insights",
                font_size=28, color=YELLOW
            ).move_to(ORIGIN)
            self.play(Write(conclusion), run_time=1)
            self.wait(2)
            self.play(FadeOut(conclusion), FadeOut(title), run_time=0.5)

        self.wait(0.5)

    def create_bipartite_graph(self, data, left_labels, right_labels, show_weights=True, scale=0.4):
        """Create a directed bipartite graph from matrix data.

        Args:
            data: 2D matrix data (rows → columns relationship)
            left_labels: Labels for left nodes (row entities)
            right_labels: Labels for right nodes (column entities)
            show_weights: Whether to show edge weights
            scale: Overall scale of the graph
        """
        graph_group = VGroup()

        num_left = len(left_labels)
        num_right = len(right_labels)

        # Calculate positions for left and right nodes
        left_spacing = 0.6
        right_spacing = 0.6
        horizontal_gap = 1.8

        # Center the nodes vertically
        left_height = (num_left - 1) * left_spacing
        right_height = (num_right - 1) * right_spacing

        left_nodes = []
        right_nodes = []

        # Create left nodes
        for i, label in enumerate(left_labels):
            y_pos = left_height / 2 - i * left_spacing
            node = Dot(point=LEFT * horizontal_gap / 2 + UP * y_pos, radius=0.08, color=BLUE)
            node_label = Text(label, font_size=14, color=BLUE).next_to(node, LEFT, buff=0.1)
            left_nodes.append(node)
            graph_group.add(node, node_label)

        # Create right nodes
        for j, label in enumerate(right_labels):
            y_pos = right_height / 2 - j * right_spacing
            node = Dot(point=RIGHT * horizontal_gap / 2 + UP * y_pos, radius=0.08, color=GREEN)
            node_label = Text(label, font_size=14, color=GREEN).next_to(node, RIGHT, buff=0.1)
            right_nodes.append(node)
            graph_group.add(node, node_label)

        # Create edges for non-zero entries
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val != 0:
                    start = left_nodes[i].get_center()
                    end = right_nodes[j].get_center()

                    # Create arrow
                    arrow = Arrow(
                        start, end,
                        buff=0.12,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.15,
                        color=GRAY
                    )
                    graph_group.add(arrow)

                    # Add weight label if requested
                    if show_weights:
                        mid = (start + end) / 2
                        # Offset label slightly to avoid overlap
                        offset = normalize(end - start)
                        perp = np.array([-offset[1], offset[0], 0]) * 0.15
                        weight_label = Text(str(val), font_size=10, color=WHITE).move_to(mid + perp)
                        graph_group.add(weight_label)

        return graph_group.scale(scale)

    def create_labeled_matrix(self, data, row_labels, col_labels):
        """Create a matrix with row and column labels."""
        matrix = Matrix(data, v_buff=0.6, h_buff=0.8).scale(0.55)

        # Hide zeros
        num_cols = len(data[0])
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val == 0:
                    matrix.get_entries()[i * num_cols + j].set_opacity(0)

        # Add row labels
        rows = matrix.get_rows()
        row_label_mobjects = VGroup()
        for i, label in enumerate(row_labels):
            lbl = Text(label, font_size=16, color=BLUE_C)
            lbl.next_to(rows[i], LEFT, buff=0.3)
            row_label_mobjects.add(lbl)

        # Add column labels
        cols = matrix.get_columns()
        col_label_mobjects = VGroup()
        for j, label in enumerate(col_labels):
            lbl = Text(label, font_size=16, color=BLUE_C)
            lbl.next_to(cols[j], UP, buff=0.2)
            col_label_mobjects.add(lbl)

        return VGroup(matrix, row_label_mobjects, col_label_mobjects)

    def create_sparse_matrix(self, data, scale=0.6):
        """Create a matrix with zeros hidden."""
        matrix = Matrix(data, v_buff=0.8, h_buff=1.0).scale(scale)

        num_cols = len(data[0])
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val == 0:
                    matrix.get_entries()[i * num_cols + j].set_opacity(0)

        return matrix

    def create_result_matrix(self, data, scale=0.6):
        """Create a matrix with actual values but all entries initially hidden."""
        matrix = Matrix(data, v_buff=0.8, h_buff=1.0).scale(scale)

        # Hide all entries initially (will be revealed with animation)
        for entry in matrix.get_entries():
            entry.set_opacity(0)

        return matrix
