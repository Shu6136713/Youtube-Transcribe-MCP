# Quick Start Guide - YouTube Transcribe MCP Server

## Installation (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements_mcp.txt
```

### 2. Set Up FFmpeg

```bash
python setup_ffmpeg.py
```

## Testing

### MCP Inspector (Integration Test)

Test the complete MCP server:

#### Step 1: Install MCP Inspector

```bash
npm install -g @modelcontextprotocol/inspector
```

#### Step 2: Run MCP Inspector

```bash
mcp-inspector python server.py
```

#### Step 3: Test in Browser

1. Open http://localhost:5173
2. Click "List Tools" → see `youtube_transcribe`
3. Click "Call Tool"
4. Enter URL: `https://www.youtube.com/watch?v=5lVfIV3JlXw`
5. Click "Execute"
6. Wait 1-2 minutes for transcription

## Usage with Claude Desktop

### 1. Find Config File

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Add Server Configuration

Edit the config file:

```json
{
  "mcpServers": {
    "youtube-transcribe": {
      "command": "python",
      "args": ["C:/full/path/to/server.py"]
    }
  }
}
```

**Important**: Use the full absolute path to `server.py`

### 3. Restart Claude Desktop

The tool will now be available to Claude.

### 4. Test in Claude

Ask Claude:

> "Can you transcribe this YouTube video for me? https://www.youtube.com/watch?v=5lVfIV3JlXw"

Claude will use the `youtube_transcribe` tool automatically.

## Example Tool Call

**Input:**
```json
{
  "url": "https://www.youtube.com/watch?v=5lVfIV3JlXw"
}
```

**Output:**
```
[Full transcription text here...]
```

## Common Issues

### "ModuleNotFoundError: No module named 'mcp'"

**Solution**: Install MCP SDK
```bash
pip install mcp
```

### "FFmpeg not found"

**Solution**: Run FFmpeg setup
```bash
python setup_ffmpeg.py
```

### "Failed to download audio"

**Possible causes:**
- No internet connection
- Invalid YouTube URL
- Video is private/age-restricted

**Solution**: Check URL and internet connection

### MCP Inspector won't start

**Solution**: Check Node.js is installed
```bash
node --version  # Should be v16+
npm install -g @modelcontextprotocol/inspector
```

## File Structure

```
.
├── server.py                          # MCP server (run this)
├── tools.py                           # Tool wrapper
├── youtube_transcribe.py              # Core function
├── setup_ffmpeg.py                    # FFmpeg setup script
├── requirements_mcp.txt               # MCP dependencies
├── requirements.txt                   # Core dependencies
├── MCP_README.md                      # Full documentation
├── QUICKSTART.md                      # This file
└── claude_desktop_config.example.json # Config template
```

## Next Steps

1. ✓ Install dependencies
2. ✓ Test with MCP Inspector
3. ✓ Add to Claude Desktop
4. ✓ Use with AI agents

## Full Documentation

See `MCP_README.md` for:
- Detailed architecture
- Error handling
- Troubleshooting
- Development guide





