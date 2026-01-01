"""
Setup script to configure FFmpeg for Whisper transcription.
Run this once after installing the required packages.
"""

import os
import shutil

try:
    import imageio_ffmpeg
    
    # Get the FFmpeg executable path
    src = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Create a copy with the standard name that Whisper expects
    dst = os.path.join(os.path.dirname(src), 'ffmpeg.exe')
    
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"✓ FFmpeg setup complete!")
        print(f"  Source: {src}")
        print(f"  Copied to: {dst}")
    else:
        print("✓ FFmpeg already configured!")
        print(f"  Location: {dst}")
    
except ImportError:
    print("✗ Error: imageio-ffmpeg not found.")
    print("  Please install it with: pip install imageio-ffmpeg")
except Exception as e:
    print(f"✗ Error during setup: {str(e)}")
