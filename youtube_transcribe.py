"""
YouTube Video Transcription Function

This module provides a function to download and transcribe YouTube videos using yt-dlp and OpenAI Whisper.

Requirements:
    pip install yt-dlp openai-whisper imageio-ffmpeg

Note: After installing imageio-ffmpeg, you need to create a copy of the FFmpeg executable:
    python -c "import imageio_ffmpeg; import shutil; import os; src = imageio_ffmpeg.get_ffmpeg_exe(); dst = os.path.join(os.path.dirname(src), 'ffmpeg.exe'); shutil.copy2(src, dst) if not os.path.exists(dst) else None"

Usage:
    text = youtube_transcribe("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(text)
"""

import re
import os
import tempfile
import time
from typing import Optional

# Set up FFmpeg path before importing whisper
try:
    import imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    # Add FFmpeg directory to PATH
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
except ImportError:
    pass  # Continue without FFmpeg setup

import whisper


def youtube_transcribe(url: str) -> str:
    """
    Download and transcribe a YouTube video.
    
    Args:
        url (str): YouTube video URL (supports both standard and short formats)
        
    Returns:
        str: The transcription text or an error message
        
    Example:
        >>> text = youtube_transcribe("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        >>> print(text)
    """
    
    # Step 1: Extract video ID from URL
    video_id = extract_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL. Please provide a valid YouTube URL."
    
    audio_file = None
    
    try:
        # Step 2: Download audio using yt-dlp
        audio_file = download_audio(video_id, url)
        if not audio_file:
            return "Error: Failed to download audio from YouTube video."
        
        # Step 3: Transcribe audio using Whisper
        transcription = transcribe_audio(audio_file)
        
        return transcription
        
    except KeyboardInterrupt:
        # Handle user interruption gracefully
        return "Error: Transcription was interrupted by user."
        
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"
        
    finally:
        # Always clean up temporary audio file (even on crash/interruption)
        if audio_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except Exception as cleanup_error:
                pass  # Silently ignore cleanup errors


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL.
    
    Supports:
        - Standard format: https://www.youtube.com/watch?v=VIDEO_ID
        - Short format: https://youtu.be/VIDEO_ID
        - Shorts format: https://www.youtube.com/shorts/VIDEO_ID
        
    Args:
        url (str): YouTube URL
        
    Returns:
        Optional[str]: Video ID if found, None otherwise
    """
    # Pattern for standard YouTube URL: https://www.youtube.com/watch?v=VIDEO_ID
    standard_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
    
    # Pattern for short YouTube URL: https://youtu.be/VIDEO_ID
    short_pattern = r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})'
    
    # Pattern for YouTube Shorts: https://www.youtube.com/shorts/VIDEO_ID
    shorts_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})'
    
    # Try standard pattern first
    match = re.search(standard_pattern, url)
    if match:
        return match.group(1)
    
    # Try short pattern
    match = re.search(short_pattern, url)
    if match:
        return match.group(1)
    
    # Try shorts pattern
    match = re.search(shorts_pattern, url)
    if match:
        return match.group(1)
    
    return None


def download_audio(video_id: str, url: str) -> Optional[str]:
    """
    Download audio from YouTube video using yt-dlp.
    
    Args:
        video_id (str): YouTube video ID
        url (str): Full YouTube URL
        
    Returns:
        Optional[str]: Path to downloaded audio file, or None if failed
    """
    try:
        import yt_dlp
        
        # Create temporary file for audio with timestamp to avoid collisions
        temp_dir = tempfile.gettempdir()
        timestamp = int(time.time() * 1000)  # milliseconds for uniqueness
        output_filename = f"youtube_audio_{video_id}_{timestamp}"
        output_path = os.path.join(temp_dir, output_filename)
        
        # Configure yt-dlp options
        # Use remote components for JS challenge solving
        ydl_opts = {
            'format': 'ba',  # Best audio only (simpler format selection)
            'outtmpl': output_path + '.%(ext)s',
            'quiet': False,
            'no_warnings': False,
            'nocheckcertificate': True,  # Bypass SSL certificate verification
            'noplaylist': True,  # Download only the single video, not the entire playlist
            'extractor_args': {
                'youtube': {
                    'remote_components': ['ejs:github'],  # Enable remote JS components for solving challenges
                }
            },
        }
        
        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Check if info was successfully extracted
            if not info:
                return None
            
            ext = info.get('ext', 'webm')
        
        # The output file will have the original extension (e.g., .webm, .m4a)
        final_output_path = output_path + f'.{ext}'
        
        if os.path.exists(final_output_path):
            return final_output_path
        else:
            return None
    
    except yt_dlp.utils.DownloadError as e:
        # Silently handle download errors
        return None
        
    except Exception as e:
        # Silently handle errors
        return None


def transcribe_audio(audio_file: str) -> str:
    """
    Transcribe audio file using OpenAI Whisper (base model).
    
    This function runs fully offline after the model is downloaded once.
    Whisper automatically detects the language, so it supports non-English content.
    
    Args:
        audio_file (str): Path to audio file
        
    Returns:
        str: Transcription text (may be empty for silent audio)
    """
    try:
        # Verify file exists before transcription
        if not os.path.exists(audio_file):
            return f"Error: Audio file not found at {audio_file}"
        
        # Check if FFmpeg is available
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], 
                                   capture_output=True, 
                                   timeout=5)
            if result.returncode != 0:
                return "Error: FFmpeg is not available. Please install FFmpeg to transcribe audio."
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return "Error: FFmpeg is not installed or not in PATH. Please install FFmpeg to transcribe audio."
        
        # Load Whisper model (base model for balance between speed and accuracy)
        model = whisper.load_model("base")
        
        # Transcribe audio
        # Whisper auto-detects language, no need to specify language parameter
        result = model.transcribe(audio_file)
        
        # Extract text from result
        transcription_text = result["text"].strip()
        
        # Return transcription (may be empty for silent audio)
        return transcription_text
        
    except Exception as e:
        error_msg = str(e)
        if 'ffmpeg' in error_msg.lower():
            return "Error: FFmpeg is required for audio processing. Please install FFmpeg."
        return f"Error during transcription: {error_msg}"


# Example usage
if __name__ == "__main__":
    # Get YouTube URL from user input
    test_url = input("Enter YouTube URL: ").strip()
    
    if test_url:
        # Call the main function
        transcription = youtube_transcribe(test_url)
