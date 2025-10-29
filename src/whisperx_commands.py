# whisperx_commands.py
"""
Centralized WhisperX command builders for subtitle generation.
Provides different WhisperX configurations for various use cases.
"""

class WhisperXConfig:
    """Configuration presets for WhisperX"""
    
    # Language models
    MODELS = {
        'large-v2': 'large-v2',
        'large-v3': 'large-v3',
        'base': 'base',
        'small': 'small',
        'medium': 'medium',
    }
    
    # Alignment models for different languages
    ALIGN_MODELS = {
        'fr': 'jonatasgrosman/wav2vec2-large-xlsr-53-french',
        'en': 'WAV2VEC2_ASR_BASE_960H',
        'es': 'jonatasgrosman/wav2vec2-large-xlsr-53-spanish',
        'de': 'jonatasgrosman/wav2vec2-large-xlsr-53-german',
    }
    
    # Default configurations
    DEFAULTS = {
        'chunk_size': '8',
        'batch_size': '8',
        'condition_on_previous_text': 'True',
    }


class WhisperXCommandMaker:
    def __init__(self) -> None:
        pass

    @staticmethod
    def make_jnatasgrosman_whisperx_command(wav_filename):
        """jonatasgrosman is an alignment model for French text -> dialogue alignment"""
        return [
            # This line suppresses the awful warning spam
            "python", "-W", "ignore", "-m",  
            # Now starts the real job:
            "whisperx", wav_filename, "--language", "fr", 
            "--model", "large-v3", 
            "--align_model", "jonatasgrosman/wav2vec2-large-xlsr-53-french", 
            "--chunk_size", "8", 
            "--batch_size", "8", 
            "--condition_on_previous_text", "True"
        ]

   