import os
import subprocess
import tempfile
import shutil
from typing import Tuple
from fastapi import UploadFile


class VideoProcessor:
    """Handles video file processing and audio extraction"""
    
    def __init__(self, sample_rate: str = "16000", channels: str = "1"):
        self.sample_rate = sample_rate
        self.channels = channels
    
    def process_video(self, video_file: UploadFile) -> Tuple[str, str]:
        """
        Process uploaded video and extract audio
        Returns: (video_path, audio_path)
        """
        video_path = self._save_video(video_file)
        audio_path = self._extract_audio(video_path)
        return video_path, audio_path
    
    @staticmethod
    def _save_video(video_file: UploadFile) -> str:
        """Save uploaded video to temporary file"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_path = temp_file.name
        
        with temp_file:
            shutil.copyfileobj(video_file.file, temp_file)
        
        return temp_path
    
    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video using FFmpeg"""
        audio_path = video_path.replace('.mp4', '.wav')
        
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", self.sample_rate,
            "-ac", self.channels,
            audio_path
        ], check=True, capture_output=True)
        
        return audio_path
    
    @staticmethod
    def cleanup(video_path: str, audio_path: str):
        """Clean up temporary files"""
        for path in [video_path, audio_path]:
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except Exception as e:
                    print(f"Warning: Failed to delete {path}: {e}")
