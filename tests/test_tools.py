import pytest
from tools import youtube_transcribe_tool

def test_tool_valid_url():
    url = "https://www.youtube.com/shorts/qi45Q860HQI"
    result = youtube_transcribe_tool(url)
    
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_tool_empty_url():
    url = ""
    with pytest.raises(ValueError):
        youtube_transcribe_tool(url)
