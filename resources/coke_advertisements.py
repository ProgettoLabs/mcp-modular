from mcp_instance import mcp


# NOTE: This is a dummy resource with sample data for demonstration purposes.
@mcp.resource("coke://media/advertisements/{ad_id}")
async def get_advertisement_media(ad_id: str) -> str:
    """Access legacy Coca-Cola advertisements and media content.

    Args:
        ad_id: Advertisement identifier (e.g., "hilltop-1971", "polar-bears-1993",
               "vintage-poster-1890s", "share-a-coke-2014")
    """
    ads = {
        "hilltop-1971": "https://cdn.coca-cola.com/ads/hilltop-1971.mp4\nIconic 'I'd Like to Buy the World a Coke' commercial",
        "polar-bears-1993": "https://cdn.coca-cola.com/ads/polar-bears-1993.mp4\nFirst animated polar bear commercial",
        "vintage-poster-1890s": "https://cdn.coca-cola.com/images/vintage-poster-1890s.jpg\nOriginal 1890s Coca-Cola advertisement poster",
        "share-a-coke-2014": "https://cdn.coca-cola.com/ads/share-a-coke-2014.mp4\nShare a Coke campaign launch"
    }
    return ads.get(ad_id, "Advertisement not found")
