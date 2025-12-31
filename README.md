# Pax

*Agentic development is dangerous. We want to fix that.*

PaxNet sits between your AI agents and your codebase, summarizing changes and scanning for vulnerabilities in real-time. 

**We help you understand your code.** PaxNet tracks every change and generatestutorials tailored to your codebase and skill level.

**Second, we scan for vulnerabilities.** Catches SQL injection, XSS, missing headers, and more before they ship.

If we lose interest in the things we create, focusing only on the ends and not the means... software is going to suck. 

## Features

- **Real-time vulnerability scanning** - SQL injection, XSS, security headers, fuzzing, AI analysis
- **Multi-level scans** - Quick checks or deep audits
- **Daily security reports** - Personalized tutorials sent to your inbox
- **MCP integration** - Works with Claude Desktop, Claude Code, and Cursor
- **Ngrok tunneling** - Automatically exposes local servers for scanning

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- [Ngrok](https://ngrok.com) account
- [PaxNet](https://paxnet.dev) account

### Quick Install

```bash
git clone https://github.com/gambitinc/pax
cd pax
uv run --with fastmcp fastmcp install claude-code --project . server.py
```

Works with `claude-code`, `claude-desktop`, and `cursor`.

## Configuration

### 1. Get Your Keys

**Ngrok:** Sign up at [ngrok.com](https://ngrok.com) → copy your authtoken

**PaxNet:** Sign up at [paxnet.dev](https://paxnet.dev) → create a project → generate API key

### 2. Add to Config

Open your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pax-vulnerabilities-server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/pax", "server.py"],
      "env": {
        "NGROK_AUTHTOKEN": "your_ngrok_token",
        "PAX_API_KEY": "pax_your_api_key"
      }
    }
  }
}
```

## Usage

```
Scan my local server on port 3000 for vulnerabilities
```

Options:
- `port_num` - Your local server port
- `level` - `low`, `medium`, or `high`

## Scan Levels

| Level | Checks | Time |
|-------|--------|------|
| **Low** | Headers, endpoints | ~5s |
| **Medium** | + SQL injection, XSS | ~20s |
| **High** | + Fuzzing, AI analysis | ~45s |

## Security

- Only scan servers you own
- Scans create temporary ngrok tunnels
- Review findings before acting

## License

MIT
