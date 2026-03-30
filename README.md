# MCP Modular Server

A modular MCP (Model Context Protocol) server built with FastMCP. Each tool, prompt, and resource lives in its own file — no central registration needed.

---

## Installation

**1. Clone the repo and navigate to the project directory.**

**2. Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## File Structure

```
mcp-modular/
├── mcp_instance.py        # Creates the shared MCP instance
├── server.py              # Entry point — auto-loads all modules
├── requirements.txt
├── prompts/
│   ├── __init__.py
│   └── my_prompt.py       # One prompt per file
├── tools/
│   ├── __init__.py
│   └── my_tool.py         # One tool per file
└── resources/
    ├── __init__.py
    └── my_resource.py     # One resource per file
```

`server.py` automatically discovers and loads every `.py` file inside `prompts/`, `tools/`, and `resources/`. You never need to register anything manually.

---

## Adding a New Prompt, Resource, or Tool

### New Tool

Create a file in `tools/`, e.g. `tools/my_tool.py`:

```python
from mcp_instance import mcp

@mcp.tool()
async def my_tool(param: str) -> str:
    """Description of what this tool does."""
    return f"Result: {param}"
```

### New Prompt

Create a file in `prompts/`, e.g. `prompts/my_prompt.py`:

```python
from mcp_instance import mcp

@mcp.prompt()
async def my_prompt(context: str) -> str:
    """Description of what this prompt does."""
    return f"You are a helpful assistant. Context: {context}"
```

### New Resource

Create a file in `resources/`, e.g. `resources/my_resource.py`:

```python
from mcp_instance import mcp

@mcp.resource("myapp://data/my-resource")
async def my_resource() -> str:
    """Description of this resource."""
    return "Resource content here"
```

That's it — no imports or registration needed anywhere else. The server picks it up automatically on next run.

---

## The Only Import You Need

Every file in `prompts/`, `tools/`, and `resources/` only needs one import:

```python
from mcp_instance import mcp
```

Use the `mcp` object to register your handlers with `@mcp.tool()`, `@mcp.prompt()`, or `@mcp.resource(...)`.

---

## Sample Email Tools

The project includes sample tools for reading and sending emails (`tools/email_reader.py` and `tools/email_sender.py`). If you want to use these tools, you need to set up your credentials in `.credentials/mail_credentials.yaml`:

```yaml
imap_host: imap.gmail.com # or any other IMAP server
smtp_host: smtp.gmail.com # or any other SMTP server
email_user: your_email@gmail.com
email_password: your_password_here
recipient_email: recipient_email@example.com
```

**Important Note on Passwords:** The `email_password` field is usually an **App Password**, which is different from your standard login password. If you are using Gmail, you can find instructions on how to generate an app password here: [Sign in with app passwords - Gmail Help](https://support.google.com/mail/answer/185833?hl=en).

---

## File Access Tools

The project includes three tools for interacting with the local file system in a restricted manner:
- `list_files`: Lists all files within the allowed directory.
- `read_file`: Reads the contents of a specific file.
- `create_file`: Creates or overwrites a file with new content.

To use these tools, you must configure the allowed directory path in `.credentials/file_access.yaml`:

```yaml
access_dir: /path/to/your/allowed/directory
```

### Helper Functions

For both the email and file access tools, the credentials and configuration loading logic is centralized in `mcp_instance.py` via two helper functions:
- `get_access_dir()`: Reads the allowed directory path from `file_access.yaml`.
- `load_email_credentials()`: Loads the email configuration from `mail_credentials.yaml`.

---

## Changing the Server Name

Open [mcp_instance.py](mcp_instance.py) and update the string passed to `FastMCP`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("your-server-name-here")
```

This name is how the server identifies itself to MCP clients.

---

## Running the Client

`client.py` is an interactive chat application powered by Ollama (`llama3.1:8b`). It connects to the MCP server, exposes all registered tools to the model, and runs a conversation loop until you type `exit` or `quit`.

**Prerequisites:** [Ollama](https://ollama.com) must be running locally with the `llama3.1:8b` model pulled:

```bash
ollama pull llama3.1:8b
```

**Start the client** (while the server is running):

```bash
python client.py
```

Override the server address with environment variables:

```bash
MCP_HOST=127.0.0.1 MCP_PORT=9000 python client.py
```

---

## Running the Server

The server supports two transports: **SSE** (default) and **stdio**.

### SSE (HTTP)

```bash
python server.py
```

Starts on `0.0.0.0:8000` by default. Override with environment variables:

```bash
MCP_HOST=127.0.0.1 MCP_PORT=9000 python server.py
```

### stdio

```bash
MCP_TRANSPORT=stdio python server.py
```

Use stdio when integrating with a client that communicates over standard input/output (e.g. Claude Desktop).
