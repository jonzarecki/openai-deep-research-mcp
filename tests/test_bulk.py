import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deep_research_mcp import call_tools_bulk, call_tool_bulk
from fastmcp.contrib.bulk_tool_caller.bulk_tool_caller import CallToolRequest


class FakeItem:
    file_id = "123"
    filename = "Test Paper"

fake_search_resp = [FakeItem()]


def test_bulk_tools(monkeypatch):
    async def fake_search(query):
        return fake_search_resp

    monkeypatch.setattr(
        "deep_research_mcp.server._search_vector_store", fake_search
    )
    reqs = [
        CallToolRequest(tool="search_papers", arguments={"query": "ai"}),
    ]
    results = asyncio.run(call_tools_bulk(reqs))
    assert len(results) == 1
    assert "Test Paper" in results[0].content[0].text


def test_bulk_tool(monkeypatch):
    async def fake_search(query):
        return fake_search_resp

    monkeypatch.setattr(
        "deep_research_mcp.server._search_vector_store", fake_search
    )

    results = asyncio.run(call_tool_bulk("search_papers", [{"query": "ai"}]))
    assert len(results) == 1
    assert not results[0].isError


def test_bulk_research(monkeypatch):
    async def fake_run(q):
        return "Deep result"

    monkeypatch.setattr(
        "deep_research_mcp.server._run_deep_research",
        fake_run,
    )

    results = asyncio.run(
        call_tool_bulk(
            "research_summary",
            [{"question": "AI"}],
        )
    )
    assert len(results) == 1
    assert not results[0].isError
