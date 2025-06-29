# Deep Research MCP

A Model Context Protocol (MCP) server exposing the OpenAI Deep Research API. It demonstrates best practices for building MCP servers with [fastmcp](https://pypi.org/project/fastmcp/).

## Installation
```bash
pip install git+https://github.com/openai/deep-research-mcp
```

### Quick Setup Outline
1. Install the package using ``pip`` or ``npx``.
2. Export the environment variables shown below (API key, vector store ID, etc.).
3. Run ``deep-research-mcp`` to start the server or call the tools from Python.

You can also run the server via `npx` without installing system wide:
```bash
npx --yes github:openai/deep-research-mcp
```

Or clone this repository and install in editable mode:
```bash
git clone <repo-url>
cd deep-research-mcp
pip install -e .
```

### Configuration
Set your OpenAI credentials and vector store ID so the server can call the Deep Research API. You may also specify `DEEP_RESEARCH_MODEL` to override the default model. `DEEP_RESEARCH_SYSTEM_PROMPT` customizes the system prompt and `DEEP_RESEARCH_TOOLS` controls which tools are sent to the API:
```bash
export OPENAI_API_KEY=<your key>
export VECTOR_STORE_ID=<vector store id>
export DEEP_RESEARCH_MODEL=o4-mini-deep-research-2025-06-26  # optional
export DEEP_RESEARCH_SYSTEM_PROMPT="You are an expert researcher"  # optional
export DEEP_RESEARCH_TOOLS="web_search_preview,code_interpreter"   # optional
```

The server uses the asynchronous OpenAI client under the hood. Ensure the above environment variables are defined before running.

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
      "command": "npx --yes github:openai/deep-research-mcp",
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
