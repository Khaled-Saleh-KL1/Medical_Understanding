from langchain_core.tools import tool
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgentExpert import DoctorAgent

# Initialize the doctor agent
doctor_agent = DoctorAgent()

@tool
def ConsultDoctorTool(medical_query: str) -> str:
    """Consult with a medical expert for health-related questions and concerns.
    
    Use this tool when:
    - User has medical symptoms or health concerns
    - User asks for medical advice or diagnosis
    - User mentions medications, treatments, or health conditions
    - User asks about anatomy, physiology, or medical procedures
    
    Args:
        medical_query: The medical question or health concern to consult about
        
    Returns:
        str: Professional medical response from the doctor agent
    """
    try:
        # Check for emergency situations
        if doctor_agent.is_emergency(medical_query):
            return (
                "⚠️ EMERGENCY ALERT: Based on your description, this may require immediate medical attention. "
                "Please call emergency services (911) or go to the nearest emergency room immediately. "
                "Do not delay seeking professional medical care.\n\n"
                f"Doctor's assessment: {doctor_agent.get_response(medical_query)}"
            )
        
        return doctor_agent.get_response(medical_query)
    
    except Exception as e:
        return (
            "I apologize, but I'm currently unable to connect with the medical expert. "
            "For any health concerns, please consult with a healthcare professional directly. "
            f"Technical issue: {str(e)}"
        )
