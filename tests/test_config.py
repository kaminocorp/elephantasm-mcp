"""Basic sanity tests for elephantasm-mcp."""

from elephantasm_mcp.config import ElephantasmConfig


def test_default_endpoint():
    """Config defaults to the production API endpoint."""
    config = ElephantasmConfig(api_key="sk_live_test")
    assert config.endpoint == "https://api.elephantasm.com/api"


def test_custom_endpoint():
    """Config accepts a custom endpoint."""
    config = ElephantasmConfig(api_key="sk_live_test", endpoint="http://localhost:8000/api")
    assert config.endpoint == "http://localhost:8000/api"
