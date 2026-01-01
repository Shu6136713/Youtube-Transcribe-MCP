# YouTube Video Transcription

A Python function to download and transcribe YouTube videos using yt-dlp and OpenAI Whisper.

## Features

- ✅ Extract video ID from standard and short YouTube URLs
- ✅ Download audio using yt-dlp (more reliable than pytube)
- ✅ Transcribe audio using OpenAI Whisper (base model)
- ✅ Fully offline operation (after initial setup)
- ✅ Comprehensive error handling
- ✅ Automatic cleanup of temporary files

## Installation

### Step 1: Install Required Packages

```bash
pip install yt-dlp openai-whisper imageio-ffmpeg
```

### Step 2: Setup FFmpeg

Run the setup script to configure FFmpeg for Whisper:

```bash
python setup_ffmpeg.py
```

Or manually:

```bash
python -c "import imageio_ffmpeg; import shutil; import os; src = imageio_ffmpeg.get_ffmpeg_exe(); dst = os.path.join(os.path.dirname(src), 'ffmpeg.exe'); shutil.copy2(src, dst) if not os.path.exists(dst) else None; print('FFmpeg setup complete!')"
```

## Usage

### As a Function

```python
from youtube_transcribe import youtube_transcribe

# Transcribe a YouTube video
text = youtube_transcribe("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(text)
```

### As a Script

Run the script and enter a YouTube URL when prompted:

```bash
python youtube_transcribe.py
```

## Supported URL Formats

- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`

## How It Works

1. **Extract Video ID**: Parses the YouTube URL to extract the video ID
2. **Download Audio**: Uses yt-dlp to download the audio stream in its original format (webm/m4a)
3. **Transcribe**: Uses OpenAI Whisper's base model to transcribe the audio
4. **Cleanup**: Automatically removes temporary audio files

## Technical Details

- **Whisper Model**: Uses the `base` model for a balance between speed and accuracy
- **Audio Format**: Downloads in original format (no conversion needed)
- **Offline**: After the first run (which downloads the Whisper model), everything runs offline
- **SSL**: Bypasses SSL certificate verification for networks with proxy issues

## Error Handling

The function handles various errors gracefully:

- Invalid YouTube URLs
- Download failures
- Transcription errors
- File system errors

All errors return clear error messages instead of crashing.

## Requirements

- Python 3.7+
- Internet connection (for downloading videos and initial model download)
- ~140MB disk space for Whisper base model
- Temporary disk space for audio files during processing

## Notes

- First run will download the Whisper base model (~140MB)
- Transcription time depends on video length and CPU speed
- Temporary audio files are automatically cleaned up after transcription
- The function runs entirely on CPU (no GPU required)

## Troubleshooting

### "SSL Certificate Error"
The script automatically bypasses SSL verification. If you still have issues, check your network/proxy settings.

### "FFmpeg not found"
Make sure you ran `setup_ffmpeg.py` after installing the packages.

### "HTTP Error 400"
This usually means YouTube has changed their API. Make sure you have the latest version of yt-dlp:
```bash
pip install --upgrade yt-dlp
```

## License

This project uses:
- yt-dlp (Unlicense)
- OpenAI Whisper (MIT License)
- imageio-ffmpeg (BSD License)


