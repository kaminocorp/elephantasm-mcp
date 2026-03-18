"""MCP resource implementations for Elephantasm."""

import json

from .client import ElephantasmClient


def read_pack(client: ElephantasmClient, anima_id: str) -> str:
    """Read the latest compiled memory pack for an anima."""
    result = client.get(f"/animas/{anima_id}/memory-packs/latest")
    if result and result.get("context"):
        return result["context"]
    return json.dumps(result, indent=2, default=str)


def read_identity(client: ElephantasmClient, anima_id: str) -> str:
    """Read identity data for an anima."""
    result = client.get(f"/identities/anima/{anima_id}")
    return json.dumps(result, indent=2, default=str)
