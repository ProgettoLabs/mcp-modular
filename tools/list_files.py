import os
from pathlib import Path
from mcp_instance import mcp, get_access_dir

@mcp.tool()
def list_files() -> str:
    """List all files in the configured allowed directory.
    
    This tool reads the allowed directory from the file_access.yaml credentials
    and returns a formatted list of all files present within that directory.
    
    Returns:
        A string containing a newline-separated list of filenames, or an error message.
    """
    allowed_dir = get_access_dir()
    files = os.listdir(allowed_dir)

    if not files:
        return "The directory is empty."
        
    return "Files in directory:\n" + "\n".join(f"- {f}" for f in files)
