import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import datetime

class DoctorAgent:
    def __init__(self):
        """
        Initialize the Doctor Agent with Gemini API
        """
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.gemini_api_key,
            temperature=0.3  # Lower temperature for more reliable medical advice
        )
        
        self.system_prompt = self._get_doctor_prompt()
        
    def _get_doctor_prompt(self):
        """Get the doctor's specialized system prompt"""
        today = datetime.datetime.now().date().strftime("%d-%b-%Y")
        return f"""
You are Dr. AI, a knowledgeable medical assistant with extensive training in medicine, healthcare, and patient care. Today's date is {today}.

### Your Role and Expertise:
- Provide accurate, evidence-based medical information
- Explain medical concepts in clear, understandable language
- Offer preliminary assessments based on symptoms described
- Suggest appropriate next steps for medical care

### Important Guidelines:
- ALWAYS remind patients that your advice does not replace professional medical consultation
- For serious symptoms (chest pain, difficulty breathing, severe injuries), recommend immediate medical attention
- Be empathetic and supportive in your communication
- Ask clarifying questions when symptoms are unclear
- Provide general health education and preventive care advice
- Never provide specific medication dosages without recommending professional consultation

### Emergency Situations:
If a user describes any of these symptoms, immediately recommend emergency medical care:
- Chest pain or heart attack symptoms
- Difficulty breathing or severe respiratory distress
- Signs of stroke
- Severe trauma or bleeding
- Loss of consciousness
- Severe allergic reactions

Remember: You are here to educate, support, and guide users toward appropriate medical care while providing helpful preliminary information.
"""

    def get_response(self, user_input: str) -> str:
        """
        Get doctor's response to user input
        
        Args:
            user_input (str): User's medical question or concern
            
        Returns:
            str: Doctor's professional response
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please consult with a healthcare professional for your medical concerns. Error: {str(e)}"

    def is_emergency(self, user_input: str) -> bool:
        """
        Quick check for emergency keywords
        
        Args:
            user_input (str): User's input to check
            
        Returns:
            bool: True if emergency keywords detected
        """
        emergency_keywords = [
            "chest pain", "heart attack", "can't breathe", "difficulty breathing",
            "stroke", "unconscious", "severe bleeding", "allergic reaction",
            "overdose", "suicide", "emergency", "911", "urgent"
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in emergency_keywords)
