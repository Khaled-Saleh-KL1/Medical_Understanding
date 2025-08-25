from langchain_core.tools import tool
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgentExpert import GeneralExpertAgent

# Initialize the general expert agent
general_expert_agent = GeneralExpertAgent()

@tool
def ConsultGeneralExpertTool(general_query: str) -> str:
    """Consult with a general knowledge expert for educational and informational questions.
    
    Use this tool when:
    - User asks about history, science, literature, or culture
    - User wants explanations of general concepts or phenomena
    - User asks about geography, countries, or world facts
    - User seeks educational information on non-medical, non-AI topics
    - User asks "what is", "how does", "explain", or similar general questions
    - User wants to learn about arts, philosophy, or humanities
    
    Args:
        general_query: The general knowledge question or educational inquiry
        
    Returns:
        str: Educational response from the general expert agent
    """
    try:
        return general_expert_agent.get_response(general_query)
    
    except Exception as e:
        return (
            "I apologize, but I'm currently unable to connect with the general knowledge expert. "
            "Please try again later or rephrase your question. "
            f"Technical issue: {str(e)}"
        )
