import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deep_research_mcp import (
    search_papers,
    get_paper_summary,
    research_summary,
    categories,
    suggest_reading,
)
from deep_research_mcp.server import _run_deep_research
import deep_research_mcp.server as server





def test_search_papers(monkeypatch):
    async def fake_search(query):
        class Item:
            file_id = "123"
            filename = "Test Paper"

        return [Item()]

    monkeypatch.setattr(
        "deep_research_mcp.server._search_vector_store", fake_search
    )
    result = asyncio.run(search_papers.fn("ai"))
    assert "Test Paper" in result


def test_get_paper_summary(monkeypatch):
    async def fake_fetch(fid):
        return "Great paper"

    monkeypatch.setattr("deep_research_mcp.server._fetch_file", fake_fetch)

    result = asyncio.run(get_paper_summary.fn("123"))
    assert "Great paper" in result


def test_research_summary(monkeypatch):
    async def fake_run(*args, **kwargs):
        return "Result about AI"

    monkeypatch.setattr("deep_research_mcp.server._run_deep_research", fake_run)
    result = asyncio.run(research_summary.fn("AI"))
    assert "Result" in result


def test_resources_and_prompts():
    assert "general" in asyncio.run(categories.read())
    msg = asyncio.run(suggest_reading.render({"topic": "AI"}))
    assert "AI" in msg[0].content.text


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
