from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from dotenv import load_dotenv
load_dotenv()

class Scene4(VoiceoverScene, Scene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(voice_name="michelp", transcription_model=None))

        # Title
        title = Text("Examples of Different Types of Networks").scale(0.8).to_edge(UP)
        self.play(Write(title))

        # Define the voiceover text and graphs
        with self.voiceover("""
            On the left, we see a small tree of predator-prey relationships, where each node
            represents a species, and the edges represent feeding relationships. In the center,
            we have a social network, where each node represents an individual, and edges represent
            social connections. Notice the triangular connections, showing mutual friendships.
            On the right, we see a flow of transactions, where each node is an entity, and directed
            edges indicate money flowing from one entity to another.
        """):
            nodes = ["Root", "Child1", "Child2", "Grandchild1", "Grandchild2", "Grandchild3", "Grandchild4"]
            edges = [
                ("Root", "Child1"), ("Root", "Child2"),
                ("Child1", "Grandchild1"), ("Child1", "Grandchild2"),
                ("Child2", "Grandchild3"), ("Child2", "Grandchild4")
            ]

            # Create the directed graph with a tree layout
            tree_graph = Graph(
                nodes, edges,
                layout="tree", root_vertex="Root", layout_scale=2,
                vertex_config={"radius": 0.5, "fill_color": BLUE},
                labels={node: Text(node, font_size=18).scale(0.8) for node in nodes}
            )

            # Display the tree graph
            self.play(Create(tree_graph.scale(0.8).to_edge(LEFT)))
            self.wait(2)

            # Social network graph with a triangle
            social_nodes = ["Alice", "Bob", "Carol", "Dave"]
            social_edges = [("Alice", "Bob"), ("Alice", "Carol"), ("Bob", "Carol"), ("Carol", "Dave")]
            social_graph = DiGraph(
                social_nodes, social_edges,
                layout="spring", layout_scale=1.5,
                vertex_config={"radius": 0.5, "fill_color": GREEN},
                labels={node: Text(node, font_size=24) for node in social_nodes}
            )

            # Position and display social network graph
            social_graph.next_to(tree_graph, RIGHT, buff=1)
            self.play(Create(social_graph.scale(0.8)))
            self.wait(2)

            # Transaction flow graph
            transaction_nodes = ["Criminal", "Entity2", "Entity3", "Bank"]
            transaction_edges = [("Criminal", "Entity2"), ("Entity2", "Entity3"), ("Entity3", "Bank"), ("Bank", "Criminal")]
            transaction_graph = DiGraph(
                transaction_nodes, transaction_edges,
                layout="circular", layout_scale=1.5,
                vertex_config={"radius": 0.5, "fill_color": ORANGE},
                labels={node: Text(node, font_size=24) for node in transaction_nodes}
            )

            # Position and display transaction graph
            transaction_graph.next_to(social_graph, RIGHT, buff=1)
            self.play(Create(transaction_graph.scale(0.8)))
            self.wait(2)

        # Fade out all elements at the end
        self.play(FadeOut(tree_graph), FadeOut(social_graph), FadeOut(transaction_graph), FadeOut(title))
        self.wait(0.5)
