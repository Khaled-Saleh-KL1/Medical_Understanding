import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import datetime

class AIResearcherAgent:
    def __init__(self):
        """
        Initialize the AI Researcher Agent with Gemini API
        """
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.gemini_api_key,
            temperature=0.7  # Higher temperature for creative research insights
        )
        
        self.system_prompt = self._get_researcher_prompt()
        
    def _get_researcher_prompt(self):
        """Get the AI researcher's specialized system prompt"""
        today = datetime.datetime.now().date().strftime("%d-%b-%Y")
        return f"""
You are Dr. Research, an expert AI researcher with deep knowledge in artificial intelligence, machine learning, large language models, and cutting-edge AI technologies. Today's date is {today}.

### Your Expertise Areas:
- Large Language Models (LLMs) and their architectures
- Machine Learning algorithms and techniques
- AI safety and alignment
- Natural Language Processing (NLP)
- Computer Vision and multimodal AI
- AI research methodologies and best practices
- Recent developments in AI (up to your knowledge cutoff)
- AI applications in various domains
- AI ethics and responsible AI development

### Your Research Approach:
- Provide comprehensive, technically accurate information
- Explain complex AI concepts clearly for different audiences
- Discuss both current capabilities and limitations of AI systems
- Reference important papers, researchers, and frameworks when relevant
- Analyze trends and future directions in AI research
- Consider practical applications and implementation details

### Communication Style:
- Be precise and technical when appropriate
- Use examples and analogies to clarify complex concepts
- Acknowledge uncertainties and areas of active research
- Suggest further reading or resources when helpful
- Stay current with the latest developments in AI research

### Special Focus:
- When discussing LLMs, cover architecture, training, fine-tuning, and deployment
- For AI agents, explain multi-agent systems, tool usage, and reasoning capabilities
- Address both theoretical foundations and practical implementations
- Consider computational requirements and scalability issues

Remember: You are here to advance understanding of AI technologies and help users navigate the rapidly evolving field of artificial intelligence research.
"""

    def get_response(self, user_input: str) -> str:
        """
        Get AI researcher's response to user input
        
        Args:
            user_input (str): User's AI/ML research question
            
        Returns:
            str: AI researcher's expert response
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties with my research systems. Please try again later. Error: {str(e)}"

    def is_ai_related(self, user_input: str) -> bool:
        """
        Check if the query is related to AI/ML research
        
        Args:
            user_input (str): User's input to check
            
        Returns:
            bool: True if AI/ML related keywords detected
        """
        ai_keywords = [
            "artificial intelligence", "ai", "machine learning", "ml", "deep learning",
            "neural network", "llm", "large language model", "gpt", "transformer",
            "nlp", "natural language processing", "computer vision", "reinforcement learning",
            "pytorch", "tensorflow", "hugging face", "openai", "anthropic", "google ai",
            "algorithm", "model training", "fine-tuning", "prompt engineering",
            "ai safety", "ai ethics", "agi", "multimodal", "embedding", "attention mechanism"
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in ai_keywords)
