from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

class Scene3(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        # Title text
        title = Tex("Graphs are Everywhere").scale(1.5).to_edge(UP)

        self.play(Write(title))
        self.wait(1)

        with self.voiceover(
            """Graphs are a powerful mathemetical structure that can model
ecosystems and food webs, social networks, financial transactions and
many other real world interconnected systems."""
        ):
            # Nodes representing species in the ecosystem
            nodes = [
                "Grass", "Berries", "Insects", "Rabbits", "Squirrels",
                "Mice", "Birds", "Snakes", "Foxes", "Hawks", "Owls"
            ]

            # Edges representing realistic feeding relationships in a forest ecosystem
            edges = [
                ("Grass", "Insects"), ("Grass", "Rabbits"),
                ("Grass", "Mice"), ("Berries", "Birds"), ("Berries", "Squirrels"),
                ("Insects", "Birds"), ("Insects", "Mice"), ("Birds", "Snakes"),
                ("Rabbits", "Foxes"), ("Squirrels", "Hawks"), ("Mice", "Snakes"),
                ("Mice", "Owls"), ("Snakes", "Hawks"), ("Birds", "Owls"),
                ("Rabbits", "Owls"), ("Foxes", "Owls")
            ]

            # Create the graph
            graph = Graph(nodes, edges, layout="spring", layout_scale=3,
                          )

            # Display the graph
            self.play(Create(graph.scale(0.75)))
            self.wait(1)

            labels = {}
            for node in nodes:
                label = Text(node, font_size=24).next_to(graph.vertices[node], UP, buff=0.1)
                labels[node] = label
                self.add(label)  # Add label to the scene

            self.wait(6)
            # Fade out at the end
            self.play(FadeOut(graph), FadeOut(*labels.values()))

        with self.voiceover(
                """ In technology, they underpin computer networks, linking devices across the internet."""
        ):
            nodes = [
                "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
                "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"
            ]

            # Edges representing realistic network connections between cities
            # These connections might represent major data routes or network backbones
            edges = [
                ("New York", "Chicago"), ("New York", "Philadelphia"), ("New York", "Dallas"),
                ("Los Angeles", "Phoenix"), ("Los Angeles", "San Diego"), ("Los Angeles", "San Jose"),
                ("Chicago", "Dallas"), ("Chicago", "Houston"), ("Chicago", "Philadelphia"),
                ("Houston", "Dallas"), ("Phoenix", "San Antonio"), ("San Antonio", "Dallas"),
                ("San Diego", "San Jose"), ("Dallas", "Austin"), ("Dallas", "Fort Worth"),
                ("Austin", "San Antonio"), ("Jacksonville", "Charlotte"), ("Charlotte", "Columbus"),
                ("Philadelphia", "Jacksonville"), ("Columbus", "Chicago"), ("San Jose", "Austin"),
                ("Charlotte", "Dallas")
            ]

            # Create the graph
            graph = Graph(
                nodes, edges,
                layout="circular", layout_scale=3,
                vertex_config={"radius": 0.2}
            )

            # Display the graph
            self.play(Create(graph.scale(0.75)))
            self.wait(1)

            # Add labels to each node
            labels = {}
            for node in nodes:
                label = Text(node, font_size=18).next_to(graph.vertices[node], DOWN, buff=0.1)
                labels[node] = label
                self.add(label)  # Add label to the scene

            self.wait(2)

            # Fade out at the end
            self.play(FadeOut(graph), *[FadeOut(label) for label in labels.values()])
            self.wait(1)

        with self.voiceover("""and power knowledge graphs that organize information for complex queries."""):
            self.wait(5)

        with self.voiceover(
                """In AI, graphs represent the interconnected layers of neural networks, allowing language models to process information efficiently."""
        ):
            # Define the number of layers and nodes per layer
            num_layers = 4
            nodes_per_layer = 4

            # Layer node positions
            layer_positions = []
            layer_spacing = 1.5  # Spacing between layers
            node_spacing = 1  # Spacing between nodes in a layer

            # Generate positions for each layer
            for layer_index in range(num_layers):
                layer_x = -5 + layer_index * layer_spacing
                layer_positions.append([
                    (layer_x, y_pos, 0) for y_pos in range(-int(nodes_per_layer/2), int(nodes_per_layer/2))
                ])

            # Create nodes and store them in a list
            nodes = []
            for layer_index, positions in enumerate(layer_positions):
                layer_nodes = [
                    Dot(point=pos, radius=0.1, color=BLUE).shift(RIGHT * layer_index * layer_spacing) for pos in positions
                ]
                nodes.append(layer_nodes)
                # Animate the nodes appearing
                self.play(*[Create(node) for node in layer_nodes])

            edges = []
            # Create edges (arrows) between each node in one layer to each node in the next layer
            for layer_index in range(num_layers - 1):
                for source_node in nodes[layer_index]:
                    for target_node in nodes[layer_index + 1]:
                        edge = Arrow(
                            start=source_node.get_center(), end=target_node.get_center(),
                            buff=0.1, stroke_width=1, color=GREY
                        )
                        edges.append(edge)
                        self.play(Create(edge), run_time=0.1)

            self.wait(2)

        # Fade out the entire network at the end
        self.play(
            *[FadeOut(node) for layer in nodes for node in layer],
        )

        # Fade out all elements at the end
        self.play(FadeOut(title), FadeOut(*edges))
        self.wait(0.5)
