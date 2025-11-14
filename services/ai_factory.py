from typing import Optional
from config import Config
from .ai_service import AIService, GroqService, GeminiService


class AIServiceFactory:
    """Factory for creating AI service instances with fallback support"""
    
    @staticmethod
    def create_service() -> AIService:
        """Create AI service with automatic fallback"""
        primary_service = AIServiceFactory._try_create_groq()
        if primary_service:
            return primary_service
        
        fallback_service = AIServiceFactory._try_create_gemini()
        if fallback_service:
            return fallback_service
        
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
