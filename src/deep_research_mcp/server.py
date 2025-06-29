"""MCP server exposing the Deep Research API."""

"""MCP server exposing the OpenAI Deep Research API."""

import logging
import os
from typing import List

from openai import AsyncOpenAI
from fastmcp import FastMCP
from fastmcp.contrib.bulk_tool_caller import BulkToolCaller

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID", "")

_client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

mcp = FastMCP("deep-research-mcp")

_bulk_tools = BulkToolCaller()
_bulk_tools.register_tools(mcp)


async def _search_vector_store(query: str):
    if not _client:
        raise RuntimeError("OPENAI_API_KEY not configured")
    resp = _client.vector_stores.search(vector_store_id=VECTOR_STORE_ID, query=query)
    results = []
    async for item in resp:
        results.append(item)
    return results


async def _fetch_file(file_id: str) -> str:
    if not _client:
        raise RuntimeError("OPENAI_API_KEY not configured")
    pager = _client.vector_stores.files.content(
        vector_store_id=VECTOR_STORE_ID, file_id=file_id
    )
    parts = []
    async for chunk in pager:
        parts.append(getattr(chunk, "text", ""))
    return "\n".join(parts)


@mcp.tool()
async def search_papers(query: str) -> str:
    """Search vector store for papers matching ``query``."""
    items = await _search_vector_store(query)
    if not items:
        return "No papers found"
    lines = [
        f"{getattr(i, 'filename', 'Untitled')} ({getattr(i, 'file_id', '')})"
        for i in items[:10]
    ]
    if len(items) > 10:
        lines.append(f"...and {len(items) - 10} more results")
    return "\n".join(lines)


@mcp.tool()
async def get_paper_summary(paper_id: str) -> str:
    """Fetch the full text for ``paper_id`` and return a short snippet."""
    text = await _fetch_file(paper_id)
    return text[:500] if text else "No summary available"


@mcp.resource("deepresearch://categories")
async def categories() -> str:
    """List research categories if available."""
    return "general"


@mcp.prompt()
def suggest_reading(topic: str) -> str:
    """Prompt text to suggest reading material."""
    return (
        f"Provide recommended research papers about {topic}. "
        "Mention key authors and venues."
    )


def main() -> None:
    """Run the MCP server."""
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
