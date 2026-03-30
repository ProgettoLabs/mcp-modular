import os
from pathlib import Path
from mcp_instance import mcp, get_access_dir

@mcp.tool()
def read_file(filename: str) -> str:
    """Read the contents of a specific file in the allowed directory.
    
    This tool takes a filename, verifies it is within the configured allowed directory,
    and returns its text contents.
    
    Args:
        filename: The name of the file to read (relative to the allowed directory).
        
    Returns:
        The text contents of the file, or an error message if it fails.
    """
    filepath = get_access_dir() / filename
    if not os.path.exists(filepath):
        return f"Error: File '{filename}' does not exist."
        
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
