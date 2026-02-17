# pax_report/ — MCP Server Implementation

The actual MCP server code that runs inside a developer's AI coding tool.

## Files

### `__init__.py`

Empty package init file.

### `server.py`

The entire MCP server. Built with `fastmcp`. Connects to `https://pax-report.vercel.app` backend.

**Server config:** Name `pax-report`, instructions tell the AI to call `report_update()` on every code change.

**Tools:**

**`report_update()`** — The core tool. Called on every code change.
- `update_type` (required): One of `code_written`, `bug_fix`, `code_review`, `learning`, `refactoring`
- `description` (required): 1-3 sentence description
- `files_changed` (optional): List of modified file paths
- `concepts` (optional): Programming concepts demonstrated
- `code_snippet` (optional): Relevant code, max 500 chars
- `session_id` (optional): Stable UUID per conversation
- `message_count` (optional): Messages in conversation so far
- `lines_changed` (optional): Estimated lines added/removed
- `time_since_last_update` (optional): Seconds since last call

Builds a JSON payload with `source: "mcp"`, the update fields as a nested `payload` object, and session context fields (if provided) as a separate `session_context` object. POSTs to `/ingest/updates` with Bearer auth.

**`get_update_types()`** — Returns a static dict describing each update type. No API call needed.

**`get_refine_context(topic)`** — Calls `POST /refine/proficiency` on the backend. Returns the user's proficiency level (beginner/intermediate/advanced), confidence score, and concept breakdown. Used by the AI to calibrate explanation depth.

**`main()`** — Entry point. Calls `mcp.run(transport="stdio")`.
