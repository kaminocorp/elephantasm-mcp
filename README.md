# elephantasm-mcp

MCP server for [Elephantasm](https://elephantasm.com) Long-Term Agentic Memory. Gives any MCP-compatible AI agent plug-and-play access to persistent memory, knowledge, and identity.

## Quick Start

```bash
pip install elephantasm-mcp
```

Set environment variables:

```bash
export ELEPHANTASM_API_KEY=sk_live_...
export ELEPHANTASM_ANIMA_ID=your-anima-id  # optional default
```

### Claude Desktop / Claude Code

Add to your MCP config:

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

### Hermes Agent

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  elephantasm:
    command: elephantasm-mcp
    env:
      ELEPHANTASM_API_KEY: sk_live_...
      ELEPHANTASM_ANIMA_ID: your-anima-id
```

## Tools

| Tool | Description |
|------|-------------|
| `query` | Cross-source brain search (memories + knowledge + identity) |
| `search_memories` | Semantic search across memories |
| `search_knowledge` | Semantic search across knowledge base |
| `get_identity` | Get personality, communication style, self-reflection |
| `ingest_event` | Record an interaction for future memory synthesis |

## Resources

| URI | Description |
|-----|-------------|
| `anima://{id}/pack` | Latest compiled memory pack |
| `anima://{id}/identity` | Identity profile |

## License

Apache 2.0
