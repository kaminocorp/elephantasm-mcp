# elephantasm-mcp

[![PyPI version](https://badge.fury.io/py/elephantasm-mcp.svg)](https://badge.fury.io/py/elephantasm-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Model Context Protocol](https://modelcontextprotocol.io) server for [Elephantasm](https://elephantasm.com) Long-Term Agentic Memory.

Give any MCP-compatible AI agent persistent memory, searchable knowledge, and an evolving identity — in one line of config.

## Installation

```bash
pip install elephantasm-mcp
```

## Quick Start

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "elephantasm": {
      "command": "elephantasm-mcp",
      "env": {
        "ELEPHANTASM_API_KEY": "sk_live_...",
        "ELEPHANTASM_ANIMA_ID": "your-anima-id"
      }
    }
  }
}
```

### Claude Code

Add to `.claude/settings.json` or `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "elephantasm": {
      "command": "elephantasm-mcp",
      "env": {
        "ELEPHANTASM_API_KEY": "sk_live_...",
        "ELEPHANTASM_ANIMA_ID": "your-anima-id"
      }
    }
  }
}
```

### Cursor / Windsurf

Add to your MCP config (Settings > MCP Servers):

```json
{
  "elephantasm": {
    "command": "elephantasm-mcp",
    "env": {
      "ELEPHANTASM_API_KEY": "sk_live_...",
      "ELEPHANTASM_ANIMA_ID": "your-anima-id"
    }
  }
}
```

### Any MCP-Compatible Agent

The server uses **stdio transport** — any MCP client that can spawn a subprocess works out of the box:

```bash
ELEPHANTASM_API_KEY=sk_live_... ELEPHANTASM_ANIMA_ID=... elephantasm-mcp
```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ELEPHANTASM_API_KEY` | Yes | — | Your API key (starts with `sk_live_`) |
| `ELEPHANTASM_ANIMA_ID` | No | — | Default anima ID (can be overridden per tool call) |
| `ELEPHANTASM_ENDPOINT` | No | `https://api.elephantasm.com/api` | API endpoint |

Get your API key and anima ID from the [Elephantasm dashboard](https://elephantasm.com).

## Tools

Five tools give your agent full read/write access to its memory:

### `query` — Search the brain

Cross-source semantic search across memories, knowledge, and identity in one call. Returns a pre-formatted context string ready for system prompt injection.

```
query("what does the user prefer for error handling")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | *required* | Natural language search query |
| `anima_id` | string | env default | Override default anima |
| `sources` | string[] | all | Filter: `"memories"`, `"knowledge"`, `"identity"` |
| `max_tokens` | int | 2000 | Token budget for results |
| `limit` | int | 20 | Max results |
| `exclude_ids` | string[] | — | Exclude IDs for multi-turn dedup |

### `search_memories` — Find past experiences

Semantic search across structured memories (reflections on past interactions).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | *required* | Search query |
| `anima_id` | string | env default | Override default anima |
| `limit` | int | 10 | Max results |
| `threshold` | float | 0.7 | Min similarity (0–1) |

### `search_knowledge` — Look up what the agent knows

Semantic search across canonicalized knowledge — facts, concepts, methods, principles, and experiences.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | *required* | Search query |
| `anima_id` | string | env default | Override default anima |
| `limit` | int | 10 | Max results |
| `threshold` | float | 0.7 | Min similarity (0–1) |
| `knowledge_type` | string | — | Filter: `FACT`, `CONCEPT`, `METHOD`, `PRINCIPLE`, `EXPERIENCE` |

### `get_identity` — Read the agent's personality

Retrieve the agent's behavioral fingerprint: personality type, communication style, and self-reflection.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `anima_id` | string | env default | Override default anima |

### `ingest_event` — Record an interaction

Capture a message, tool call, or system event. Queued for automatic memory synthesis.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | string | *required* | Event content |
| `event_type` | string | `message.in` | `message.in`, `message.out`, `tool.call`, `tool.result`, `system` |
| `anima_id` | string | env default | Override default anima |
| `role` | string | — | `user`, `assistant`, `system`, `tool` |
| `author` | string | — | Who generated this event |
| `session_id` | string | — | Group related events |

## Resources

Two resources provide context that MCP clients can embed directly into system prompts:

| URI | Type | Description |
|-----|------|-------------|
| `anima://{id}/pack` | `text/plain` | Latest compiled memory pack — memories, knowledge, identity, and temporal context assembled into a single prompt-ready string |
| `anima://{id}/identity` | `application/json` | Identity profile — personality type, communication style, self-reflection |

## How It Works

Elephantasm is a **Long-Term Agentic Memory** framework. The MCP server connects your agent to its memory backend:

```
Your Agent ←→ elephantasm-mcp ←→ api.elephantasm.com ←→ PostgreSQL + pgVector
```

**Write path:** `ingest_event` → Events accumulate → Memory Synthesis (LLM) → Knowledge Synthesis (LLM) → Identity evolution

**Read path:** `query` / `search_memories` / `search_knowledge` → pgVector semantic search → scored, formatted results

Memory is curated automatically by two background loops:
- **Dreamer** — decays, merges, splits, and archives memories
- **Meditator** — clusters, merges, reclassifies, and refines knowledge

## SDKs

For programmatic access without MCP, use the native SDKs:

- **Python**: [`elephantasm`](https://pypi.org/project/elephantasm/) — `pip install elephantasm`
- **TypeScript**: [`@elephantasm/client`](https://www.npmjs.com/package/@elephantasm/client) — `npm install @elephantasm/client`

## Links

- [Documentation](https://elephantasm.com/docs)
- [Dashboard](https://elephantasm.com)
- [GitHub](https://github.com/kaminocorp/elephantasm-mcp)
- [API Reference](https://api.elephantasm.com/docs)

## License

Apache 2.0
