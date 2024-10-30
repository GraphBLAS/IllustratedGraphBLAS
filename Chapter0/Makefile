# Variables
SCENE_FILES := $(wildcard Scene*.py)
MANIM_CMD = manim

# Quality setting: l = 480p15, m = 720p30, h = 1080p60, p = 1440p60, k = 4K
QUALITY ?= m
QUALITY_DIR := $(shell echo $(QUALITY) | sed -n \
    -e 's/^l$$/480p15/p' \
    -e 's/^m$$/720p30/p' \
    -e 's/^h$$/1080p60/p' \
    -e 's/^p$$/1440p60/p' \
    -e 's/^k$$/4K/p' | head -n 1)

# Default target: List available targets
.PHONY: all
all:
	@echo "Available targets:"
	@echo "  make SceneN [QUALITY=...] - Build a specific scene (e.g., make Scene0 QUALITY=m)"
	@echo "  make all_scenes           - Build all scenes"
	@echo "  make final                - Create final movie from all scenes"
	@echo "  make clean                - Remove generated videos"

# Pattern rule to build each scene into the appropriate quality directory
media/videos/%/$(QUALITY_DIR)/%.mp4: %.py
	@mkdir -p media/videos/$*/$(QUALITY_DIR)
	$(MANIM_CMD) --quality $(QUALITY) $<

# Create individual targets for each scene with dependency on the Python file
$(foreach scene,$(basename $(SCENE_FILES)),\
  $(eval $(scene): media/videos/$(scene)/$(QUALITY_DIR)/$(scene).mp4))

# Target to build all scenes
.PHONY: all_scenes
all_scenes: $(patsubst %.py,media/videos/%/$(QUALITY_DIR)/%.mp4,$(SCENE_FILES))

# Final movie target: Stitch all videos together with FFmpeg (including subtitles if any)
.PHONY: final
final: all_scenes
	@echo "Creating video list..."
	@rm -f video_list.txt
	@for scene in $(basename $(SCENE_FILES)); do \
		echo "file 'media/videos/$$scene/$(QUALITY_DIR)/$$scene.mp4'" >> video_list.txt; \
	done
	@echo "Concatenating all scenes into final_movie.mp4..."
	ffmpeg -f concat -safe 0 -i video_list.txt -c copy -map 0:v -map 0:s? final_movie.mp4

# Clean target to remove all generated videos
.PHONY: clean
clean:
	rm -rf media/videos video_list.txt final_movie.mp4
