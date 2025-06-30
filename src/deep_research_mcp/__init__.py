"""Deep Research MCP server."""

from .server import main, mcp, research_summary, _bulk_tools

__all__ = [
    "main",
    "mcp",
    "research_summary",
    "call_tool_bulk",
    "call_tools_bulk",
]

call_tool_bulk = _bulk_tools.call_tool_bulk
call_tools_bulk = _bulk_tools.call_tools_bulk
