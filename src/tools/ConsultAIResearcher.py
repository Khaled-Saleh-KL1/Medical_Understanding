from langchain_core.tools import tool
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgentExpert import AIResearcherAgent

# Initialize the AI researcher agent
ai_researcher_agent = AIResearcherAgent()

@tool
def ConsultAIResearcherTool(research_query: str) -> str:
    """Consult with an AI/ML research expert for technical questions about artificial intelligence.
    
    Use this tool when:
    - User asks about AI, machine learning, or deep learning concepts
    - User wants to understand LLMs, neural networks, or AI architectures
    - User asks about AI research papers, frameworks, or methodologies
    - User needs help with AI implementation or best practices
    - User asks about recent developments in AI technology
    
    Args:
        research_query: The AI/ML research question or technical inquiry
        
    Returns:
        str: Expert response from the AI researcher agent
    """
    try:
        return ai_researcher_agent.get_response(research_query)
    
    except Exception as e:
        return (
            "I apologize, but I'm currently unable to connect with the AI research expert. "
            "Please try again later or rephrase your question. "
            f"Technical issue: {str(e)}"
        )
