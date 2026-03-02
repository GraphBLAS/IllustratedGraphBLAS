from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from dotenv import load_dotenv
load_dotenv()
import os

class Scene1(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(voice_name="michelp", transcription_model=None))

        # Title text
        title = Tex("Graphs are Everywhere").scale(1.5).to_edge(UP)

        self.play(Write(title))
        self.wait(1)

        with self.voiceover(
            """Graphs are a powerful mathematical structure that can
            model social networks, financial transactions, language
            models, drug interactions, and many other real-world
            interconnected systems. In a graph, entities are
            represented as nodes, and the relationships between them
            are represented as edges. This simple structure can
            capture remarkably complex patterns."""
        ):
            # Nodes representing species in the ecosystem
            nodes = [
                "Jane", "Rick", "Jessica", "Teagan", "Justin",
                "Matt", "Mike", "Sandra", "Olive", "Hank", "Cooper"
            ]

            # Edges representing realistic feeding relationships in a forest ecosystem
            edges = [
                ("Jane", "Rick"), ("Jane", "Jessica"),
                ("Jane", "Mike"), ("Teagan", "Matt"), ("Teagan", "Justin"),
                ("Rick", "Matt"), ("Rick", "Mike"), ("Matt", "Sandra"),
                ("Jessica", "Olive"), ("Justin", "Hank"), ("Mike", "Sandra"),
                ("Mike", "Cooper"), ("Sandra", "Hank"), ("Matt", "Cooper"),
                ("Jessica", "Cooper"), ("Olive", "Cooper")
            ]

            # Create the graph
            graph = Graph(nodes, edges, layout="kamada_kawai", layout_scale=3,
                          )

            # Display the graph
            self.play(Create(graph.scale(0.8)))
            self.wait(4)

            labels = {}
            for node in nodes:
                label = Text(node, font_size=28).next_to(graph.vertices[node], UP, buff=0.15)
                labels[node] = label
                self.add(label)  # Add label to the scene

            self.wait(6)
            # Fade out at the end
            self.play(FadeOut(graph), FadeOut(*labels.values()))

        with self.voiceover(
                """In technology, graphs underpin the analysis and
                security architecture of computer networks, linking
                devices across the internet. Network administrators
                use graph algorithms to detect intrusions, optimize
                routing, and identify critical infrastructure."""
        ):
            nodes = [
                "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
                "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"
            ]

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

            graph = Graph(
                nodes, edges,
                layout="circular", layout_scale=3,
                vertex_config={"radius": 0.2}
            )

            self.play(Create(graph.scale(0.75)))
            self.wait(1)

            # Add labels to each node
            labels = {}
            for node in nodes:
                label = Text(node, font_size=18).next_to(graph.vertices[node], DOWN, buff=0.1)
                labels[node] = label
                self.add(label)  # Add label to the scene

            self.wait(4)

            # Fade out at the end
            self.play(FadeOut(graph), *[FadeOut(label) for label in labels.values()])

        with self.voiceover(
                """Graphs also power knowledge bases that organize
                information for complex queries. Each node can
                represent a concept, and edges define the relationships
                between them, enabling systems to answer sophisticated
                questions by traversing these connections."""
        ):
            # Define nodes and edges for the knowledge graph
            nodes = [
                "LM", "Transformer", "SelfAttention", "Pretraining", "FineTuning",
                "Tokenization", "EmbeddingLayer", "PositionalEncoding", "MLM", "TransferLearning"
            ]

            # Define edges between nodes to represent relationships
            edges = [
                ("LM", "Transformer"),
                ("LM", "SelfAttention"),
                ("LM", "Pretraining"),
                ("LM", "FineTuning"),
                ("Transformer", "SelfAttention"),
                ("Transformer", "EmbeddingLayer"),
                ("SelfAttention", "PositionalEncoding"),
                ("Pretraining", "MLM"),
                ("Pretraining", "TransferLearning"),
                ("Tokenization", "EmbeddingLayer"),
                ("EmbeddingLayer", "SelfAttention"),
                ("MLM", "FineTuning")
            ]

            # Create the directed graph without labels
            graph = DiGraph(
                vertices=nodes,
                edges=edges,
                layout="shell",
                vertex_config={
                    "radius": 0.2,
                    "fill_color": BLUE,
                },
                edge_config={
                    "stroke_color": GREY,
                    "stroke_width": 2,
                    "tip_length": 0.2,
                }
            )

            # Add the graph to the scene
            self.play(Create(graph))
            self.wait(1)

            # Define labels for each node
            labels = {
                "LM": "Language Models",
                "Transformer": "Transformer Architecture",
                "SelfAttention": "Self-Attention",
                "Pretraining": "Pretraining",
                "FineTuning": "Fine-Tuning",
                "Tokenization": "Tokenization",
                "EmbeddingLayer": "Embedding Layer",
                "PositionalEncoding": "Positional Encoding",
                "MLM": "Masked Language Modeling",
                "TransferLearning": "Transfer Learning"
            }

            # Add labels next to each node
            label_objects = []
            for node_key in graph.vertices:
                node = graph.vertices[node_key]
                label_text = labels[node_key]
                label = Text(label_text, font_size=20)

                # Position label next to the node
                label.next_to(node, DOWN, buff=0.2)
                label_objects.append(label)

                # Animate the label appearing
                self.play(FadeIn(label), run_time=0.5)

            # Fade out the graph and labels at the end
            self.play(FadeOut(graph), *[FadeOut(label) for label in label_objects])
            self.wait(1)

        with self.voiceover(
                """In artificial intelligence, graphs represent the
                interconnected layers of neural networks. Each layer
                passes information forward through weighted edges,
                allowing language models and other deep learning
                systems to process and transform data efficiently."""
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
                            buff=0.1, stroke_width=1, color=GREY)
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
