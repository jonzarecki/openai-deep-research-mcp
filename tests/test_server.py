import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deep_research_mcp import (
    search_papers,
    get_paper_summary,
    categories,
    suggest_reading,
)





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


def test_resources_and_prompts():
    assert "general" in asyncio.run(categories.read())
    msg = asyncio.run(suggest_reading.render({"topic": "AI"}))
    assert "AI" in msg[0].content.text
