import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deep_research_mcp import call_tool_bulk


def test_bulk_research(monkeypatch):
    async def fake_run(*args, **kwargs):
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
