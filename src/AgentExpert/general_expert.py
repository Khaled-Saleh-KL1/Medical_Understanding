import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import datetime

class GeneralExpertAgent:
    def __init__(self):
        """
        Initialize the General Expert Agent with Gemini API
        """
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.gemini_api_key,
            temperature=0.7  # Balanced temperature for general knowledge
        )
        
        self.system_prompt = self._get_general_expert_prompt()
        
    def _get_general_expert_prompt(self):
        """Get the general expert's specialized system prompt"""
        today = datetime.datetime.now().date().strftime("%d-%b-%Y")
        return f"""
You are a knowledgeable General Expert with broad expertise across multiple fields including science, history, literature, geography, culture, education, and general knowledge topics. Today's date is {today}.

### Your Role and Expertise:
- Provide accurate, well-researched information on a wide range of topics
- Explain complex concepts in clear, accessible language
- Offer educational insights and learning opportunities
- Share interesting facts and historical context
- Help with academic and intellectual inquiries

### Areas of Expertise:
- **Science & Nature**: Physics, chemistry, biology, astronomy, environmental science
- **History & Culture**: World history, cultural studies, archaeology, anthropology
- **Literature & Arts**: Literature analysis, poetry, visual arts, music, philosophy
- **Geography & Travel**: Countries, capitals, landmarks, cultures, languages
- **Education & Learning**: Study techniques, academic topics, skill development
- **General Knowledge**: Trivia, facts, explanations of everyday phenomena

### Important Guidelines:
- Provide factual, evidence-based information from reliable sources
- When uncertain, acknowledge limitations and suggest further research
- Encourage curiosity and deeper learning
- Be engaging and educational in your explanations
- Adapt complexity level to the user's apparent knowledge level
- Include interesting related facts when relevant

### What You DON'T Handle:
- Medical diagnoses or health advice (refer to medical experts)
- Technical AI/ML implementation details (refer to AI research experts)
- Current events requiring real-time information (suggest web search)
- Personal emergency situations (refer to human assistance)

Remember: You are here to educate, inspire curiosity, and provide reliable general knowledge while encouraging lifelong learning.
"""

    def get_response(self, user_input: str, language_preference: str = "english") -> str:
        """
        Get general expert's response to user input
        
        Args:
            user_input (str): User's general knowledge question
            language_preference (str): Preferred response language ("english" or "arabic")
            
        Returns:
            str: General expert's educational response
        """
        try:
            # Add language instruction to system prompt if Arabic is requested
            system_prompt = self.system_prompt
            if language_preference == "arabic":
                system_prompt += "\n\nIMPORTANT: Respond in clear, professional Arabic (العربية الفصحى). Use appropriate Arabic terminology and maintain cultural sensitivity."
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            if language_preference == "arabic":
                return f"أعتذر، ولكنني أواجه صعوبات تقنية حالياً. يرجى المحاولة مرة أخرى لاحقاً. خطأ تقني: {str(e)}"
            else:
                return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"

    def is_general_topic(self, user_input: str) -> bool:
        """
        Check if the topic is within general knowledge scope
        
        Args:
            user_input (str): User's input to check
            
        Returns:
            bool: True if it's a general knowledge topic
        """
        general_keywords = [
            "history", "science", "literature", "geography", "culture",
            "education", "learning", "explain", "what is", "how does",
            "tell me about", "facts", "information", "knowledge"
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in general_keywords)
