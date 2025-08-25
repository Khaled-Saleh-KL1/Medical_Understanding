"""
Detection helper functions for the Medical Understanding AI API
"""
import re
from ..models import ExpertType


def detect_expert_used(response: str) -> ExpertType:
    """Detect which expert was likely used based on response content"""
    response_lower = response.lower()
    
    # Check for Arabic content first
    arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    
    if re.search(arabic_pattern, response):
        if any(keyword in response for keyword in ["طبيب", "طبي", "صحة", "دكتور"]):
            return ExpertType.DOCTOR
        elif any(keyword in response for keyword in ["ذكاء اصطناعي", "تعلم الآلة", "تقنية"]):
            return ExpertType.AI_RESEARCHER
    
    # English detection
    if any(keyword in response_lower for keyword in ["dr.", "medical", "health", "symptoms", "diagnosis", "doctor"]):
        return ExpertType.DOCTOR
    elif any(keyword in response_lower for keyword in ["ai", "machine learning", "neural", "algorithm", "model", "research"]):
        return ExpertType.AI_RESEARCHER
    elif any(keyword in response_lower for keyword in ["search", "found", "according to", "website"]):
        return ExpertType.WEB_SEARCH
    elif "human" in response_lower or "assistance" in response_lower:
        return ExpertType.HUMAN
    else:
        return ExpertType.NONE


def detect_language(text: str) -> str:
    """Detect language of input text"""
    arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    
    if re.search(arabic_pattern, text):
        return "ar"
    else:
        return "en"


def detect_emergency(text: str) -> bool:
    """Detect if message contains emergency keywords"""
    text_lower = text.lower()
    
    emergency_keywords_english = [
        "chest pain", "heart attack", "can't breathe", "difficulty breathing",
        "stroke", "unconscious", "severe bleeding", "allergic reaction",
        "overdose", "suicide", "emergency", "911", "urgent", "help me"
    ]
    
    emergency_keywords_arabic = [
        "ألم في الصدر", "ألم الصدر", "نوبة قلبية", "لا أستطيع التنفس", "صعوبة التنفس",
        "سكتة دماغية", "فاقد الوعي", "نزيف شديد", "حساسية شديدة", "جرعة زائدة",
        "انتحار", "طوارئ", "عاجل", "إسعاف", "ساعدني"
    ]
    
    return (any(keyword in text_lower for keyword in emergency_keywords_english) or
            any(keyword in text for keyword in emergency_keywords_arabic))
