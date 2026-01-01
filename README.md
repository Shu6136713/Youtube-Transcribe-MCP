# YouTube Transcription MCP Server

A Model Context Protocol (MCP) server that enables AI agents to transcribe YouTube videos using OpenAI Whisper. This tool downloads audio from YouTube videos and generates accurate transcriptions locally, supporting multiple URL formats and automatic language detection.

## Project Overview

This project provides a YouTube video transcription capability exposed as an MCP tool. AI agents (like Cursor, Claude Desktop, or other MCP-compatible clients) can request transcriptions by providing a YouTube URL. The server handles video download via `yt-dlp`, audio extraction, and transcription using OpenAI's Whisper model—all running locally on your machine.

**Key Features:**
- 🎥 Supports standard YouTube URLs, short URLs (`youtu.be`), and YouTube Shorts
- 🗣️ Automatic language detection via Whisper
- 🔒 Fully local transcription (no external API calls after initial setup)
- ⚡ Async MCP server implementation for responsive agent interactions
- 🧹 Automatic cleanup of temporary audio files

---

## Architecture & File Structure

```
nebius/
├── server.py                 # MCP server exposing the transcription tool
├── youtube_transcribe.py     # Core transcription logic (Whisper + yt-dlp)
├── tools.py                  # MCP tool wrapper with validation
├── setup_ffmpeg.py           # FFmpeg configuration helper script
├── requirements.txt          # Dependencies for standalone transcription
├── requirements_mcp.txt      # Dependencies for MCP server + transcription
├── README.md                 # This file
├── QUICKSTART.md             # Quick setup guide (if present)
└── MCP_README.md             # MCP-specific documentation (if present)
```

### File Descriptions

#### `server.py`
The main MCP server implementation using the official MCP Python SDK. It:
- Exposes the `youtube_transcribe` tool to MCP clients
- Handles async tool execution via `stdio` transport
- Provides error handling and logging (to stderr, as MCP uses stdout for protocol messages)
- Runs the transcription function in a thread pool to avoid blocking the event loop

**Key Components:**
- `list_tools()`: Returns tool metadata for MCP clients
- `call_tool()`: Executes transcription requests
- `main()`: Initializes and runs the stdio-based MCP server

#### `youtube_transcribe.py`
Core transcription logic with three main functions:
- `extract_video_id(url)`: Parses YouTube URLs to extract video IDs (supports multiple formats)
- `download_audio(video_id, url)`: Downloads audio using `yt-dlp` to a temporary file
- `transcribe_audio(audio_file)`: Transcribes audio using Whisper's `base` model

**Features:**
- Automatic FFmpeg path configuration via `imageio-ffmpeg`
- Temporary file management with unique timestamps
- Graceful error handling with user-friendly messages
- Automatic cleanup of downloaded audio files

#### `tools.py`
MCP tool wrapper that bridges the server and core transcription logic:
- `validate_url(url)`: Validates input parameters (type checking, empty string detection)
- `youtube_transcribe_tool(url)`: Wraps `youtube_transcribe()` with MCP-friendly error handling

This layer converts error strings (e.g., `"Error: ..."`) into proper exceptions that the MCP server can handle.

#### `setup_ffmpeg.py`
Helper script to configure FFmpeg for Whisper. It:
- Locates the FFmpeg executable installed by `imageio-ffmpeg`
- Creates a copy with the standard name (`ffmpeg.exe`) that Whisper expects
- Provides clear success/error messages

**Usage:**
```bash
python setup_ffmpeg.py
```

#### Configuration Files

**`.cursor/` directory** (to be created):
Contains MCP configuration for Cursor IDE. You'll create a `mcp.json` file here to register this server.

**`requirements.txt`**:
Minimal dependencies for standalone transcription:
```
yt-dlp>=2025.12.8
openai-whisper>=20250625
imageio-ffmpeg>=0.6.0
```

**`requirements_mcp.txt`**:
Full dependencies including MCP SDK:
```
mcp>=1.0.0
yt-dlp>=2025.12.8
openai-whisper>=20250625
imageio-ffmpeg>=0.6.0
```

---

## MCP Tool Integration

To use this server with Cursor or another MCP-compatible agent, you need to register it in your MCP configuration file.

### Configuration for Cursor IDE

