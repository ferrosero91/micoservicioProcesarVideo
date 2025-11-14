from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from config import Config
from services import VideoProcessor
from services.ai_factory import AIServiceFactory

Config.validate()

app = FastAPI(title="Video Profile Extractor API")
video_processor = VideoProcessor(
    sample_rate=Config.AUDIO_SAMPLE_RATE,
    channels=Config.AUDIO_CHANNELS
)
ai_service = AIServiceFactory.create_service()


@app.get("/", response_class=HTMLResponse)
async def get_upload_form():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Video Upload - JSON API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .info { background: #e8f4fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>🎥 Video Profile Extraction</h1>
    <div class="info">
        <h3>📋 This API returns JSON responses</h3>
        <p>The application processes videos and returns:</p>
        <pre>{
  "cv_profile": "Professional profile text for CV",
  "profile_data": {
    "name": "Extracted name",
    "profession": "Profession/occupation",
    "experience": "Years and areas of experience",
    "education": "Academic training",
    "technologies": "Tools and technologies",
    "languages": "Spoken languages",
    "achievements": "Recognition and achievements",
    "soft_skills": "Personal skills"
  }
}</pre>
    </div>
    <form action="/upload-video" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="video/*" required>
        <button type="submit">📤 Upload and Process Video</button>
    </form>
    <p><em>Note: Use tools like Postman, curl or browser inspector to see the complete JSON response.</em></p>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    video_path = None
    audio_path = None
    
    try:
        video_path, audio_path = video_processor.process_video(file)
        transcription = ai_service.transcribe_audio(audio_path)
        profile_data = ai_service.extract_profile(transcription)
        cv_profile = ai_service.generate_cv_profile(transcription, profile_data)
        
        return JSONResponse(content={
            "cv_profile": cv_profile,
            "profile_data": profile_data
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if video_path and audio_path:
            video_processor.cleanup(video_path, audio_path)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
