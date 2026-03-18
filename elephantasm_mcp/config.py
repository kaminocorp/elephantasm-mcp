"""Configuration for Elephantasm MCP server."""

from pydantic_settings import BaseSettings


class ElephantasmConfig(BaseSettings):
    """MCP server configuration via env vars or constructor."""

    api_key: str = ""
    anima_id: str = ""
    endpoint: str = "https://api.elephantasm.com/api"

    model_config = {"env_prefix": "ELEPHANTASM_"}


settings = ElephantasmConfig()
