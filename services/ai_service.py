import json
import re
from abc import ABC, abstractmethod
from config import Config
from database import PromptRepository


class AIService(ABC):
    """Abstract base class for AI services"""
    
    def __init__(self):
        self.prompt_repo = PromptRepository()
    
    @abstractmethod
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio file to text"""
        pass
    
    @abstractmethod
    def extract_profile(self, text: str) -> dict:
        """Extract profile information from text"""
        pass
    
    @abstractmethod
    def generate_cv_profile(self, transcription: str, profile_data: dict) -> str:
        """Generate professional CV profile"""
        pass


class GroqService(AIService):
    """Groq AI service implementation"""
    
    def __init__(self):
        super().__init__()
        from groq import Groq
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        print("Groq AI service initialized")
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Groq Whisper"""
        try:
            with open(audio_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_path, file.read()),
                    model=Config.GROQ_TRANSCRIPTION_MODEL,
                    prompt="Transcribe this audio in Spanish. It's a personal or professional presentation.",
                    response_format="text",
                    language="es"
                )
            return transcription.strip() if transcription else "Unable to transcribe audio."
        except Exception as e:
            raise Exception(f"Groq transcription error: {str(e)}")
    
    def extract_profile(self, text: str) -> dict:
        """Extract profile information using Groq"""
        prompt = self.prompt_repo.get_prompt_with_variables("profile_extraction", text=text)
        
        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an assistant that extracts professional profile information from transcribed texts. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content.strip()
            return self._parse_json_response(response_text)
        except Exception as e:
            raise Exception(f"Groq profile extraction error: {str(e)}")
    
    def generate_cv_profile(self, transcription: str, profile_data: dict) -> str:
        """Generate CV profile using Groq"""
        prompt = self.prompt_repo.get_prompt_with_variables(
            "cv_generation",
            transcription=transcription,
            profile_data=json.dumps(profile_data, ensure_ascii=False)
        )
        
        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an assistant specialized in creating professional CV profiles. Generate persuasive and professional texts in Spanish."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Groq CV generation error: {str(e)}")
    
    @staticmethod
    def _parse_json_response(response_text: str) -> dict:
        """Parse JSON from AI response"""
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("No valid JSON found in response")


class GeminiService(AIService):
    """Gemini AI service implementation"""
    
    def __init__(self):
        super().__init__()
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        try:
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            print(f"Gemini AI service initialized with {Config.GEMINI_MODEL}")
        except Exception:
            self.model = genai.GenerativeModel(Config.GEMINI_FALLBACK_MODEL)
            print(f"Gemini AI service initialized with {Config.GEMINI_FALLBACK_MODEL}")
        
        self.genai = genai
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Gemini"""
        try:
            audio_file = self.genai.upload_file(audio_path)
            response = self.model.generate_content([
                "Transcribe this audio in Spanish. Provide only the speech transcription, without additional comments or special formatting.",
                audio_file
            ])
            return response.text.strip() if response.text else "Unable to transcribe audio."
        except Exception as e:
            raise Exception(f"Gemini transcription error: {str(e)}")
    
    def extract_profile(self, text: str) -> dict:
        """Extract profile information using Gemini"""
        prompt = self.prompt_repo.get_prompt_with_variables("profile_extraction", text=text)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            return GroqService._parse_json_response(response_text)
        except Exception as e:
            raise Exception(f"Gemini profile extraction error: {str(e)}")
    
    def generate_cv_profile(self, transcription: str, profile_data: dict) -> str:
        """Generate CV profile using Gemini"""
        prompt = self.prompt_repo.get_prompt_with_variables(
            "cv_generation",
            transcription=transcription,
            profile_data=json.dumps(profile_data, ensure_ascii=False)
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini CV generation error: {str(e)}")
