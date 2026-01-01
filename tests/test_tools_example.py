import pytest
from tools import youtube_transcribe_tool

def test_tool_example_video():
    url = "https://www.youtube.com/shorts/qi45Q860HQI"
    
    expected_snippet = "The entire island changes countries every six months"
    
    result = youtube_transcribe_tool(url)
    
    # Check the transcription includes the expected snippet
    assert expected_snippet in result

def test_tool_invalid_url():
    url = ""
    with pytest.raises(ValueError):
        youtube_transcribe_tool(url)
