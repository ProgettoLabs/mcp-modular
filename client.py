import asyncio
import os
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    host = os.getenv("MCP_HOST", "localhost")
    port = int(os.getenv("MCP_PORT", "8000"))
    url = f"http://{host}:{port}/sse"

    print(f"Connecting to MCP server at {url}...\n")

    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print(f"Found {len(tools.tools)} tool(s):\n")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")


if __name__ == "__main__":
    asyncio.run(main())
