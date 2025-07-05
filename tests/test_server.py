import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deep_research_mcp import research_summary, get_cached_research
from deep_research_mcp.server import _run_deep_research, _CACHE
import deep_research_mcp.server as server





def test_research_summary(monkeypatch, tmp_path):
    async def fake_run(*args, **kwargs):
        return "Result about AI"

    monkeypatch.setattr("deep_research_mcp.server._run_deep_research", fake_run)
    monkeypatch.setenv("DEEP_RESEARCH_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("DEEP_RESEARCH_CACHE_PATH", str(tmp_path / "cache.json"))
    monkeypatch.setenv("DEEP_RESEARCH_LOG_FILE", str(tmp_path / "log.txt"))

    result = asyncio.run(research_summary.fn("AI"))
    assert "Result" in result
    # second call should use cache
    result2 = asyncio.run(research_summary.fn("AI"))
    assert result2 == result


def test_run_deep_research_env(monkeypatch):
    class FakeResp:
        output = [type("O", (), {"content": [type("C", (), {"text": "done"})()]})]

    async def fake_create(self, **kwargs):
        assert kwargs["model"] == "test-model"
        assert kwargs["input"][0]["content"][0]["text"] == "my prompt"
        assert kwargs["tools"] == [{"type": "web_search_preview"}]
        return FakeResp()

    fake_client = type(
        "Cli",
        (),
        {"responses": type("Resp", (), {"create": fake_create})()},
    )

    monkeypatch.setattr(server, "_client", fake_client)

    result = asyncio.run(
        _run_deep_research(
            "hi",
            model="test-model",
            system_prompt="my prompt",
            tools=["web_search_preview"],
        )
    )
    assert result == "done"


def test_get_cached_research(monkeypatch):
    _CACHE.clear()
    _CACHE["key"] = {"result": "cached", "path": "p"}
    def fake_key(*args, **kwargs):
        return "key"

    monkeypatch.setattr("deep_research_mcp.server._cache_key", fake_key)
    result = asyncio.run(get_cached_research.fn("ignored"))
    assert result == "cached"
