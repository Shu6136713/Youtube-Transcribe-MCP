import pytest
from youtube_transcribe import youtube_transcribe

def test_transcribe_example_video():
    # Example YouTube short (small video with predictable speech)
    url = "https://www.youtube.com/shorts/qi45Q860HQI"
    
    # Expected transcription (trimmed or normalized for test)
    expected_snippet = "Let's check out three of the strangest borders in the world"
    
    result = youtube_transcribe(url)
    
    # Assert the result contains the expected snippet
    assert expected_snippet in result
