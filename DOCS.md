# pax/ — MCP Package Source

The publishable Python package. This is the actual git repository (has its own `.git`). Published to PyPI as `pax-report`.

## Files

### `pyproject.toml`

Package config. Entry point: `pax-report-mcp = "pax_report.server:main"`. Dependencies: `fastmcp`, `python-dotenv`, `requests`. Build system: hatchling.

### `uv.lock`

Dependency lock file for the `uv` package manager.

### `README.md`

PyPI package README. Installation and configuration instructions for end users.

## Subdirectories

### `pax_report/`

Contains the MCP server implementation. See `pax_report/DOCS.md`.

### `dist/`

Built package artifacts (wheel files). Not checked into git.
