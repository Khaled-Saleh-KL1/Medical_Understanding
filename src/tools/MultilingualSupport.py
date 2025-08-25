from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import re

class MultilingualAgent:
    def __init__(self):
        """Initialize the Multilingual Agent with Gemini API"""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.gemini_api_key,
            temperature=0.7
        )
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        # Simple Arabic detection using Unicode ranges
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        
        if arabic_pattern.search(text):
            return "arabic"
        else:
            return "english"
    
    def get_system_prompt(self, target_language: str) -> str:
        """Get system prompt in the target language"""
        if target_language == "arabic":
            return """
أنت مساعد ذكي طبي ومتخصص في الأبحاث. مهمتك الأساسية هي تقديم إجابات دقيقة ومفيدة باللغة العربية.

### إرشادات الاستجابة:
- **كن موجزاً:** اجعل إجاباتك قصيرة ومباشرة
- **كن دقيقاً:** أعط الأولوية للمعلومات الصحيحة والموثوقة
- **استخدم العربية الفصحى:** تحدث بلغة عربية واضحة ومفهومة

### الأدوات المتاحة:
- **أداة البحث الطبي:** للاستشارات الطبية والصحية
- **أداة الباحث في الذكاء الاصطناعي:** للأسئلة التقنية حول الذكاء الاصطناعي
- **أداة البحث على الإنترنت:** للمعلومات الحديثة والأحداث الجارية
- **أداة المساعدة البشرية:** للحالات المعقدة التي تتطلب تدخل بشري

### تنبيهات طبية مهمة:
- دائماً انصح المستخدمين بمراجعة الطبيب للاستشارات الطبية الشخصية
- في حالات الطوارئ الطبية، انصح بالاتصال بالطوارئ فوراً
- لا تقدم تشخيصات طبية نهائية

تذكر: أنت هنا لتقديم المعلومات والدعم باللغة العربية مع الحفاظ على الدقة والسلامة.
"""
        else:
            return """
You are a helpful medical and research AI assistant. Your primary goal is to provide accurate, concise, and direct answers to user questions in English.

### Response Guidelines:
- **Be Brief:** Keep your answers short and to the point
- **Be Factual:** Prioritize accuracy and verifiable information in all responses
- **Use Clear English:** Communicate in clear, professional English

### Available Tools:
- **Medical Consultation Tool:** For medical and health-related questions
- **AI Research Tool:** For AI/ML and technical questions
- **Web Search Tool:** For current information and recent events
- **Human Assistance Tool:** For complex situations requiring human judgment

### Important Medical Notes:
- Always remind users to consult healthcare professionals for personal medical advice
- For medical emergencies, recommend contacting emergency services immediately
- Do not provide definitive medical diagnoses

Remember: You are here to provide informative support in English while maintaining accuracy and safety.
"""
    
    def translate_response(self, text: str, target_language: str) -> str:
        """Translate response to target language if needed"""
        if target_language == "arabic":
            system_prompt = """
أنت مترجم محترف. مهمتك ترجمة النص التالي إلى اللغة العربية الفصحى مع الحفاظ على:
- الدقة الطبية والعلمية
- المعنى الأصلي
- الوضوح والفهم
- المصطلحات التخصصية المناسبة

ترجم النص التالي إلى العربية:
"""
        else:
            system_prompt = """
You are a professional translator. Your task is to translate the following text to English while maintaining:
- Medical and scientific accuracy
- Original meaning
- Clarity and understanding
- Appropriate technical terminology

Translate the following text to English:
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=text)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Translation error: {str(e)}"

# Initialize the multilingual agent
multilingual_agent = MultilingualAgent()

@tool
def MultilingualSupportTool(user_input: str) -> str:
    """Provide multilingual support for Arabic and English users.
    
    **ALWAYS CALL THIS TOOL FIRST** for every user input to ensure consistent language handling.
    
    This tool:
    - Detects the language of user input (Arabic or English)
    - Provides response instructions in the detected language
    - Ensures all subsequent expert responses match the user's language
    - Provides culturally appropriate guidance for responses
    
    Args:
        user_input: The user's message in Arabic or English
        
    Returns:
        str: Language detection result and detailed response guidance for the system
    """
    try:
        detected_language = multilingual_agent.detect_language(user_input)
        
        if detected_language == "arabic":
            return f"""
LANGUAGE DETECTED: ARABIC
USER INPUT: {user_input}

MANDATORY INSTRUCTIONS FOR ALL EXPERT TOOLS:
- Respond ONLY in Arabic (العربية الفصحى)
- Use proper Arabic medical/technical terminology
- Include appropriate Arabic greetings and cultural expressions
- For medical emergencies, mention Arabic emergency numbers
- Be respectful and culturally sensitive

RESPONSE GUIDELINES:
- Use formal Arabic language structure
- Include Islamic cultural considerations when relevant
- Provide clear explanations using familiar Arabic concepts
- End responses with encouraging Arabic phrases when appropriate

ALL SUBSEQUENT EXPERT RESPONSES MUST BE IN ARABIC.
"""
        else:
            return f"""
LANGUAGE DETECTED: ENGLISH
USER INPUT: {user_input}

MANDATORY INSTRUCTIONS FOR ALL EXPERT TOOLS:
- Respond ONLY in clear, professional English
- Use standard medical/technical terminology
- Include appropriate English greetings and expressions
- For medical emergencies, mention standard emergency numbers (911)
- Be professional and accessible

RESPONSE GUIDELINES:
- Use clear, concise English language
- Provide explanations using familiar Western concepts and examples
- Maintain professional but friendly tone
- Include helpful context and educational information

ALL SUBSEQUENT EXPERT RESPONSES MUST BE IN ENGLISH.
"""
            
    except Exception as e:
        return f"Language detection error: {str(e)}. Defaulting to English for responses."
