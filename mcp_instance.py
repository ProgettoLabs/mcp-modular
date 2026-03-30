from mcp.server.fastmcp import FastMCP
import yaml
from pathlib import Path

mcp = FastMCP("my-mcp-server")

def get_access_dir() -> Path:
    creds_path = Path(__file__).parent / ".credentials" / "file_access.yaml"
    with open(creds_path) as f:
        data = yaml.safe_load(f)
        return Path(data["access_dir"]).resolve()

def load_email_credentials():
    creds_path = Path(__file__).parent / ".credentials" / "mail_credentials.yaml"
    with open(creds_path) as f:
        return yaml.safe_load(f)
