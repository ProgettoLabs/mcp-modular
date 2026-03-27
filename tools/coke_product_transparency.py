from mcp_instance import mcp


PRODUCT_DATABASE = {
    "COKE-355ML-001": {
        "verified": True,
        "product_name": "Coca-Cola Classic 355ml Can",
        "manufactured_date": "2026-01-15",
        "manufacturing_plant": "Atlanta, GA, USA - Plant #42",
        "ingredients": {
            "carbonated_water": {"source": "Municipal water supply, triple-filtered", "percentage": 89.2},
            "sugar": {"source": "Fair Trade certified cane sugar from Brazil", "percentage": 10.0},
            "caramel_color": {"source": "Plant-based caramel", "percentage": 0.5},
            "phosphoric_acid": {"percentage": 0.2},
            "natural_flavors": {"percentage": 0.1}
        },
        "nutritional_info": {
            "calories": 140,
            "sugar_g": 39,
            "sodium_mg": 45,
            "caffeine_mg": 34
        },
        "sustainability": {
            "packaging_recyclable": True,
            "recycled_content_percentage": 50,
            "carbon_footprint_kg": 0.17,
            "water_usage_liters": 1.89
        },
        "certifications": ["ISO 9001", "Fair Trade", "Kosher"],
        "supply_chain_verified": True
    }
}


@mcp.tool()
async def verify_product_transparency(product_code: str) -> dict:
    """Verify and retrieve complete transparency information for a Coca-Cola product.

    This tool demonstrates trust-building through radical transparency - providing
    customers with comprehensive information about ingredients, sourcing, nutritional
    content, and environmental impact.

    Args:
        product_code: The product code found on the package (e.g., "COKE-355ML-001")

    Returns:
        A dictionary containing detailed product information including ingredients,
        sourcing locations, nutritional facts, sustainability metrics, and verification status
    """
    if product_code in PRODUCT_DATABASE:
        return PRODUCT_DATABASE[product_code]
    else:
        return {
            "verified": False,
            "message": "Product code not found. This may indicate a counterfeit product. Please contact Coca-Cola customer service."
        }
