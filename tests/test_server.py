import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deep_research_mcp import research_summary
from deep_research_mcp.server import _run_deep_research
import deep_research_mcp.server as server





def test_research_summary(monkeypatch):
    async def fake_run(*args, **kwargs):
        return "Result about AI"

    monkeypatch.setattr("deep_research_mcp.server._run_deep_research", fake_run)
    result = asyncio.run(research_summary.fn("AI"))
    assert "Result" in result


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
