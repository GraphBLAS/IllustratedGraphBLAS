import os
from manim import Text, UP, RIGHT


def get_speech_service():
    """
    Returns the appropriate speech service based on the VOICE_SERVICE environment variable.

    - VOICE_SERVICE=elevenlabs: Uses ElevenLabs (paid, high quality)
    - VOICE_SERVICE=gtts or unset: Uses Google TTS (free, online)
    """
    voice_service = os.environ.get('VOICE_SERVICE', 'gtts').lower()

    if voice_service == 'elevenlabs':
        from manim_voiceover.services.elevenlabs import ElevenLabsService
        return ElevenLabsService(voice_name="michelp", transcription_model=None)
    else:
        from manim_voiceover.services.gtts import GTTSService
        return GTTSService()


def is_prod_mode():
    """Check if we're in production mode."""
    return os.environ.get('PROD_MODE', '') == '1'


def get_scene_indicator():
    """Get the chapter/scene indicator string (e.g., '1/2' for Chapter 1, Scene 2)."""
    chapter_num = os.environ.get('CHAPTER_NUM', '0')
    scene_num = os.environ.get('SCENE_NUM', '0')
    return f"{chapter_num}/{scene_num}"


def setup_scene(scene):
    """
    Set up a scene with the appropriate speech service and dev indicator.

    Call this at the start of construct() instead of set_speech_service().

    In dev mode (when --prod flag is NOT used), adds a small indicator
    in the upper right corner showing chapter/scene (e.g., "1/2").

    Args:
        scene: The VoiceoverScene instance
    """
    # Set up speech service
    scene.set_speech_service(get_speech_service())

    # Add dev indicator if not in production mode
    if not is_prod_mode():
        indicator_text = get_scene_indicator()
        indicator = Text(indicator_text, font_size=20, color="#666666")
        indicator.to_corner(UP + RIGHT, buff=0.2)
        scene.add(indicator)
