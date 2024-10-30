from invoke import task
from pathlib import Path
import subprocess

MANIM = "manim"
MANIM_FLAGS = "-ql"
OUTPUT_DIR = Path("media/videos")

def scenes_in_chapter(chapter):
    return sorted(Path(chapter).glob("Scene*.py"))

@task
def render_scene(c, chapter, scene):
    """Render a specific scene from a chapter."""
    scene_file = f"{chapter}/{scene}.py"

    if Path(scene_file).exists():
        c.run(f"{MANIM} {MANIM_FLAGS} {scene_file} {scene}")
    else:
        print(f"Scene {scene_file} not found.")

@task
def build_chapter(c, chapter):
    """Render all scenes in a chapter."""
    for scene_file in scenes_in_chapter(chapter):
        scene_name = scene_file.stem
        render_scene(c, chapter, scene_name)
