import os

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
