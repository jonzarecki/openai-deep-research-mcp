# Deep Research MCP

A Model Context Protocol (MCP) server exposing the OpenAI Deep Research API. It demonstrates best practices for building MCP servers with [fastmcp](https://pypi.org/project/fastmcp/).

## Installation
```bash
pip install git+https://github.com/jonzarecki/openai-deep-research-mcp
```

### Quick Setup Outline
1. Install the package using ``pip`` or ``npx``.
2. Set ``OPENAI_API_KEY`` and any optional variables shown below.
3. Add the server entry to your ``mcp.json`` so clients like Cursor can launch it automatically.
4. Run ``deep-research-mcp`` to start the server or call the tool from Python.

You can also run the server via `npx` without installing system wide:
```bash
npx --yes github:jonzarecki/openai-deep-research-mcp
```

Or clone this repository and install in editable mode:
```bash
git clone <repo-url>
cd deep-research-mcp
pip install -e .
```

### Configuration
Set your OpenAI credentials so the server can call the Deep Research API:
```bash
export OPENAI_API_KEY=<your key>
```
Optional environment variables `DEEP_RESEARCH_MODEL`, `DEEP_RESEARCH_SYSTEM_PROMPT` and `DEEP_RESEARCH_TOOLS` define defaults for the Deep Research call. You can override them when invoking the `research_summary` tool.

The server uses the asynchronous OpenAI client under the hood. Ensure the above environment variables are defined before running.

### Caching
Results are automatically cached on disk so repeated queries don't consume extra
API credits. You can configure caching behaviour with these optional variables:

* `DEEP_RESEARCH_CACHE_PATH` – JSON file storing cached responses.
* `DEEP_RESEARCH_OUTPUT_DIR` – directory where each research result is written.
* `DEEP_RESEARCH_LOG_FILE` – log file path recording cache and API events.

Use the `get_cached_research` tool to retrieve a cached result without making a
new API call.

## Usage
Run the server directly (stdout/stdin transport):
```bash
deep-research-mcp
```

The server exposes tools for querying the Deep Research API. See the docstrings in `deep_research_mcp.server` for details.

### Simple API example
For a minimal script that calls the Deep Research API directly using the OpenAI SDK, see ``examples/deep_research_example.py``.

### MCP client configuration
To let your MCP client automatically install and run this server, add the following JSON to your `mcp.json`:
```json
{
  "mcpServers": {
    "deep-research-mcp": {
      "command": "npx --yes github:jonzarecki/openai-deep-research-mcp",
      "env": {}
    }
  }
}
```

## Development
Contributions are welcome. After cloning run:
```bash
pip install -e .[test]
pre-commit install
```
Run the test suite with coverage:
```bash
pytest --cov=deep_research_mcp --cov-report=term-missing
```
