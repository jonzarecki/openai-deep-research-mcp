# Deep Research MCP

A Model Context Protocol (MCP) server exposing the OpenAI Deep Research API. It demonstrates best practices for building MCP servers with [fastmcp](https://pypi.org/project/fastmcp/).

## Installation
```bash
pip install git+https://github.com/openai/deep-research-mcp
```

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
Set your OpenAI credentials and vector store ID so the server can call the Deep Research API:
```bash
export OPENAI_API_KEY=<your key>
export VECTOR_STORE_ID=<vector store id>
```

The server uses the asynchronous OpenAI client under the hood. Ensure the above environment variables are defined before running.

## Usage
Run the server directly (stdout/stdin transport):
```bash
deep-research-mcp
```

The server exposes tools for querying the Deep Research API. See the docstrings in `deep_research_mcp.server` for details.

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
