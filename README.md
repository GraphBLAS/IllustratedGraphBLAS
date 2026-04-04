# IllustratedGraphBLAS

## Local Development Setup

Create a virtual environment and install requirements:

```
virtualenv --python=python3 .virt
. .virt/bin/activate
pip install -r requirements.txt
```

### Quality Settings

Manim quality settings control resolution and framerate. Pass them via the
`--quality` argument (default is `l`):

| Flag | Resolution | Framerate |
|------|-----------|-----------|
| `l`  | 480p      | 15 fps    |
| `m`  | 720p      | 30 fps    |
| `h`  | 1080p     | 60 fps    |

### Production Builds (Local)

By default, builds use Google TTS for free narration. Production builds use
ElevenLabs TTS for high-quality narration. To enable production builds, add
your ElevenLabs API key to a `.env` file in the repo root:

```
ELEVEN_API_KEY=sk_your_key_here
```

Then pass `--prod` to any build command. In production mode, the small
chapter/scene indicator in the upper-right corner is hidden.

### Build Commands

#### `invoke build-scene`

Renders a single Manim scene from a chapter. The scene is rendered using Manim
with voiceover narration. In dev mode (default), a small chapter/scene
indicator appears in the upper-right corner. The rendered video is saved to
the chapter's `media/videos/` directory.

```
invoke build-scene --chapter Chapter0 --scene Scene0 --quality l
```

| Option | Description |
|--------|-------------|
| `--chapter` | Chapter directory name (e.g. `Chapter0`). Required. |
| `--scene` | Scene file name without `.py` extension (e.g. `Scene0`). Required. |
| `--quality` | Render quality: `l`, `m`, or `h`. Default: `l`. |
| `--prod` | Use ElevenLabs TTS and hide the dev indicator. Requires `ELEVEN_API_KEY` in `.env`. |

#### `invoke build-chapter`

Builds all scenes in a chapter sequentially, then stitches them into a single
video file. Scenes are discovered by finding all `Scene*.py` files in the
chapter directory and sorting them by number. A configurable pause is inserted
between scene builds to respect ElevenLabs API concurrency limits.

```
invoke build-chapter --chapter Chapter0 --quality l
```

| Option | Description |
|--------|-------------|
| `--chapter` | Chapter directory name (e.g. `Chapter0`). Required. |
| `--quality` | Render quality: `l`, `m`, or `h`. Default: `l`. |
| `--pause-time` | Seconds to wait between scene builds. Default: `3`. Set to `0` for CI builds. |
| `--prod` | Use ElevenLabs TTS and hide the dev indicator. |
| `--no-stitch` | Build all scenes but skip stitching them into a final video. |

#### `invoke build-all`

Builds every chapter in the repository. Iterates through all directories
matching `Chapter*` in sorted order, calling `build-chapter` for each one.

```
invoke build-all --quality l
```

| Option | Description |
|--------|-------------|
| `--quality` | Render quality: `l`, `m`, or `h`. Default: `l`. |
| `--prod` | Use ElevenLabs TTS and hide the dev indicator. |

#### `invoke stitch-chapter`

Concatenates all rendered scene videos for a chapter into a single MP4 file
using ffmpeg. Finds all `Scene*/[resolution]/Scene*.mp4` files in the
chapter's `media/videos/` directory, sorts them by scene number, and produces
a final video at `docs/ChapterN_[resolution].mp4`.

```
invoke stitch-chapter --chapter Chapter0 --quality l
```

| Option | Description |
|--------|-------------|
| `--chapter` | Chapter directory name (e.g. `Chapter0`). Required. |
| `--quality` | Determines which resolution folder to stitch from: `l` = 480p15, `m` = 720p30, `h` = 1080p60. Default: `l`. |

#### `invoke stitch-all`

Stitches all chapters. Iterates through all `Chapter*` directories in sorted
order, calling `stitch-chapter` for each one.

```
invoke stitch-all --quality l
```

