from langchain_core.tools import tool
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgentExpert.arabic_doctor import ArabicDoctorAgent

# Initialize the Arabic doctor agent
arabic_doctor_agent = ArabicDoctorAgent()

@tool
def ConsultArabicDoctorTool(medical_query: str) -> str:
    """Consult with a bilingual medical expert for health-related questions in Arabic or English.
    
    Use this tool when:
    - User has medical symptoms or health concerns (in Arabic or English)
    - User asks for medical advice or diagnosis
    - User mentions medications, treatments, or health conditions
    - User asks about anatomy, physiology, or medical procedures
    - Input is in Arabic and needs medical expertise
    
    The tool automatically detects the language and responds appropriately.
    
    Args:
        medical_query: The medical question or health concern in Arabic or English
        
    Returns:
        str: Professional medical response in the same language as the input
    """
    try:
        # Check for emergency situations
        if arabic_doctor_agent.is_emergency(medical_query):
            language = arabic_doctor_agent.detect_language(medical_query)
            
            if language == "arabic":
                emergency_msg = (
                    "⚠️ تنبيه طارئ: بناءً على وصفك، قد تحتاج هذه الحالة إلى عناية طبية فورية. "
                    "يرجى الاتصال بخدمات الطوارئ (999 أو 997) أو التوجه إلى أقرب قسم طوارئ فوراً. "
                    "لا تؤخر طلب الرعاية الطبية المتخصصة.\n\n"
                    f"تقييم الطبيب: {arabic_doctor_agent.get_response(medical_query)}"
                )
            else:
                emergency_msg = (
                    "⚠️ EMERGENCY ALERT: Based on your description, this may require immediate medical attention. "
                    "Please call emergency services (911) or go to the nearest emergency room immediately. "
                    "Do not delay seeking professional medical care.\n\n"
                    f"Doctor's assessment: {arabic_doctor_agent.get_response(medical_query)}"
                )
            
            return emergency_msg
        
        return arabic_doctor_agent.get_response(medical_query)
    
    except Exception as e:
        language = arabic_doctor_agent.detect_language(medical_query)
        
        if language == "arabic":
            return (
                "أعتذر، ولكنني غير قادر حالياً على الاتصال بالخبير الطبي. "
                "لأي مخاوف صحية، يرجى استشارة طبيب مختص مباشرة. "
                f"مشكلة تقنية: {str(e)}"
            )
        else:
            return (
                "I apologize, but I'm currently unable to connect with the medical expert. "
                "For any health concerns, please consult with a healthcare professional directly. "
                f"Technical issue: {str(e)}"
            )
