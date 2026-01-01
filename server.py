"""
MCP Server for YouTube Transcription

This server exposes the youtube_transcribe function as an MCP tool.
It uses the standard MCP Python SDK and can be tested with MCP Inspector.

Usage:
    python server.py
"""

import asyncio
import logging
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from tools import youtube_transcribe_tool

# Configure logging to stderr (MCP protocol uses stdout exclusively)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Create MCP server instance
app = Server("youtube-transcribe-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.
    
    Returns:
        List containing the youtube_transcribe tool definition
    """
    return [
        Tool(
            name="youtube_transcribe",
            description="Download and transcribe a YouTube video locally using Whisper. "
                       "Supports standard YouTube URLs (youtube.com/watch?v=...), "
                       "short URLs (youtu.be/...), and YouTube Shorts. "
                       "Returns the full transcription text. "
                       "Note: This may take several minutes depending on video length.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution requests.
    
    Args:
        name: Tool name to execute
        arguments: Tool arguments
        
    Returns:
        List of TextContent with the result
        
    Raises:
        ValueError: If tool name is unknown or arguments are invalid
        RuntimeError: If transcription fails
    """
    if name != "youtube_transcribe":
        raise ValueError(f"Unknown tool: {name}")
    
    # Extract URL from arguments
    url = arguments.get("url")
    
    try:
        # Call the tool implementation
        # Note: We run the blocking function in a thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, youtube_transcribe_tool, url)
        
        # Return successful result
        return [
            TextContent(
                type="text",
                text=result
            )
        ]
    
    except ValueError as e:
        # Input validation error - provide clear message
        error_message = f"Invalid input: {str(e)}"
        logger.error(error_message)
        raise ValueError(error_message)
    
    except RuntimeError as e:
        # Transcription error - provide user-friendly message
        error_message = f"Transcription failed: {str(e)}"
        logger.error(error_message)
        raise RuntimeError(error_message)
    
    except Exception as e:
        # Unexpected error - log it but don't expose stack trace
        error_message = f"An unexpected error occurred: {str(e)}"
        logger.exception("Unexpected error during transcription")
        raise RuntimeError(error_message)


async def main():
    """
    Main entry point for the MCP server.
    Runs the server using stdio transport.
    """
    logger.info("Starting YouTube Transcribe MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server initialized, waiting for requests...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    # Run the server
    asyncio.run(main())
