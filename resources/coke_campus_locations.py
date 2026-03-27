from mcp_instance import mcp


# NOTE: This is a dummy resource with sample data for demonstration purposes.
@mcp.resource("coke://locations/mit-campus")
async def get_mit_locations() -> str:
    """List of Coke availability on MIT campus organized by type."""
    try:
        file_path = "resources/data/mit_campus.txt"
        with open(file_path, 'r') as f:
            location_data = f.read()
        return location_data
    except FileNotFoundError:
        return f"Location data file not found: {file_path}"
