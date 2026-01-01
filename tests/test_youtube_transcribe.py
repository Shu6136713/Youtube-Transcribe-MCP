import pytest
from youtube_transcribe import youtube_transcribe

def test_transcribe_basic():
    # Small YouTube short for testing
    url = "https://www.youtube.com/shorts/qi45Q860HQI"
    result = youtube_transcribe(url)
    
    # Check it returns a non-empty string
    assert isinstance(result, str)
    assert len(result.strip()) > 0
