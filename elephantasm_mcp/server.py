"""Elephantasm MCP Server — plug-and-play long-term memory for AI agents.

Usage:
    # Via environment variables
    export ELEPHANTASM_API_KEY=sk_live_...
    export ELEPHANTASM_ANIMA_ID=your-anima-id
    elephantasm-mcp

    # Or via uvx
    uvx elephantasm-mcp
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool

from .client import ElephantasmClient
from .config import settings
from . import tools as tool_fns
from . import resources as resource_fns

server = Server("elephantasm-mcp")


def _get_client() -> ElephantasmClient:
    """Get or create the HTTP client."""
    if not hasattr(_get_client, "_instance"):
        _get_client._instance = ElephantasmClient()
    return _get_client._instance


# ─── Tool Definitions ────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query",
            description=(
                "Search an Anima's brain across memories, knowledge, and identity. "
                "Returns relevant results ranked by semantic similarity to your query. "
                "Use this for general questions about what the Anima knows or remembers."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query to search the Anima's brain",
                    },
                    "anima_id": {
                        "type": "string",
                        "description": "Anima ID (optional, uses default if not set)",
                    },
                    "sources": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["memories", "knowledge", "identity"]},
                        "description": "Which layers to search (default: all)",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Token budget for results (default: 2000)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of results (default: 20)",
                    },
                    "exclude_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "IDs to exclude (for multi-turn dedup)",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="search_memories",
            description=(
                "Semantic search across an Anima's memories. Returns memories "
                "ranked by similarity to your query. Use this when you want to "
                "find specific past experiences or interactions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "anima_id": {"type": "string"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)"},
                    "threshold": {
                        "type": "number",
                        "description": "Min similarity 0-1 (default: 0.7)",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="search_knowledge",
            description=(
                "Semantic search across an Anima's knowledge base. Returns "
                "canonicalized truths (facts, concepts, methods, principles, experiences) "
                "ranked by similarity. Use this for structured knowledge retrieval."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "anima_id": {"type": "string"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)"},
                    "threshold": {
                        "type": "number",
                        "description": "Min similarity 0-1 (default: 0.7)",
                    },
                    "knowledge_type": {
                        "type": "string",
                        "enum": ["FACT", "CONCEPT", "METHOD", "PRINCIPLE", "EXPERIENCE"],
                        "description": "Filter by knowledge type",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_identity",
            description=(
                "Get an Anima's identity profile — personality type, "
                "communication style, and self-reflection data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "anima_id": {"type": "string"},
                },
                "required": [],
            },
        ),
        Tool(
            name="ingest_event",
            description=(
                "Record an interaction event for future memory synthesis. "
                "Use this to capture messages, tool calls, or other signals "
                "that should become part of the Anima's long-term memory."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Event content (message text, tool output, etc.)",
                    },
                    "event_type": {
                        "type": "string",
                        "enum": ["message.in", "message.out", "tool.call", "tool.result", "system"],
                        "description": "Event type (default: message.in)",
                    },
                    "anima_id": {"type": "string"},
                    "role": {"type": "string", "description": "Message role (user, assistant, etc.)"},
                    "author": {"type": "string", "description": "Author identifier"},
                    "session_id": {"type": "string", "description": "Session grouping ID"},
                },
                "required": ["content"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    client = _get_client()

    if name == "query":
        result = tool_fns.query(
            client,
            query=arguments["query"],
            anima_id=arguments.get("anima_id"),
            sources=arguments.get("sources"),
            max_tokens=arguments.get("max_tokens", 2000),
            limit=arguments.get("limit", 20),
            exclude_ids=arguments.get("exclude_ids"),
        )
    elif name == "search_memories":
        result = tool_fns.search_memories(
            client,
            query=arguments["query"],
            anima_id=arguments.get("anima_id"),
            limit=arguments.get("limit", 10),
            threshold=arguments.get("threshold", 0.7),
        )
    elif name == "search_knowledge":
        result = tool_fns.search_knowledge(
            client,
            query=arguments["query"],
            anima_id=arguments.get("anima_id"),
            limit=arguments.get("limit", 10),
            threshold=arguments.get("threshold", 0.7),
            knowledge_type=arguments.get("knowledge_type"),
        )
    elif name == "get_identity":
        result = tool_fns.get_identity(
            client,
            anima_id=arguments.get("anima_id"),
        )
    elif name == "ingest_event":
        result = tool_fns.ingest_event(
            client,
            content=arguments["content"],
            event_type=arguments.get("event_type", "message.in"),
            anima_id=arguments.get("anima_id"),
            role=arguments.get("role"),
            author=arguments.get("author"),
            session_id=arguments.get("session_id"),
        )
    else:
        result = f"Unknown tool: {name}"

    return [TextContent(type="text", text=result)]


# ─── Resource Definitions ────────────────────────────────────────

@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = []
    if settings.anima_id:
        resources.extend([
            Resource(
                uri=f"anima://{settings.anima_id}/pack",
                name="Memory Pack",
                description="Latest compiled memory pack for the default Anima",
                mimeType="text/plain",
            ),
            Resource(
                uri=f"anima://{settings.anima_id}/identity",
                name="Identity",
                description="Identity profile for the default Anima",
                mimeType="application/json",
            ),
        ])
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    client = _get_client()

    # Parse anima:// URI
    if not uri.startswith("anima://"):
        raise ValueError(f"Unknown resource URI scheme: {uri}")

    # anima://{anima_id}/{resource_type}
    parts = uri[len("anima://"):].split("/", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid resource URI: {uri}")

    anima_id, resource_type = parts

    if resource_type == "pack":
        return resource_fns.read_pack(client, anima_id)
    elif resource_type == "identity":
        return resource_fns.read_identity(client, anima_id)
    else:
        raise ValueError(f"Unknown resource type: {resource_type}")


# ─── Entry Point ─────────────────────────────────────────────────

def main():
    """Run the Elephantasm MCP server (stdio transport)."""
    import asyncio

    async def _run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(_run())


if __name__ == "__main__":
    main()
