import os
from pathlib import Path
from mcp_instance import mcp, get_access_dir

@mcp.tool()
def create_file(filename: str, content: str) -> str:
    """Create a new file with the given content in the allowed directory.
    
    This tool takes a filename and text content, verifies the path is within 
    the configured allowed directory, and writes the content to the file.
    If the file already exists, it will be overwritten.
    
    Args:
        filename: The name of the file to create (relative to the allowed directory).
        content: The text content to write into the file.
        
    Returns:
        A success message indicating the file was created, or an error message.
    """
    try:
        filepath = get_access_dir() / filename

        # Ensure the allowed directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Successfully created/updated file: {filename}"
    except Exception as e:
        return f"Error creating file: {str(e)}"
