from manim import *
import os

# Single source of truth for logo filenames used in Chapter0
LOGO_FILENAMES = [
    "aristotle.png", "anaconda.png", "berkeley.png",
    "cmu.png", "cwi.png", "du.png",
    "graphegon.png", "humboldt.png", "intel.png",
    "imbr.png", "lucata.png", "mit.png",
    "njit.png", "nvidia.png", "pnnl.png",
    "redis.png", "romatre.png", "tamu.png",
    "ucdavis.png", "ucsb.png", "unibz.png",
    "JuliaComputing.jpg", "falkor.png", "supabase3.png",
]


def create_logo_grid(img_dir="../imgs", scale=0.5, rows=4, cols=6, buff=0.5):
    """
    Create a grid of logo images.

    Args:
        img_dir: Directory containing logo images (relative to chapter directory)
        scale: Scale factor for each logo
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        buff: Buffer space between logos

    Returns:
        Group of logos arranged in a grid
    """
    logos = [
        ImageMobject(os.path.join(img_dir, filename)).scale(scale)
        for filename in LOGO_FILENAMES
    ]
    return Group(*logos).arrange_in_grid(rows=rows, cols=cols, buff=buff)