1. **Create the configuration directory** (if it doesn't exist):
   ```bash
   mkdir -p .cursor
   ```

2. **Create or edit `.cursor/mcp.json`**:
   ```json
   {
    "mcpServers": {
        "youtube-transcribe": {
        "command": "python",
        "args": ["server.py"]
        }
    }
    }
   ```

   **Note:** Adjust the `cwd` path to match your project location.

3. **Restart Cursor** to load the new MCP server configuration.

### Configuration for Claude Desktop

Edit your Claude Desktop MCP configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

Add the server configuration:
```json
{
  "mcpServers": {
    "youtube-transcribe": {
      "command": "python",
      "args": ["C:\\Users\\User\\Dropbox\\bootcamp\\nebius\\server.py"]
    }
  }
}
```

### Verification

After configuration, the MCP client should automatically start the server when needed. You can verify the tool is available by asking your agent:

> "What MCP tools do you have access to?"

You should see `youtube_transcribe` listed among available tools.

---

## Usage

### Starting the Server (Manual Testing)

For manual testing with MCP Inspector:

```bash
# Install dependencies
pip install -r requirements_mcp.txt

# Configure FFmpeg
python setup_ffmpeg.py

# Start the server
python server.py
```

The server will run in stdio mode, waiting for MCP protocol messages on stdin.

### Agent Workflow Example

Once configured, agents can use the tool naturally in conversation:

**User Request:**
> "Please transcribe this YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"

**Agent Action:**
The agent calls the `youtube_transcribe` tool with:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Process:**
1. Server receives the tool call via MCP protocol
2. Downloads audio from YouTube using `yt-dlp`
3. Transcribes audio using Whisper (may take 1-5 minutes depending on video length)
4. Returns transcription text to the agent
5. Automatically cleans up temporary audio file

**Agent Response:**
> "Here's the transcription of the video:
> 
> [Full transcription text...]"

### Supported URL Formats

The tool accepts various YouTube URL formats:
- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`
- Shorts: `https://www.youtube.com/shorts/VIDEO_ID`

### Example Direct Usage (Python)

You can also use the transcription function directly in Python:

```python
from youtube_transcribe import youtube_transcribe

# Transcribe a video
transcription = youtube_transcribe("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(transcription)
```

---

## Dependencies & Requirements

### Python Packages

**Core Dependencies:**
- **`yt-dlp`** (≥2025.12.8): YouTube video/audio downloader
- **`openai-whisper`** (≥20250625): OpenAI's speech recognition model
- **`imageio-ffmpeg`** (≥0.6.0): FFmpeg binaries for audio processing

**MCP Server (additional):**
- **`mcp`** (≥1.0.0): Model Context Protocol SDK

### Runtime Requirements

**FFmpeg:**
- Required for audio processing by Whisper
- Automatically installed via `imageio-ffmpeg`
- Must be configured using `setup_ffmpeg.py` after installation

**Python Version:**
- Python 3.8 or higher recommended
- Async/await support required for MCP server

**Disk Space:**
- Whisper models: ~140MB (base model, downloaded on first use)
- Temporary audio files: Varies by video length (automatically cleaned up)

### Installation

**For MCP Server Usage:**
```bash
pip install -r requirements_mcp.txt
python setup_ffmpeg.py
```

**For Standalone Transcription:**
```bash
pip install -r requirements.txt
python setup_ffmpeg.py
```

---

## Notes

### Standalone vs. MCP Server Usage

This project supports two modes of operation:

1. **Standalone Transcription** (`requirements.txt`):
   - Use `youtube_transcribe.py` directly in your Python scripts
   - Minimal dependencies (no MCP SDK required)
   - Suitable for batch processing or integration into existing applications

2. **MCP Server** (`requirements_mcp.txt`):
   - Exposes transcription as an MCP tool for AI agents
   - Requires MCP SDK and server infrastructure
   - Enables natural language requests via compatible agents (Cursor, Claude Desktop, etc.)

### Performance Considerations

- **First Run**: Whisper downloads the `base` model (~140MB) on first use
- **Transcription Speed**: Typically 1-5 minutes depending on video length and CPU
- **Model Selection**: Currently uses Whisper's `base` model (balance of speed/accuracy)
  - For faster transcription: Edit `youtube_transcribe.py` to use `tiny` model
  - For better accuracy: Use `small`, `medium`, or `large` models (slower)

### Troubleshooting

**FFmpeg Errors:**
If you see FFmpeg-related errors, ensure you've run the setup script:
```bash
python setup_ffmpeg.py
```

**Download Failures:**
YouTube occasionally changes their API. If downloads fail:
- Update `yt-dlp`: `pip install --upgrade yt-dlp`
- Check if the video is available in your region
- Verify the URL is correct

**MCP Connection Issues:**
- Ensure the `cwd` path in `mcp.json` is correct and uses absolute paths
- Check that Python is in your system PATH
- Restart your MCP client after configuration changes

---

## Testing & Verification

✅ **Project Status: Fully Tested & Operational**

The MCP server and `youtube_transcribe` tool have been fully tested and work correctly. All code is clean, dependencies are aligned, and the project has passed all checks.

**Verified Components:**
- MCP server initialization and stdio communication
- YouTube URL parsing (standard, short, and Shorts formats)
- Audio download via `yt-dlp`
- Whisper transcription pipeline
- Error handling and cleanup mechanisms
- Tool integration with MCP clients

---

## License

This project uses the following open-source components:
- **yt-dlp**: Unlicense
- **OpenAI Whisper**: MIT License
- **MCP SDK**: MIT License

---

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style and structure
- Error handling is comprehensive
- Documentation is updated for new features

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the MCP documentation: https://modelcontextprotocol.io
3. Verify dependencies are up to date

---

**Happy transcribing! 🎙️**

