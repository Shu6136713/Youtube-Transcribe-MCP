# YouTube Transcribe MCP Server

This is an MCP (Model Context Protocol) server that exposes the `youtube_transcribe` function as a tool for AI coding agents.

## Overview

The server provides a single tool:

- **Tool Name**: `youtube_transcribe`
- **Description**: Download and transcribe a YouTube video locally using Whisper
- **Input**: YouTube URL (string)
- **Output**: Transcription text (string)

## Architecture

```
┌─────────────────┐
│   MCP Client    │  (e.g., MCP Inspector, Claude Desktop)
│  (AI Agent)     │
└────────┬────────┘
         │ MCP Protocol (stdio)
         │
┌────────▼────────┐
│   server.py     │  MCP server bootstrap
│                 │  - Handles MCP protocol
│                 │  - Routes tool calls
└────────┬────────┘
         │
┌────────▼────────┐
│    tools.py     │  Tool implementation
│                 │  - Input validation
│                 │  - Error handling
└────────┬────────┘
         │
┌────────▼────────┐
│ youtube_        │  Core transcription logic
│ transcribe.py   │  (unchanged)
└─────────────────┘
```

## Files

- **`server.py`**: MCP server implementation using the standard MCP Python SDK
- **`tools.py`**: Tool definition with validation and error handling
- **`youtube_transcribe.py`**: Core transcription function (unchanged)
- **`requirements_mcp.txt`**: Python dependencies for the MCP server

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements_mcp.txt
```

### 2. Set Up FFmpeg

The transcription requires FFmpeg. After installing `imageio-ffmpeg`, create a copy of the FFmpeg executable:

```bash
python -c "import imageio_ffmpeg; import shutil; import os; src = imageio_ffmpeg.get_ffmpeg_exe(); dst = os.path.join(os.path.dirname(src), 'ffmpeg.exe'); shutil.copy2(src, dst) if not os.path.exists(dst) else None"
```

Or use the provided setup script:

```bash
python setup_ffmpeg.py
```

## Running the Server

### Start the MCP Server

```bash
python server.py
```

The server runs on stdio and waits for MCP protocol messages.

## Testing with MCP Inspector

MCP Inspector is the official tool for testing MCP servers.

### 1. Install MCP Inspector

```bash
npm install -g @modelcontextprotocol/inspector
```

### 2. Run MCP Inspector

```bash
mcp-inspector python server.py
```

This will:
1. Start the MCP server
2. Open a web interface (usually at http://localhost:5173)
3. Allow you to interact with the server

### 3. Test the Tool

In the MCP Inspector web interface:

1. **Discover the tool**: Click "List Tools" to see `youtube_transcribe`
2. **Call the tool**: 
   - Select `youtube_transcribe`
   - Enter a YouTube URL in the `url` field
   - Click "Call Tool"
3. **View results**: The transcription text will appear in the response

### Example Test URLs

Short videos for quick testing:

- **Very short (< 1 min)**: `https://www.youtube.com/watch?v=5lVfIV3JlXw`
- **Short format**: `https://youtu.be/5lVfIV3JlXw`

## Tool Specification

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "url": {
      "type": "string",
      "description": "YouTube video URL"
    }
  },
  "required": ["url"]
}
```

### Supported URL Formats

- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`
- Shorts: `https://www.youtube.com/shorts/VIDEO_ID`

### Output

- **Success**: Returns the full transcription text as a plain string
- **Failure**: Returns an MCP error with a user-friendly message

### Error Handling

The tool validates input and provides clear error messages:

| Error Type | Example Message |
|------------|----------------|
| Missing URL | `Invalid input: URL parameter is required` |
| Invalid type | `Invalid input: URL must be a string, got int` |
| Empty URL | `Invalid input: URL cannot be empty` |
| Invalid URL format | `Transcription failed: Invalid YouTube URL. Please provide a valid YouTube URL.` |
| Download failure | `Transcription failed: Failed to download audio from YouTube video.` |
| Network error | `Transcription failed: Network connection failed. Please check your internet connection and try again.` |
| FFmpeg missing | `Transcription failed: FFmpeg is not installed or not in PATH. Please install FFmpeg to transcribe audio.` |

## Integration with AI Agents

### Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "youtube-transcribe": {
      "command": "python",
      "args": ["C:/path/to/server.py"]
    }
  }
}
```

### Other MCP Clients

Any MCP-compatible client can use this server by:
1. Starting the server as a subprocess
2. Communicating via stdio using the MCP protocol
3. Calling the `youtube_transcribe` tool with a URL

## Design Principles

1. **No modifications to core logic**: The `youtube_transcribe` function remains unchanged
2. **Minimal MCP layer**: The server and tool wrapper are thin layers
3. **Clear error messages**: No stack traces exposed to clients
4. **Input validation**: URL is validated before calling the core function
5. **Async-safe**: Blocking transcription runs in a thread pool
6. **Local execution**: No paid APIs, fully offline after initial setup

## Limitations

- **Processing time**: Transcription can take several minutes for longer videos
- **Memory usage**: Whisper model requires ~1-2 GB RAM
- **Internet required**: For downloading videos (transcription is offline)
- **No streaming**: Returns complete transcription after processing

## Troubleshooting

### Server won't start

- Check that all dependencies are installed: `pip install -r requirements_mcp.txt`
- Verify Python version is 3.8+

### FFmpeg errors

- Run the FFmpeg setup script: `python setup_ffmpeg.py`
- Verify FFmpeg is accessible: `ffmpeg -version`

### Download errors

- Check internet connection
- Verify the YouTube URL is valid and accessible
- Some videos may be age-restricted or private

### MCP Inspector connection issues

- Make sure the server path is correct
- Check that no other process is using the same port
- Try restarting MCP Inspector

## Development

### Testing Changes

1. **Unit tests**: Test the tool wrapper directly
   ```python
   from tools import youtube_transcribe_tool
   result = youtube_transcribe_tool("https://www.youtube.com/watch?v=...")
   print(result)
   ```

2. **Integration tests**: Use MCP Inspector to test the full server

3. **Error cases**: Test with invalid inputs
   ```python
   from tools import youtube_transcribe_tool
   try:
       youtube_transcribe_tool("")  # Should raise ValueError
   except ValueError as e:
       print(f"Expected error: {e}")
   ```

### Logging

The server uses Python's `logging` module with all logs directed to **stderr** (not stdout). This is required because the MCP protocol uses stdout exclusively for protocol messages.

**Current configuration:**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Critical: logs must go to stderr
)
```

**To increase verbosity:**
```python
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
```

**Important**: Never write logs to stdout, as this will break MCP protocol parsing.

## License

Same as the parent project.

## Support

For issues related to:
- **MCP protocol**: Check the [MCP documentation](https://modelcontextprotocol.io/)
- **Transcription**: See the main README.md
- **This server**: Open an issue in the project repository

