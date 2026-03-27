import json
from mcp_instance import mcp


@mcp.resource("coke://media/advertisements/{ad_id}")
async def get_advertisement_media(ad_id: str) -> str:
    """Access legacy Coca-Cola advertisements and media content."""
    ads = {
        "hilltop-1971": "https://cdn.coca-cola.com/ads/hilltop-1971.mp4\nIconic 'I'd Like to Buy the World a Coke' commercial",
        "polar-bears-1993": "https://cdn.coca-cola.com/ads/polar-bears-1993.mp4\nFirst animated polar bear commercial",
        "vintage-poster-1890s": "https://cdn.coca-cola.com/images/vintage-poster-1890s.jpg\nOriginal 1890s Coca-Cola advertisement poster",
        "share-a-coke-2014": "https://cdn.coca-cola.com/ads/share-a-coke-2014.mp4\nShare a Coke campaign launch"
    }
    return ads.get(ad_id, "Advertisement not found")


@mcp.resource("coke://locations/mit-campus")
async def get_mit_locations() -> str:
    """List of Coke availability on MIT campus organized by type."""
    try:
        file_path = "data/locations/mit_campus.txt"
        with open(file_path, 'r') as f:
            location_data = f.read()
        return location_data
    except FileNotFoundError:
        return f"Location data file not found: {file_path}"


@mcp.resource("coke://regulations/massachusetts")
async def get_massachusetts_regulations() -> str:
    """Massachusetts state legislation related to beverages."""
    try:
        file_path = "data/regulations/massachusetts.json"
        with open(file_path, 'r') as f:
            regulations = json.load(f)
        return regulations
    except FileNotFoundError:
        return f"Regulations data file not found: {file_path}"
