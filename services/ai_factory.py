from typing import Optional
from config import Config
from .ai_service import AIService, GroqService, GeminiService, HuggingFaceService


class AIServiceFactory:
    """Factory for creating AI service instances with fallback support"""
    
    @staticmethod
    def create_service() -> AIService:
        """Create AI service with automatic fallback: Groq → Gemini → Hugging Face"""
        # Try Groq first (best for transcription)
        groq_service = AIServiceFactory._try_create_groq()
        if groq_service:
            return groq_service
        
        # Try Gemini second (powerful and free)
        gemini_service = AIServiceFactory._try_create_gemini()
        if gemini_service:
            return gemini_service
        
        # Try Hugging Face third (free, many models)
        hf_service = AIServiceFactory._try_create_huggingface()
        if hf_service:
            return hf_service
        
        raise RuntimeError("No AI service available. Check your API keys and dependencies.")
    
    @staticmethod
    def _try_create_groq() -> Optional[AIService]:
        """Try to create Groq service"""
        if not Config.GROQ_API_KEY:
            return None
        
        try:
            return GroqService()
        except ImportError:
            print("Warning: Groq library not installed. Install with: pip install groq")
            return None
        except Exception as e:
            print(f"Warning: Failed to initialize Groq service: {e}")
            return None
    
    @staticmethod
    def _try_create_gemini() -> Optional[AIService]:
        """Try to create Gemini service"""
        if not Config.GEMINI_API_KEY:
            return None
        
        try:
            return GeminiService()
        except ImportError:
            print("Warning: Google Generative AI library not installed. Install with: pip install google-generativeai")
            return None
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini service: {e}")
            return None
    
    @staticmethod
    def _try_create_huggingface() -> Optional[AIService]:
        """Try to create Hugging Face service"""
        if not Config.HUGGINGFACE_API_KEY:
            return None
        
        try:
            return HuggingFaceService()
        except ImportError:
            print("Warning: Hugging Face Hub library not installed. Install with: pip install huggingface_hub")
            return None
        except Exception as e:
            print(f"Warning: Failed to initialize Hugging Face service: {e}")
            return None
