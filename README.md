# Video Profile Extractor API

API for extracting professional profiles from video presentations using AI transcription and analysis.

## Features

- Video upload and audio extraction
- AI-powered audio transcription (Groq Whisper / Gemini)
- Automatic profile information extraction
- Professional CV profile generation
- Automatic fallback between AI services

## Architecture

The application follows Object-Oriented Programming principles with clear separation of concerns:

```
├── main.py                    # FastAPI application and endpoints
├── config.py                  # Configuration management
├── services/
│   ├── __init__.py           # Service exports
│   ├── ai_service.py         # AI service implementations (Groq, Gemini)
│   ├── ai_factory.py         # Factory pattern for AI service creation
│   └── video_processor.py    # Video processing and audio extraction
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables in `.env`:
```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

3. Run the application:
```bash
python main.py
```

## API Endpoints

### `GET /`
Returns HTML upload form

### `POST /upload-video`
Process video and extract profile

**Request:** multipart/form-data with video file

**Response:**
```json
{
  "cv_profile": "Professional profile text...",
  "profile_data": {
    "name": "John Doe",
    "profession": "Software Engineer",
    "experience": "5 years in web development",
    "education": "Computer Science degree",
    "technologies": "Python, JavaScript, React",
    "languages": "English, Spanish",
    "achievements": "Led team of 5 developers",
    "soft_skills": "Leadership, communication"
  }
}
```

### `GET /health`
Health check endpoint

## Configuration

All configuration is centralized in `config.py`:

- `GROQ_API_KEY`: Groq API key for transcription
- `GEMINI_API_KEY`: Gemini API key (fallback)
- `PORT`: Server port (default: 9000)
- `AUDIO_SAMPLE_RATE`: Audio sample rate (default: 16000)
- `AUDIO_CHANNELS`: Audio channels (default: 1)

## Deployment

### Docker
```bash
docker build -t video-profile-extractor .
docker run -p 9000:9000 -e GROQ_API_KEY=xxx -e GEMINI_API_KEY=xxx video-profile-extractor
```

### Render
Configure environment variables in Render dashboard:
- `GROQ_API_KEY`
- `GEMINI_API_KEY`

## Design Patterns

- **Factory Pattern**: `AIServiceFactory` creates appropriate AI service instances
- **Strategy Pattern**: `AIService` abstract class with multiple implementations
- **Dependency Injection**: Services injected at application startup
- **Single Responsibility**: Each class has one clear purpose
