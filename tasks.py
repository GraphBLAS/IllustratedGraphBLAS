import os
import shutil
import glob
import re
from invoke import task
from time import sleep

@task
def build_scene(ctx, chapter, scene, quality='l', prod=False):
    """Build a single scene. Use --prod for production build with ElevenLabs TTS."""
    # Extract chapter and scene numbers
    chapter_match = re.search(r'Chapter(\d+)', chapter)
    scene_match = re.search(r'Scene(\d+)', scene)
    chapter_num = chapter_match.group(1) if chapter_match else '0'
    scene_num = scene_match.group(1) if scene_match else '0'

    # Set environment variables
    env_vars = [
        f"CHAPTER_NUM={chapter_num}",
        f"SCENE_NUM={scene_num}",
    ]
    if prod:
        env_vars.append("PROD_MODE=1")
        env_vars.append("VOICE_SERVICE=elevenlabs")
    else:
        env_vars.append("VOICE_SERVICE=gtts")

    env_prefix = " ".join(env_vars)
    command = f"{env_prefix} manim -q{quality} {scene}.py"
    with ctx.cd(chapter):
        ctx.run(command)

@task
def build_chapter(ctx, chapter, quality='l', pause_time=3, prod=False):
    """Build all scenes in a chapter. Use --prod for production build with ElevenLabs TTS."""
    for filename in sorted(os.listdir(chapter)):
        if filename.startswith("Scene") and filename.endswith(".py"):
            scene = filename.replace(".py", "")
            build_scene(ctx, chapter, scene, quality, prod)
            sleep(pause_time)

@task
def build_all(ctx, quality="l", prod=False):
    """Build all chapters. Use --prod for production build with ElevenLabs TTS."""
    for chapter in sorted(os.listdir()):
        if os.path.isdir(chapter) and chapter.startswith("Chapter"):
            build_chapter(ctx, chapter, quality, prod=prod)

@task
def stitch_chapter(ctx, chapter, quality="l"):
    os.chdir(chapter)
    media_folder = os.path.join("media", "videos")
    video_files = []
    resolution = dict(l='480p15', m='720p30', h='1080p60')[quality]

    search_pattern = os.path.join(media_folder, f"Scene*/{resolution}/Scene*.mp4")
    for video in glob.glob(search_pattern):
        if video.endswith(".mp4"):
            video_files.append(video)

    # Sort videos based on scene order (Scene0, Scene1, etc.)
    video_files.sort(key=lambda x: int(x.split("Scene")[-1].split(".")[0]))

    if not video_files:
        print(f"No videos found for resolution '{resolution}' in {media_folder}")
        return

    # Create temporary file list for ffmpeg
    with open(f"videos_to_stitch.txt", "w") as f:
        for video in video_files:
            f.write(f"file '{video}'\n")

    # Stitch videos using ffmpeg
    ctx.run(f"ffmpeg -y -f concat -safe 0 -i videos_to_stitch.txt -c copy ../docs/{chapter}_{resolution}.mp4")
    os.unlink('videos_to_stitch.txt')
    os.chdir('..')

@task
def stitch_all(ctx, quality="l"):
    for chapter in sorted(os.listdir()):
        if os.path.isdir(chapter) and chapter.startswith("Chapter"):
            stitch_chapter(ctx, chapter, quality)

@task
def clean_chapter(ctx, chapter):
    media_folder = os.path.join(chapter, "media")

    if not os.path.exists(media_folder):
        print(f"No media folder found in {chapter}")
        return

    for root, dirs, files in os.walk(media_folder):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

    print(f"Cleaned media folder in {chapter}")

@task
def clean_all(ctx):
    for chapter in sorted(os.listdir()):
        if os.path.isdir(chapter) and chapter.startswith("Chapter"):
            clean_chapter(ctx, chapter)

@task
def render_thumbnails(ctx, quality='l'):
    # Look for chapter directories like "Chapter0", "Chapter1", etc.
    for chapter in sorted(os.listdir()):
        if os.path.isdir(chapter) and chapter.startswith("Chapter"):
            scene_file = os.path.join("Thumb.py")
            output_image = os.path.join(f"../../../../docs/{chapter}.png")
            command = f"manim -q{quality} -s {scene_file} Thumb -o {output_image}"
            with ctx.cd(chapter):
                ctx.run(command)

@task
def all(ctx, quality='l', prod=False):
    """Full rebuild: clean, build, stitch, thumbnails. Use --prod for production."""
    build_all(ctx, quality, prod=prod)
    stitch_all(ctx, quality)
    render_thumbnails(ctx, quality)
