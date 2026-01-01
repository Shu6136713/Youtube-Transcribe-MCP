"""
MCP Tool Definition for YouTube Transcription

This module defines the youtube_transcribe tool for the MCP server.
It wraps the existing youtube_transcribe function without modifying its core logic.
"""

from typing import Any
from youtube_transcribe import youtube_transcribe as _youtube_transcribe


def validate_url(url: Any) -> str:
    """
    Validate that the URL parameter is provided and is a string.
    
    Args:
        url: The URL parameter to validate
        
    Returns:
        str: The validated URL string
        
    Raises:
        ValueError: If URL is missing or not a string
    """
    if url is None:
        raise ValueError("URL parameter is required")
    
    if not isinstance(url, str):
        raise ValueError(f"URL must be a string, got {type(url).__name__}")
    
    if not url.strip():
        raise ValueError("URL cannot be empty")
    
    return url.strip()


def youtube_transcribe_tool(url: str) -> str:
    """
    MCP tool implementation for YouTube video transcription.
    
    This function validates input, calls the core youtube_transcribe function,
    and handles errors appropriately for MCP clients.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Transcription text on success
        
    Raises:
        ValueError: If input validation fails
        RuntimeError: If transcription fails (with user-friendly message)
    """
    # Step 1: Validate input
    try:
        validated_url = validate_url(url)
    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    
    # Step 2: Call the core transcription function
    result = _youtube_transcribe(validated_url)
    
    # Step 3: Check if result is an error message
    # The youtube_transcribe function returns error messages starting with "Error:"
    if result.startswith("Error:"):
        # Extract the error message (remove "Error:" prefix)
        error_message = result[6:].strip()
        raise RuntimeError(error_message)
    
    # Step 4: Return successful transcription
    return result


