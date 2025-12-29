# Pax MCP - Security Vulnerability Scanner

Agentic development is dangerous. We're trying to fix that.

A Model Context Protocol (MCP) server that scans local servers for security vulnerabilities using ngrok tunneling and comprehensive security testing.

## Features

- **Multi-level scanning**: Choose between low, medium, and high intensity scans
- **Comprehensive testing**: Security headers, SQL injection, XSS, fuzzing, and AI analysis
- **Easy integration**: Works seamlessly with Claude Desktop and other MCP clients
- **Ngrok tunneling**: Automatically exposes local servers for external scanning

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager 
- Ngrok account and auth token (get one at [ngrok.com](https://ngrok.com))

### Quick Install (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/gambitinc/pax
cd pax
```

2. Install the MCP server:
```bash
uv run --with fastmcp fastmcp install claude-code --project . server.py
```

This command works for `claude-code`, `claude-desktop`, and `cursor`.

This automatically:
- Installs all dependencies
- Adds the server to your configuration
- Sets up the proper environment

## Configuration

### 1. Configure Claude Desktop

The `fastmcp install` command automatically adds the server to your Claude Desktop configuration.

**Add your Ngrok token to the config:**

Open your Claude Desktop config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Add your Ngrok token to the `pax-vulnerabilities-server` entry:

```json
{
  "mcpServers": {
    "pax-vulnerabilities-server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/pax-mcp", "server.py"],
      "env": {
        "NGROK_AUTHTOKEN": "your_ngrok_token_here"
      }
    }
  }
}
```


## Usage

Once installed, you can use the following tools in Claude Desktop:

### 1. Scan for vulnerabilities

```
Can you scan my local server running on port 3000 for security vulnerabilities?
```

The scan function accepts:
- `port_num`: The local port number where your server is running
- `level`: Scan intensity - "low", "medium" (default), or "high"

### 2. Get scan options

```
What scan levels are available?
```

This returns details about each scan level, what tests they include, and estimated times.

## Scan Levels

| Level | Tests Included | Estimated Time | Use Case |
|-------|---------------|----------------|----------|
| **Low** | Security headers, quick endpoint discovery | 2-5 seconds | Fast initial assessment |
| **Medium** | Headers, endpoints, SQL injection, XSS | 10-30 seconds | Regular security checks |
| **High** | All medium tests + fuzzing + AI analysis | 30-60+ seconds | Full security audit |

## Example Output

```json
{
  "tunnel_url": "https://abc123.ngrok.io",
  "local_port": 3000,
  "vulnerabilities": {
    "critical": [...],
    "high": [...],
    "medium": [...],
    "low": [...]
  },
  "scan_level": "medium",
  "timestamp": "2025-12-29T10:30:00Z"
}
```


### Testing with Claude Desktop

After making changes, restart Claude Desktop to reload the server.

## Security Considerations

- This tool creates public ngrok tunnels to expose your local servers
- Only scan servers you own or have permission to test
- Be cautious when scanning production servers
- Review scan results carefully before taking action

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or feature requests, please open an issue on GitHub. 
