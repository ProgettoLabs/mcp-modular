import json
from mcp_instance import mcp


# NOTE: This is a dummy resource with sample data for demonstration purposes.
@mcp.resource("coke://regulations/massachusetts/{regulation_id}")
async def get_massachusetts_regulations(regulation_id: str) -> str:
    """Massachusetts state legislation related to beverages.

    Args:
        regulation_id: Regulation identifier (e.g., "bottle-bill", "sugar-tax",
                       "labeling", "school-sales")
    """
    try:
        file_path = "resources/data/massachusetts_regulations.json"
        with open(file_path, 'r') as f:
            regulations = json.load(f)
    except FileNotFoundError:
        return f"Regulations data file not found: {file_path}"

    if regulation_id not in regulations:
        return json.dumps({
            "found": False,
            "message": f"No regulation found for '{regulation_id}'",
            "available_regulations": list(regulations.keys()),
        })

    return json.dumps(regulations[regulation_id], indent=2)
