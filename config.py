import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PORT = int(os.getenv("PORT", 9000))
    HOST = "0.0.0.0"
    
    # Audio processing settings
    AUDIO_SAMPLE_RATE = "16000"
    AUDIO_CHANNELS = "1"
    
    # AI Model settings
    GROQ_TRANSCRIPTION_MODEL = "whisper-large-v3"
    GROQ_CHAT_MODEL = "llama-3.1-8b-instant"
    GEMINI_MODEL = "gemini-2.0-flash"
    GEMINI_FALLBACK_MODEL = "gemini-pro"
    
    # MongoDB settings
    MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "video_profile_extractor")
    MONGODB_AUTH_DATABASE = os.getenv("MONGODB_AUTH_DATABASE", "admin")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GROQ_API_KEY and not cls.GEMINI_API_KEY:
            raise ValueError("At least one API key (GROQ_API_KEY or GEMINI_API_KEY) must be set")
