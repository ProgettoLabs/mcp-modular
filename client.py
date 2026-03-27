import asyncio
import os
import re
import ollama
from mcp import ClientSession
from mcp.client.sse import sse_client

RESOURCE_PATTERN = re.compile(r'@(\S+)')
PROMPT_PATTERN = re.compile(r'/(\w+)((?:\s+\w+=\S+)*)\s*$')
KWARG_PATTERN = re.compile(r'(\w+)=(\S+)')


def uri_template_to_regex(template):
    """Convert a URI template like 'myapp://data/{id}' to a compiled regex."""
    escaped = re.escape(template)
    pattern = re.sub(r'\\\{(\w+)\\\}', r'(?P<\1>[^/]+)', escaped)
    return re.compile(f'^{pattern}$')


def build_tools_for_ollama(tools):
    """Convert MCP tools to the format ollama expects."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools
    ]


async def load_server_capabilities(session):
    """Fetch tools, resources, resource templates, and prompts from the MCP server."""
    tools_resp, resources_resp, templates_resp, prompts_resp = await asyncio.gather(
        session.list_tools(),
        session.list_resources(),
        session.list_resource_templates(),
        session.list_prompts(),
    )

    ollama_tools = build_tools_for_ollama(tools_resp.tools)
    known_uris = {str(r.uri) for r in resources_resp.resources}
    known_templates = [str(t.uriTemplate) for t in templates_resp.resourceTemplates]
    template_regexes = [uri_template_to_regex(t) for t in known_templates]
    known_prompts = {p.name for p in prompts_resp.prompts}

    return ollama_tools, known_uris, known_templates, template_regexes, known_prompts


def print_capabilities(known_uris, known_templates, known_prompts):
    print("MCP chat ready. Type 'exit' or 'quit' to stop.")
    if known_uris:
        print(f"  Resources:          {', '.join(sorted(known_uris))}")
    if known_templates:
        print(f"  Resource templates: {', '.join(sorted(known_templates))}")
    if known_prompts:
        print(f"  Prompts:            {', '.join(sorted(known_prompts))}")
    print()


async def call_mcp_tool(session, name, arguments):
    result = await session.call_tool(name, arguments)
    return "\n".join(
        block.text for block in result.content if hasattr(block, "text")
    )


async def resolve_resources(session, user_input, known_uris, template_regexes):
    """Fetch any @uri references in user_input. Returns extra context string."""
    mentions = RESOURCE_PATTERN.findall(user_input)
    if not mentions:
        return None

    parts = []
    for uri in mentions:
        if uri in known_uris:
            print(f"  [fetching resource: {uri}]")
            result = await session.read_resource(uri)
        elif any(r.match(uri) for r in template_regexes):
            print(f"  [fetching resource (template): {uri}]")
            result = await session.read_resource(uri)
        else:
            print(f"  [unknown resource: {uri}]")
            continue

        content_text = "\n".join(
            block.text for block in result.contents if hasattr(block, "text")
        )
        parts.append(f"Resource {uri}:\n{content_text}")

    return "\n\n".join(parts) if parts else None


async def resolve_prompt(session, user_input, known_prompts):
    """If user_input is /promptname [key=val ...], fetch and return its messages."""
    match = PROMPT_PATTERN.match(user_input.strip())
    if not match or match.group(1) not in known_prompts:
        return None

    prompt_name = match.group(1)
    arguments = {k: v for k, v in KWARG_PATTERN.findall(match.group(2))}

    print(f"  [fetching prompt: {prompt_name} {arguments}]")
    result = await session.get_prompt(prompt_name, arguments=arguments if arguments else None)

    return [
        {"role": msg.role, "content": msg.content.text}
        for msg in result.messages
        if hasattr(msg.content, "text")
    ]


async def build_user_turn(session, user_input, known_uris, template_regexes, known_prompts):
    """Parse user input and return messages to append to the conversation."""
    prompt_messages = await resolve_prompt(session, user_input, known_prompts)
    if prompt_messages is not None:
        return prompt_messages

    resource_context = await resolve_resources(session, user_input, known_uris, template_regexes)
    content = f"{user_input}\n\n{resource_context}" if resource_context else user_input
    return [{"role": "user", "content": content}]


async def run_ollama_turn(session, messages, ollama_tools):
    """Send messages to ollama, execute any tool calls, and return when the model is done."""
    while True:
        response = ollama.chat(
            model="llama3.1:8b",
            messages=messages,
            tools=ollama_tools if ollama_tools else None,
        )

        assistant_message = response.message
        messages.append(assistant_message)

        if not assistant_message.tool_calls:
            print(f"\nAssistant: {assistant_message.content}\n")
            return

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = dict(tool_call.function.arguments)
            print(f"  [calling tool: {tool_name}]")
            result = await call_mcp_tool(session, tool_name, tool_args)
            messages.append({"role": "tool", "content": result})


async def chat_loop(session, ollama_tools, known_uris, template_regexes, known_prompts):
    """Main interactive loop."""
    messages = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            return

        if not user_input:
            continue

        turn = await build_user_turn(session, user_input, known_uris, template_regexes, known_prompts)
        messages.extend(turn)
        await run_ollama_turn(session, messages, ollama_tools)


async def main():
    host = os.getenv("MCP_HOST", "localhost")
    port = int(os.getenv("MCP_PORT", "8000"))
    url = f"http://{host}:{port}/sse"

    print(f"Connecting to MCP server at {url}...\n")

    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            ollama_tools, known_uris, known_templates, template_regexes, known_prompts = \
                await load_server_capabilities(session)

            print_capabilities(known_uris, known_templates, known_prompts)

            await chat_loop(session, ollama_tools, known_uris, template_regexes, known_prompts)


if __name__ == "__main__":
    asyncio.run(main())