| Option | Description |
|--------|-------------|
| `--quality` | Resolution to stitch. Default: `l`. |

#### `invoke clean-chapter`

Recursively deletes all files and subdirectories inside a chapter's `media/`
folder. This removes all rendered videos, cached LaTeX, generated images, and
voiceover audio files for that chapter. The source `.py` files are not
affected.

```
invoke clean-chapter --chapter Chapter0
```

| Option | Description |
|--------|-------------|
| `--chapter` | Chapter directory name (e.g. `Chapter0`). Required. |

#### `invoke clean-all`

Cleans every chapter's media directory. Iterates through all `Chapter*`
directories in sorted order, calling `clean-chapter` for each one.

```
invoke clean-all
```

No options.

#### `invoke render-thumbnails`

Renders a static thumbnail image for each chapter by running each chapter's
`Thumb.py` file with Manim's screenshot mode (`-s`). The resulting PNG is
saved to `docs/ChapterN.png` for use on the site.

```
invoke render-thumbnails --quality l
```

| Option | Description |
|--------|-------------|
| `--quality` | Render quality for the thumbnail. Default: `l`. |

#### `invoke all`

Full rebuild pipeline. Builds all chapters, stitches all final videos, and
renders all thumbnails. Equivalent to running `build-all`, `stitch-all`, and
`render-thumbnails` in sequence.

```
invoke all --quality l
```

| Option | Description |
|--------|-------------|
| `--quality` | Render quality: `l`, `m`, or `h`. Default: `l`. |
| `--prod` | Use ElevenLabs TTS and hide the dev indicator. |

#### `invoke demo`

Renders a quick demo of a `scene_utils` component for testing and development.
Each utility registered in `_demos/demo.py` can be previewed in isolation
without building a full chapter scene.

```
invoke demo --util create_sparse_matrix --quality l
invoke demo --list
```

| Option | Description |
|--------|-------------|
| `--util` | Name of the scene_utils component to demo (e.g. `create_sparse_matrix`). |
| `--quality` | Render quality: `l`, `m`, or `h`. Default: `l`. |
| `--list` | Print all available demo utilities and exit. |

#### `invoke notebooks`

Launches the Jupyter notebook browser, opening the interactive GraphBLAS
tutorial index at `notebooks/index.ipynb`.

```
invoke notebooks
```

No options.

## CI/CD Build System

Videos are built automatically by GitHub Actions and deployed to GitHub Pages.
Video files are not stored in git.

### Dev and Prod Views

The site has two views, built from the same source but with different videos:

- **Prod** (root URL) — production-quality narration via ElevenLabs TTS.
  Updated only when a manual prod build is triggered.
- **Dev** (`/dev/` path) — development narration via Google TTS (free).
  Updated automatically on every push to `main` that changes chapter source files.

### Automatic Builds (Dev)

Any push to `main` that modifies chapter source files, `scene_utils/`, `imgs/`,
`docs/*.md`, `mkdocs.yml`, `manim.cfg`, or `requirements.txt` triggers a dev
build. Only chapters with source changes are rebuilt; unchanged chapters use
cached videos from previous runs.

### Manual Builds

Go to **Actions > Build Videos and Deploy Site > Run workflow** to trigger a
manual build. Options:

- **chapters** — comma-separated chapter numbers to rebuild (e.g. `0,3,5`) or
  `all` (default)
- **prod** — check this box to build with ElevenLabs TTS and update the prod
  site at the root URL

### Required Secrets for Prod Builds

Prod builds require an ElevenLabs API key. Contributors who fork this repo need
to add their own key:

1. Sign up at [elevenlabs.io](https://elevenlabs.io) and get an API key
2. In your fork, go to **Settings > Secrets and variables > Actions**
3. Add a repository secret named `ELEVEN_API_KEY` with your key

Without this secret, dev builds (Google TTS) still work. Only prod builds
require the ElevenLabs key.
