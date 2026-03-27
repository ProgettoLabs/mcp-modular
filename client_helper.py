import re

RESOURCE_PATTERN = re.compile(r'@(\S+)')
PROMPT_PATTERN = re.compile(r'/(\w+)((?:\s+\w+=\S+)*)\s*$')
KWARG_PATTERN = re.compile(r'(\w+)=(\S+)')

# ANSI color helpers
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
BLUE   = "\033[34m"

def c(text, *codes):
    return "".join(codes) + str(text) + RESET


def uri_template_to_regex(template):
    """Convert a URI template like 'myapp://data/{id}' to a compiled regex."""
    escaped = re.escape(template)
    pattern = re.sub(r'\\\{(\w+)\\\}', r'(?P<\1>[^/]+)', escaped)
    return re.compile(f'^{pattern}$')


def process_server_capabilities(tools_resp, resources_resp, templates_resp, prompts_resp):
    """Transform raw MCP responses into the data structures used by the client."""
    ollama_tools = build_tools_for_ollama(tools_resp.tools)
    known_uris = {str(r.uri) for r in resources_resp.resources}
    known_templates = [str(t.uriTemplate) for t in templates_resp.resourceTemplates]
    template_regexes = [uri_template_to_regex(t) for t in known_templates]
    known_prompts = {p.name for p in prompts_resp.prompts}
    return ollama_tools, known_uris, known_templates, template_regexes, known_prompts


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



def print_capabilities(known_uris, known_templates, known_prompts):
    print(c("MCP Chat", BOLD, CYAN) + c("  —  type 'exit' or 'quit' to stop", DIM))
    print()
    print(c("Usage:", BOLD))
    print(c("  @<uri>", CYAN) + "                        attach a resource into your message")
    print(c("  @<uri-template-with-values>", CYAN) + "   attach a resource template into your message")
    print(c("  /<prompt>", CYAN) + c(" [key=val ...]", DIM) + "        inject a prompt into the conversation")
    print()
    if known_uris:
        print(c("  Resources:          ", BOLD) + c(', '.join(sorted(known_uris)), CYAN))
    if known_templates:
        print(c("  Resource templates: ", BOLD) + c(', '.join(sorted(known_templates)), CYAN))
    if known_prompts:
        print(c("  Prompts:            ", BOLD) + c(', '.join(sorted(known_prompts)), CYAN))
    print()


def parse_prompt_command(user_input, known_prompts):
    """If user_input is a prompt command, return (prompt_name, arguments), else None."""
    match = PROMPT_PATTERN.match(user_input.strip())
    if not match or match.group(1) not in known_prompts:
        return None
    prompt_name = match.group(1)
    arguments = {k: v for k, v in KWARG_PATTERN.findall(match.group(2))}
    return prompt_name, arguments


def parse_resource_mentions(user_input, known_uris, template_regexes):
    """Return (uri, is_template) pairs for valid @uri mentions in user_input."""
    valid = []
    for uri in RESOURCE_PATTERN.findall(user_input):
        if uri in known_uris:
            valid.append((uri, False))
        elif any(r.match(uri) for r in template_regexes):
            valid.append((uri, True))
        else:
            print(c(f"  ✗ unknown resource: {uri}", RED))
    return valid
