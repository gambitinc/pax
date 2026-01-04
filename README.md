# Pax Report

Agentic development is dangerous, we're trying to fix that.

Paxnet tracks your vibecoding activity and generates personalized daily learning reports.

Every meaningful interaction — writing code, fixing bugs, designing infra — gets recorded and synthesized into a tutorial tailored to your skill level. The system learns what you know and adapts its explanations accordingly.

## Installation

**Prerequisites:** Python 3.10+

Run this one-liner to install:

```bash
curl -fsSL https://paxnet.dev/install.sh | bash
```

The installer will prompt you for:
- Your client (Claude Code, Claude Desktop, or Cursor)
- Your PaxNet API key (get one at [paxnet.dev/dashboard](https://paxnet.dev/dashboard))

### Manual Installation

If you prefer to install manually:

```bash
git clone https://github.com/gambitinc/pax
cd pax/pax_report
uv run --with fastmcp fastmcp install claude-code server.py \
  --env PAX_API_KEY=pax_your_api_key
```

Replace `claude-code` with `claude-desktop` or `cursor` depending on your client.

## License

MIT
