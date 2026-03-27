import os
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with transport security settings
mcp = FastMCP("coke-mcp-server")

# === Tools ===

PRODUCT_DATABASE =  {
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

# Dummy RAG database with crisis management protocols
CRISIS_PROTOCOLS_RAG = None # Will have the RAG system implemented

@mcp.tool()
async def query_crisis_protocol(crisis_type: str) -> dict:
    """Query internal RAG system for crisis management protocols.
    
    This tool demonstrates trust-building through preparedness and transparency - 
    showing that the company has clear, documented procedures for handling various 
    crisis situations.
    
    Args:
        crisis_type: Type of crisis (e.g., "product recall", "contamination", 
                    "supply chain disruption", "social media crisis")
    
    Returns:
        A dictionary containing the crisis protocol steps, contacts, and priority level
    """
    
    # Query the vector database for relevant crisis protocols
    query_text = f"crisis management protocol for {crisis_type}"
    
    # Perform semantic search in the vector database
    results = CRISIS_PROTOCOLS_RAG.search(
        query=query_text,
        top_k=1,
        threshold=0.7  # Similarity threshold
    )
    
    if results and len(results) > 0:
        # Extract the top matching protocol
        top_result = results[0]
        return {
            "found": True,
            "protocol": top_result["metadata"],
            "similarity_score": top_result["score"],
            "matched_query": crisis_type
        }
    else:
        return {
            "found": False,
            "message": f"No relevant protocol found for '{crisis_type}' above similarity threshold",
            "suggestion": "Please contact crisis-team@coca-cola.com for guidance on this specific situation"
        }

# === Prompts ===

@mcp.prompt()
async def evaluate_beverage_choice(beverage_context: str) -> str:
    """Guide users through a chain-of-thought reasoning process to make informed beverage choices.
    
    This prompt demonstrates trust-building through education and empowerment - helping
    customers think critically about their choices rather than just selling products.
    
    Args:
        beverage_context: Context about the situation (e.g., "choosing a drink for lunch")
    """
    return f"""You are a helpful beverage advisor working with Coca-Cola's transparency initiative. 
Your goal is to help the user make an informed decision about their beverage choice through careful reasoning.

Context: {beverage_context}

Please guide the user through the following chain of thought:

1. **Understand Their Needs**
   - What is the occasion? (exercise, meal, social gathering, etc.)
   - What are their health goals? (energy boost, hydration, low-calorie, etc.)
   - Are there any dietary restrictions to consider?

2. **Evaluate Options Transparently**
   - Compare nutritional profiles (calories, sugar, caffeine)
   - Consider ingredient sourcing and quality
   - Assess environmental impact of different package sizes
   - Review any relevant health considerations

3. **Consider Trade-offs**
   - Taste preference vs. nutritional goals
   - Environmental impact vs. convenience
   - Cost vs. quality/sustainability
   - Short-term satisfaction vs. long-term health

4. **Provide Honest Recommendation**
   - Recommend the best option based on their stated priorities
   - Acknowledge when a competitor's product might be better suited
   - Explain the reasoning clearly
   - Highlight Coca-Cola products when they genuinely fit, but never force it

5. **Educate on Long-term Patterns**
   - Discuss moderation and balance
   - Suggest hydration strategies
   - Provide context on sugar intake recommendations
   - Empower informed future decisions

Remember: Building trust means sometimes recommending water, competitor products, or less frequent 
consumption of sugary beverages. Honesty builds lasting customer relationships.

Please think through each step explicitly before providing your final recommendation."""

# === Resources ===

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
    # In production, this would fetch from a database or file system    
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
    # In production, this would fetch from a legal database or regulatory API
    try:
        file_path = "data/regulations/massachusetts.json"
        with open(file_path, 'r') as f:
            regulations = json.load(f)
        return regulations
    except FileNotFoundError:
        return f"Regulations data file not found: {file_path}"


def main():
    transport = os.getenv("MCP_TRANSPORT", "sse")
    
    if transport == "sse":
        mcp.settings.host = os.getenv("MCP_HOST", "0.0.0.0")
        mcp.settings.port = int(os.getenv("MCP_PORT", "8000"))
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()