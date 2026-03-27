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

            resources = await session.list_resources()
            print(f"\nFound {len(resources.resources)} resource(s):\n")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.description}")

            resource_templates = await session.list_resource_templates()
            print(f"\nFound {len(resource_templates.resourceTemplates)} resource template(s):\n")
            for template in resource_templates.resourceTemplates:
                print(f"  - {template.uriTemplate}: {template.description}")

            prompts = await session.list_prompts()
            print(f"\nFound {len(prompts.prompts)} prompt(s):\n")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")


if __name__ == "__main__":
    asyncio.run(main())
