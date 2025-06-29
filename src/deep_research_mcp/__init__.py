"""Deep Research MCP server."""

from .server import (
    main,
    mcp,
    search_papers,
    get_paper_summary,
    categories,
    suggest_reading,
    _bulk_tools,
)

__all__ = [
    "main",
    "mcp",
    "search_papers",
    "get_paper_summary",
    "categories",
    "suggest_reading",
    "call_tool_bulk",
    "call_tools_bulk",
]

call_tool_bulk = _bulk_tools.call_tool_bulk
call_tools_bulk = _bulk_tools.call_tools_bulk
