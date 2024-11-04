import os
import shutil
import glob
from invoke import task

@task
def build_scene(ctx, chapter, scene, quality='l'):
    command = f"manim -q{quality} {scene}.py"
    with ctx.cd(chapter):
        ctx.run(command)

@task
def build_chapter(ctx, chapter, quality='l'):
    for filename in sorted(os.listdir(chapter)):
        if filename.startswith("Scene") and filename.endswith(".py"):
            scene = filename.replace(".py", "")
            build_scene(ctx, chapter, scene, quality)

@task
def build_all(ctx, quality="l"):
    for chapter in sorted(os.listdir()):
        if os.path.isdir(chapter) and chapter.startswith("Chapter"):
            build_chapter(ctx, chapter, quality)

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
    ctx.run(f"ffmpeg -f concat -safe 0 -i videos_to_stitch.txt -c copy ../docs/{chapter}_{resolution}.mp4")
    os.unlink('videos_to_stitch.txt')
    os.chdir('..')

@task
def stitch_all(ctx, quality="l"):
    for chapter in sorted(os.listdir()):
        if os.path.isdir(chapter) and chapter.startswith("Chapter"):
            stitch_chapter(ctx, chapter, quality)

@task
def clean_media(ctx, chapter):
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

from invoke import task
import os

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
