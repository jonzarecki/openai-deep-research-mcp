# Usage Examples

A few short examples using the tools provided by the server. Environment variables are used to configure the model, system prompt and tools.

```python
from deep_research_mcp import search_papers, get_paper_summary, research_summary

print(search_papers.fn("machine learning"))
print(get_paper_summary.fn("file-123"))
print(research_summary.fn("impact of AI"))
```
