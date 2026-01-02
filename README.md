# Pax Report

MCP server that tracks your coding activity and generates personalized daily learning reports.

Every meaningful interaction—writing code, fixing bugs, reviewing PRs, learning concepts—gets recorded and synthesized into a tutorial tailored to your skill level. The system learns what you know and adapts its explanations accordingly.

## Installation

**Prerequisites:** Python 3.10+, [uv](https://docs.astral.sh/uv/), and a [PaxNet](https://paxnet.dev) API key.

```bash
git clone https://github.com/gambitinc/pax
cd pax/pax_mcp/pax
uv run --with fastmcp fastmcp install claude-code server.py \
  --env PAX_API_KEY=pax_your_api_key
```

Replace `claude-code` with `claude-desktop` or `cursor` depending on your client.

## License

MIT
