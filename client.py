import asyncio
import os
import ollama
from mcp import ClientSession
from mcp.client.sse import sse_client
from client_helper import (
    process_server_capabilities,
    print_capabilities,
    parse_prompt_command,
    parse_resource_mentions,
    c, BOLD, BLUE, DIM, YELLOW, GREEN,
)

MODEL = "llama3.1:8b"


async def build_user_turn(session, user_input, known_uris, template_regexes, known_prompts):
    # If the input is a prompt command (/name key=val), fetch it from the server and return its messages directly
    parsed = parse_prompt_command(user_input, known_prompts)
    if parsed is not None:
        prompt_name, arguments = parsed
        print(c(f"  ↳ fetching prompt: {prompt_name} {arguments}", DIM, YELLOW))
        result = await session.get_prompt(prompt_name, arguments=arguments if arguments else None)
        return [{"role": msg.role, "content": msg.content.text} for msg in result.messages if hasattr(msg.content, "text")]

    # Otherwise, fetch any @uri resources mentioned and prepend them as context
    parts = []
    for uri, is_template in parse_resource_mentions(user_input, known_uris, template_regexes):
        label = " (template)" if is_template else ""
        print(c(f"  ↳ fetching resource{label}: {uri}", DIM, YELLOW))
        result = await session.read_resource(uri)
        content_text = "\n".join(block.text for block in result.contents if hasattr(block, "text"))
        parts.append(f"Resource {uri}:\n{content_text}")

    # Attach fetched resource content to the message, or send the raw input if none
    resource_context = "\n\n".join(parts) if parts else None
    content = f"{user_input}\n\n{resource_context}" if resource_context else user_input
    return [{"role": "user", "content": content}]


async def run_ollama_turn(session, messages, ollama_tools):
    # Keep looping until the model produces a plain text response with no tool calls
    while True:
        response = ollama.chat(model=MODEL, messages=messages, tools=ollama_tools or None)
        assistant_message = response.message
        messages.append(assistant_message)

        # No tool calls — the model is done, print the response and exit
        if not assistant_message.tool_calls:
            print()
            print(c("Assistant: ", BOLD, GREEN) + assistant_message.content)
            print()
            return

        # Execute each requested tool call and feed the results back for the next iteration
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = dict(tool_call.function.arguments)
            print(c(f"  ⚙ calling tool: {tool_name}", DIM, YELLOW))
            result = await session.call_tool(tool_name, tool_args)
            result_text = "\n".join(block.text for block in result.content if hasattr(block, "text"))
            messages.append({"role": "tool", "content": result_text})


async def chat_loop(session, ollama_tools, known_uris, template_regexes, known_prompts):
    messages = []

    while True:
        # Read user input, exiting gracefully on Ctrl-C or EOF
        try:
            user_input = input(c("You: ", BOLD, BLUE)).strip()
        except (EOFError, KeyboardInterrupt):
            print(c("\nGoodbye!", DIM))
            return

        # Exit on explicit quit command
        if user_input.lower() in ("exit", "quit"):
            print(c("Goodbye!", DIM))
            return

        # Skip blank lines
        if not user_input:
            continue

        # Build the user turn (resolving any prompts/resources) then get the model's response
        turn = await build_user_turn(session, user_input, known_uris, template_regexes, known_prompts)
        messages.extend(turn)
        await run_ollama_turn(session, messages, ollama_tools)


async def main():
    # Connect to the MCP server
    host = os.getenv("MCP_HOST", "localhost")
    port = int(os.getenv("MCP_PORT", "8000"))
    url = f"http://{host}:{port}/sse"

    print(c(f"Connecting to MCP server at {url}…", DIM))

    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Query the MCP server for all available tools, resources, and prompts
            tools_resp, resources_resp, templates_resp, prompts_resp = await asyncio.gather(
                session.list_tools(),
                session.list_resources(),
                session.list_resource_templates(),
                session.list_prompts(),
            )
            # Transform the raw responses into the data structures the client needs
            ollama_tools, known_uris, known_templates, template_regexes, known_prompts = \
                process_server_capabilities(tools_resp, resources_resp, templates_resp, prompts_resp)

            # Show the user what resources and prompts are available before starting
            print_capabilities(known_uris, known_templates, known_prompts)

            await chat_loop(session, ollama_tools, known_uris, template_regexes, known_prompts)


if __name__ == "__main__":
    asyncio.run(main())
