import os
import importlib
import pkgutil

import prompts
import tools
import resources
from mcp_instance import mcp

for pkg in [prompts, tools, resources]:
    for _, name, _ in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        importlib.import_module(name)


def main():
    transport = os.getenv("MCP_TRANSPORT", "sse")

    if transport == "sse":
        mcp.settings.host = os.getenv("MCP_HOST", "0.0.0.0")
        mcp.settings.port = int(os.getenv("MCP_PORT", "8000"))
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
