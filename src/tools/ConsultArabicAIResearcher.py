from langchain_core.tools import tool
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgentExpert.arabic_ai_researcher import ArabicAIResearcherAgent

# Initialize the Arabic AI researcher agent
arabic_ai_researcher_agent = ArabicAIResearcherAgent()

@tool
def ConsultArabicAIResearcherTool(research_query: str) -> str:
    """Consult with a bilingual AI/ML research expert for technical questions in Arabic or English.
    
    Use this tool when:
    - User asks about AI, machine learning, or deep learning concepts (in Arabic or English)
    - User wants to understand LLMs, neural networks, or AI architectures
    - User asks about AI research papers, frameworks, or methodologies
    - User needs help with AI implementation or best practices
    - User asks about recent developments in AI technology
    - Input is in Arabic and needs AI/ML expertise
    
    The tool automatically detects the language and responds appropriately.
    
    Args:
        research_query: The AI/ML research question or technical inquiry in Arabic or English
        
    Returns:
        str: Expert response in the same language as the input
    """
    try:
        return arabic_ai_researcher_agent.get_response(research_query)
    
    except Exception as e:
        language = arabic_ai_researcher_agent.detect_language(research_query)
        
        if language == "arabic":
            return (
                "أعتذر، ولكنني غير قادر حالياً على الاتصال بخبير أبحاث الذكاء الاصطناعي. "
                "يرجى المحاولة مرة أخرى لاحقاً أو إعادة صياغة سؤالك. "
                f"مشكلة تقنية: {str(e)}"
            )
        else:
            return (
                "I apologize, but I'm currently unable to connect with the AI research expert. "
                "Please try again later or rephrase your question. "
                f"Technical issue: {str(e)}"
            )
