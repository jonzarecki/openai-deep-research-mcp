# Usage Examples

A few short examples using the tools provided by the server. Defaults can be set via environment variables, but you may override them per call.

```python
from deep_research_mcp import research_summary
print(
    research_summary.fn(
        "impact of AI",
        system_prompt="You are a helpful research assistant",
        model="o4-mini-deep-research-2025-06-26",
        tools=["web_search_preview"],
    )
)
```
