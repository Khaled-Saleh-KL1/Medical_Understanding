from langgraph.types import Command, interrupt
from langchain_core.tools import tool

@tool
def HumanAssistanceTool(query: str) -> str:
    """Request assistance from a human.
    
    Args:
        query: The question or request to send to a human assistant
        
    Returns:
        str: The human's response to the query
    """
    human_response = interrupt({"query": query})
    return human_response.get("data", "No response received from human")