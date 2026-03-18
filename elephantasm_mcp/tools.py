"""MCP tool implementations for Elephantasm brain search."""

from typing import Any

from .client import ElephantasmClient
from .config import settings


def _resolve_anima_id(anima_id: str | None) -> str:
    """Resolve anima_id from parameter or config default."""
    aid = anima_id or settings.anima_id
    if not aid:
        raise ValueError(
            "anima_id required. Provide parameter or set ELEPHANTASM_ANIMA_ID."
        )
    return aid


def query(
    client: ElephantasmClient,
    query: str,
    anima_id: str | None = None,
    sources: list[str] | None = None,
    max_tokens: int = 2000,
    limit: int = 20,
    exclude_ids: list[str] | None = None,
) -> str:
    """Unified cross-source brain search. Returns formatted context string."""
    body: dict[str, Any] = {
        "anima_id": _resolve_anima_id(anima_id),
        "query": query,
        "max_tokens": max_tokens,
        "limit": limit,
    }
    if sources:
        body["sources"] = sources
    if exclude_ids:
        body["exclude_ids"] = exclude_ids

    result = client.post("/query", json=body)
    return result.get("context", "")


def search_memories(
    client: ElephantasmClient,
    query: str,
    anima_id: str | None = None,
    limit: int = 10,
    threshold: float = 0.7,
) -> str:
    """Semantic search across memories. Returns formatted results."""
    body = {
        "anima_id": _resolve_anima_id(anima_id),
        "query": query,
        "limit": limit,
        "threshold": threshold,
    }
    results = client.post("/memories/search/semantic", json=body)

    if not results:
        return "No matching memories found."

    lines = []
    for item in results:
        memory = item.get("memory", {})
        score = item.get("score", 0)
        summary = memory.get("summary", memory.get("content", ""))
        lines.append(f"- [{score:.2f}] {summary}")
    return "\n".join(lines)


def search_knowledge(
    client: ElephantasmClient,
    query: str,
    anima_id: str | None = None,
    limit: int = 10,
    threshold: float = 0.7,
    knowledge_type: str | None = None,
) -> str:
    """Semantic search across knowledge. Returns formatted results."""
    body: dict[str, Any] = {
        "anima_id": _resolve_anima_id(anima_id),
        "query": query,
        "limit": limit,
        "threshold": threshold,
    }
    if knowledge_type:
        body["knowledge_type"] = knowledge_type

    results = client.post("/knowledge/search/semantic", json=body)

    if not results:
        return "No matching knowledge found."

    lines = []
    for item in results:
        knowledge = item.get("knowledge", {})
        score = item.get("score", 0)
        ktype = knowledge.get("knowledge_type", "")
        content = knowledge.get("content", "")
        topic = knowledge.get("topic", "")
        prefix = f"[{ktype}] {topic}: " if topic else f"[{ktype}] "
        lines.append(f"- [{score:.2f}] {prefix}{content}")
    return "\n".join(lines)


def get_identity(
    client: ElephantasmClient,
    anima_id: str | None = None,
) -> str:
    """Get anima identity (personality, communication style, self-reflection)."""
    aid = _resolve_anima_id(anima_id)
    result = client.get(f"/identities/anima/{aid}")

    parts = []
    if result.get("personality_type"):
        parts.append(f"Personality: {result['personality_type']}")
    if result.get("communication_style"):
        parts.append(f"Communication: {result['communication_style']}")
    self_data = result.get("self", {})
    if self_data:
        for key, value in self_data.items():
            if isinstance(value, list):
                parts.append(f"{key}: {', '.join(str(v) for v in value)}")
            elif value:
                parts.append(f"{key}: {value}")
    return "\n".join(parts) if parts else "No identity data available."


def ingest_event(
    client: ElephantasmClient,
    content: str,
    event_type: str = "message.in",
    anima_id: str | None = None,
    role: str | None = None,
    author: str | None = None,
    session_id: str | None = None,
) -> str:
    """Record an interaction event for memory synthesis."""
    body: dict[str, Any] = {
        "anima_id": _resolve_anima_id(anima_id),
        "event_type": event_type,
        "content": content,
    }
    if role:
        body["role"] = role
    if author:
        body["author"] = author
    if session_id:
        body["session_id"] = session_id

    result = client.post("/events", json=body)
    event_id = result.get("id", "unknown")
    return f"Event recorded: {event_id}"
