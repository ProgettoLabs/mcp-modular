from mcp_instance import mcp


# An actual RAG implementation would look something like this:
# CRISIS_PROTOCOLS_RAG = RAGSystem(
#     embedding_model="text-embedding-3-small",
#     vector_store="pinecone",  # or weaviate, qdrant, etc.
#     index_name="crisis-protocols"
# )

# This is a dummy implementation of the crisis protocols.
CRISIS_PROTOCOLS = {
    "product recall": {
        "priority": "CRITICAL",
        "steps": [
            "Immediately notify the Crisis Management Team (CMT)",
            "Identify and isolate affected product batches",
            "Coordinate with regulatory affairs for FDA/CPSC notification",
            "Issue internal hold on distribution of affected SKUs",
            "Prepare public statement with Legal and Communications",
            "Initiate consumer notification and recall logistics",
        ],
        "contacts": ["recall-team@coca-cola.com", "regulatory@coca-cola.com"],
    },
    "contamination": {
        "priority": "CRITICAL",
        "steps": [
            "Halt production at affected facility immediately",
            "Notify food safety and quality assurance teams",
            "Collect and quarantine samples for lab analysis",
            "Engage third-party testing if required",
            "Report to relevant health authorities",
            "Assess scope and initiate recall if necessary",
        ],
        "contacts": ["food-safety@coca-cola.com", "quality@coca-cola.com"],
    },
    "supply chain disruption": {
        "priority": "HIGH",
        "steps": [
            "Assess impact on production and distribution timelines",
            "Activate alternative supplier or logistics contingencies",
            "Notify sales and operations planning teams",
            "Communicate adjusted lead times to distributors",
            "Monitor situation and update stakeholders daily",
        ],
        "contacts": ["supply-chain@coca-cola.com", "operations@coca-cola.com"],
    },
    "social media crisis": {
        "priority": "HIGH",
        "steps": [
            "Monitor and document the scope of the issue",
            "Brief Communications and Legal teams immediately",
            "Pause scheduled social media posts",
            "Draft an initial holding statement within 1 hour",
            "Identify root cause and prepare factual response",
            "Engage influencers or media contacts as needed",
        ],
        "contacts": ["communications@coca-cola.com", "pr@coca-cola.com"],
    },
}


@mcp.tool()
async def query_crisis_protocol(crisis_type: str) -> dict:
    """Query internal crisis management protocols.

    This tool demonstrates trust-building through preparedness and transparency -
    showing that the company has clear, documented procedures for handling various
    crisis situations.

    Args:
        crisis_type: Type of crisis (e.g., "product recall", "contamination",
                    "supply chain disruption", "social media crisis")

    Returns:
        A dictionary containing the crisis protocol steps, contacts, and priority level
    """
    # An actual RAG implementation would look something like this:
    # query_text = f"crisis management protocol for {crisis_type}"
    # results = CRISIS_PROTOCOLS_RAG.search(query=query_text, top_k=1, threshold=0.7)
    # if results and len(results) > 0:
    #     top_result = results[0]
    #     return {
    #         "found": True,
    #         "protocol": top_result["metadata"],
    #         "similarity_score": top_result["score"],
    #         "matched_query": crisis_type,
    #     }

    normalized = crisis_type.lower().strip()
    protocol = CRISIS_PROTOCOLS.get(normalized)

    if protocol:
        return {
            "found": True,
            "protocol": protocol,
            "matched_query": crisis_type,
        }
    else:
        return {
            "found": False,
            "message": f"No relevant protocol found for '{crisis_type}'",
            "available_protocols": list(CRISIS_PROTOCOLS.keys()),
            "suggestion": "Please contact crisis-team@coca-cola.com for guidance on this specific situation",
        }
